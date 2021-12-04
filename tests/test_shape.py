import numpy as np
from typing import Any, List, Optional

from TaichiGAME.math.matrix import Matrix
from TaichiGAME.geometry.shape import *


class TestShape():
    shape1: Shape = Shape()
    assert 1


class TestShapePrimitive():
    def test_translate(self):
        prim: ShapePrimitive = ShapePrimitive()
        vec1 = Matrix([23.0, 234.0], 'vec')
        assert prim.translate(vec1) == Matrix([23.0, 234.0], 'vec')


class TestPoint():
    def test_init(self):
        p1: Point = Point()
        assert np.isclose(p1.pos.x, 0)
        assert np.isclose(p1.pos.y, 0)

    def test_conains(self):
        p1: Point = Point()
        p1.pos = Matrix([2.0, 3.0], 'vec')
        assert p1.contains(Matrix([2.0, 3.0], 'vec'))
        assert not p1.contains(Matrix([2.0, 10.0], 'vec'))


class TestPolygon():
    def test_contains(self):
        poly1: Polygon = Polygon()
        ver_list: List[Matrix] = []
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        poly1.vertices = ver_list

        # the pos is normalizated to the [-width/2, widhth/2] [-heigh/2, heigh/2]
        assert poly1.contains(Matrix([0.0, 0.0], 'vec'))
        assert poly1.contains(Matrix([2.0, 2.0], 'vec'))
        assert not poly1.contains(Matrix([2.0, 3.0], 'vec'))
        assert not poly1.contains(Matrix([2.0, 4.0], 'vec'))

    def test_center(self):
        poly1: Polygon = Polygon()
        ver_list: List[Matrix] = []
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        poly1.vertices = ver_list

        assert poly1.center() == Matrix([0.0, 0.0], 'vec')


class TestRectangle():
    def test_contains(self):
        rect1: Rectangle = Rectangle(12.0, 12.0)
        assert rect1.contains(Matrix([4.0, -3.0], 'vec'))
        assert not rect1.contains(Matrix([6.0, -3.0], 'vec'))

    def test_calc_vertices(self):
        rect1: Rectangle = Rectangle(12.0, 12.0)
        assert rect1.vertices[0] == Matrix([-6.0, 6.0], 'vec')
        assert rect1.vertices[1] == Matrix([-6.0, -6.0], 'vec')
        assert rect1.vertices[2] == Matrix([6.0, -6.0], 'vec')
        assert rect1.vertices[3] == Matrix([6.0, 6.0], 'vec')
        assert rect1.vertices[4] == Matrix([-6.0, 6.0], 'vec')


class TestCricle():
    def test_contains(self):
        cir1: Circle = Circle(12)
        assert cir1.contains(Matrix([2.0, 3.0], 'vec'))
        assert cir1.contains(Matrix([6.0, 6.0], 'vec'))


class TestEllipse():
    def test_contains(self):
        ellipse: Ellipse = Ellipse()
        assert not ellipse.contains(Matrix([0.0, 0.0], 'vec'))


class TestEdge():
    def test_contains(self):
        edg1: Edge = Edge()
        edg1.set_value(Matrix([2.0, 2.0], 'vec'), Matrix([8.0, 8.0], 'vec'))
        print(edg1._normal)
        assert edg1.contains(Matrix([3.0, 3.0], 'vec'))
        assert not edg1.contains(Matrix([1.0, 8.0], 'vec'))


class TestCurve():
    def test_contains(self):
        curve: Curve = Curve()
        assert not curve.contains(Matrix([0.0, 0.0], 'vec'))


class TestCapsule():
    def test_top_left(self):
        cap: Capsule = Capsule(16.0, 8.0)
        assert cap.top_left() == Matrix([-4.0, 4.0], 'vec')

    def test_bottom_left(self):
        cap: Capsule = Capsule(16.0, 8.0)
        assert cap.bottom_left() == Matrix([-4.0, -4.0], 'vec')

    def test_contains(self):
        cap: Capsule = Capsule(16.0, 8.0)
        assert cap.contains(Matrix([0.0, 0.0], 'vec'))
        assert cap.contains(Matrix([4.0, 4.0], 'vec'))
        assert not cap.contains(Matrix([4.0, 5], 'vec'))
        assert cap.contains(Matrix([5.0, 3.0], 'vec'))


class TestSector():
    def test_vertices(self):
        sect: Sector = Sector()
        sect.set_value(0, np.pi / 4, 6)
        res: List[Matrix] = sect.vertices()
        assert res[0] == Matrix([0.0, 0.0], 'vec')
        assert res[1] == Matrix([6.0, 0.0], 'vec')
        assert res[2] == Matrix([4.2426, 4.2426], 'vec')
        assert res[3] == Matrix([0.0, 0.0], 'vec')

    def test_contains(self):
        sect: Sector = Sector()
        sect.set_value(0, np.pi / 4, 6)
        assert sect.contains(Matrix([1.0, 0.0], 'vec'))
        assert sect.contains(Matrix([0.0, 4.0], 'vec'))
        assert sect.contains(Matrix([0.0, 6.0], 'vec'))
        assert not sect.contains(Matrix([0.0, 7.0], 'vec'))
