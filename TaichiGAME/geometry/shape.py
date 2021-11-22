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

    def get_type(self):
        return self.type

    def scale(self, factor):
        pass

    def contains(self, point):
        pass

    def center(self):
        pass


class ShapePrimitive():
    def __init__(self):
        self.shape = None
        self.transform = None
        self.rotation = 0

    def translate(self, src):
        pass


class Point(Shape):
    def __init__(self):
        self.type = self.Type.Point
        self.pos = Matrix([0, 0], 'vec')

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def scale(self, factor):
        self.pos *= factor

    def contains(self, point):
        return np.isclose(self.pos - point)

    def center(self):
        return self.pos


class Polygon(Shape):
    def __init__(self):
        self.type = self.Type.Polygon
        self.vertices = []

    def get_vertices(self):
        return self.vertices

    def append(self, vertices):
        for v in vertices:
            self.vertices.append(v)
        self.update_vertices()

    def scale(self, factor):
        assert (len(self.vertices))
        self.vertices = [v * factor for v in self.vertices]

    def contains(self, point):
        assert (len(self.vertices) > 2)
        num = len(self.vertices)
        for i in range(num):
            p1 = self.vertices[i]
            p2 = self.vertices[i + 1]
            ref = self.vertices[1] if i + 2 == num else self.vertices[
                i + 2]  # TODO: why [1]?
            if not GeomAlgo2D.is_point_on_same_side(p1, p2, ref, point):
                return False

        return True

    def center(self):
        return GeomAlgo2D.calculate_center(self.vertices)

    def update_vertices(self):
        center_point = self.center()
        self.vertices = [v - center_point for v in self.vertices]


class Rectangle(Polygon):
    def __init__(self, width, height):
        super().__init__()
        self.set(width, height)

    def set(self, width, height):
        self.width = width
        self.height = height
        self.calc_vertices()

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self.calc_vertices()

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height
        self.calc_vertices()

    def scale(self, factor):
        self.width *= factor
        self.height *= factor
        self.calc_vertices()

    def contains(self, point):
        return (point.val[0] > -self.width * 0.5 and point.val[0] <
                self.width * 0.5) and (point.val[1] > -self.height * 0.5
                                       and point.val[1] < self.height * 0.5)

    def calc_vertices(self):
        self.vertices = []
        self.vertices.append(
            Matrix([-self.width * 0.5, self.height * 0.5], 'vec'))
        self.vertices.append(
            Matrix([-self.width * 0.5, -self.height * 0.5], 'vec'))
        self.vertices.append(
            Matrix([self.width * 0.5, -self.height * 0.5], 'vec'))
        self.vertices.append(
            Matrix([self.width * 0.5, self.height * 0.5], 'vec'))
        self.vertices.append(
            Matrix([-self.width * 0.5, self.height * 0.5], 'vec'))


class Circle(Shape):
    def __init__(self, radius):
        self.type = self.Type.Circle
        self.radius = radius

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius

    def scale(self, factor):
        self.radius *= factor

    def contains(self, point):
        return np.isclose(point.len_square(), self.radius * self.radius)

    def center(self):
        return Matrix([0, 0], 'vec')


class Ellipse(Shape):
    def __init__(self):
        pass

    def set(self):
        pass

    def width(self):
        pass

    def set_width(self):
        pass

    def height(self):
        pass

    def set_height(self):
        pass

    def scale(self):
        pass

    def contains(self):
        pass

    def center(self):
        pass

    def A():
        pass

    def B():
        pass

    def C():
        pass


class Edge(Shape):
    def __init__(self):
        pass

    def set(self):
        pass

    def startPoint(self):
        pass

    def setStartPoint(self):
        pass

    def endPoint(self):
        pass

    def setEndPoint(self):
        pass

    def scale(self):
        pass

    def contains(self):
        pass

    def center(self):
        pass

    def normal(self):
        pass

    def setNormal(self):
        pass


class Curve(Shape):
    def __init__(self):
        pass

    def startPoint(self):
        pass

    def setStartPoint(self):
        pass

    def control1(self):
        pass

    def setControl1(self):
        pass

    def control2(self):
        pass

    def setControl2(self):
        pass

    def endPoint(self):
        pass

    def setEndPoint(self):
        pass

    def scale(self):
        pass

    def contains(self):
        pass

    def center(self):
        pass


class Capsule(Shape):
    def __init__(self):
        pass

    def set(self):
        pass

    def width(self):
        pass

    def set_width(self):
        pass

    def height(self):
        pass

    def set_height(self):
        pass

    def topLeft(self):
        pass

    def bottomLeft(self):
        pass

    def topRight(self):
        pass

    def bottomRight(self):
        pass

    def boxVertices(self):
        pass

    def scale(self):
        pass

    def contains(self):
        pass

    def center(self):
        pass


class Sector(Shape):
    def __init__(self):
        pass

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

    def set(self):
        pass

    def area(self):
        pass

    def scale(self):
        pass

    def contains(self):
        pass

    def center(self):
        pass


p1 = Point()
