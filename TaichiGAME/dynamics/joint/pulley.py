class PulleyJointPrimitive():
    def __init__(self):
        self._type = JointType.Pulley

    def set_value(self, primitive):
        self._primitive = primitive

    def prepare(self, dt):
        pass

    def solve_velocity(self, dt):
        pass

    def solve_position(self, dt):
        pass


class PulleyJoint(Joint):
    def __init__(self):
        self._primitive = PulleyJointPrimitive()
