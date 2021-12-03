from typing import List, Dict, Optional, Tuple

import numpy as np

from TaichiGAME.math.matrix import Matrix
from TaichiGAME.geometry.geom_algo import GeomAlgo2D


class TestGeomAlgo2D():
    org: Matrix = Matrix([0.0, 0.0], 'vec')
    pa1: Matrix = Matrix([1.0, 1.0], 'vec')
    pb1: Matrix = Matrix([2.0, 2.0], 'vec')
    pc1: Matrix = Matrix([-3.0, -3.0], 'vec')

    pa2: Matrix = Matrix([-1.0, 2.0], 'vec')
    pb2: Matrix = Matrix([3.0, 1.0], 'vec')
    pc2: Matrix = Matrix([-3.0, 0.0], 'vec')

    dir_0: Matrix = Matrix([1.0, 0.0], 'vec')
    dir_45: Matrix = Matrix([1.0, 1.0], 'vec')
    dir_90: Matrix = Matrix([0.0, 1.0], 'vec')
    dir_135: Matrix = Matrix([-1.0, 1.0], 'vec')
    dir_180: Matrix = Matrix([-1.0, 0.0], 'vec')

    poly1: List[Matrix] = [
        Matrix([-3.0, -3.0], 'vec'),
        Matrix([3.0, -3.0], 'vec'),
        Matrix([3.0, 3.0], 'vec'),
        Matrix([-3.0, 3.0], 'vec'),
        Matrix([-3.0, -3.0], 'vec')
    ]

    poly2: List[Matrix] = [
        Matrix([-2.0, -3.0], 'vec'),
        Matrix([2.0, -3.0], 'vec'),
        Matrix([0.0, 5.0], 'vec'),
        Matrix([-2.0, -3.0], 'vec'),
    ]

    poly3: List[Matrix] = [
        Matrix([2.0, -3.0], 'vec'),
        Matrix([0.5, 3.0], 'vec'),
        Matrix([-0.5, 3.0], 'vec'),
        Matrix([-2.0, -3.0], 'vec'),
        Matrix([2.0, -3.0], 'vec'),
    ]

    poly4: List[Matrix] = [
        Matrix([-3.0, -3.0], 'vec'),
        Matrix([3.0, -3.0], 'vec'),
        Matrix([-1.0, -1.0], 'vec'),
        Matrix([-3.0, 3.0], 'vec'),
        Matrix([-3.0, -3.0], 'vec')
    ]

    poly5: List[Matrix] = [
        Matrix([-3.0, -3.0], 'vec'),
        Matrix([-3.0, -3.0], 'vec'),
        Matrix([3.0, -3.0], 'vec'),
        Matrix([-3.0, 3.0], 'vec'),
        Matrix([-3.0, -3.0], 'vec')
    ]

    def test_sutherland_hodgment_polygon_clipping(self):
        # NOTE: need to test more, the seq is important
        res = GeomAlgo2D.Clipper.sutherland_hodgment_polygon_clipping(
            TestGeomAlgo2D.poly2, TestGeomAlgo2D.poly1)

        for dut, ref in zip(res, TestGeomAlgo2D.poly3):
            assert dut == ref

    def test_is_collinear(self):
        assert GeomAlgo2D.is_collinear(TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1,
                                       TestGeomAlgo2D.pc1)

        assert not GeomAlgo2D.is_collinear(
            TestGeomAlgo2D.pa2, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pc1)

    def test_is_fuzzy_collinear(self):
        assert not GeomAlgo2D.is_fuzzy_collinear(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pc1)
        assert GeomAlgo2D.is_fuzzy_collinear(TestGeomAlgo2D.pc1,
                                             TestGeomAlgo2D.pb1,
                                             TestGeomAlgo2D.pa1)
        assert GeomAlgo2D.is_fuzzy_collinear(TestGeomAlgo2D.pb1,
                                             TestGeomAlgo2D.pc1,
                                             TestGeomAlgo2D.pa1)

    def test_is_point_on_segment(self):
        assert not GeomAlgo2D.is_point_on_segment(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pc1)

        assert GeomAlgo2D.is_point_on_segment(TestGeomAlgo2D.pc1,
                                              TestGeomAlgo2D.pb1,
                                              TestGeomAlgo2D.pa1)
        assert GeomAlgo2D.is_point_on_segment(TestGeomAlgo2D.pb1,
                                              TestGeomAlgo2D.pc1,
                                              TestGeomAlgo2D.pa1)

    def test_line_segment_intersection(self):
        #NOTE: need to check the valid under the overlap situation
        assert (GeomAlgo2D.line_segment_intersection(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pa2,
            TestGeomAlgo2D.pb2)._val == [1.4, 1.4]).all()

        assert GeomAlgo2D.line_segment_intersection(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pa2,
            TestGeomAlgo2D.pa1) == TestGeomAlgo2D.pa1

        assert GeomAlgo2D.line_segment_intersection(TestGeomAlgo2D.pa1,
                                                    TestGeomAlgo2D.pb1,
                                                    TestGeomAlgo2D.pa2,
                                                    TestGeomAlgo2D.pc1) == None

    def test_line_intersection(self):
        assert GeomAlgo2D.line_intersection(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pa2,
            TestGeomAlgo2D.pb2) == Matrix([1.4, 1.4], 'vec')

        assert GeomAlgo2D.line_intersection(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pa2,
            TestGeomAlgo2D.pc1) == TestGeomAlgo2D.pc1

        assert GeomAlgo2D.line_intersection(TestGeomAlgo2D.pa1,
                                            TestGeomAlgo2D.pb1,
                                            TestGeomAlgo2D.pa2,
                                            TestGeomAlgo2D.pc2) == None

    def test_calc_circum_center(self):
        assert GeomAlgo2D.calc_circum_center(TestGeomAlgo2D.pa1,
                                             TestGeomAlgo2D.pb1,
                                             TestGeomAlgo2D.pc1) == None

        dut1: Tuple[Matrix, float] = GeomAlgo2D.calc_circum_center(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pa2)

        assert dut1[0] == Matrix([0.5, 2.5], 'vec')
        assert np.isclose(dut1[1], 1.58113)

    def test_calc_inscribed_center(self):
        assert GeomAlgo2D.calc_inscribed_center(TestGeomAlgo2D.pa1,
                                                TestGeomAlgo2D.pb1,
                                                TestGeomAlgo2D.pc1) == None

        dut1: Tuple[Matrix, float] = GeomAlgo2D.calc_inscribed_center(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1, TestGeomAlgo2D.pa2)

        assert dut1[0] == Matrix([0.91092, 1.54889], 'vec')
        assert np.isclose(dut1[1], 0.451108)

    def test_is_convex_polygon(self):
        assert GeomAlgo2D.is_convex_polygon(TestGeomAlgo2D.poly1)
        assert GeomAlgo2D.is_convex_polygon(TestGeomAlgo2D.poly2)
        assert GeomAlgo2D.is_convex_polygon(TestGeomAlgo2D.poly3)
        assert not GeomAlgo2D.is_convex_polygon(TestGeomAlgo2D.poly4)

    def test_graham_scan(self):
        # NOTE: need to focus on the convex hull format
        dut1 = GeomAlgo2D.graham_scan(TestGeomAlgo2D.poly4)

        for dut, ref in zip(dut1, TestGeomAlgo2D.poly5):
            assert dut == ref

    def test_point_to_line_segment(self):
        assert GeomAlgo2D.point_to_line_segment(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1,
            TestGeomAlgo2D.pc1) == TestGeomAlgo2D.pa1

        assert GeomAlgo2D.point_to_line_segment(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1,
            TestGeomAlgo2D.pa2) == Matrix([1.0, 1.0], 'vec')

    def test_shortest_length_point_of_ellipse(self):
        assert GeomAlgo2D.shortest_length_point_of_ellipse(
            2, 1, TestGeomAlgo2D.pc2) == Matrix([-2.0, 0], 'vec')

    def test_triangle_centroid(self):
        assert 1

    def test_triangle_area(self):
        assert np.isclose(
            GeomAlgo2D.triangle_area(TestGeomAlgo2D.pa1, TestGeomAlgo2D.pb1,
                                     TestGeomAlgo2D.pa2), 1.5)

    def test_calc_mass_center(self):
        assert GeomAlgo2D.calc_mass_center(TestGeomAlgo2D.poly1) == Matrix(
            [0.0, 0.0], 'vec')

    def test_shortest_length_line_segment_ellipse(self):
        assert 1  #FIXME: need to modify

    def test_raycast(self):
        assert GeomAlgo2D.raycast(TestGeomAlgo2D.pa2, Matrix([1.0, -1.0],
                                                             'vec'),
                                  TestGeomAlgo2D.pb1,
                                  TestGeomAlgo2D.pc1) == Matrix([0.2, 0.2],
                                                                'vec')

        assert GeomAlgo2D.raycast(TestGeomAlgo2D.pa2, Matrix([-1.0, 1.0],
                                                             'vec'),
                                  TestGeomAlgo2D.pa1,
                                  TestGeomAlgo2D.pb1) == None

    def test_raycastAABB(self):
        assert 1  #FIXME: need to modify

    def test_is_point_on_AABB(self):
        assert GeomAlgo2D.is_point_on_AABB(TestGeomAlgo2D.pa1,
                                           TestGeomAlgo2D.pa2,
                                           TestGeomAlgo2D.pb2)

        assert GeomAlgo2D.is_point_on_AABB(TestGeomAlgo2D.pb1,
                                           TestGeomAlgo2D.pa2,
                                           TestGeomAlgo2D.pb2)

        assert not GeomAlgo2D.is_point_on_AABB(
            TestGeomAlgo2D.pc1, TestGeomAlgo2D.pa2, TestGeomAlgo2D.pb2)

    def test_rotate(self):
        GeomAlgo2D.rotate(TestGeomAlgo2D.pa1, TestGeomAlgo2D.org, np.pi / 4) == Matrix([0.0, 1.41421], 'vec')

    def test_calc_ellipse_project_on_point(self):
        print (GeomAlgo2D.calc_ellipse_project_on_point(2, 1, TestGeomAlgo2D.dir_0))
        print (GeomAlgo2D.calc_ellipse_project_on_point(2, 1, TestGeomAlgo2D.dir_45))
        print (GeomAlgo2D.calc_ellipse_project_on_point(2, 1, TestGeomAlgo2D.dir_90))
        print (GeomAlgo2D.calc_ellipse_project_on_point(2, 1, TestGeomAlgo2D.dir_135))
        print (GeomAlgo2D.calc_ellipse_project_on_point(2, 1, TestGeomAlgo2D.dir_180))
        assert 1

    def test_calc_capsule_project_on_point(self):
        assert 1

    def test_calc_sector_project_on_point(self):
        assert 1

    def test_is_triangle_contain_origin(self):
        assert not GeomAlgo2D.is_triangle_contain_origin(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pa2, TestGeomAlgo2D.pc2)

        assert GeomAlgo2D.is_triangle_contain_origin(TestGeomAlgo2D.pa2,
                                                     TestGeomAlgo2D.pb2,
                                                     TestGeomAlgo2D.pc1)

    def test_is_point_on_same_side(self):
        assert not GeomAlgo2D.is_point_on_same_side(
            TestGeomAlgo2D.pa1, TestGeomAlgo2D.pc1, TestGeomAlgo2D.pa2,
            TestGeomAlgo2D.pb2)

        assert GeomAlgo2D.is_point_on_same_side(TestGeomAlgo2D.pa1,
                                                TestGeomAlgo2D.pc1,
                                                TestGeomAlgo2D.pa2,
                                                TestGeomAlgo2D.pc2)
