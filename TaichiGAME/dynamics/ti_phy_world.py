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

        # body physics params
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

        # body shape
        self._cir_radius = ti.field(float, shape=self._body_len)

        self._edg_st = ti.Vector.field(2, float, shape=self._body_len)
        self._edg_ed = ti.Vector.field(2, float, shape=self._body_len)
        self._tri_a = ti.Vector.field(2, float, shape=self._body_len)
        self._tri_b = ti.Vector.field(2, float, shape=self._body_len)
        self._tri_c = ti.Vector.field(2, float, shape=self._body_len)
        self._polyx = ti.Vector.field(6, float, shape=self._body_len)
        self._polyy = ti.Vector.field(6, float, shape=self._body_len)
        self._poly_st = ti.Vector.field(2, float, shape=(self._body_len, 6))
        self._poly_ed = ti.Vector.field(2, float, shape=(self._body_len, 6))

    @ti.kernel
    def random_set(self):
        for i in range(self._body_len):
            self._pos[i] = ti.Vector([ti.random(), ti.random()])
            self._cir_radius[i] = ti.random() * 4 + 2
            self._edg_st[i] = ti.Vector([ti.random(), ti.random()])
            self._edg_ed[i] = self._edg_st[i] + 0.1
            self._tri_a[i] = ti.Vector([ti.random(), ti.random()])
            self._tri_b[i] = self._tri_a[i] + 0.05
            self._tri_c[i] = ti.Vector(
                [self._tri_a[i].x, self._tri_a[i].y + 0.05])

            # self._polyx[i][0] = 0.5
            # self._polyy[i][0] = 0.5
            # self._polyx[i][1] = 0.6
            # self._polyy[i][1] = 0.6
            # self._polyx[i][2] = 0.5
            # self._polyy[i][2] = 0.7
            # self._polyx[i][3] = 0.4
            # self._polyy[i][3] = 0.7
            # self._polyx[i][4] = 0.3
            # self._polyy[i][4] = 0.6
            # self._polyx[i][5] = 0.4
            # self._polyy[i][5] = 0.5
            # for j in range(6):
                # self._poly_st[i, j] = self._polyx[i][j]
                # self._poly_ed[i, j] = self._poly

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
