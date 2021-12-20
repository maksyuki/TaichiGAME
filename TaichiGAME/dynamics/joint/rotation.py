import numpy as np

from ...math.matrix import Matrix
from ..body import Body
from .joint import Joint, JointType


class RotationJointPrimitive():
    def __init__(self):
        self._bodya: Body = Body()
        self._bodyb: Body = Body()
        self._ref_rot: float = 0.0
        self._eff_mass: float = 0.0
        self._bias: float = 0.0


class OrientationJointPrimitive():
    def __init__(self):
        self._bodya: Body = Body()
        self._target_point: Matrix = Matrix([0.0, 0.0], 'vec')
        self._ref_rot: float = 0.0
        self._eff_mass: float = 0.0
        self._bias: float = 0.0


class RotationJoint(Joint):
    def __init__(self,
                 prim: RotationJointPrimitive = RotationJointPrimitive()):
        super().__init__()
        self._type: JointType = JointType.Rotation
        self._prim: RotationJointPrimitive = prim
        self._factor: float = 0.2

    def set_value(self, prim: RotationJointPrimitive) -> None:
        self._prim = prim

    def prepare(self, dt: float) -> None:
        if self._prim._bodya is None or self._prim._bodyb is None:
            return

        ii_a: float = self._prim._bodya.inv_inertia
        ii_b: float = self._prim._bodyb.inv_inertia
        inv_dt: float = 1.0 / dt

        self._prim._eff_mass = 1.0 / (ii_a + ii_b)
        c: float = self._prim._bodya.rot - self._prim._bodyb.rot
        c -= self._prim._ref_rot  # NOTE: just for static check
        self._prim._bias = -self._factor * inv_dt * c

    def solve_velocity(self, dt: float) -> None:
        dw: float = self._prim._bodya.ang_vel - self._prim._bodyb.ang_vel
        impulse: float = self._prim._eff_mass * (-dw + self._prim._bias)

        self._prim._bodya.ang_vel += self._prim._bodya.inv_inertia * impulse
        self._prim._bodyb.ang_vel -= self._prim._bodyb.inv_inertia * impulse

    def solve_position(self, dt: float) -> None:
        pass

    def prim(self) -> RotationJointPrimitive:
        return self._prim


class OrientationJoint(Joint):
    def __init__(
        self, prim: OrientationJointPrimitive = OrientationJointPrimitive()):
        super().__init__()
        self._type: JointType = JointType.Orientation
        self._prim: OrientationJointPrimitive = prim
        self._factor: float = 1.0

    def set_value(self, prim: OrientationJointPrimitive) -> None:
        self._prim = prim

    def prepare(self, dt: float) -> None:
        if self._prim._bodya is None:
            return

        bodya: Body = self._prim._bodya
        point: Matrix = self._prim._target_point - bodya.pos
        target_rot: float = point.theta()

        ii_a: float = self._prim._bodya.inv_inertia
        inv_dt: float = 1.0 / dt
        self._prim._eff_mass = 1.0 / ii_a
        c: float = target_rot - self._prim._bodya.rot - self._prim._ref_rot

        if np.isclose(c, 2.0 * np.pi) or np.isclose(c, -2.0 * np.pi):
            c = 0
            bodya.rot = target_rot

        self._prim._bias = self._factor * inv_dt * c

    def solve_velocity(self, dt: float) -> None:
        dw: float = self._prim._bodya.ang_vel
        impulse: float = self._prim._eff_mass * (-dw * self._prim._bias)
        self._prim._bodya.ang_vel += self._prim._bodya.inv_inertia * impulse

    def solve_position(self, dt: float) -> None:
        pass

    def prim(self) -> OrientationJointPrimitive:
        return self._prim
