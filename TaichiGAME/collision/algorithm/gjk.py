from __future__ import annotations
from typing import List, Optional, Tuple, cast

import numpy as np

from ...math.matrix import Matrix
from ...common.config import Config
from ...geometry.geom_algo import GeomAlgo2D
from ...geometry.shape import Capsule, Circle, Edge, Ellipse, Point
from ...geometry.shape import Polygon, Sector, Shape, ShapePrimitive


class Minkowski():
    def __init__(self,
                 pa: Matrix = Matrix([0.0, 0.0], 'vec'),
                 pb: Matrix = Matrix([0.0, 0.0], 'vec')):
        self._pa: Matrix = pa
        self._pb: Matrix = pb
        self._res: Matrix = self._pa - self._pb

    def __eq__(self, other) -> bool:
        return self._pa == other._pa and self._pb == other._pb

    def __ne__(self, other) -> bool:
        return not (self._pa == other._pa and self._pb == other._pb)


class Simplex():
    '''simplex structure for gjk/epa test.

    By convention:
    1 points:   p0, construct a single point
    2 points:   p0->pa, construct a segment
    >=4 points: p0->pa->pb->p0, construct a polygon
    '''
    def __init__(self):
        self._is_contain_origin: bool = False
        self._vertices: List[Minkowski] = []

    def contain_origin(self, strict: bool = False) -> bool:
        self._is_contain_origin = Simplex._contain_origin(self, strict)
        return self._is_contain_origin

    def insert(self, pos: int, vertex: Minkowski) -> None:
        self._vertices.insert(pos + 1, vertex)

    def contains(self, minkowski: Minkowski) -> bool:
        for v in self._vertices:
            if v == minkowski:
                return True

        return False

    def last_vertex(self) -> Matrix:
        vert_len: int = len(self._vertices)
        if vert_len == 2:
            return self._vertices[vert_len - 1]._res

        return self._vertices[vert_len - 2]._res

    @staticmethod
    def _contain_origin(simplex, strict: bool = False) -> bool:
        vert_len: int = len(simplex._vertices)
        if vert_len == 4:
            return GeomAlgo2D.is_triangle_contain_origin(
                simplex._vertices[0]._res, simplex._vertices[1]._res,
                simplex._vertices[2]._res)

        elif vert_len == 2:
            oa: Matrix = -simplex._vertices[0]._res
            ob: Matrix = -simplex._vertices[1]._res
            return GeomAlgo2D.is_point_on_segment(oa, ob,
                                                  Matrix([0.0, 0.0], 'vec'))

        else:
            return False


class PenetrationInfo():
    def __init__(self):
        self._normal: Matrix = Matrix([0.0, 0.0], 'vec')
        self._penetration: float = 0.0


class PenetrationSource():
    def __init__(self):
        self._a1: Matrix = Matrix([0.0, 0.0], 'vec')
        self._a2: Matrix = Matrix([0.0, 0.0], 'vec')
        self._b1: Matrix = Matrix([0.0, 0.0], 'vec')
        self._b2: Matrix = Matrix([0.0, 0.0], 'vec')


class PointPair():
    def __init__(self):
        self._pa: Matrix = Matrix([0.0, 0.0], 'vec')
        self._pb: Matrix = Matrix([0.0, 0.0], 'vec')

    def __eq__(self, other) -> bool:
        return self._pa == other._pa and self._pb == other._pb

    def __ne__(self, other) -> bool:
        return not (self._pa == other._pa and self._pb == other._pb)

    def is_empty(self) -> bool:
        return self._pa == Matrix([0.0, 0.0], 'vec') and self._pb == Matrix(
            [0.0, 0.0], 'vec')


class GJK():
    @staticmethod
    def gjk(prima: ShapePrimitive,
            primb: ShapePrimitive,
            iter_val: int = 20) -> Tuple[bool, Simplex]:
        '''Gilbert-Johnson-Keerthi distance algorithm

        Parameters
        ----------
        prima : ShapePrimitive
            primitive a
        primb : ShapePrimitive
            primitive b
        iter_val : int, optional
            iter num, by default 20

        Returns
        -------
        Tuple[bool, Simplex]
            return initial simplex and whether collision exist
        '''
        simplex: Simplex = Simplex()
        is_found: bool = False
        dirn: Matrix = primb._xform - prima._xform

        if dirn == Matrix([0.0, 0.0], 'vec'):
            dirn.set_value([1.0, 1.0])

        diff: Minkowski = GJK.support(prima, primb, dirn)
        simplex._vertices.append(diff)
        dirn.negate()

        removed: List[Minkowski] = []
        for i in range(iter_val):
            diff = GJK.support(prima, primb, dirn)
            simplex._vertices.append(diff)
            # print(f'i: {i}')

            # build a close polygon
            if len(simplex._vertices) == 3:
                simplex._vertices.append(simplex._vertices[0])
                # for v in simplex._vertices:
                # print(f'vertice res: {v._res}')

            if simplex.last_vertex().dot(dirn) <= 0:
                break

            if simplex.contain_origin(True):
                is_found = True
                break

            # if not contain origin
            # find edg closest to origin
            # reconstruct simplex
            # find the point that is not belong to the edg closest to origin
            # if found, there is no more minkowski difference, exit loop
            # if not, add the point to the list
            (idx1, idx2) = GJK.find_edge_closest_to_origin(simplex)
            dirn = GJK.calc_direction_by_edge(simplex._vertices[idx1]._res,
                                              simplex._vertices[idx2]._res,
                                              True)

            # print(f'idx1: {idx1} idx2: {idx2}')
            # print(f'dirn: {dirn}')
            res: Optional[Minkowski] = GJK.adjust_simplex(simplex, idx1, idx2)

            if res is not None:
                for v in removed:
                    if v == res:
                        break
                removed.append(res)

        return (is_found, simplex)

    @staticmethod
    def epa(prima: ShapePrimitive,
            primb: ShapePrimitive,
            src: Simplex,
            iter_val: int = 20) -> Simplex:
        '''Expanding Polygon Algorithm

        Parameters
        ----------
        prima : ShapePrimitive
            primitive a
        primb : ShapePrimitive
            primitive b
        src : Simplex
            init simplex
        iter_val : int, optional
            iter num, by default 20

        Returns
        -------
        Simplex
            return expanded simplex
        '''

        # edg: Simplex = Simplex()
        simplex: Simplex = src
        normal: Matrix = Matrix([0.0, 0.0], 'vec')
        p: Minkowski = Minkowski()

        for i in range(iter_val):
            (idx1, idx2) = GJK.find_edge_closest_to_origin(simplex)
            normal = GJK.calc_direction_by_edge(simplex._vertices[idx1]._res,
                                                simplex._vertices[idx2]._res,
                                                False).normal()

            if GeomAlgo2D.is_point_on_segment(simplex._vertices[idx1]._res,
                                              simplex._vertices[idx2]._res,
                                              Matrix([0.0, 0.0], 'vec')):
                normal.negate()

            p = GJK.support(prima, primb, normal)

            if simplex.contains(p):
                break

            simplex.insert(idx1, p)

        return simplex

    @staticmethod
    def dump_info(src: PenetrationSource) -> PenetrationInfo:
        '''Dump collision penetration normal and depth

        Parameters
        ----------
        src : PenetrationSource
            source data

        Returns
        -------
        PenetrationInfo
            collision info
        '''

        res: PenetrationInfo = PenetrationInfo()
        edg1: Matrix = src._a1 - src._b1
        edg2: Matrix = src._a2 - src._b2
        normal: Matrix = GJK.calc_direction_by_edge(edg1, edg2, False).normal()
        origin_to_edge: float = np.fabs(normal.dot(edg1))
        res._normal = normal.negate()
        res._penetration = origin_to_edge

        return res

    @staticmethod
    def support(prima: ShapePrimitive, primb: ShapePrimitive,
                dirn: Matrix) -> Minkowski:
        return Minkowski(GJK.find_farthest_point(prima, dirn),
                         GJK.find_farthest_point(primb, -dirn))

    @staticmethod
    def find_edge_closest_to_origin(simplex: Simplex) -> Tuple[int, int]:
        '''Find two points that can form an edge closest to origin of simplex

        Parameters
        ----------
        simplex : Simplex
            simplex

        Returns
        -------
        Tuple[int, int]
            the two idx of the point on the simplex match needed
        '''
        idx1: int = 0
        idx2: int = 0
        dist_min: float = Config.Max

        if len(simplex._vertices) == 2:
            return (0, 1)

        vert_len: int = len(simplex._vertices)
        for i in range(vert_len - 1):
            a: Matrix = simplex._vertices[i]._res
            b: Matrix = simplex._vertices[i + 1]._res
            p: Matrix = GeomAlgo2D.point_to_line_segment(
                a, b, Matrix([0.0, 0.0], 'vec'))

            proj: float = p.len()

            if dist_min > proj:
                idx1 = i
                idx2 = i + 1
                dist_min = proj

            elif np.isclose(dist_min, proj):
                length1: float = a.len_square() + b.len_square()
                length2: float = simplex._vertices[idx1]._res.len_square(
                ) + simplex._vertices[idx2]._res.len_square()

                if length1 < length2:
                    idx1 = i
                    idx2 = i + 1

        return (idx1, idx2)

    @staticmethod
    def find_farthest_point(prim: ShapePrimitive, dirn: Matrix) -> Matrix:
        '''Find farthest projection point in given direction

        Parameters
        ----------
        prim : ShapePrimitive
            primitive
        dirn : Matrix
            given direction

        Returns
        -------
        Matrix
            farthest point's val
        '''
        target: Matrix = Matrix([0.0, 0.0], 'vec')
        rot: Matrix = Matrix.rotate_mat(-prim._rot)
        rot_dir: Matrix = rot * dirn

        assert prim._shape is not None
        if prim._shape.type == Shape.Type.Polygon:
            poly: Polygon = cast(Polygon, prim._shape)
            (vertex, idx) = GJK.find_farthest_point2(poly.vertices, rot_dir)
            target = vertex

        elif prim._shape.type == Shape.Type.Circle:
            cir: Circle = cast(Circle, prim._shape)
            return dirn.normal() * cir.radius + prim._xform

        elif prim._shape.type == Shape.Type.Ellipse:
            elli: Ellipse = cast(Ellipse, prim._shape)
            target = GeomAlgo2D.calc_ellipse_project_on_point(
                elli.A(), elli.B(), rot_dir)

        elif prim._shape.type == Shape.Type.Edge:
            edg: Edge = cast(Edge, prim._shape)
            dot1: float = Matrix.dot_product(edg.start, dirn)
            dot2: float = Matrix.dot_product(edg.end, dirn)
            target = edg.start if dot1 > dot2 else edg.end

        elif prim._shape.type == Shape.Type.Point:
            point: Point = cast(Point, prim._shape)
            return point.pos

        elif prim._shape.type == Shape.Type.Capsule:
            cap: Capsule = cast(Capsule, prim._shape)
            target = GeomAlgo2D.calc_capsule_project_on_point(
                cap.width, cap.height, rot_dir)

        elif prim._shape.type == Shape.Type.Sector:
            sec: Sector = cast(Sector, prim._shape)
            target = GeomAlgo2D.calc_sector_project_on_point(
                sec.start, sec.span, sec.radius, rot_dir)

        # calc gemo algo in origin-base axis system
        # return the 'target' back in former coord
        rot.set_value(Matrix.rotate_mat(prim._rot))
        target = rot * target + prim._xform
        # print(f'target: {target}')
        return target

    @staticmethod
    def find_farthest_point2(vertices: List[Matrix],
                             dirn: Matrix) -> Tuple[Matrix, int]:
        '''find the farthest point of polygon
        in a given direction

        Parameters
        ----------
        vertices : List[Matrix]
            polygon's vertices
        dirn : Matrix
            given direction

        Returns
        -------
        Tuple[Matrix, int]
            pos and its index in polygon's vertices list
        '''
        val_max: float = Config.NegativeMin
        tgt_max: Matrix = Matrix([0.0, 0.0], 'vec')
        tgt_idx: int = 0
        vert_len: int = len(vertices)
        for i in range(vert_len):
            tmp: float = Matrix.dot_product(vertices[i], dirn)
            if val_max < tmp:
                val_max = tmp
                tgt_max = vertices[i]
                tgt_idx = i

        return (tgt_max, tgt_idx)

    @staticmethod
    def adjust_simplex(simplex: Simplex, closest1: int,
                       closest2: int) -> Optional[Minkowski]:
        '''Adjust triangle simplex, remove the point that can not form a
        triangle that contains origin

        Parameters
        ----------
        simplex : Simplex
            simplex
        closest1 : int
            closest idx1 on simplex
        closest2 : int
            closest idx2 on simplex

        Returns
        -------
        Optional[Minkowski]
            target minkowski
        '''

        vert_len: int = len(simplex._vertices)
        if vert_len == 4:
            idx: int = -1
            for i in range(vert_len - 1):
                if i != closest1 and i != closest2:
                    idx = i

            target: Minkowski = simplex._vertices[idx]
            del simplex._vertices[idx]

            # NOTE: need to calc again, because del oper
            vert_len = len(simplex._vertices)
            del simplex._vertices[vert_len - 1]

            return target

        return None

    @staticmethod
    def calc_direction_by_edge(pa: Matrix,
                               pb: Matrix,
                               point_to_origin: bool = True) -> Matrix:
        '''Given two points, calculate the perpendicular vector and
        the orientation is user-defined.

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        point_to_origin : bool, optional
            if point the origin, by default True

        Returns
        -------
        Matrix
            perpendicular vector
        '''

        ao: Matrix = -pa
        ab: Matrix = pb - pa
        perp_of_ab: Matrix = ab.perpendicular()

        if (Matrix.dot_product(ao, perp_of_ab) < 0
                and point_to_origin) or (Matrix.dot_product(ao, perp_of_ab) > 0
                                         and not point_to_origin):
            perp_of_ab.negate()

        return perp_of_ab

    @staticmethod
    def distance(prima: ShapePrimitive,
                 primb: ShapePrimitive,
                 iter_val: int = 20) -> PointPair:
        '''Calculate the distance of two shape primitive

        Parameters
        ----------
        prima : ShapePrimitive
            primitive a
        primb : ShapePrimitive
            primitive b
        iter_val : int, optional
            iter num, by default 20

        Returns
        -------
        PointPair
            point result
        '''

        simplex: Simplex = Simplex()
        dirn: Matrix = primb._xform - prima._xform

        # calc two minkowski
        m: Minkowski = GJK.support(prima, primb, dirn)
        simplex._vertices.append(m)
        dirn.negate()
        m = GJK.support(prima, primb, dirn)
        simplex._vertices.append(m)

        for i in range(iter_val):
            dirn = GJK.calc_direction_by_edge(simplex._vertices[0]._res,
                                              simplex._vertices[1]._res, True)
            m = GJK.support(prima, primb, dirn)

            if simplex.contains(m):
                break

            simplex._vertices.append(m)
            simplex._vertices.append(simplex._vertices[0])
            (idx1, idx2) = GJK.find_edge_closest_to_origin(simplex)
            GJK.adjust_simplex(simplex, idx1, idx2)

        return GJK.dump_points(GJK.dump_source(simplex))

    @staticmethod
    def dump_source(simplex: Simplex) -> PenetrationSource:
        res: PenetrationSource = PenetrationSource()

        (idx1, idx2) = GJK.find_edge_closest_to_origin(simplex)
        res._a1 = simplex._vertices[idx1]._pa
        res._a2 = simplex._vertices[idx2]._pa
        res._b1 = simplex._vertices[idx1]._pb
        res._b2 = simplex._vertices[idx2]._pb

        return res

    @staticmethod
    def dump_points(src: PenetrationSource) -> PointPair:
        res: PointPair = PointPair()

        a_s1: Matrix = src._a1
        b_s1: Matrix = src._a2
        a_s2: Matrix = src._b1
        b_s2: Matrix = src._b2

        a: Matrix = src._a1 - src._b1
        b: Matrix = src._a2 - src._b2
        lval: Matrix = b - a
        ll: float = lval.dot(lval)
        la: float = lval.dot(a)
        lambda2: float = -la / ll
        lambda1: float = 1 - lambda2

        res._pa.set_value(a_s1 * lambda1 + b_s1 * lambda2)
        res._pb.set_value(a_s2 * lambda1 + b_s2 * lambda2)

        if lval == Matrix([0.0, 0.0], 'vec') or lambda2 < 0:
            res._pa.set_value([a_s1.x, a_s1.y])
            res._pb.set_value([a_s2.x, a_s2.y])

        if lambda1 < 0:
            res._pa.set_value([b_s1.x, b_s1.y])
            res._pb.set_value([b_s2.x, b_s2.y])

        return res
