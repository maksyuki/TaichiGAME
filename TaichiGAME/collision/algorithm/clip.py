from typing import List, Dict, Optional, Tuple

import numpy as np

from ...math.matrix import Matrix
from ...geometry.shape import Capsule, Edge, Polygon, Sector, Shape, ShapePrimitive
from ...geometry.geom_algo import GeomAlgo2D
from .gjk import GJK, PointPair


class ContactGenerator():
    class ClipEdge():
        def __init__(self):
            self._p1: Matrix = Matrix([0.0, 0.0], 'vec')
            self._p2: Matrix = Matrix([0.0, 0.0], 'vec')
            self._normal: Matrix = Matrix([0.0, 0.0], 'vec')

        def is_empty(self):
            return self._p1.is_origin() and self._p2.is_origin()

    @staticmethod
    def dump_vertices(prim: ShapePrimitive) -> List[Matrix]:
        vertices: List[Matrix] = []

        if prim._shap.type() == Shape.Type.Capsule:
            cap: Capsule = prim._shape
            vertices = cap.box_vertices()

        elif prim._shap.type() == Shape.Type.Polygon:
            poly: Polygon = prim._shape
            vertices = poly.vertices

        elif prim._shap.type() == Shape.Type.Edge:
            edg: Edge = prim._shape
            vertices.append(edg.start)
            vertices.append(edg.end)

        elif prim._shap.type() == Shape.Type.Sector:
            sec: Sector = prim._shape
            vertices = sec.vertices()

        vertices = [prim.translate(v) for v in vertices]
        return vertices

    @staticmethod
    def find_clip_edge(vertices: List[Matrix], idx: int,
                       normal: Matrix) -> ClipEdge:
        edg1 = ContactGenerator.ClipEdge()
        edg2 = ContactGenerator.ClipEdge()
        edg1._p2 = vertices[idx]
        edg2._p1 = vertices[idx]

        if idx == 0:
            edg1._p1 = vertices[len(vertices) - 2]
            edg2._p2 = vertices[idx + 1]

        elif idx == len(vertices) - 1:
            edg1._p1 = vertices[idx - 1]
            edg2._p2 = vertices[1]

        else:
            edg1._p1 = vertices[idx - 1]
            edg2._p2 = vertices[idx + 1]

        # compare which is closest to normal
        final_edg: ContactGenerator.ClipEdge = ContactGenerator.ClipEdge()
        if np.fabs((edg1._p2 - edg1._p1).dot(normal)) >= np.fabs(
            (edg2._p2 - edg2._p1).dot(normal)):
            final_edg = edg2
            p: Matrix = (edg2._p2 - edg2._p1).normal().perpendicular()
            if GeomAlgo2D.is_point_on_same_side(edg2._p1, edg2._p2, edg1._p1,
                                                edg2._p1 + p):
                final_edg._normal = p
            else:
                final_edg._normal = -p
        else:
            final_edg = edg1
            p: Matrix = (edg1._p2 - edg1._p1).normal().perpendicular()
            if GeomAlgo2D.is_point_on_same_side(edg1._p1, edg1._p2, edg2._p2,
                                                edg1._p1 + p):
                final_edg._normal = p
            else:
                final_edg._normal = -p

        return final_edg

    @staticmethod
    def dump_clip_edge(prim: ShapePrimitive, vertices: List[Matrix],
                       normal: Matrix) -> ClipEdge:
        edg: ContactGenerator.ClipEdge = ContactGenerator.ClipEdge()

        if len(vertices) == 2:
            edg._p1 = vertices[0]
            edg._p2 = vertices[1]

            if prim._shape.type() == Shape.Type.Edge:
                edg._normal = prim.normal()

        else:
            support, idx = GJK.find_farthest_point(vertices, normal)
            edg = ContactGenerator.find_clip_edge(vertices, idx, normal)

        return edg

    @staticmethod
    def recognize(prima: ShapePrimitive, primb: ShapePrimitive,
                  normal: Matrix) -> Tuple[ClipEdge, ClipEdge]:
        typea = prima._shape.type()
        typeb = primb._shape.type()

        if typea == Shape.Type.Point or typea == Shape.Type.Circle or typea == Shape.Type.Ellipse or typeb == Shape.Type.Point or typeb == Shape.Type.Circle or typeb == Shape.Type.Ellipse:
            return (ContactGenerator.ClipEdge(), ContactGenerator.ClipEdge())

        verta: List[Matrix] = ContactGenerator.dump_vertices(prima)
        vertb: List[Matrix] = ContactGenerator.dump_vertices(primb)
        edga = ContactGenerator.dump_clip_edge(prima, verta, -normal)
        edgb = ContactGenerator.dump_clip_edge(primb, vertb, normal)

        return (edga, edgb)

    @staticmethod
    def clip(clip_edga: ClipEdge, clip_edgb: ClipEdge,
             normal: Matrix) -> List[PointPair]:
        res: List[PointPair] = []

        if clip_edga.is_empty() or clip_edgb.is_empty():
            return res

        d1: float = Matrix(clip_edga._p1 - clip_edga._p2).dot(normal)
        d2: float = Matrix(clip_edgb._p1 - clip_edgb._p2).dot(normal)
        ref_edg: ContactGenerator.ClipEdge = clip_edga
        incident_edge: ContactGenerator.ClipEdge = clip_edgb
        swap: bool = False

        if np.fabs(d1) > np.fabs(d2):
            # edge B is reference edge
            ref_edg = clip_edgb
            incident_edge = clip_edga
            swap = True

        # 1. clip left region
        u: Matrix = (ref_edg._p2 - ref_edg._p1).normal()
        ref_anchor1: Matrix = u.perpendicular() + ref_edg._p1

        if not GeomAlgo2D.is_point_on_same_side(
                ref_edg._p1, ref_anchor1, ref_edg._p2, incident_edge._p1):
            incident_edge._p1 = GeomAlgo2D.line_intersection(
                ref_edg._p1, ref_anchor1, incident_edge._p1, incident_edge._p2)

        if not GeomAlgo2D.is_point_on_same_side(
                ref_edg._p1, ref_anchor1, ref_edg._p2, incident_edge._p2):
            incident_edge._p2 = GeomAlgo2D.line_intersection(
                ref_edg._p1, ref_anchor1, incident_edge._p1, incident_edge._p2)

        # 2. clip right region
        u.negate()
        ref_anchor2: Matrix = u.perpendicular() + ref_edg._p2
        if not GeomAlgo2D.is_point_on_same_side(
                ref_edg._p2, ref_anchor2, ref_edg._p1, incident_edge._p1):
            incident_edge._p1 = GeomAlgo2D.line_intersection(
                ref_edg._p2, ref_anchor2, incident_edge._p1, incident_edge._p2)

        if not GeomAlgo2D.is_point_on_same_side(
                ref_edg._p2, ref_anchor2, ref_edg._p1, incident_edge._p2):
            incident_edge._p2 = GeomAlgo2D.line_intersection(
                ref_edg._p2, ref_anchor2, incident_edge._p1, incident_edge._p2)

        # 3. clip normal region
        ref_anchor3: Matrix = (ref_edg._p2 +
                               ref_edg._p1) / 2.0 + ref_edg._normal

        p1_on_clip_area: bool = GeomAlgo2D.is_point_on_same_side(
            ref_edg._p1, ref_edg._p2, ref_anchor3, incident_edge._p1)
        p2_on_clip_area: bool = GeomAlgo2D.is_point_on_same_side(
            ref_edg._p1, ref_edg._p2, ref_anchor3, incident_edge._p2)

        if not (p1_on_clip_area and p2_on_clip_area):
            return res

        if p1_on_clip_area and not p2_on_clip_area:
            incident_edge._p2 = GeomAlgo2D.line_intersection(
                ref_edg._p1, ref_edg._p2, incident_edge._p1, incident_edge._p2)

        if not p1_on_clip_area and p2_on_clip_area:
            incident_edge._p1 = GeomAlgo2D.line_intersection(
                ref_edg._p1, ref_edg._p2, incident_edge._p1, incident_edge._p2)

        # p1 and p2 are inside, clip nothing, just go to project
        # 4. project to reference edge
        pp1: Matrix = GeomAlgo2D.point_to_line_segment(ref_edg._p1,
                                                       ref_edg._p2,
                                                       incident_edge._p1)
        pp2: Matrix = GeomAlgo2D.point_to_line_segment(ref_edg._p1,
                                                       ref_edg._p2,
                                                       incident_edge._p2)

        pair1: PointPair = PointPair()
        pair2: PointPair = PointPair()

        if not swap:
            pair1._pa = pp1
            pair1._pb = incident_edge._p1
            pair2._pa = pp2
            pair2._pb = incident_edge._p2
        else:
            pair1._pa = incident_edge._p1
            pair1._pb = pp1
            pair2._pa = incident_edge._p2
            pair2._pb = pp2

        res.append(pair1)
        res.append(pair2)
        return res
