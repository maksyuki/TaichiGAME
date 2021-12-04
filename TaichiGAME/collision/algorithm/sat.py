from typing import List, Dict, Optional, Tuple

import numpy as np
from numpy.linalg import norm

from ...math.matrix import Matrix
from ...common.config import Config
from .gjk import PointPair
from ...geometry.geom_algo import GeomAlgo2D
from ...geometry.shape import Circle, Edge, Ellipse, Polygon, Shape, ShapePrimitive


class ProjectedPoint():
    def __init__(self):
        self._vertex: Matrix = Matrix([0.0, 0.0], 'vec')
        self._val: float = 0.0
        self._idx: int = -1

    def __eq__(self, other) -> bool:
        return self._vertex == other._vertex and np.isclose(
            self._val, other._val)


class ProjectedEdge():
    def __init__(self):
        self._vertex1 = Matrix([0.0, 0.0], 'vec')
        self._vertex2 = Matrix([0.0, 0.0], 'vec')


class ProjectedSegment():
    def __init__(self):
        self._min = ProjectedPoint()
        self._max = ProjectedPoint()

    @staticmethod
    def intersect(s1, s2):
        diff: float = Config.NegativeMin
        res = ProjectedSegment()

        if s1._min._val <= s2._min._val and s1._max._val <= s2._max._val:
            diff = s1._max._val - s2._min._val
            res._max = s1._max
            res._min = s2._min

        elif s2._min._val <= s1._min._val and s2._max._val <= s1._max._val:
            diff = s2._max._val - s1._min._val
            res._max = s2._max
            res._min = s1._min

        elif s1._min._val >= s2._min._val and s1._max._val <= s2._max._val:

            if (s1._max._val - s2._min._val) > (s2._max._val - s1._min._val):

                diff = s1._max._val - s2._min._val
                res._max = s1._max
                res._min = s2._min

            else:

                diff = s2._max._val - s1._min._val
                res._max = s2._max
                res._min = s1._min

        elif s2._min._val >= s1._min._val and s2._max._val <= s1._max._val:

            if (s2._max._val - s1._min._val) > (s1._max._val - s2._min._val):

                diff = s2._max._val - s1._min._val
                res._max = s2._max
                res._min = s1._min

            else:

                diff = s1._max._val - s2._min._val
                res._max = s1._max
                res._min = s2._min

        return (res, diff)


class SATResult():
    def __init__(self):
        self._contact_pair: List[PointPair] = []
        self._contact_pair_count: int = 0
        self._normal: Matrix = Matrix([0.0, 0.0], 'vec')
        self._penetration: float = 0.0
        self._is_colliding: bool = False


class SAT():
    @staticmethod
    def circle_vs_capsule(prima: ShapePrimitive,
                          primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Circle
        assert primb._shape.type() == Shape.Type.Capsule
        res: SATResult = SATResult()
        return res

    @staticmethod
    def circle_vs_sector(prima: ShapePrimitive,
                         primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Circle
        assert primb._shape.type() == Shape.Type.Sector
        res: SATResult = SATResult()
        return res

    @staticmethod
    def circle_vs_edge(prima: ShapePrimitive,
                       primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Circle
        assert primb._shape.type() == Shape.Type.Edge

        res: SATResult = SATResult()
        circle: Circle = prima._shape
        edg: Edge = primb._shape

        actual_start: Matrix = primb._xform + edg.start
        actual_end: Matrix = primb._xform + edg.end
        normal: Matrix = (actual_start - actual_end).normal()

        if (actual_start - prima._xform).dot(normal) < 0 and (
                actual_end - primb._xform).dot(normal) < 0:
            normal.negate()

        proj_point: Matrix = GeomAlgo2D.point_to_line_segment(
            actual_start, actual_end, prima._xform)
        diff: Matrix = proj_point - prima._xform

        res._normal = diff.normal()
        length: float = diff.len()

        res._is_colliding = (length < circle.radius)
        res._penetration = circle.radius - length
        res._contact_pair[0]._pa = prima._xform + circle.radius * res._normal
        res._contact_pair[0]._pb = proj_point
        res._contact_pair_count += 1

        return res

    @staticmethod
    def circle_vs_circle(prima: ShapePrimitive,
                         primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Circle
        assert primb._shape.type() == Shape.Type.Circle

        res: SATResult = SATResult()
        cira: Circle = prima._shape
        cirb: Circle = primb._shape

        ba: Matrix = prima._xform - primb._xform
        dp: float = cira.radius + cirb.radius
        length: float = ba.len()

        if length <= dp:
            res._normal = ba.normal()
            res._penetration = dp - length
            res._is_colliding = True
            res._contact_pair[0]._pa = prima._xform - cira.radius * res._normal
            res._contact_pair[0]._pb = primb._xform + cirb.radius * res._normal
            res._contact_pair_count += 1

        return res

    @staticmethod
    def circle_vs_polygon(prima: ShapePrimitive,
                          primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Circle
        assert primb._shape.type() == Shape.Type.Polygon

        cira: Circle = prima._shape
        polyb: Polygon = primb._shape
        colliding_axis: int = 0
        res: SATResult = SATResult()

        len_min: float = Config.Max
        closest: Matrix = Matrix([0.0, 0.0], 'vec')

        for elem in polyb.vertices:
            vertex: Matrix = primb.translate(elem)
            length: float = (vertex - prima._xform).len_square()
            if len_min > length:
                len_min = length
                closest = vertex

        normal: Matrix = closest.normal()
        seg_cir: ProjectedSegment = SAT._axis_projection(prima, cira, normal)
        seg_poly: ProjectedSegment = SAT._axis_projection(primb, polyb, normal)

        (final_seg, length) = ProjectedSegment.intersect(seg_cir, seg_poly)

        if length > 0:
            colliding_axis += 1

        if res._penetration > length:
            res._penetration = length
            res._normal = normal

        cirp: ProjectedPoint = final_seg._max if seg_cir._max == final_seg._max else final_seg._min

        vert_len: int = len(polyb.vertices)
        for i in range(vert_len - 1):
            v1: Matrix = primb.translate(polyb.vertices[i])
            v2: Matrix = primb.translate(polyb.vertices[i + 1])
            edg: Matrix = v1 - v2
            normal: Matrix = edg.perpendicular().normal()

            segc = SAT._axis_projection(prima, cira, normal)
            segp = SAT._axis_projection(primb, polyb, normal)

            (tmp_segment,
             tmp_length) = ProjectedSegment.intersect(segc, segp)
            if tmp_length > 0:
                colliding_axis += 1

            if res._penetration > tmp_length and tmp_length > 0:
                res._penetration = tmp_length
                res._normal = normal
                cirp = tmp_segment._max if segc._max == tmp_segment._max else tmp_segment._min

        if colliding_axis == len(polyb.vertices):
            res._is_colliding = True

        res._contact_pair[0]._pa = cirp._vertex
        res._contact_pair[0]._pb = cirp._vertex + -res._normal * res._penetration
        res._contact_pair_count += 1

        return res

    @staticmethod
    def polygon_vs_polygon(prima: ShapePrimitive,
                           primb: ShapePrimitive) -> SATResult:

        def _test(prima: ShapePrimitive, primb: ShapePrimitive) -> SATResult:
            polya: Polygon = prima._shape
            polyb: Polygon = primb._shape

            final_normal: Matrix = Matrix([0.0, 0.0], 'vec')
            len_min: float = Config.Max
            colliding_axis: int = 0

            tgtap: ProjectedPoint = ProjectedPoint()
            tgtbp: ProjectedPoint = ProjectedPoint()

            polya_len: int = len(polya.vertices)
            for i in range(polya_len - 1):
                v1: Matrix = prima.translate(polya.vertices[i])
                v2: Matrix = prima.translate(polya.vertices[i + 1])
                edg: Matrix = v1 - v2
                normal: Matrix = edg.perpendicular().normal()

                sega: ProjectedSegment = SAT._axis_projection(prima, polya, normal)
                segb: ProjectedSegment = SAT._axis_projection(primb, polyb, normal)

                (final_seg, length) = ProjectedSegment.intersect(sega, segb)
                if length > 0:
                    colliding_axis += 1

                polyap:ProjectedPoint = final_seg._max if sega._max == final_seg._max else final_seg._min
                polybp:ProjectedPoint = final_seg._max if segb._max == final_seg._max else final_seg._min

                if len_min > length:
                    len_min = length
                    final_normal = normal
                    tgtap = polyap
                    tgtbp = polybp

            return (final_normal, len_min, colliding_axis, tgtap, tgtbp)


        assert prima._shape.type() == Shape.Type.Polygon
        assert primb._shape.type() == Shape.Type.Polygon

        polya: Polygon = prima._shape
        polyb: Polygon = primb._shape

        res:SATResult = SATResult()
        (normal1, length1, axis1, polyap1, polybp1) = _test(prima, primb)
        (normal2, length2, axis2, polybp2, polyap2) = _test(primb, prima)

        if axis1 + axis2 == len(polya.vertices) + len(polyb.vertices) - 2:
            res._is_colliding = True

        if length1 < length2:
            res._penetration = length1
            res._normal = normal1
        else:
            res._penetration = length2
            res.normal = normal2

    @staticmethod
    def polygon_vs_edge(prima: ShapePrimitive,
                        primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Polygon
        assert primb._shape.type() == Shape.Type.Edge
        return SATResult()

    @staticmethod
    def polygon_vs_capsule(prima: ShapePrimitive,
                           primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Polygon
        assert primb._shape.type() == Shape.Type.Capsule
        return SATResult()

    @staticmethod
    def polygon_vs_sector(prima: ShapePrimitive,
                          primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Polygon
        assert primb._shape.type() == Shape.Type.Sector
        return SATResult()

    @staticmethod
    def capsule_vs_edge(prima: ShapePrimitive,
                        primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Capsule
        assert primb._shape.type() == Shape.Type.Edge
        return SATResult()

    @staticmethod
    def capsule_vs_capsule(prima: ShapePrimitive,
                           primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Capsule
        assert primb._shape.type() == Shape.Type.Capsule
        return SATResult()

    @staticmethod
    def capsule_vs_sector(prima: ShapePrimitive,
                          primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Capsule
        assert primb._shape.type() == Shape.Type.Sector
        return SATResult()

    @staticmethod
    def sector_vs_sector(prima: ShapePrimitive,
                         primb: ShapePrimitive) -> SATResult:
        assert prima._shape.type() == Shape.Type.Sector
        assert primb._shape.type() == Shape.Type.Sector
        return SATResult()

    @staticmethod
    def _axis_projection(prim: ShapePrimitive, shape: Shape, normal: Matrix) -> ProjectedSegment:
        if shape.type() == Shape.Type.Polygon:
            point_min: ProjectedPoint = ProjectedPoint()
            point_max: ProjectedPoint = ProjectedPoint()

            point_min._val = Config.Max
            point_max._val = Config.NegativeMin

            shape_len: int = len(shape.vertices)
            for i in range(shape_len):
                vertex: Matrix = prim.translate(shape.vertices[i])
                value: float = vertex.dot(normal)

                if value < point_min._val:
                    point_min._vertex = vertex
                    point_min._val = value
                    point_min._idx = i
                
                if value > point_max._val:
                    point_max._vertex = vertex
                    point_max._val = value
                    point_max._idx = i


            segment: ProjectedSegment = ProjectedSegment()
            segment._max = point_max
            segment._min = point_min

            return segment

        elif shape.type() == Shape.Type.Circle:
            cir_min: ProjectedPoint = ProjectedPoint()
            cir_max: ProjectedPoint = ProjectedPoint()

            cir_min._vertex = prim._xform - normal * shape.radius
            cir_min._val = prim._xform.dot(normal) - shape.radius

            cir_max._vertex = prim._xform + normal * shape.radius
            cir_max._val = prim._xform.dot(normal) + shape.radius
            
            segment: ProjectedSegment = ProjectedSegment()
            segment._min = cir_min
            segment._max = cir_max

            return segment

        elif shape.type() == Shape.Type.Ellipse:
            elli_min: ProjectedPoint = ProjectedPoint()
            elli_max: ProjectedPoint = ProjectedPoint()

            rot_dir: Matrix = Matrix.rotate_mat(-prim._rot) * -normal
            elli_min._vertex = GeomAlgo2D.calc_ellipse_project_on_point(shape.A(), shape.B(), rot_dir)
            elli_min._vertex = prim.translate( elli_min._vertex)
            elli_min._val = elli_min._vertex.dot(normal)

            rot_dir= Matrix.rotate_mat(-prim._rot) * normal
            elli_max._vertex = GeomAlgo2D.calc_ellipse_project_on_point(shape.A(), shape.B(), rot_dir)
            elli_max._vertex = prim.translate( elli_max._vertex)
            elli_max._val = elli_max._vertex.dot(normal)

            segment: ProjectedSegment = ProjectedSegment()
            segment._min = elli_min
            segment._max = elli_max

            return segment

        elif shape.type() == Shape.Type.Capsule:
            capsule_min: ProjectedPoint = ProjectedPoint()
            capsule_max: ProjectedPoint = ProjectedPoint()

            dir: Matrix = Matrix.rotate_mat(-prim._rot) * normal
            p1: Matrix = GeomAlgo2D.calc_capsule_project_on_point(shape.width, shape.height, dir)
            p2: Matrix = GeomAlgo2D.calc_capsule_project_on_point(shape.width, shape.height, -dir)
            p1 = prim.translate(p1)
            p2 = prim.translate(p2)

            capsule_min._vertex = p2
            capsule_min._val = capsule_min._vertex.dot(normal)

            capsule_max._vertex = p1
            capsule_max._val = capsule_max._vertex.dot(normal)

            segment: ProjectedSegment = ProjectedSegment()
            segment._min = capsule_min
            segment._max = capsule_max

            return segment

        elif shape.type() == Shape.Type.Sector:
            sector_min: ProjectedPoint = ProjectedPoint()
            sector_max: ProjectedPoint = ProjectedPoint()

            dir: Matrix = Matrix.rotate_mat(-prim._rot) * normal
            p1: Matrix = GeomAlgo2D.calc_sector_project_on_point(shape.start, shape.span, shape.radius, dir)
            p2: Matrix = GeomAlgo2D.calc_sector_project_on_point(shape.start, shape.span, shape.radius, -dir)
            p1 = prim.translate(p1)
            p2 = prim.translate(p2)

            sector_min._vertex = p2
            sector_min._val = sector_min._vertex.dot(normal)

            sector_max._vertex = p1
            sector_max._val = sector_max._vertex.dot(normal)

            segment: ProjectedSegment = ProjectedSegment()
            segment._min = sector_min
            segment._max = sector_max

            return segment
