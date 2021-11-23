import numpy as np

from ..math.matrix import Matrix
from .geom_algo import GeomAlgo2D


class Shape():
    class Type():
        Point = 0
        Polygon = 1
        Circle = 2
        Ellipse = 3
        Capsule = 4
        Edge = 5
        Curve = 6
        Secto = 7

    def __init__(self):
        pass

    def type(self):
        return self._type

    def scale(self, factor):
        pass

    def contains(self, point):
        pass

    def center(self):
        pass


class ShapePrimitive():
    def __init__(self):
        self._shape = None
        self._transform = None
        self._rotation = 0

    def translate(self, src):
        return Matrix.rotate_mat(self._rotation) * source + self._transform


class Point(Shape):
    def __init__(self):
        self._type = self.Type.Point
        self._pos = Matrix([0.0, 0.0], 'vec')

    def pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos

    def scale(self, factor):
        self._pos *= factor

    def contains(self, point):
        return np.isclose(self._pos - point)

    def center(self):
        return self._pos


class Polygon(Shape):
    def __init__(self):
        self._type = self.Type.Polygon
        self._vertices = []

    def vertices(self):
        return self._vertices

    def append(self, vertices):
        self._vertices = vertices
        self.update_vertices()

    def scale(self, factor):
        assert len(self._vertices)
        self._vertices = [v * factor for v in self._vertices]

    def contains(self, point):
        assert len(self._vertices) > 2
        num = len(self._vertices)
        for i in range(num - 1):
            p1 = self._vertices[i]
            p2 = self._vertices[i + 1]
            ref = self._vertices[1] if i + 2 == num else self._vertices[
                i + 2]  # TODO: why [1]? according to the vertices list type
            if not GeomAlgo2D.is_point_on_same_side(p1, p2, ref, point):
                return False

        return True

    def center(self):
        return GeomAlgo2D.calc_center(self._vertices)

    def update_vertices(self):
        center_point = self.center()
        self._vertices = [v - center_point for v in self._vertices]


class Rectangle(Polygon):
    def __init__(self, width=0.0, height=0.0):
        super().__init__()
        self.set_value(width, height)

    def set_value(self, width, height):
        self._width = width
        self._height = height
        self.calc_vertices()

    def width(self):
        return self._width

    def set_width(self, width):
        self._width = width
        self.calc_vertices()

    def height(self):
        return self._height

    def set_height(self, height):
        self._height = height
        self.calc_vertices()

    def scale(self, factor):
        self._width *= factor
        self._height *= factor
        self.calc_vertices()

    def contains(self, point):
        return (point.val[0] > -self._width * 0.5 and point.val[0] <
                self._width * 0.5) and (point.val[1] > -self._height * 0.5
                                        and point.val[1] < self._height * 0.5)

    def calc_vertices(self):
        self._vertices = []
        self._vertices.append(
            Matrix([-self._width * 0.5, self._height * 0.5], 'vec'))
        self._vertices.append(
            Matrix([-self._width * 0.5, -self._height * 0.5], 'vec'))
        self._vertices.append(
            Matrix([self._width * 0.5, -self._height * 0.5], 'vec'))
        self._vertices.append(
            Matrix([self._width * 0.5, self._height * 0.5], 'vec'))
        self._vertices.append(
            Matrix([-self._width * 0.5, self._height * 0.5], 'vec'))


class Circle(Shape):
    def __init__(self, radius=0):
        self._type = self.Type.Circle
        self.set_radius(radius)

    def radius(self):
        return self._radius

    def set_radius(self, radius):
        self._radius = radius

    def scale(self, factor):
        self._radius *= factor

    def contains(self, point):
        return np.isclose(point.len_square(), self._radius * self._radius)

    def center(self):
        return Matrix([0.0, 0.0], 'vec')


class Ellipse(Shape):
    def __init__(self, width=0.0, height=0.0):
        self._type = self.Type.Ellipse
        self.set_value(width, height)

    def set_value(self, width, height):
        self._width = width
        self._height = height

    def width(self):
        return self._width

    def set_width(self, width):
        self._width = width

    def height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    def scale(self, factor):
        self._width *= factor
        self._height *= factor

    def contains(self, point):
        return False

    def center(self):
        return Matrix([0.0, 0.0], 'vec')

    def A(self):
        return self._width / 2.0

    def B(self):
        return self._height / 2.0

    def C(self):
        va = self.A()
        vb = self.B()
        return np.sqrt(va * va - vb * vb)


class Edge(Shape):
    def __init__(self):
        self._type = self.Type.Edge

    def set_value(self, start_point, end_point):
        self._start_point = start_point
        self._end_point = end_point
        self._normal = (self.end_point -
                        self.start_point).perpendicular().normal().negate()

    def start_point(self):
        return self._start_point

    def set_start_point(self, point):
        self._start_point = point

    def end_point(self):
        return self._end_point

    def set_end_point(self, point):
        self._end_point = point

    def scale(self, factor):
        self._start_point *= factor
        self._end_point *= factor

    def contains(self, point):
        return GeomAlgo2D.is_point_on_segment(self._start_point,
                                              self._end_point, point)

    def center(self):
        return (self._start_point + self._end_point) / 2.0

    def normal(self):
        return self._normal

    def set_normal(self, normal):
        self._normal = normal


class Curve(Shape):
    def __init__(self):
        self._type = self.Type.Curve

    def set_value(self, start_point, ctrl_p1, ctrl_p2, end_point):
        self._start_point = start_point
        self._ctrl_point1 = ctrl_p1
        self._ctrl_point2 = ctrl_p2
        self._end_point = end_point

    def start_point(self):
        return self._start_point

    def set_start_point(self, point):
        self._start_point = point

    def control1(self):
        return self._ctrl_point1

    def set_control1(self, point):
        self._ctrl_point1 = point

    def control2(self):
        return self._ctrl_point2

    def set_control2(self, point):
        self._ctrl_point2 = point

    def end_point(self):
        return self._end_point

    def set_end_point(self, point):
        self._end_point = point

    def scale(self, factor):
        self._start_point *= factor
        self._ctrl_point1 *= factor
        self._ctrl_point2 *= factor
        self._end_point *= factor

    def contains(self, Point):
        return False

    def center(self):
        return Matrix([0.0, 0.0], 'vec')


class Capsule(Shape):
    def __init__(self, width=0.0, height=0.0):
        self._type = self.Type.Capsule
        self.set_value(width, height)

    def set_value(self, width, height):
        self._width = width
        self._height = height

    def width(self):
        return self._width

    def set_width(self, width):
        sellf._width = width

    def height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    def top_left(self):
        res = Matrix([0.0, 0.0], 'vec')
        if self._width > self._height:
            tmp = self._height / 2.0
            res.set_value(-self._width / 2.0 + tmp, tmp)
        else:
            tmp = self._width / 2.0
            res.set_value(-tmp, self._height / 2.0 - tmp)

        return res

    def bottom_left(self):
        res = Matrix([0.0, 0.0], 'vec')
        if self._width > self._height:
            tmp = self._height / 2.0
            res.set_value(-self._width / 2.0 + tmp, -tmp)
        else:
            tmp = self._width / 2.0
            res.set_value(-tmp, -self._height / 2.0 + tmp)

        return res

    def top_right(self):
        return -self.bottom_left()

    def bottom_right(self):
        return -self.top_left()

    def box_vertices(self):
        vertices = []
        vertices.append(self.top_left())
        vertices.append(self.bottom_left())
        vertices.append(self.bottom_right())
        vertices.append(self.top_right())
        vertices.append(self.top_left())
        return vertices

    def scale(self, factor):
        self._width *= factor
        self._height *= factor

    def contains(self, point):
        # anchor_p1 = Matrix([0.0, 0.0], 'vec')
        # anchor_p2 = Matrix([0.0, 0.0], 'vec')
        # x_len = y_len = 0
        # if self._width >= self._height:
        #     y_len = self._height / 2.0
        #     x_len = self._width - self._height
        #     anchor_p1.set_value([x_len/2.0, 0.0])
        #     anchor_p2.set_value([-x_len/2.0, 0.0])
        #     if np.isclose(point.val[0], anchor_p1.val[0]) and point.val[0] > anchor_p2.val[0] and
        #     np.isclose(point.val[1], y_len) and point.val[1]
        # else:
        #     pass
        return False

    def center(self):
        return Matrix([0.0, 0.0], 'vec')


class Sector(Shape):
    def __init__(self):
        self._type = self.Type.Sector
        self.set_value()

    def vertices(self):
        res = []
        res.append(Matrix([0.0, 0.0], 'vec'))
        res.append(
            Matrix.rotate_mat(self._start_radian) *
            Matrix([self._radius, 0], 'vec'))
        res.append(
            Matrix.rotate_mat(self._start_radian + self._span_radian) *
            Matrix([self._radius, 0], 'vec'))
        res.append(Matrix([0.0, 0.0], 'vec'))
        return res

    def start_radian(self):
        return self._start_radian

    def set_start_radian(self, radian):
        self._start_radian = radian

    def span_radian(self):
        return self._span_radian

    def set_span_raidin(self, radian):
        self._span_radian = radian

    def radius(self):
        return self._radius

    def set_radius(self, radius):
        self._radius = radius

    def set_value(self, start=0, span=0, radius=0):
        self._start_radian = start
        self._span_radian = span
        self._radius = radius

    def area(self):
        return self._span_radian * self._radius * self._radius / 2.0

    def scale(self, factor):
        self._radius *= factor

    def contains(self, point):
        theta = point.theta()
        return theta >= self._start_radian and theta <= self._start_radian + self._span_radian and point.len_square(
        ) <= self._radius * self._radius

    def center(self):
        vertices = self.vertices()
        point1 = vertices[1]
        point2 = vertices[2]
        normal = (point1 + point2) / 2
        normal.normalize()

        point_len = (point1 - point2).len()
        rad_len = self._radius * self._span_radian
        res = normal * (2.0 * self._radius * point_len / (3.0 * rad_len))
        return res
