class RotationJointPrimitive():
    def __init__(self):
        self._bodya = Body()
        self._bodyb = Body()
        self._reference_rot = 0.0
        self._effective_mass = 0.0
        self._bias = 0.0


class OrientationJointPrimitive():
    def __init__(self):
        self._bodya = Body()
        self._target_point = Matrix([0.0, 0.0], 'vec')
        self._reference_rot = 0.0
        self._effective_mass = 0.0
        self._bias = 0.0


class RotationJoint(Joint):
    def __init__(self):
        self._type = JointType.Rotation
        self._primitive = RotationJointPrimitive
        self._factor = 0.2

    def set_value(self, primitive):
        self._primitive = primitive

    def prepare(self, dt):
        if self._primitive._bodya == None or self._primitive._bodyb == None:
            return

        ii_a = self._primitive._bodya.inverse_inertia()
        ii_b = self._primitive._bodyb.inverse_inertia()

        inv_dt = 1.0 / dt
        self._primitive._effective_mass = 1.0 / (ii_a + ii_b)
        c = self._primitive._bodya.rotation(
        ) - self._primitive._bodyb.rotation(
        ) - self._primitive._reference_rot
        self._primitive._bias = -self._factor * inv_dt * c

    def solve_velocity(self, dt):
        dw = self._primitive._bodya.angular_velocity(
        ) - self._primitive._bodyb.angular_velocity()
        impulse = self._primitive._effective_mass * (-dw +
                                                     self._primitive._bias)

        self._primitive._bodya.angular_velocity(
        ) += self._primitive._bodya.inverse_inertia() * impulse
        self._primitive._bodyb.angular_velocity(
        ) -= self._primitive._bodyb.inverse_inertia() * impulse

    def solve_position(self, dt):
        pass

    def primitive(self):
        return self._primitive


class OrientationJoint(Joint):
    def __init__(self):
        self._type = JointType.Orientation
        self._primitive = OrientationJointPrimitive()
        self._factor = 1.0

    def set_value(self, primitive):
        self._primitive = primitive

    def prepare(self, dt):
        if self._primitive._bodya == None:
            return

        bodya = self._primitive._bodya
        point = self._primitive._target_point - bodya.position()
        target_rot = point.theta()

        ii_a = self._primitive._bodya.inverse_inertia()
        inv_dt = 1.0 / dt
        self._primitive._effective_mass = 1.0 / ii_a
        c = target_rot - self._primitive._bodya.rotation(
        ) - self._primitive._reference_rot

        if np.isclose(c, 2.0 * np.pi) or np.isclose(c, -2.0 * np.pi):
            c = 0
            bodya.rotation() = target_rot

        self._primitive._bias = self._factor * inv_dt * c

        def solve_velocity(self, dt):
            dw = self._primitive._bodya.angular_velocity()
            impulse = self._primitive._effective_mass * (-dw *
                                                         self._primitive._bias)

            self._primitive._bodya.angular_velocity(
            ) += self._primitive._bodya.inverse_inertia() * impulse

        def solve_position(self, dt):
            pass

        def primitive(self):
            return self._primitive
