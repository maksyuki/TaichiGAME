from typing import List, Dict, cast

import numpy as np

from ...math.matrix import Matrix
from ...common.config import Config
from ...collision.algorithm.gjk import PointPair
from ...collision.detector import Collsion
from ..body import Body


# FIXME:
def generate_relation(bodya: Body, bodyb: Body) -> int:
    # Combine two 32-bit id into one 64-bit id in unique form
    ida: int = bodya.id
    idb: int = bodyb.id

    return ida + idb


class VelocityConstraintPoint():
    def __init__(self):
        self._ra: Matrix = Matrix([0.0, 0.0], 'vec')
        self._rb: Matrix = Matrix([0.0, 0.0], 'vec')
        self._va: Matrix = Matrix([0.0, 0.0], 'vec')
        self._vb: Matrix = Matrix([0.0, 0.0], 'vec')
        self._normal: Matrix = Matrix([0.0, 0.0], 'vec')
        self._tangent: Matrix = Matrix([0.0, 0.0], 'vec')
        self._vel_bias: Matrix = Matrix([0.0, 0.0], 'vec')
        self._bias: float = 0.0
        self._penetration: float = 0.0
        self._restit: float = 0.8
        self._eff_mass_normal: float = 0.0
        self._eff_mass_tangent: float = 0.0
        self._accum_normal_impulse: float = 0.0
        self._accum_tangent_impulse: float = 0.0


class ContactConstraintPoint():
    def __init__(self):
        self._relation: int = 0
        self._fric: float = 0.2
        self._active: bool = True
        self._locala: Matrix = Matrix([0.0, 0.0], 'vec')
        self._localb: Matrix = Matrix([0.0, 0.0], 'vec')
        self._bodya: Body = Body()
        self._bodyb: Body = Body()
        self._vcp: VelocityConstraintPoint = VelocityConstraintPoint()


class ContactMaintainer():
    def __init__(self):
        self._penetration_max: float = 0.01
        self._bias_factor: float = 0.03
        self._contact_table: Dict[int, List[ContactConstraintPoint]] = {}

    def clear_all(self) -> None:
        self._contact_table.clear()

    def solve_velocity(self, dt: float) -> None:
        for val in self._contact_table.values():
            if len(val) == 0 or not val[0]._active:
                continue

            for ccp in val:
                vcp: VelocityConstraintPoint = ccp._vcp
                wa: Matrix = Matrix.cross_product2(ccp._bodya.ang_vel, vcp._ra)
                wb: Matrix = Matrix.cross_product2(ccp._bodyb.ang_vel, vcp._rb)
                vcp._va = ccp._bodya.vel + wa
                vcp._vb = ccp._bodyb.vel + wb

                dv: Matrix = vcp._va - vcp._vb
                jv: float = -1.0 * vcp._normal.dot(dv - vcp._vel_bias)
                lambda_n: float = vcp._eff_mass_normal * jv
                old_impulse: float = vcp._accum_normal_impulse
                vcp._accum_normal_impulse = np.fmax(old_impulse + lambda_n, 0)

                lambda_n = vcp._accum_normal_impulse - old_impulse
                impulse_n: Matrix = vcp._normal * lambda_n

                ccp._bodya.apply_impulse(impulse_n, vcp._ra)
                ccp._bodyb.apply_impulse(-impulse_n, vcp._rb)

                vcp._va = ccp._bodya.vel + Matrix.cross_product2(
                    ccp._bodya.ang_vel, vcp._ra)
                vcp._vb = ccp._bodyb.vel + Matrix.cross_product2(
                    ccp._bodyb.ang_vel, vcp._rb)
                dv = vcp._va - vcp._vb

                jvt: float = vcp._tangent.dot(dv)
                lambda_t: float = vcp._eff_mass_tangent * -jvt

                maxT: float = ccp._fric * vcp._accum_normal_impulse
                old_impulse = vcp._accum_tangent_impulse

                vcp._accum_tangent_impulse = Config.clamp(
                    old_impulse + lambda_t, -maxT, maxT)
                lambda_t = vcp._accum_tangent_impulse - old_impulse
                impulse_t: Matrix = vcp._tangent * lambda_t

                ccp._bodya.apply_impulse(impulse_t, vcp._ra)
                ccp._bodyb.apply_impulse(-impulse_t, vcp._rb)

    def solve_position(self, dt: float) -> None:
        for val in self._contact_table.values():
            if len(val) == 0 or not val[0]._active:
                continue

            for ccp in val:
                vcp: VelocityConstraintPoint = ccp._vcp
                bodya: Body = ccp._bodya
                bodyb: Body = ccp._bodyb
                pa: Matrix = vcp._ra + bodya.pos
                pb: Matrix = vcp._rb + bodyb.pos
                c: Matrix = pa - pb

                # already solved by vel
                if c.dot(vcp._normal) < 0.0:
                    continue

                bias: float = self._bias_factor * np.fmax(
                    c.len() - self._penetration_max, 0.0)
                val_lambda: float = vcp._eff_mass_normal * bias
                impulse: Matrix = vcp._normal * val_lambda

                if bodya.type != Body.Type.Static and not ccp._bodya.sleep:
                    bodya.pos += impulse * bodya.inv_mass
                    bodya.rot += bodya.inv_inertia * vcp._ra.cross(impulse)

                if bodyb.type != Body.Type.Static and not ccp._bodyb.sleep:
                    bodyb.pos -= impulse * bodyb.inv_mass
                    bodyb.rot -= bodyb.inv_inertia * vcp._rb.cross(impulse)

    def add(self, collision: Collsion) -> None:
        assert collision._bodya is not None
        assert collision._bodyb is not None
        bodya: Body = collision._bodya
        bodyb: Body = collision._bodyb

        print(f'bodya id: {bodya.id}')
        print(f'bodyb id: {bodyb.id}')
        relation: int = generate_relation(bodya, bodyb)

        contact_list: List[ContactConstraintPoint] = []
        if self._contact_table.get(relation, False):
            contact_list = self._contact_table[relation]
        else:
            self._contact_table[relation] = []
            contact_list = self._contact_table[relation]

        for elem in collision._contact_list:
            existed: bool = False
            locala: Matrix = bodya.to_local_point(elem._pa)
            localb: Matrix = bodyb.to_local_point(elem._pb)

            for contact in contact_list:
                print('x')
                is_pointa: bool = np.isclose(contact._locala._val,
                                             locala._val).all()
                is_pointb: bool = np.isclose(contact._localb._val,
                                             localb._val).all()

                if is_pointa and is_pointb:
                    # satisfy the condition, transmit the old
                    # accumulated value to new value
                    contact._locala = locala
                    contact._localb = localb
                    self.prepare(contact, elem, collision)
                    existed = True
                    break

            if existed:
                continue

            # no eligible contact, push new contact points
            ccp: ContactConstraintPoint = ContactConstraintPoint()
            ccp._locala = locala
            ccp._localb = localb
            ccp._relation = relation
            self.prepare(ccp, elem, collision)
            contact_list.append(ccp)

    def prepare(self, ccp: ContactConstraintPoint, pair: PointPair,
                collision: Collsion) -> None:
        assert collision._bodya is not None
        assert collision._bodyb is not None

        ccp._bodya = collision._bodya
        ccp._bodyb = collision._bodyb
        ccp._active = True

        ccp._fric = np.sqrt(ccp._bodya.fric * ccp._bodyb.fric)

        vcp: VelocityConstraintPoint = ccp._vcp
        vcp._ra = pair._pa - collision._bodya.pos
        vcp._rb = pair._pb - collision._bodyb.pos

        vcp._normal = collision._normal
        vcp._tangent = vcp._normal.perpendicular()

        im_a: float = collision._bodya.inv_mass
        im_b: float = collision._bodyb.inv_mass
        ii_a: float = collision._bodya.inv_inertia
        ii_b: float = collision._bodyb.inv_inertia

        rn_a: float = vcp._ra.cross(vcp._normal)
        rn_b: float = vcp._rb.cross(vcp._normal)

        rt_a: float = vcp._ra.cross(vcp._tangent)
        rt_b: float = vcp._rb.cross(vcp._tangent)

        k_normal: float = im_a + ii_a * rn_a * rn_a
        k_normal += im_b + ii_b * rn_b * rn_b
        k_tangent: float = im_a + ii_a * rt_a * rt_a
        k_tangent += im_b + ii_b * rt_b * rt_b

        vcp._eff_mass_normal = 0.0 if np.isclose(k_normal,
                                                 0) else 1.0 / k_normal
        vcp._eff_mass_tangent = 0.0 if np.isclose(k_tangent,
                                                  0) else 1.0 / k_tangent

        vcp._restit = np.fmin(ccp._bodya.restit, ccp._bodyb.restit)
        vcp._penetration = collision._penetration

        wa: Matrix = Matrix.cross_product2(ccp._bodya.ang_vel, vcp._ra)
        wb: Matrix = Matrix.cross_product2(ccp._bodyb.ang_vel, vcp._rb)
        vcp._va = ccp._bodya.vel + wa
        vcp._vb = ccp._bodyb.vel + wb

        vcp._vel_bias = (vcp._va - vcp._vb) * -vcp._restit

        # accumulate inherited impulse
        impulse: Matrix = vcp._normal * vcp._accum_normal_impulse
        impulse += vcp._tangent * vcp._accum_tangent_impulse

        ccp._bodya.apply_impulse(impulse, vcp._ra)
        ccp._bodyb.apply_impulse(-impulse, vcp._rb)

    def clear_inactive_points(self) -> None:
        clear_list: List[int] = []
        removed_list: List[ContactConstraintPoint] = []

        for key, val in self._contact_table.items():
            if len(val) == 0:
                clear_list.append(key)
                continue

            for v1 in val:
                if not v1._active:
                    removed_list.append(v1)

            for v1 in removed_list:
                for re in val:
                    if re == v1:
                        val.remove(re)

            removed_list.clear()

        for v2 in clear_list:
            for item in self._contact_table.items():
                if item[0] == v2:
                    del self._contact_table[item[0]]
                    break

    def deactivate_all_points(self) -> None:
        for val in self._contact_table.values():
            if len(val) == 0 or not val[0]._active:
                continue

            for ccp in val:
                ccp._active = False
