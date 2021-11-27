class Body():
    class BodyType():
        Kinematic = 0
        Static = 1
        Dynamic = 2
        Bullet = 3

    class PhysicsAttribute():
        def __init__(self):
            self._position = Matrix([0.0, 0.0], 'vec')
            self._velocity = Matrix([0.0, 0.0], 'vec')
            self._rotation = 0.0
            self._angular_velocity = 0.0

        def step(dt):
            self._position += self._velocity * dt
            self._rotation += self._angular_velocity * dt

    def __init__(self):
        self._id = 0
        self._bitmask = 1
        self._mass = 0.0
        self._inv_mass = 0.0
        self._inertia = 0.0
        self._inv_inertia = 0.0
        self._position = Matrix([0.0, 0.0], 'vec')
        self._velocity = Matrix([0.0, 0.0], 'vec')
        self._rotation = 0.0
        self._angular_velocity = 0.0
        self._forces = 0.0
        self._torques = 0.0

        self._shape = Shape()
        self._type = Body.BodyType.Static

        self._sleep = False
        self._friction = 0.2
        self._restitution = 0.0

    def position(self):
        return self._position

    def velocity(self):
        return self._velocity

    def rotation(self):
        return self._rotation

    def angular_velocity(self):
        return self._angular_velocity

    def forces(self):
        return self._forces

    def clear_torque(self):
        self._torques = 0.0

    def torques(self):
        return self._torques

    def shape(self):
        return self._shape

    def set_shape(self, shape):
        self._shape = shape
        self.calc_inertia()

    def type(self):
        return self._type

    def set_type(self, type):
        self._type = type

    def mass(self):
        return self._mass

    def set_mass(self, mass):
        self._mass = mass
        #FIXME: need to set the right max limit value
        if mass == 222222:
            self._inv_mass = 0.0
        else:
            self._inv_mass = 0.0 if np.isclose(mass, 0) else 1.0 / mass

        self.calc_inertia()

    def inertia(self):
        return self._inertia

    def aabb(self, factor=1.0):
        primitive = ShapePrimitive()
        primitive._transform = self._position
        primitive._rotation = self._rotation
        primitive._shape = self._shape
        return AABB.from_shape(primitive, factor)

    def friction(self):
        return self._friction

    def set_friction(self, friction):
        self._friction = friction

    def sleep(self):
        return self._sleep

    def set_sleep(self, sleep):
        self._sleep = sleep

    def inverse_mass(self):
        return self._inv_mass

    def inverse_inertia(self):
        return self._inv_inertia

    def physic_attribute(self):
        return PhysicsAttribute(self._position, self._velocity,
                                self._angular_velocity)

    def set_physics_attribute(self, info):
        self._position = info._position
        self._rotation = info._rotation
        self._velocity = info._velocity
        self._angular_velocity = info._angular_velocity

    def step_position(self, dt):
        self._position += self._velocity * dt
        self._rotation += self._angular_velocity * dt

    def apply_impulse(self, impulse, r):
        self._velocity += self._inv_mass * impulse
        self._angular_velocity += self._inv_inertia * r.cross(impulse)

    def to_local_point(self, point):
        return Matrix.rotate_mat(-self._rotation) * (point - self._position)

    def to_world_point(self, point):
        return Matrix.rotate_mat(self._rotation) * point + self._position

    def to_actual_point(self, point):
        return Matrix.rotate_mat(self._rotation) * point

    def id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def bitmask(self):
        return self._bitmask

    def set_bitmask(self, bitmask):
        self._bitmask = bitmask

    def restitution(self):
        return self._restitution

    def set_restitution(self, restitution):
        self._restitution = restitution

    def calc_inertia(self):
        shape_type = self._shape.type()

        if shape_type == Shape.Type.Circle:
            circle = self._shape
            self._inertia = self._mass * circle.radius() * circle.radius(
            ) / 2.0
            break
        elif shape_type == Shape.Type.Polygon:
            polygon = self._shape
            center = polygon.center()

            sum1 = 0.0
            sum2 = 0.0
            for i in range(len(polygon.vertices()) - 1):
                n1 = polygon.vertices()[i] - center
                n2 = polygon.vertices()[i + 1] - center
                cross = np.fabs(n1.cross(n2))
                dot = n2.dot(n2) + n2.dot(d1) + n1.dot(n1)
                sum1 += cross * dot
                sum2 += cross

            self._inertia = self._mass * (1.0 / 6.0) * sum1 / sum2
            break

        elif shape_type == Shape.Type.Ellipse:
            ellipse = self._shape
            a = ellipse.A()
            b = ellipse.B()
            self._inertia = self._mass * (a * a + b * b) * (1.0 / 5.0)
            break

        elif shape_type == Shape.Type.Capsule:
            capsule = self._shape
            r = 0.0
            h = 0.0
            mass_s = 0.0
            inertia_s = 0.0
            mass_c = 0.0
            inertia_c = 0.0
            volume = 0.0

            if capsule.width() >= capsule.height():
                r = capsule.height() / 2.0
                h = capsule.width() - capsule.height()

            else:
                r = capsule.width() / 2.0
                h = capsule.height() - capsule.width()

            volume = np.pi * r * r + h * 2 * r
            rho = self._mass / volume
            mass_s = rho * pi * r * r
            mass_c = rho * h * 2.0 * r
            inertia_c = (1.0 / 12.0) * mass_c * (h * h + (2.0 * r) * (2.0 * r))
            inertia_s = mass_s * r * r * 0.5
            self._inertia = inertia_c + inertia_s + mass_s * (
                3.0 * r + 2.0 * h) * h / 8.0
            break
        elif shape_type == Shape.Type.Sector:
            sector = self._shape
            self._inertia = self._mass * (
                sector.span_radian() - np.sin(sector.span_radian())
            ) * sector.radius() * sector.radius() / 4.0 * sector.span_radian()
            break

        # FIXME: need to set right max value
        if np.isclose(self._mass, 22222):
            self._inv_inertia = 0.0
        else:
            self._inv_inertia = 1.0 / self._inertia if not np.isclose(
                self._inertia, 0) else 0.0
