from typing import List, Dict, Optional, Tuple

import numpy as np

from .gjk import Simplex, Minkowski, GJK
from ...math.matrix import Matrix
from ...geometry.shape import ShapePrimitive
from ...geometry.geom_algo import GeomAlgo2D


class MPR():
    '''Minkowski Portal Refinement
    
    The implementation of MPR still remain some bugs when computing deeper object penetration.
    It may causes error penetration depth and normal.
    '''
    @staticmethod
    def discover(prima: ShapePrimitive,
                 primb: ShapePrimitive) -> Tuple[Matrix, Simplex]:
        '''Discover a portal for next collision test

        Parameters
        ----------
        prima : ShapePrimitive
            primitive a
        primb : ShapePrimitive
            primitive b

        Returns
        -------
        Tuple[Matrix, Simplex]
            return a vector from center of simplex to origin, an initial simplex
        '''

        simplex: Simplex = Simplex()
        ctra: Matrix = Matrix.rotate_mat(prima._rot) * prima._shape.center()
        ctrb: Matrix = Matrix.rotate_mat(primb._rot) * primb._shape.center()
        origin: Matrix = primb._xform - prima._xform
        v0: Minkowski = Minkowski(ctra + prima._xform, ctrb + primb._xform)
        dir: Matrix = ctrb - ctra + origin

        if dir == Matrix([0.0, 0.0], 'vec'):
            dir.set_value([1.0, 1.0])

        v1: Minkowski = GJK.support(prima, primb, dir)
        dir = GJK.calc_direction_by_edge(v0._res, v1._res, True)
        v2: Minkowski = GJK.support(prima, primb, dir)

        simplex._vertices.append(v0)
        simplex._vertices.append(v1)
        simplex._vertices.append(v2)

        return (ctrb - ctra + origin, simplex)

    @staticmethod
    def refine(prima: ShapePrimitive,
               primb: ShapePrimitive,
               src: Simplex,
               center_to_origin: Matrix,
               iter_val: int = 50) -> Tuple[boo, Simplex]:
        '''Refine portal close to origin

        Parameters
        ----------
        prima : ShapePrimitive
            primitive a
        primb : ShapePrimitive
            primitive b
        src : Simplex
            init simplex
        center_to_origin : Matrix
            none
        iter_val : int, optional
            iter num, by default 50

        Returns
        -------
        Tuple[boo, Simplex]
            return if there is a collision, the final simplex
        '''

        simplex: Simplex = src
        is_colliding: bool = False
        v1: Matrix = Matrix([0.0, 0.0], 'vec')
        v2: Matrix = Matrix([0.0, 0.0], 'vec')
        dir: Matrix = Matrix([0.0, 0.0], 'vec')

        for i in range(iter_val):
            v1 = simplex._vertices[1]._res
            v2 = simplex._vertices[2]._res
            dir = GJK.calc_direction_by_edge(v1, v2, True)

            if (dir.dot(center_to_origin) < 0):
                dir.negate()
                is_colliding = True

            new_vertex: Minkowski = GJK.support(prima, primb, dir)

            if v1 == new_vertex._res or v2 == new_vertex._res:
                break

            dist13: float = GeomAlgo2D.point_to_line_segment(
                v1, new_vertex._res, [0.0, 0.0]).len_square()
            dist23: float = GeomAlgo2D.point_to_line_segment(
                v2, new_vertex._res, [0.0, 0.0]).len_square()

            if dist13 < dist23:
                simplex._vertices[2] = new_vertex
            else:
                simplex._vertices[1] = new_vertex

        return (is_colliding, simplex)
