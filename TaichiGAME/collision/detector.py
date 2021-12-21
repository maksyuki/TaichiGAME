from typing import List, Optional

import numpy as np

from ..math.matrix import Matrix
from ..dynamics.body import Body
from .algorithm.clip import ContactGenerator
from ..geometry.shape import ShapePrimitive
from ..collision.algorithm.gjk import PenetrationInfo, PenetrationSource
from ..collision.algorithm.gjk import GJK, PointPair


class Collsion():
    def __init__(self):
        self._is_colliding: bool = False
        self._bodya: Optional[Body] = None
        self._bodyb: Optional[Body] = None
        self._contact_list: List[PointPair] = []
        self._normal: Matrix = Matrix([0.0, 0.0], 'vec')
        self._penetration: float = 0.0


class Detector():
    @staticmethod
    def collide(bodya: Body, bodyb: Body) -> bool:
        assert bodya is not None
        assert bodyb is not None

        prima: ShapePrimitive = ShapePrimitive()
        primb: ShapePrimitive = ShapePrimitive()

        prima._shape = bodya.shape
        prima._rot = bodya.rot
        prima._xform = bodya.pos

        primb._shape = bodyb.shape
        primb._rot = bodyb.rot
        primb._xform = bodyb.pos

        (is_colliding, simplex) = GJK.gjk(prima, primb)
        if prima._xform == primb._xform and not is_colliding:
            is_colliding = simplex.contain_origin(True)

        return is_colliding

    @staticmethod
    def detect(bodya: Body, bodyb: Body) -> Collsion:
        res: Collsion = Collsion()

        if bodya is None or bodyb is None:
            return res

        if bodya == bodyb:
            return res

        if bodya.id > bodyb.id:
            bodya, bodyb = bodyb, bodya

        res._bodya = bodya
        res._bodyb = bodyb

        prima: ShapePrimitive = ShapePrimitive()
        primb: ShapePrimitive = ShapePrimitive()

        prima._shape = bodya.shape
        prima._rot = bodya.rot
        prima._xform = bodya.pos

        primb._shape = bodyb.shape
        primb._rot = bodyb.rot
        primb._xform = bodyb.pos

        (is_colliding, simplex) = GJK.gjk(prima, primb)
        if prima._xform == primb._xform and not is_colliding:
            is_colliding = simplex.contain_origin(True)

        res._is_colliding = is_colliding

        if is_colliding:
            # old_simplex: Simplex = simplex
            simplex = GJK.epa(prima, primb, simplex)
            source: PenetrationSource = GJK.dump_source(simplex)
            info: PenetrationInfo = GJK.dump_info(source)

            res._normal = info._normal
            res._penetration = info._penetration

            (clip_edga,
             clip_edgb) = ContactGenerator.recognize(prima, primb,
                                                     info._normal)

            pair_list: List[PointPair] = ContactGenerator.clip(
                clip_edga, clip_edgb, info._normal)

            val_pass: bool = False
            for elem in pair_list:
                tmp_val: float = (elem._pa - elem._pb).len_square()
                if np.isclose(tmp_val, res._penetration * res._penetration):
                    val_pass = True

            # if fail, there must be a deeper contact point, use it:
            if val_pass:
                res._contact_list = pair_list
            else:
                res._contact_list.append(GJK.dump_points(source))

        assert len(res._contact_list) != 3
        return res

    @staticmethod
    def distance(bodya: Body, bodyb: Body) -> PointPair:
        res: PointPair = PointPair()

        if bodya is None or bodyb is None:
            return res

        if bodya == bodyb:
            return res

        prima: ShapePrimitive = ShapePrimitive()
        primb: ShapePrimitive = ShapePrimitive()

        prima._shape = bodya.shape
        prima._rot = bodya.rot
        prima._xform = bodya.pos

        primb._shape = bodyb.shape
        primb._rot = bodyb.rot
        primb._xform = bodyb.pos
        return GJK.distance(prima, primb)
