import numpy as np

from ..math.matrix import Matrix


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

    def position(self):
        return self.pos

    def set_position(self, pos):
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
        self.updateVertices()

    def scale(self, factor):
        assert (len(self.vertices))
        self.vertices = [v * factor for v in self.vertices]

    def contains(self):
        assert (1)

    def center(self):
        pass

    def updateVertices(self):
        pass


class Rectangle(Shape):
    def __init__(self):
        pass

    def set(self):
        pass

    def width(self):
        pass

    def setWidth(self):
        pass

    def height(self):
        pass

    def setHeight(self):
        pass

    def scale(self):
        pass

    def contains(self):
        pass

    def calcVertices(self):
        pass


class Circle(Shape):
    def __init__(self):
        pass

    def radius(self):
        pass

    def setRadius(self):
        pass

    def scale(self):
        pass

    def contains(self):
        pass

    def center(self):
        pass


class Ellipse(Shape):
    def __init__(self):
        pass

    def set(self):
        pass

    def width(self):
        pass

    def setWidth(self):
        pass

    def height(self):
        pass

    def setHeight(self):
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

    def setWidth(self):
        pass

    def height(self):
        pass

    def setHeight(self):
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

    def setRadius(self):
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
