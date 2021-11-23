import numpy as np

from TaichiGAME.math.matrix import Matrix
from TaichiGAME.geometry.shape import *


class TestShape():
    assert 1


class TestPoint():
    def test_init(self):
        p1 = Point()
        assert np.isclose(p1._pos.val[0], 0)
        assert np.isclose(p1._pos.val[1], 0)

    def test_conains(self):
        p1 = Point()
        p1.set_pos(Matrix([2.0, 3.0], 'vec'))
        assert p1.contains(Matrix([2.0, 3.0], 'vec'))
        assert not p1.contains(Matrix([2.0, 10.0], 'vec'))


class TestPolygon():
    def test_contains(self):
        poly1 = Polygon()
        ver_list = []
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        poly1.append(ver_list)

        # the pos is normalizated to the [-width/2, widhth/2] [-heigh/2, heigh/2]
        assert poly1.contains(Matrix([2.0, 2.0], 'vec'))
        assert not poly1.contains(Matrix([2.0, 4.0], 'vec'))

    def test_center(self):
        poly1 = Polygon()
        ver_list = []
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 0.0], 'vec'))
        ver_list.append(Matrix([6.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 6.0], 'vec'))
        ver_list.append(Matrix([0.0, 0.0], 'vec'))
        poly1.append(ver_list)

        assert poly1.center() == Matrix([0.0, 0.0], 'vec')


class TestRectangle():
    def test_contains(self):
        rect1 = Rectangle(12.0, 12.0)
        assert rect1.contains(Matrix([4.0, -3.0], 'vec'))
        assert not rect1.contains(Matrix([6.0, -3.0], 'vec'))

    def test_calc_vertices(self):
        rect1 = Rectangle(12.0, 12.0)
        assert rect1._vertices[0] == Matrix([-6.0, 6.0], 'vec')
        assert rect1._vertices[1] == Matrix([-6.0, -6.0], 'vec')
        assert rect1._vertices[2] == Matrix([6.0, -6.0], 'vec')
        assert rect1._vertices[3] == Matrix([6.0, 6.0], 'vec')
        assert rect1._vertices[4] == Matrix([-6.0, 6.0], 'vec')


class TestCricle():
    def test_contains(self):
        cir1 = Circle(12)
        assert cir1.contains(Matrix([2.0, 3.0], 'vec'))
        assert cir1.contains(Matrix([6.0, 6.0], 'vec'))


class TestEllipse():
    assert 1


class TestEdge():
    def test_contains(self):
        edg1 = Edge()
        edg1.set_value(Matrix([2.0, 2.0], 'vec'), Matrix([8.0, 8.0], 'vec'))
        print(edg1._normal)
        assert edg1.contains(Matrix([3.0, 3.0], 'vec'))
        assert not edg1.contains(Matrix([1.0, 8.0], 'vec'))


class TestCurve():
    assert 1


class TestCapsule():
    assert 1


class TestSector():
    assert 1
