import numpy as np

from ...math.matrix import Matrix
from ...geometry.gemo_algo import GeomAlgo2D
from ...geometry.shape import *


class AABB():
    def __init__(self):
        self._pos = Matrix([0.0, 0.0], 'vec')
        self._width = 0.0
        self._height = 0.0

    def __eq__(self, other):
        return np.isclose(self._width, other._width) and np.isclose(
            self._height, other._width) and self._pos == other._pos

    def top_left(self):
        return Matrix([
            -self._width / 2.0 + self._pos.val[0],
            self._height / 2.0 + self._pos.val[1]
        ], 'vec')

    def top_right(self):
        return Matrix([
            self._width / 2.0 + self._pos.val[0],
            self._height / 2.0 + self._pos.val[1]
        ], 'vec')

    def bottom_left(self):
        return Matrix([
            -self._width / 2.0 + self._pos.val[0],
            -self._height / 2.0 + self._pos.val[1]
        ], 'vec')

    def bottom_right(self):
        return Matrix([
            self._width / 2.0 + self._pos.val[0],
            -self._height / 2.0 + self._pos.val[1]
        ], 'vec')

    def collide(self, aabb):
        return AABB.collide_det(self, aabb)

    def expand(self, factor):
        return AABB.expand_oper(self, factor)

    def scale(self, factor):
        self._width *= factor
        self._height *= factor

    def clear(self):
        self._pos.clear()
        self._width = 0.0
        self._height = 0.0

    def unite(self, aabb):
        return AABB.unite_oper(self, aabb)

    def surface_area(self):
        return (self._width + self._height) * 2.0  #TODO: why? mean Perimeter?

    def volume(self):
        return self._width * self._height

    def is_subset(self, aabb):
        return is_subset_det(aabb, self)  #NOTE: the seq is important

    def is_empty(self):
        return np.isclose(self._width, 0.0) and np.isclose(
            self._height, 0.0) and np.isclose(self._pos, [0.0, 0.0]).all()

    def raycast(self, start_point, dir):
        return AABB.raycast_oper(self, start_point, dir)

    @staticmethod
    def from_shape(shape, factor=0.0):
        res = AABB()
        shape_type = shape._shape.type()

        if shape_type == Shape.Type.Polygon:
            pass
        elif shape_type == Shape.Type.Ellipse:
            pass
        elif shape_type == Shape.Type.Circle:
            pass
        elif shape_type == Shape.Type.Edge:
            pass
        elif shape_type == Shape.Type.Curve:
            pass
        elif shape_type == Shape.Type.Point:
            pass
        elif shape_type == Shape.Type.Capsule:
            pass
        elif shape_type == Shape.Type.Sector:
            pass

        res._pos += shape._transform
        res.expand(factor)
        return res

    @staticmethod
    def from_body(body, factor=0.0):
        assert body != None
        assert body.shape() != None

        primitive = ShapePrimitive()
        primitive._shape = body.shape()
        primitive._rotation = body.rotation()
        primitive._transform = body.transform()
        return AABB.from_shape(primitive, factor)

    @staticmethod
    def from_box(top_left, bottom_right):
        res = AABB()
        res._width = bottom_right.val[0] - top_left.val[0]
        res._height = top_left.val[1] - bottom_right.val[1]
        res._pos = (top_left + bottom_right) / 2.0
        return res

    @staticmethod
    def collide_det(src, target):
        src_top_left = src.top_left()
        src_bottom_right = src.bottom_right()
        target_top_left = target.top_left()
        target_bottom_right = target.bottom_right()
        return not (src_bottom_right.val[0] < target_top_left.val[0]
                    or target_bottom_right.val[0] < src_top_left.val[0]
                    or src_top_left.val[1] < target_bottom_right.val[1]
                    or target_top_left.val[1] < src_bottom_right.val[1])

    @staticmethod
    def unite_oper(src, target, factor=0.0):
        if src.is_empty():
            return target
        elif target.is_empty():
            return src

        src_top_left = src.top_left()
        src_bottom_right = src.bottom_right()
        target_top_left = target.top_left()
        target_bottom_right = target.bottom_right()

        x_min = np.fmin(src_top_left.val[0], target_top_left.val[0])
        x_max = np.fmax(src_bottom_right.val[0], target_bottom_right.val[0])
        y_min = np.fmin(src_bottom_right.val[1], target_bottom_right.val[1])
        y_max = np.fmax(src_top_left.val[1], target_top_left.val[1])

        res = AABB()
        res._pos.set_value([(x_min + x_max) / 2.0, (y_min + y_max) / 2.0])
        res._width = x_max - x_min
        res._height = y_max - y_min
        res.expand(factor)
        return res

    @staticmethod
    def is_subset_det(src, target):
        src_top_left = src.top_left()
        src_bottom_right = src.bottom_right()
        target_top_left = target.top_left()
        target_bottom_right = target.bottom_right()

        return target_top_left.val[0] >= src_top_left.val[
            0] and target_bottom_right.val[0] <= src_bottom_right.val[
                0] and target_bottom_right.val[1] >= src_bottom_right.val[
                    1] and target_top_left.val[1] <= src_top_left.val[1]

    @staticmethod
    def expand_oper(aabb, factor=0.0):
        aabb._width += factor
        aabb._height += factor

    @staticmethod
    def raycast_oper(aabb, start_point, dir):
        res = GeomAlgo2D.raycastAABB(start_point, dir, aabb.top_left(),
                                     aabb.bottom_right())
        if res == None:
            return False

        p1, p2 = res[0], res[1]
        return GeomAlgo2D.is_point_on_AABB(
            p1, aabb.top_left(),
            aabb.bottom_right()) and GeomAlgo2D.is_point_on_AABB(
                p2, aabb.top_left(), aabb.bottom_right())
