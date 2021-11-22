import numpy as np

from ..math.matrix import Matrix
from geom_algo import GeomAlgo2D


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
        pass


class Point(Shape):
    def __init__(self):
        self._type = self.Type.Point
        self._pos = Matrix([0, 0], 'vec')

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
        for v in vertices:
            self._vertices.append(v)
        self.update_vertices()

    def scale(self, factor):
        assert (len(self._vertices))
        self._vertices = [v * factor for v in self._vertices]

    def contains(self, point):
        assert (len(self._vertices) > 2)
        num = len(self._vertices)
        for i in range(num):
            p1 = self._vertices[i]
            p2 = self._vertices[i + 1]
            ref = self._vertices[1] if i + 2 == num else self._vertices[
                i + 2]  # TODO: why [1]?
            if not GeomAlgo2D.is_point_on_same_side(p1, p2, ref, point):
                return False

        return True

    def center(self):
        return GeomAlgo2D.calculate_center(self._vertices)

    def update_vertices(self):
        center_point = self.center()
        self._vertices = [v - center_point for v in self._vertices]


class Rectangle(Polygon):
    def __init__(self, width, height):
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
    def __init__(self, radius):
        self._type = self.Type.Circle
        self._radius = radius

    def radius(self):
        return self._radius

    def set_radius(self, radius):
        self._radius = radius

    def scale(self, factor):
        self._radius *= factor

    def contains(self, point):
        return np.isclose(point.len_square(), self._radius * self._radius)

    def center(self):
        return Matrix([0, 0], 'vec')


class Ellipse(Shape):
    def __init__(self, width, height):
        self._type = self.Type.Ellipse
        self._width = width
        self._height = height

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
        return Matrix([0, 0], 'vec')

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
        self._start_point = Matrix[0, 0, 'vec']
        self._ctrl_point1 = Matrix[0, 0, 'vec']
        self._ctrl_point2 = Matrix[0, 0, 'vec']
        self._end_point = Matrix[0, 0, 'vec']

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
        return Matrix([0, 0], 'vec')


class Capsule(Shape):
    def __init__(self, width, height):
        self._type = self.Type.Capsule
        self._width = width
        self._height = height

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

    def topLeft(self):
        res = Matrix([0, 0], 'vec')
        if self._width > self._height:
            tmp = self._height / 2.0
            res.set_value(-self._width / 2.0 + tmp, tmp)
        else:
            tmp = self._width / 2.0
            res.set_value(-tmp, self._height / 2.0 - tmp)

        return res

    def bottomLeft(self):
        res = Matrix([0, 0], 'vec')
        if self._width > self._height:
            tmp = self._height / 2.0
            res.set_value(-self._width / 2.0 + tmp, -tmp)
        else:
            tmp = self._width / 2.0
            res.set_value(-tmp, -self._height / 2.0 + tmp)

        return res

    def topRight(self):
        return -self.bottomLeft()

    def bottomRight(self):
        return -self.topLeft()

    def boxVertices(self):
        vertices = []
        vertices.append(self.topLeft())
        vertices.append(self.bottomLeft())
        vertices.append(self.bottomRight())
        vertices.append(self.topRight())
        vertices.append(self.topLeft())
        return vertices

    def scale(self, factor):
        self._width *= factor
        self._height *= factor

    # TODO: no impl
    def contains(self, point):
        return False

    def center(self):
        return Matrix([0, 0], 'vec')


class Sector(Shape):
    def __init__(self):
        self._type = self.Type.Sector
        self._start_radian = 0
        self._end_radian = 0
        self._radius = 0

    def vertices(self):
        pass

    def startRadian(self):
        pass

    def setStartRadian(self):
        pass

    def spanRadian(self):
        pass

    def setSpanRaidin(self):
        pass

    def radius(self):
        pass

    def set_radius(self):
        pass

    def set_value(self):
        pass

    def area(self):
        pass

    def scale(self):
        pass

    def contains(self, point):
        theta = point.theta()
        return

    def center(self):
        pass


p1 = Point()
