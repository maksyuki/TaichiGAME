class VelocityConstraintPoint():
    def __init__(self):
        self._ra = Matrix([0.0, 0.0], 'vec')
        self._rb = Matrix([0.0, 0.0], 'vec')
        self._va = Matrix([0.0, 0.0], 'vec')
        self._vb = Matrix([0.0, 0.0], 'vec')
        self._normal = Matrix([0.0, 0.0], 'vec')
        self._tangent = Matrix([0.0, 0.0], 'vec')
        self._velocity_bias = Matrix([0.0, 0.0], 'vec')
        self._bias = 0.0
        self._penetration = 0.0
        self._restitution = 0.8
        self._effective_mass_normal = 0.0
        self._effective_mass_tangent = 0.0
        self._accumulate_normal_impulse = 0.0
        self._accumulate_tangent_impulse = 0.0


class ContactConstraintPoint():
    def __init__(self):
        self._relation = 0
        self._friction = 0.2
        self._active = True
        self._locala = Matrix([0.0, 0.0], 'vec')
        self._localb = Matrix([0.0, 0.0], 'vec')
        self._vcp = VelocityConstraintPoint()


class ContactMaintainer():
    def __init__(self):
        self._max_penetration = 0.01
        self._bias_factor = 0.03
        self._contact_table = {}

    def clear_all(self):
        self._contact_table.clear()

    def solve_velocity(self, dt):
        for key, val in self._contact_table.items():
            if val.empty() or not val[0]._active:
                continue

            for ccp in val:
                vcp = ccp._vcp
                wa = Matrix.cross_product(ccp._bodya.angular_velocity(),
                                          vcp._ra)
                wb = Matrix.cross_product(ccp._bodyb.angular_velocity(),
                                          vcp._rb)
                vcp._va = ccp._bodya.velocity() + wa
                vcp._vb = ccp._bodyb.velocity() + wb

                dv = vcp._va - vpc._vb
                jv = -1.0 * vcp._normal.dot(dv - vcp._velocity_bias)
                lambda_n = vcp._effective_mass_normal * jv
                old_impulse = vcp._accumulate_normal_impulse
                vcp._accumulate_normal_impulse = np.fmax(
                    old_impulse + lambda_n, 0)
                lambda_n = vcp._accumulate_normal_impulse - old_impulse
                impulse_n = lambda_n * vcp._normal

                ccp._bodya.apply_impulse(impulse_n, vcp._ra)
                ccp._bodyb.apply_impulse(-impulse_n, vcp._rb)

                vcp._va = ccp._bodya.velocity() + Matrix.cross_product(
                    ccp._bodya.angular_velocity(), vcp._ra)
                vcp._vb = ccp._bodyb.velocity() + Matrix.cross_product(
                    ccp._bodyb.angular_velocity(), vcp._rb)
                dv = vcp._va - vcp._vb

                jvt = vcp._tangent.dot(dv)
                lambda_t = vcp._effective_mass_tangent * -jvt
                maxT = ccp._friction * vcp._accumulate_normal_impulse
                old_impulse = vcp._accumulate_tangent_impulse
                # FIXME: have np.clamp ??
                vcp._accumulate_tangent_impulse = np.clamp(
                    old_impulse + lambda_t, -maxT, maxT)
                lambda_t = vcp._accumulate_tangent_impulse - old_impulse
                impulse_t = lambda_t * vcp._tangent

                ccp._bodya.apply_impulse(impulse_t, vcp._ra)
                ccp._bodyb.apply_impulse(-impulse_t, vcp._rb)

    def solve_position(self, dt):
        for key, val in self._contact_table.items():
            if val.empty() or not val[0]._active:
                continue

            for ccp in val:
                vcp = ccp.vcp
                bodya = ccp._bodya
                bodyb = ccp._bodyb
                pa = vcp._ra + bodya.position()
                pb = vcp._rb + bodyb.position()
                c = pa - pb

                if c.dot(vcp._normal) < 0.0:
                    continue

                bias = self._bias_factor * np.fmax(
                    c.len() - self._max_penetration, 0.0)
                val_lambda = vcp._effective_mass_normal * bias
                impulse = val_lambda * vcp._normal

                if bodya.type(
                ) != Body.BodyType.Static and not ccp._bodya.sleep():
                    bodya.position() += bodya.inverse_mass() * impulse
                    bodya.rotation(
                    ) += bodya.inverse_inertia() * vcp._ra.cross(impulse)

                if bodyb.type(
                ) != Body.BodyType.Static and not ccp._bodyb.sleep():
                    bodyb.position() += bodyb.inverse_mass() * impulse
                    bodyb.rotation(
                    ) += bodyb.inverse_inertia() * vcp._rb.cross(impulse)

    def add(self, collision):
        bodya = collision._bodya
        bodyb = collision._bodyb
        # FIXME:
        relation = generate_relation(collision._bodya, Collsion._bodyb)
        contact_list = self._contact_table[relation]

        for elem in collision._contact_list:
            existed = False
            locala = bodya.to_local_point(elem._pointa)
            localb = bodyb.to_local_point(elem._pointb)
            for contact in contact_list:
                # FIXME:
                is_pointa = np.isclose(contain._locala, 0.1)
                is_pointb = np.isclose(contain._localb, 0.1)
                if is_pointa and is_pointb:
                    contact._locala = locala
                    contact._localb = localb
                    self.prepare(contact, elem, collsion)
                    existed = True
                    break
            if existed:
                continue

            ccp = ContactConstraintPoint()
            ccp._locala = locala
            ccp._localb = localb
            ccp._relation = relation
            self.prepare(ccp, elem, collision)
            contact_list.append(ccp)

    def prepare(self, ccp, pair, collision):
        ccp._bodya = collision._bodya
        ccp._bodyb = collision._bodyb
        ccp._active = True

        ccp._friction = np.sqrt(ccp._bodya.friction() * ccp._bodyb.friction())

    def clear_inactive_points(self):
        clear_list = []
        removed_list = []
        for key, val in self._contact_table.items():
            if val.empty():
                clear_list.append(key)
                continue

            for v in val:
                if not v._active:
                    removed_list.append(v)

            # TODO:
            # for v in removed_list:
            #     for re in v:
            #         if re == id

    def deactivate_all_points(self):
        for val in self._contact_table.values():
            if val.empty() or not val[0]._active:
                continue

            for ccp in val:
                ccp._active = False
