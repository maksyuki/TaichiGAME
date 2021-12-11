from typing import List
import numpy as np
from TaichiGAME.geometry.shape import Polygon, ShapePrimitive

from TaichiGAME.math.matrix import Matrix
from TaichiGAME.collision.algorithm.gjk import GJK, Simplex
from TaichiGAME.collision.algorithm.gjk import Minkowski, PenetrationInfo
from TaichiGAME.collision.algorithm.gjk import PenetrationSource, PointPair


class TestMinkowski():
    def test__init__(self):
        dut: Minkowski = Minkowski()
        assert dut._pa == Matrix([0.0, 0.0], 'vec')
        assert dut._pb == Matrix([0.0, 0.0], 'vec')
        assert dut._res == Matrix([0.0, 0.0], 'vec')

        dut = Minkowski(Matrix([1.2, 3.4], 'vec'), Matrix([5.6, 7.8], 'vec'))
        assert dut._pa == Matrix([1.2, 3.4], 'vec')
        assert dut._pb == Matrix([5.6, 7.8], 'vec')
        assert dut._res == Matrix([-4.4, -4.4], 'vec')

    def test__eq__(self):
        dut1: Minkowski = Minkowski()
        dut2: Minkowski = Minkowski()
        dut3: Minkowski = Minkowski(Matrix([1.2, 3.4], 'vec'),
                                    Matrix([5.6, 7.8], 'vec'))
        assert dut1 == dut2
        assert dut1 != dut3

    def test__neq__(self):
        dut1: Minkowski = Minkowski()
        dut2: Minkowski = Minkowski()
        dut3: Minkowski = Minkowski(Matrix([1.2, 3.4], 'vec'),
                                    Matrix([5.6, 7.8], 'vec'))
        assert dut1 == dut2
        assert dut1 != dut3


class TestSimplex():
    def test__init__(self):
        dut: Simplex = Simplex()

        assert not dut._is_contain_origin
        assert len(dut._vertices) == 0

    def test_contain_origin(self):
        # same as test__contain_origin
        dut: Simplex = Simplex()
        assert not dut.contain_origin()

        dut._vertices.append(
            Minkowski(Matrix([2.0, 2.0], 'vec'), Matrix([1.0, 1.0], 'vec')))
        dut._vertices.append(
            Minkowski(Matrix([-2.0, 1.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        assert not dut.contain_origin()

        dut._vertices.append(
            Minkowski(Matrix([3.0, 0.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        dut._vertices.append(
            Minkowski(Matrix([2.0, 2.0], 'vec'), Matrix([1.0, 1.0], 'vec')))
        assert dut.contain_origin()

    def test_insert(self):
        dut: Simplex = Simplex()
        dut.insert(0, Minkowski())
        dut.insert(
            1, Minkowski(Matrix([3.0, 0.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        dut.insert(
            1, Minkowski(Matrix([1.0, 0.0], 'vec'), Matrix([3.0, 3.0], 'vec')))

        print(dut._vertices[0]._pa)
        print(dut._vertices[0]._pb)
        print(dut._vertices[1]._pa)
        print(dut._vertices[1]._pb)
        print(dut._vertices[2]._pa)
        print(dut._vertices[2]._pb)

        assert dut._vertices[1] == Minkowski(Matrix([3.0, 0.0], 'vec'),
                                             Matrix([3.0, 3.0], 'vec'))

    def test_contain(self):
        dut: Simplex = Simplex()
        dut.insert(0, Minkowski())
        dut.insert(
            1, Minkowski(Matrix([3.0, 0.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        dut.insert(
            1, Minkowski(Matrix([1.0, 0.0], 'vec'), Matrix([3.0, 3.0], 'vec')))

        assert dut.contains(Minkowski())
        assert dut.contains(
            Minkowski(Matrix([3.0, 0.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        assert not dut.contains(
            Minkowski(Matrix([3.0, 0.0], 'vec'), Matrix([3.0, 4.0], 'vec')))

    def test_last_vertex(self):
        dut: Simplex = Simplex()
        dut.insert(0, Minkowski())
        dut.insert(
            1, Minkowski(Matrix([3.0, 0.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        assert dut.last_vertex() == Matrix([0.0, -3.0], 'vec')

        dut.insert(
            1, Minkowski(Matrix([3.0, 4.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        assert dut.last_vertex() == Matrix([0.0, -3.0], 'vec')

        dut.insert(
            1, Minkowski(Matrix([3.0, 5.0], 'vec'), Matrix([3.0, 3.0], 'vec')))
        assert dut.last_vertex() == Matrix([0.0, 2.0], 'vec')


class TestPenetrationInfo():
    def test__init__(self):
        dut: PenetrationInfo = PenetrationInfo()

        assert dut._normal == Matrix([0.0, 0.0], 'vec')
        assert np.isclose(dut._penetration, 0)


class TestPenetrationSource():
    def test__init__(self):
        dut: PenetrationSource = PenetrationSource()

        assert dut._a1 == Matrix([0.0, 0.0], 'vec')
        assert dut._a2 == Matrix([0.0, 0.0], 'vec')
        assert dut._b1 == Matrix([0.0, 0.0], 'vec')
        assert dut._b2 == Matrix([0.0, 0.0], 'vec')


class TestPointPair():
    def test__init__(self):
        dut: PointPair = PointPair()

        assert dut._pa == Matrix([0.0, 0.0], 'vec')
        assert dut._pb == Matrix([0.0, 0.0], 'vec')

    def test__eq__(self):
        dut1: PointPair = PointPair()
        dut2: PointPair = PointPair()
        dut3: PointPair = PointPair()
        dut3._pa = Matrix([2.3, 4.5], 'vec')

        assert dut1 == dut2
        assert dut1 != dut3

    def test_is_empty(self):
        dut1: PointPair = PointPair()
        dut2: PointPair = PointPair()
        dut2._pa = Matrix([2.3, 4.5], 'vec')

        assert dut1.is_empty()
        assert not dut2.is_empty()


class TestGJK():
    def test_gjk(self):
        prima: ShapePrimitive = ShapePrimitive()
        primb: ShapePrimitive = ShapePrimitive()

        polya: Polygon = Polygon()
        polyb: Polygon = Polygon()

        dataa: List[Matrix] = [
            Matrix([4.0, 4.0], 'vec'),
            Matrix([3.0, 3.0], 'vec'),
            Matrix([3.0, 1.0], 'vec'),
            Matrix([6.0, 2.0], 'vec'),
            Matrix([4.0, 4.0], 'vec')
        ]

        datab: List[Matrix] = [
            Matrix([2.0, 3.0], 'vec'),
            Matrix([4.0, 2.0], 'vec'),
            Matrix([1.0, 1.0], 'vec'),
            Matrix([0.0, 2.0], 'vec'),
            Matrix([2.0, 3.0], 'vec')
        ]
        polya.vertices = dataa
        polyb.vertices = datab

        prima._shape = polya
        primb._shape = polyb
        prima._xform = Matrix([4.0, 3.0], 'vec')
        primb._xform = Matrix([2.0, 2.0], 'vec')
        prima._rot = 0.0
        primb._rot = 0.0

        # print(f'polya center: {polya.center()}')
        # print(f'polyb center: {polyb.center()}')
        (is_collision, simplex) = GJK.gjk(prima, primb)
        print(f'collision: {is_collision}')
        assert is_collision

        simplex = GJK.epa(prima, primb, simplex)
        for m in simplex._vertices:
            print(f'point: {m._res}')

        assert 1

    def test_epa(self):
        # tested in test_gjk
        assert 1

    def test_dump_info(self):
        assert 1

    def test_support(self):
        # tested in test_gjk
        assert 1

    def test_find_edge_closest_to_origin(self):
        # tested in test_gjk
        assert 1

    def test_find_farthest_point(self):
        # tested in test_gjk
        assert 1

    def test_adjust_simplex(self):
        # tested in test_gjk
        assert 1

    def test_calc_direction_by_edge(self):
        # tested in test_gjk
        assert 1

    def test_distance(self):
        assert 1

    def test_dump_source(self):
        assert 1

    def test_dump_points(self):
        assert 1
