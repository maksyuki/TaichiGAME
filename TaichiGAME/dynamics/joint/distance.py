class DistanceJointPrimitive():
    def __init__(self):
        self._bodya = None
        self._local_pointa = Matrix([0.0, 0.0], 'vec')
        self._target_point = Matrix([0.0, 0.0], 'vec')
        self._normal = Matrix([0.0, 0.0], 'vec')
        self._bias_factor = 0.3
        self._bias = 0.0
        self._min_distance = 0.0
        self._max_distance = 0.0
        self._effective_mass = 0.0
        self._accumulated_impulse = 0.0


class DistanceConstraintPrimitive():
    def __init__(self):
        self._bodya = None
        self._bodyb = None
        self._nearest_pointa = Matrix([0.0, 0.0], 'vec')
        self._nearest_pointb = Matrix([0.0, 0.0], 'vec')
        self._ra = Matrix([0.0, 0.0], 'vec')
        self._rb = Matrix([0.0, 0.0], 'vec')
        self._bias = Matrix([0.0, 0.0], 'vec')
        self._effective_mass = Matrix()
        self._impluse = Matrix([0.0, 0.0], 'vec')
        self._max_force = 200.0


class DistanceJoint(Joint):
    def __init__(self):
        self._type = JointType.Distance
        self._primitive = DistanceJointPrimitive()
        self._factor = 0.4

    def set_value(self, primitive):
        self._primitive = primitive

    def prepare(self, dt):
        assert self._primitive._min_distance <= self._primitive._max_distance

        boyda = self._primitive._bodya
        pa = bodya.to_world_point(self._primitive._local_pointa)
        ra = pa - bodya.position()
        pb = self._primitive._target_point
        im_a = self._primitive._bodya.inverse_mass()
        ii_a = self._primitive._bodya.inverse_inertia()
        error = pb - pa
        val_len = error.len()
        c = 0

        self._primitive._normal = error.normal()
        if val_len < self._primitive._min_distance:
            c = self._primitive._min_distance - val_len
            self._primitive._normal.negate()
        elif val_len > self._primitive._max_distance:
            c = val_len - self._primitive._max_distance
        else:
            self._primitive._accumulated_impulse = 0.0
            self._primitive._normal.clear()
            self._bias = 0.0
            return

        if self._primitive._bodya.velocity().dot(self._primitive._normal) > 0:
            self._primitive._accumulated_impulse = 0.0
            self._primitive._normal.clear()
            self._primitive._bias = 0.0
            return

        rn_a = self._primitive._normal.dot(ra)
        self._primitive._effective_mass = 1.0 / (im_a + ii_a * rn_a * rn_a)
        self._primitive._bias = self._primitive._bias_factor * c / dt

    def solve_velocity(self, dt):
        if self._primitive._bias == 0:
            return

        ra = self._primitive._bodya.to_world_point(
            self._primitive._local_pointa) - self._primitive._bodya.position()
        va = self._primitive._bodya.velocity() + Matrix.cross_product(
            self._primitive._bodya.angular_velocity(), ra)
        dv = va
        jv = self._primitive._normal.dot(dv)
        jvb = -jv + self._primitive._bias
        lambda_n = self._primitive._effective_mass * jvb

        old_impulse = self._primitive._accumulated_impulse
        self._primitive._accumulated_impulse = np.fmax(old_impulse + lambda_n,
                                                       0)
        lambda_n = self._primitive._accumulated_impulse - old_impulse

        impulse = lambda_n * self._primitive._normal
        self._primitive._bodya.apply_impulse(impulse, ra)

        def solve_position(self, dt):
            pass

        def primitive(self):
            return self._primitive


class DistanceConstraint(Joint):
    def __init__(self):
        self._primitive = DistanceConstraintPrimitive()
        self._factor = 0.1

    def prepare(self, dt):
        if self._primitive._bodya == None or self._primitive._bodyb:
            return

        bodya = self._primitive._bodyb
        bodyb = self._primitive._bodyb
        im_a = bodya.inverse_mass()
        ii_a = bodya.inverse_inertia()

        im_b = bodyb.inverse_mass()
        ii_b = bodyb.inverse_inertia()

        self._primitive._ra = self._primitive._nearest_pointa - bodya.position(
        )
        self._primitive._rb = self._primitive._nearest_pointb - bodyb.position(
        )
        ra = self._primitive._ra
        rb = self._primitive._rb
        error = self._primitive._nearest_pointa - self._primitive._nearest_pointb

        k = Matrix()
        data_arr = []
        data_arr.append(im_a + ra.val[1] * ra.val[1] * ii_a + im_b +
                        rb.val[1] * rb.val[1] * ii_b)
        data_arr.append(-ra.val[0] * ra.val[1] * ii_a -
                        rb.val[0] * rb.val[1] * ii_b)
        data_arr.append(-ra.val[0] * ra.val[1] * ii_a -
                        rb.val[0] * rb.val[1] * ii_b)
        data_arr.append(im_a + ra.val[0] * ra.val[0] * ii_a + im_b +
                        rb.val[0] * rb.val[0] * ii_b)

        k.set_value(data_arr)
        self._primitive._bias = erro * self._factor
        self._primitive._effective_mass = k.invert()

    def solve_velocity(self, dt):
        if self._primitive._bodya == None or self._primitive._bodyb == None:
            return

        va = self._primitive._bodya.velocity() + Matrix.cross_product(
            self._primitive._bodya.angular_velocity(), self._primitive._ra)
        vb = self._primitive._bodyb.velocity() + Matrix.cross_product(
            self._primitive._bodyb.angular_velocity(), self._primitive._rb)

        jvb = va - vb
        jvb += self._primitive._bias
        jvb.negate()

        J = self._primitive._effective_mass * jvb
        old_impulse = self._primitive._impluse
        self._primitive._impluse += J

        max_impulse = dt * self._primitive._max_force

        if self._primitive._impluse.len_square() > max_impulse * max_impulse:
            self._primitive.impulse.normalize()
            self._primitive.impulse *= max_impulse

        J = self._primitive._impluse - old_impulse
        self._primitive._bodya.apply_impulse(J, self._primitive._ra)
        self._primitive._bodyb.apply_impulse(J, self._primitive._rb)

        def set_value(self, pointa, pointb):
            self._primitive._nearest_pointa = pointa
            self._primitive._nearest_pointb = pointb

        def solve_position(self):
            pass

        def primitive(self):
            return self._primitive
