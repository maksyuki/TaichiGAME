class JointType():
    Distance = 0
    Point = 1
    Rotation = 2
    Orientation = 3
    Pulley = 4
    Prismatic = 5
    Wheel = 6
    Revolut = 7


class Joint():
    def __init__(self):
        self._active = True
        self._type = None
        self._id = 0

    def prepare(self, dt):
        pass

    def solve_velocity(self, dt):
        pass

    def solve_position(self, dt):
        pass

    def active(self):
        return self._active

    def set_active(self, active):
        self._active = active

    def type(self):
        return self._type

    def id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    @staticmethod
    def natural_frequency(frequency):
        return np.pi * frequency

    @staticmethod
    def spring_damping_cofficient(mass, natural_freq, damping_radio):
        return damping_radio * 2.0 * mass * natural_freq

    @staticmethod
    def spring_stiffness(mass, natural_freq):
        return mass * natural_freq * natural_freq

    @staticmethod
    def constraint_impulse_mixing(dt, stiffness, damping):
        cim = dt * (dt * stiffness + damping)
        return 0.0 if np.isclose(cim, 0.0) else 1.0 / cim

    @staticmethod
    def error_reduction_parameter(dt, stiffness, damping):
        erp = dt * stiffness + damping
        return 0.0 if np.isclose(erp, 0.0) else stiffness / erp
