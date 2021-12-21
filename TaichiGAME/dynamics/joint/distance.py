from typing import List, Optional

import numpy as np

from ...math.matrix import Matrix
from ..body import Body
from .joint import Joint, JointType


class DistanceJointPrimitive():
    def __init__(self):
        self._bodya: Optional[Body] = None
        self._local_pointa: Matrix = Matrix([0.0, 0.0], 'vec')
        self._target_point: Matrix = Matrix([0.0, 0.0], 'vec')
        self._normal: Matrix = Matrix([0.0, 0.0], 'vec')
        self._bias_factor: float = 0.3
        self._bias: float = 0.0
        self._dist_min: float = 0.0
        self._dist_max: float = 0.0
        self._eff_mass: float = 0.0
        self._accum_impulse: float = 0.0


class DistanceConstraintPrimitive():
    def __init__(self):
        self._bodya: Optional[Body] = None
        self._bodyb: Optional[Body] = None
        self._nearest_pa: Matrix = Matrix([0.0, 0.0], 'vec')
        self._nearest_pb: Matrix = Matrix([0.0, 0.0], 'vec')
        self._ra: Matrix = Matrix([0.0, 0.0], 'vec')
        self._rb: Matrix = Matrix([0.0, 0.0], 'vec')
        self._bias: Matrix = Matrix([0.0, 0.0], 'vec')
        self._eff_mass: Matrix = Matrix([0.0, 0.0, 0.0, 0.0])
        self._impulse: Matrix = Matrix([0.0, 0.0], 'vec')
        self._force_max: float = 200.0


class DistanceJoint(Joint):
    def __init__(self,
                 prim: DistanceJointPrimitive = DistanceJointPrimitive()):
        super().__init__()
        self._type: JointType = JointType.Distance
        self._prim: DistanceJointPrimitive = prim
        self._factor: float = 0.4

    def set_value(self, prim: DistanceJointPrimitive) -> None:
        self._prim = prim

    def prepare(self, dt: float) -> None:
        assert self._prim._dist_min <= self._prim._dist_max
        assert self._prim._bodya is not None

        bodya: Body = self._prim._bodya
        pa: Matrix = bodya.to_world_point(self._prim._local_pointa)
        ra: Matrix = pa - bodya.pos
        pb: Matrix = self._prim._target_point
        im_a: float = self._prim._bodya.inv_mass
        ii_a: float = self._prim._bodya.inv_inertia
        error: Matrix = pb - pa
        val_len: float = error.len()
        c: float = 0.0

        self._prim._normal = error.normal()
        if val_len < self._prim._dist_min:
            c = self._prim._dist_min - val_len
            self._prim._normal.negate()

        elif val_len > self._prim._dist_max:
            c = val_len - self._prim._dist_max

        else:
            self._prim._accum_impulse = 0.0
            self._prim._normal.clear()
            self._prim._bias = 0.0
            return

        if self._prim._bodya.vel.dot(self._prim._normal) > 0:
            self._prim._accum_impulse = 0.0
            self._prim._normal.clear()
            self._prim._bias = 0.0
            return

        rn_a: float = self._prim._normal.dot(ra)
        self._prim._eff_mass = 1.0 / (im_a + ii_a * rn_a * rn_a)
        self._prim._bias = self._prim._bias_factor * c / dt

    def solve_velocity(self, dt: float) -> None:
        if np.isclose(self._prim._bias, 0):
            return

        assert self._prim._bodya is not None

        ra: Matrix = self._prim._bodya.to_world_point(
            self._prim._local_pointa) - self._prim._bodya.pos
        va: Matrix = self._prim._bodya.vel + Matrix.cross_product2(
            self._prim._bodya.ang_vel, ra)
        dv: Matrix = va
        jv: float = self._prim._normal.dot(dv)
        jvb: float = -jv + self._prim._bias
        lambda_n: float = self._prim._eff_mass * jvb

        old_impulse: float = self._prim._accum_impulse
        self._prim._accum_impulse = np.fmax(old_impulse + lambda_n, 0)
        lambda_n = self._prim._accum_impulse - old_impulse

        impulse: Matrix = self._prim._normal * lambda_n
        self._prim._bodya.apply_impulse(impulse, ra)

    def solve_position(self, dt: float) -> None:
        pass

    @property
    def prim(self) -> DistanceJointPrimitive:
        return self._prim


class DistanceConstraint(Joint):
    def __init__(
        self,
        prim: DistanceConstraintPrimitive = DistanceConstraintPrimitive()):
        super().__init__()
        self._prim: DistanceConstraintPrimitive = prim
        self._factor: float = 0.1

    def prepare(self, dt: float) -> None:
        if self._prim._bodya is None or self._prim._bodyb is None:
            return

        bodya: Body = self._prim._bodya
        bodyb: Body = self._prim._bodyb

        im_a: float = bodya.inv_mass
        ii_a: float = bodya.inv_inertia
        im_b: float = bodyb.inv_mass
        ii_b: float = bodyb.inv_inertia

        self._prim._ra = self._prim._nearest_pa - bodya.pos
        self._prim._rb = self._prim._nearest_pb - bodyb.pos
        ra: Matrix = self._prim._ra
        rb: Matrix = self._prim._rb
        error: Matrix = self._prim._nearest_pa - self._prim._nearest_pb

        k: Matrix = Matrix([0.0, 0.0, 0.0, 0.0])
        data_arr: List[float] = []
        data_arr.append(im_a + ra.y * ra.y * ii_a + im_b + rb.y * rb.y * ii_b)
        data_arr.append(-ra.x * ra.y * ii_a - rb.x * rb.y * ii_b)
        data_arr.append(data_arr[1])
        data_arr.append(im_a + ra.x * ra.x * ii_a + im_b + rb.x * rb.x * ii_b)
        k.set_value(data_arr)

        self._prim._bias = error * self._factor
        self._prim._eff_mass = k.invert()

    def solve_velocity(self, dt: float) -> None:
        if self._prim._bodya is None or self._prim._bodyb is None:
            return

        va: Matrix = self._prim._bodya.vel + Matrix.cross_product2(
            self._prim._bodya.ang_vel, self._prim._ra)
        vb: Matrix = self._prim._bodyb.vel + Matrix.cross_product2(
            self._prim._bodyb.ang_vel, self._prim._rb)

        jvb: Matrix = va - vb
        jvb += self._prim._bias
        jvb.negate()

        J: Matrix = self._prim._eff_mass * jvb
        old_impulse: Matrix = self._prim._impulse
        self._prim._impulse += J

        max_impulse: float = dt * self._prim._force_max

        if self._prim._impulse.len_square() > max_impulse * max_impulse:
            self._prim._impulse.normalize()
            self._prim._impulse *= max_impulse

        J = self._prim._impulse - old_impulse
        self._prim._bodya.apply_impulse(J, self._prim._ra)
        self._prim._bodyb.apply_impulse(-J, self._prim._rb)

    def set_value(self, pa: Matrix, pb: Matrix) -> None:
        self._prim._nearest_pa = pa
        self._prim._nearest_pb = pb

    def solve_position(self, dt: float) -> None:
        pass

    def prim(self) -> DistanceConstraintPrimitive:
        return self._prim
