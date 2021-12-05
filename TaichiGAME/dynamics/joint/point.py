from typing import List, Dict, Optional, Tuple

import numpy as np

from ...math.matrix import Matrix
from ..body import Body
from .joint import Joint, JointType


class PointJointPrimitive():
    def __init__(self):
        self._bodya: Body = Body()
        self._local_pointa: Matrix = Matrix([0.0, 0.0], 'vec')
        self._target_point: Matrix = Matrix([0.0, 0.0], 'vec')
        self._normal: Matrix = Matrix([0.0, 0.0], 'vec')

        self._damping: float = 0.0
        self._stiff: float = 0.0
        self._freq: float = 8.0
        self._force_max: float = 1000.0
        self._damping_radio: float = 1.0
        self._gamma: float = 0.0
        self._bias: Matrix = Matrix([0.0, 0.0], 'vec')
        self._eff_mass: Matrix = Matrix([0.0, 0.0, 0.0, 0.0])
        self._impulse: Matrix = Matrix([0.0, 0.0], 'vec')


class PointJoint(Joint):
    def __init__(self, prim: PointJointPrimitive = PointJointPrimitive()):
        self._type: JointType = JointType.Point
        self._prim: PointJointPrimitive = prim
        self._factor: float = 0.22

    def set_value(self, prim: PointJointPrimitive):
        self._prim = prim

    def prepare(self, dt: float):
        if self._prim._bodya == None:
            return

        bodya: Body = self._prim._bodya
        m_a: float = bodya.mass
        im_a: float = bodya.inv_mass
        ii_a: float = bodya.inv_inertia

        if self._prim._freq > 0.0:
            nf: float = self.natural_frequency(self._prim._freq)
            self._prim._stiff = self.spring_stiff(m_a, nf)
            self._prim._damping = self.spring_damping_cofficient(
                m_a, nf, self._prim._damping_radio)
        else:
            self._prim._stiff = 0.0
            self._prim._damping = 0.0

        self._prim._gamma = self.constraint_impulse_mixing(
            dt, self._prim._stiff, self._prim._damping)
        erp: float = self.error_reduction_parameter(dt, self._prim._stiff,
                                                    self._prim._damping)

        pa: Matrix = bodya.to_world_point(self._prim._local_pointa)
        ra: Matrix = pa - bodya.pos
        pb: Matrix = self._prim._target_point

        self._prim._bias = (pa - pb) * erp
        k: Matrix = Matrix([0.0, 0.0, 0.0, 0.0])
        data_arr: List[float] = []
        data_arr.append(im_a + ra.y * ra.y * ii_a)
        data_arr.append(-ra.x * ra.y * ii_a)
        data_arr.append(data_arr[1])
        data_arr.append(im_a + ra.x * ra.x * ii_a)

        data_arr[0] += self._prim._gamma
        data_arr[3] += self._prim._gamma

        k.set_value(data_arr)
        self._prim._eff_mass = k.invert()
        bodya.apply_impulse(self._prim._impluse, ra)

    def solve_velocity(self, dt: float):
        if self._prim._bodya == None:
            return

        ra: Matrix = self._prim._bodya.to_world_point(
            self._prim._local_pointa) - self._prim._bodya.pos
        va: Matrix = self._prim._bodya.vel + Matrix.cross_product(
            self._prim._bodya.ang_vel, ra)

        jvb: Matrix = va
        jvb += self._prim._bias
        jvb += self._prim._impluse * self._prim._gamma
        jvb.negate()

        J: Matrix = self._prim._eff_mass * jvb
        old_impulse: Matrix = self._prim._impluse
        self._prim._impulse += J

        max_impulse: float = dt * self._prim._force_max
        if self._prim._impulse.len_square() > max_impulse * max_impulse:
            self._prim._impulse.normalize()
            self._prim._impulse *= max_impulse

        J = self._prim._impulse - old_impulse
        self._prim._bodya.apply_impulse(J, ra)

    def solve_position(self, dt: float):
        pass

    def prim(self) -> PointJointPrimitive:
        return self._prim
