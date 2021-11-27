class RevoluteJointPrimitive():
    def __init__(self):
        self._bodya = None
        self._bodyb = None
        self._local_pointa = Matrix([0.0, 0.0], 'vec')
        self._local_pointb = Matrix([0.0, 0.0], 'vec')
        self._damping = 0.0
        self._stiffness = 0.0
        self._frequency = 8.0
        self._max_force = 5000.0
        self._damping_radio = 0.2
        self._gamma = 0.0
        self._bias = Matrix([0.0, 0.0], 'vec')
        self._effective_mass = Matrix()
        self._impulse = Matrix([0.0, 0.0], 'vec')


class RevoluteJoint(Joint):
    def __init__(self):
        self._type = JointType.Revolute
        self._primitive = RevoluteJointPrimitive()

    def set_value(self, primitive):
        self._primitive = primitive

    def prepare(self, dt):
        if self._primitive._bodya == None or self._primitive._bodyb == None:
            return

        boyda = self._primitive._bodya
        bodyb = self._primitive._bodyb

        m_a = bodya.mass()
        im_a = bodya.inverse_mass()
        ii_a = bodya.inverse_inertia()

        m_b = bodyb.mass()
        im_b = bodyb.inverse_mass()
        ii_b = bodyb.inverse_inertia()

        if self._primitive._frequency > 0.0:
            nrf = self.natural_frequency(self._primitive._frequency)
            self._primitive._stiffness = self.spring_stiffness(m_a + m_b, nf)
            self._primitive._damping = self.spring_damping_cofficient(
                m_a + m_b, self._primitive._damping_radio)

        else:
            self._primitive._stiffness = 0.0
            self._primitive._damping = 0.0

        self._primitive._gamma = self.constraint_impulse_mixing(
            dt, self._primitive._stiffness, self._primitive._damping)
        erp = self.error_reduction_parameter(dt, self._primitive._stiffness,
                                             self._primitive._damping)

        pa = bodya.to_world_point(self._primitive._local_pointa)
        ra = pa - bodya.position()
        pb = bodyb.to_world_point(self._primitive._local_pointb)
        rb = pb - bodyb.position()

        self._primitive._bias = (pa - pb) * erp
        k = Matrix()

        data_arr = []

        data_arr.append(im_a + ra.val[1] * ra.val[1] * ii_a +
                        rb.val[1] * rb.val[1] * ii_b)
        data_arr.append(-ra.val[0] * ra.val[1] * ii_a -
                        rb.val[0] * rb.val[1] * ii_b)
        data_arr.append(data_arr[1])
        data_arr.append(im_a + ra.val[0] * ra.val[0] * ii_a + im_b +
                        rb.val[0] * rb.val[0] * ii_b)

        data_arr[0] += self._primitive._gamma
        data_arr[3] += self._primitive._gamma

        k.set_value(data_arr)

        self._primitive._effective_mass = k.invert()
        self._primitive._bodya.apply_impulse(self._primitive._impulse, ra)
        self._primitive._bodyb.apply_impulse(self._primitive._impulse, rb)

    def solve_velocity(self, dt):
        if self._primitive._bodya == None or self._primitive._bodyb:
            return

        ra = self._primitive._bodya.to_world_point(
            self._primitive._local_pointa) - self._primitive._bodya.position()
        va = self._primitive._bodya.velocity() + Matrix.cross_product(
            self._primitive._bodya.angular_velocity(), ra)
        rb = self._primitive._bodyb.to_world_point(
            self._primitive._local_pointb) - self._primitive._bodyb.position()
        vb = self._primitive._bodyb.velocity() + Matrix.cross_product(
            self._primitive._bodyb.angular_velocity(), rb)

        jvb = va - vb
        jvb += self._primitive._bias
        jvb += self._primitive._impulse * self._primitive._gamma
        jvb.negate()

        J = self._primitive._effective_mass * jvb
        old_impulse = self._primitive._impulse
        self._primitive._impulse += J

        max_impulse = dt * self._primitive._max_force

        if self._primitive._impulse.len_square() > max_impulse * max_impulse:
            self._primitive._impulse.normalize()
            self._primitive._impulse *= max_impulse

        J = self._primitive._impulse - old_impulse
        self._primitive._bodya.apply_impulse(J, ra)
        self._primitive._bodyb.apply_impulse(-J, rb)

    def solve_position(self, dt):
        if self._primitive._bodya == None or self._primitive._bodby == None:
            return

    def primitive(self):
        return self._primitive
