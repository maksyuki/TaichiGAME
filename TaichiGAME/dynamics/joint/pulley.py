from .joint import Joint, JointType


class PulleyJointPrimitive():
    def __init__(self):
        pass


class PulleyJoint(Joint):
    def __init__(self, prim: PulleyJointPrimitive = PulleyJointPrimitive()):
        super().__init__()
        self._type: JointType = JointType.Pulley
        self._prim: PulleyJointPrimitive = prim

    def set_value(self, prim: PulleyJointPrimitive):
        self._prim = prim

    def prepare(self, dt: float) -> None:
        raise NotImplementedError

    def solve_velocity(self, dt: float) -> None:
        raise NotImplementedError

    def solve_position(self, dt: float) -> None:
        raise NotImplementedError
