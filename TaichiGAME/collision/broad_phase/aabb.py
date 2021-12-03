import numpy as np

from ...common.config import Config
from ...math.matrix import Matrix
from ...geometry.geom_algo import GeomAlgo2D
from ...geometry.shape import Circle, Edge, Ellipse, Polygon, Shape, ShapePrimitive
from ...dynamics.body import Body


class AABB():
    def __init__(self, width: float = 0.0, height: float = 0.0):
        self._pos: Matrix = Matrix([0.0, 0.0], 'vec')
        self._width: float = width
        self._height: float = height

    def __eq__(self, other):
        return np.isclose(self._width, other._width) and np.isclose(
            self._height, other._height) and self._pos == other._pos

    def top_left(self) -> Matrix:
        return Matrix([
            -self._width / 2.0 + self._pos.x, self._height / 2.0 + self._pos.y
        ], 'vec')

    def top_right(self) -> Matrix:
        return Matrix([
            self._width / 2.0 + self._pos.x, self._height / 2.0 + self._pos.y
        ], 'vec')

    def bot_left(self) -> Matrix:
        return Matrix([
            -self._width / 2.0 + self._pos.x, -self._height / 2.0 + self._pos.y
        ], 'vec')

    def bot_right(self) -> Matrix:
        return Matrix([
            self._width / 2.0 + self._pos.x, -self._height / 2.0 + self._pos.y
        ], 'vec')

    def collide(self, aabb) -> bool:
        '''check if two aabbs are overlapping

        Parameters
        ----------
        aabb : AABB
            other AABB

        Returns
        -------
        bool
            True: collide, otherwise not
        '''
        return AABB._collide(self, aabb)

    def expand(self, factor: float):
        AABB._expand(self, factor)

    def scale(self, factor: float):
        self._width *= factor
        self._height *= factor

    def clear(self):
        self._pos.clear()
        self._width = 0.0
        self._height = 0.0

    def unite(self, aabb):
        '''return two AABB union result

        Parameters
        ----------
        aabb : AABB
            other AABB

        Returns
        -------
        AABB
            union AABB
        '''
        return AABB._unite(self, aabb)

    def surface_area(self) -> float:
        return (self._width + self._height) * 2.0

    def volume(self) -> float:
        return self._width * self._height

    def is_subset(self, aabb) -> bool:
        '''check if self is the subset of aabb

        Parameters
        ----------
        aabb : AABB
            ref AABB

        Returns
        -------
        bool
            True: is subset, otherwise not
        '''
        return AABB._is_subset(aabb, self)  #NOTE: the seq is important

    def is_empty(self) -> bool:
        return np.isclose(self._width, 0.0) and np.isclose(
            self._height, 0.0) and np.isclose(self._pos, [0.0, 0.0]).all()

    def raycast(self, start: Matrix, dir: Matrix) -> bool:
        return AABB._raycast(self, start, dir)

    @staticmethod
    def from_shape(shape: Shape, factor: float = 0.0):
        res = AABB()
        shape_type = shape._shape.type()

        if shape_type == Shape.Type.Polygon:
            polygon: Polygon = shape._shape
            x_max: float = Config.NegativeMin
            y_max: float = Config.NegativeMin
            x_min: float = Config.Max
            y_min: float = Config.Max
            for v in polygon.vertices():
                vertex: Matrix = Matrix.rotate_mat(shape._rotation) * v

                if x_max < vertex.x:
                    x_max = vertex.x

                if x_min > vertex.x:
                    x_min = vertex.x

                if y_max < vertex.y:
                    y_max = vertex.y

                if y_min > vertex.y:
                    y_min = vertex.y

            res._width = np.fabs(x_max - x_min)
            res._height = np.fabs(y_max - y_min)
            res._pos.set_value((x_max + x_min) / 2.0, (y_max + y_min) / 2.0)

        elif shape_type == Shape.Type.Ellipse:
            ellipse: Ellipse = shape._shape

            top_dir: Matrix = Matrix([0.0, 1.0], 'vec')
            left_dir: Matrix = Matrix([-1.0, 0.0], 'vec')
            bot_dir: Matrix = Matrix([0.0, -1.0], 'vec')
            right_dir: Matrix = Matrix([1.0, 0.0], 'vec')

            top_dir = Matrix.rotate_mat(-shape._rotation).multiply(top_dir)
            left_dir = Matrix.rotate_mat(-shape._rotation).multiply(left_dir)
            bot_dir = Matrix.rotate_mat(-shape._rotation).multiply(bot_dir)
            right_dir = Matrix.rotate_mat(-shape._rotation).multiply(right_dir)

            top: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), top_dir)
            left: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), left_dir)
            bot: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), bot_dir)
            right: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), right_dir)

            top = Matrix.rotate_mat(shape._rotation).multiply(top)
            left = Matrix.rotate_mat(shape._rotation).multiply(left)
            bot = Matrix.rotate_mat(shape._rotation).multiply(bot)
            right = Matrix.rotate_mat(shape._rotation).multiply(right)

            res._height = np.fabs(top.y - bot.y)
            res._width = np.fabs(right.x - left.x)

        elif shape_type == Shape.Type.Circle:
            cir: Circle = shape._shape
            res._width = cir.radius * 2.0
            res._height = cir.radius * 2.0

        elif shape_type == Shape.Type.Edge:
            edg: Edge = Shape._shape
            res._width = np.fabs(edg.start.x - edg.end.x)
            res._height = np.fabs(edg.start.y - edg.end.y)
            res._pos.set_value(
                [edg.start.x + edg.end.x, edg.start.y + edg.end.y])
            res._pos *= 2.0

        elif shape_type == Shape.Type.Curve:
            pass
        elif shape_type == Shape.Type.Point:
            res._width = 1.0
            res._height = 1.0

        elif shape_type == Shape.Type.Capsule:
            pass
        elif shape_type == Shape.Type.Sector:
            pass

        res._pos += shape._transform
        res.expand(factor)
        return res

    @staticmethod
    def from_body(body: Body, factor: float = 0.0):
        assert body != None
        assert body.shape() != None

        primitive: ShapePrimitive = ShapePrimitive()
        primitive._shape = body.shape()
        primitive._rotation = body.rotation()
        primitive._transform = body.transform()
        return AABB.from_shape(primitive, factor)  #FIXME: the type is right?

    @staticmethod
    def from_box(top_left, bot_right):
        res = AABB()
        res._width = bot_right.x - top_left.x
        res._height = top_left.y - bot_right.y
        res._pos = (top_left + bot_right) / 2.0
        return res

    @staticmethod
    def _collide(src, target) -> bool:
        '''check if two aabbs are overlapping

        Parameters
        ----------
        src : AABB
            src AABB
        target : AABB
            target AABB

        Returns
        -------
        bool
            True: collide, otherwise not
        '''
        src_top_left: Matrix = src.top_left()
        src_bot_right: Matrix = src.bot_right()
        target_top_left: Matrix = target.top_left()
        target_bot_right: Matrix = target.bot_right()

        return not (src_bot_right.x < target_top_left.x
                    or target_bot_right.x < src_top_left.x
                    or src_top_left.y < target_bot_right.y
                    or target_top_left.y < src_bot_right.y)

    @staticmethod
    def _unite(src, target, factor: float = 0.0):
        '''return two AABB union result

        Parameters
        ----------
        src : AABB
            source AABB
        target : AABB
            target AABB
        factor : float
            expand factor

        Returns
        -------
        AABB
            union AABB
        '''

        if src.is_empty():
            return target
        elif target.is_empty():
            return src

        src_top_left: Matrix = src.top_left()
        src_bot_right: Matrix = src.bot_right()
        target_top_left: Matrix = target.top_left()
        target_bot_right: Matrix = target.bot_right()

        x_min: float = np.fmin(src_top_left.x, target_top_left.x)
        x_max: float = np.fmax(src_bot_right.x, target_bot_right.x)
        y_min: float = np.fmin(src_bot_right.y, target_bot_right.y)
        y_max: float = np.fmax(src_top_left.y, target_top_left.y)

        res = AABB()
        res._pos.set_value([(x_min + x_max) / 2.0, (y_min + y_max) / 2.0])
        res._width = x_max - x_min
        res._height = y_max - y_min
        res.expand(factor)

        return res

    @staticmethod
    def _is_subset(src, target) -> bool:
        '''check if target is the subset of src

        Parameters
        ----------
        src : AABB
            ref AABB
        target : AABB
            dut AABB

        Returns
        -------
        bool
            True: is subset, otherwise not
        '''
        src_top_left: Matrix = src.top_left()
        src_bot_right: Matrix = src.bot_right()
        target_top_left: Matrix = target.top_left()
        target_bot_right: Matrix = target.bot_right()

        return src_bot_right.x >= target_bot_right.x and target_top_left.x >= src_top_left.x and src_top_left.y >= target_top_left.y and target_bot_right.y >= src_bot_right.y

    @staticmethod
    def _expand(aabb, factor: float = 0.0):
        aabb._width += factor
        aabb._height += factor

    @staticmethod
    def _raycast(aabb, start: Matrix, dir: Matrix) -> bool:
        res = GeomAlgo2D.raycastAABB(start, dir, aabb.top_left(),
                                     aabb.bot_right())
        if res == None:
            return False

        p1, p2 = res[0], res[1]
        return GeomAlgo2D.is_point_on_AABB(
            p1, aabb.top_left(),
            aabb.bot_right()) and GeomAlgo2D.is_point_on_AABB(
                p2, aabb.top_left(), aabb.bot_right())
