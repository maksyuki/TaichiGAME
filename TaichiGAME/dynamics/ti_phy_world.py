import taichi as ti


@ti.data_oriented
class PhysicsWorld():
    def __init__(self, body_len: int = 100):
        # env var
        self._grav_ena: bool = True
        self._grav: ti.Vector = ti.Vector([0.0, -1.0])

        self._damping_ena: bool = True
        self._linear_vel_damping: float = 0.9
        self._ang_vel_damping: float = 0.9

        self._body_len: int = body_len
        self._mass = ti.field(float, shape=self._body_len)
        self._inertia = ti.field(float, shape=self._body_len)
        # -1: static 0: dynamic 1: kinematic
        self._type = ti.field(float, shape=self._body_len)
        self._pos = ti.Vector.field(2, float, shape=self._body_len)
        self._vel = ti.Vector.field(2, float, shape=self._body_len)
        self._rot = ti.Vector.field(2, float, shape=self._body_len)
        self._ang_vel = ti.field(float, shape=self._body_len)
        self._force = ti.Vector.field(2, float, shape=self._body_len)
        self._torque = ti.field(float, shape=self._body_len)

    @ti.kernel
    def step_velocity(self, dt: float):
        lvd = 1.0 / (1.0 + dt * self._linear_vel_damping)
        avd = 1.0 / (1.0 + dt * self._ang_vel_damping)
        g = self._grav

        for i in range(self._body_len):
            if self._type[i] == -1:
                self._vel[i] = ti.Vector([0.0, 0.0])
                self._ang_vel[i] = 0.0

            elif self._type[i] == 0:
                self._force[i] = self._force[i] + self._mass[i] * g
                self._vel[
                    i] = self._vel[i] + self._force[i] / self._mass[i] * dt
                self._ang_vel[i] = self._ang_vel[
                    i] + self._torque[i] / self._inertia[i] * dt

                self._vel[i] = self._vel[i] * lvd
                self._ang_vel[i] = self._ang_vel[i] * avd

            elif self._type[i] == 1:
                self._vel[
                    i] = self._vel[i] + self._force[i] / self._mass[i] * dt
                self._ang_vel[i] = self._ang_vel[
                    i] + self._torque[i] / self._inertia[i] * dt

                self._vel[i] = self._vel[i] * lvd
                self._ang_vel[i] = self._ang_vel[i] * avd

    @ti.kernel
    def step_position(self, dt: float):
        for i in range(self._body_len):
            if self._type[i] == -1:
                pass

            elif self._type[i] == 0 or self._type[i] == 1:
                self._pos[i] = self._pos[i] + self._vel[i] * dt
                self._rot[i] = self._rot[i] + self._ang_vel[i] * dt
                self._force[i] = ti.Vector([0.0, 0.0])
                self._torque[i] = 0.0
