class PointJointPrimitive():
    def __init__(self):
        self._bodya = Body()
        self._local_pointa = Matrix([0.0, 0.0], 'vec')
        self._target_point = Matrix([0.0, 0.0], 'vec')
        self._normal = Matrix([0.0, 0.0], 'vec')

        self._damping = 0.0
        self._stiffness = 0.0
        self._frequency = 8.0
        self._max_force = 1000.0
        self._damping_radio = 1.0
        self._gamma = 0.0
        self._bias = Matrix([0.0, 0.0], 'vec')
        self._effective_mass = Matrix()
        self._impulse = Matrix([0.0, 0.0], 'vec')


class PointJoint(Joint):
    def __init__(self):
        self._type = JointType.Point
        self._primitive = PointJointPrimitive()
        self._factor = 0.22

    def set_value(self, prim):
        self._primitive = prim

    def prepare(self, dt):
        if self._primitive._bodya == None:
            return

        bodya = self._primitive._bodya
        m_a = bodya.mass()
        im_a = bodya.inverse_mass()
        ii_a = bodya.inverse_inertia()

        if self._primitive._frequency > 0.0:
            nf = self.natural_frequency(self._primitive._frequency)
            self._primitive._stiffness = self.spring_stiffness(m_a, nf)
            self._primitive._damping = self.spring_damping_cofficient(
                m_a, nf, self._primitive._damping_radio)
        else:
            self._primitive._stiffness = 0.0
            self._primitive._damping = 0.0

        self._primitive._gamma = self.constraint_impulse_mixing(
            dt, self._primitive._stiffness, self._primitive._damping)
        erp = self.error_reduction_parameter(dt, self._primitive._stiffness,
                                             self._primitive._damping)

        pa = bodya.to_world_point(self._primitive._local_pointa)
        ra = pa - bodya.position()
        pb = self._primitive._target_point

        self._primitive._bias = (pa - pb) * erp
        k = Matrix()
        data_arr = []
        data_arr.append(im_a + ra.val[1] * ra.val[1] * ii_a)
        data_arr.append(-ra.val[0] * ra.val[1] * ii_a)
        data_arr.append(-ra.val[0] * ra.val[1] * ii_a)
        data_arr.append(im_a + ra.val[0] * ra.val[0] * ii_a)

        data_arr[0] += self._primitive._gamma
        data_arr[3] += self._primitive._gamma

        k.set_value(data_arr)
        self._primitive._effective_mass = k.invert()
        bodya.apply_impulse(self._primitive._impluse, ra)

    def solve_velocity(self, dt):
        if self._primitive._bodya == None:
            return

        ra = self._primitive._bodya.to_world_point(
            self._primitive._local_pointa) - self._primitive._bodya.position()
        va = self._primitive._bodya.velocity() + Matrix.cross_product(
            self._primitive._bodya.angular_velocity(), ra)
        jvb = va
        jvb += self._primitive._bias
        jvb += self._primitive._impluse * self._primitive._gamma
        jvb.negate()

        J = self._primitive._effective_mass * jvb
        old_impulse = self._primitive._impluse
        self._primitive._impulse += J
        max_impulse = dt * self._primitive._max_force

        if self._primitive._impulse.len_square() > max_impulse * max_impulse:
            self._primitive._impulse.normalize()
            self._primitive._impulse *= max_impulse

        J = self._primitive._impulse - old_impulse
        self._primitive._bodya.apply_impulse(J, ra)

    def solve_position(self, dt):
        pass

    def prim(self):
        return self._primitive
