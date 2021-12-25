from typing import Optional, Union, List, cast

import taichi as ti

from ..dynamics.body import Body
from .joint.joint import Joint
from ..common.random import RandomGenerator
from ..geometry.shape import Circle, Edge, Shape


@ti.data_oriented
class PhysicsWorld():
    def __init__(self, body_len: int = 100):
        # env var
        self._grav_ena: bool = True
        self._grav: ti.Vector = ti.Vector([0.0, -1.0])

        self._damping_ena: bool = True
        self._linear_vel_damping: float = 0.9
        self._ang_vel_damping: float = 0.9

        self._body_list: List[Body] = []
        self._joint_list: List[Joint] = []

        # body physics params
        self._body_len: int = body_len
        self._mass = ti.field(float, shape=self._body_len)
        self._inertia = ti.field(float, shape=self._body_len)
        # 0: kinematic 1: static 2: dynamic
        self._type = ti.field(float, shape=self._body_len)
        self._pos = ti.Vector.field(2, float, shape=self._body_len)
        self._vel = ti.Vector.field(2, float, shape=self._body_len)
        self._rot = ti.field(float, shape=self._body_len)
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
        self._poly_st = ti.Vector.field(2, float, shape=6)
        self._poly_ed = ti.Vector.field(2, float, shape=6)
        self._polytri_a = ti.Vector.field(2, float, shape=4)
        self._polytri_b = ti.Vector.field(2, float, shape=4)
        self._polytri_c = ti.Vector.field(2, float, shape=4)

    def create_body(self):
        body: Body = Body()
        body.id = RandomGenerator.unique()
        self._body_list.append(body)
        return body

    def init_data(self):
        bd_len: int = len(self._body_list)
        for i in range(bd_len):
            self._mass[i] = self._body_list[i].mass
            self._inertia[i] = self._body_list[i].inertia
            self._type[i] = self._body_list[i].type
            self._pos[i] = ti.Vector(
                [self._body_list[i].pos.x, self._body_list[i].pos.y])
            self._vel[i] = ti.Vector(
                [self._body_list[i].vel.x, self._body_list[i].vel.y])
            self._rot[i] = self._body_list[i].rot
            self._ang_vel[i] = self._body_list[i].ang_vel
            self._force[i] = ti.Vector(
                [self._body_list[i].forces.x, self._body_list[i].forces.y])
            self._torque[i] = self._body_list[i].torques

            if self._body_list[i].shape == Shape.Type.Circle:
                cir: Circle = cast(Circle, self._body_list[i].shape)
                self._cir_radius[i] = cir.radius
            elif self._body_list[i].shape == Shape.Type.Edge:
                edg: Edge = cast(Edge, self._body_list[i].shape)
                self._edg_st[i] = ti.Vector([edg.start.x, edg.start.y])
                self._edg_ed[i] = ti.Vector([edg.end.x, edg.end.y])
            elif self._body_list[i].shape == Shape.Type.Polygon:
                pass

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

        self._poly_st[0] = ti.Vector([ti.random(), ti.random()])
        self._poly_st[1] = self._poly_st[0] + 0.1
        self._poly_st[2] = ti.Vector(
            [self._poly_st[0].x, self._poly_st[0].y + 0.2])
        self._poly_st[3] = ti.Vector(
            [self._poly_st[0].x - 0.1, self._poly_st[0].y + 0.2])
        self._poly_st[4] = ti.Vector(
            [self._poly_st[0].x - 0.2, self._poly_st[0].y + 0.1])
        self._poly_st[5] = ti.Vector(
            [self._poly_st[0].x - 0.1, self._poly_st[0].y])

        self._poly_ed[0] = self._poly_st[0] + 0.1
        self._poly_ed[1] = ti.Vector(
            [self._poly_st[0].x, self._poly_st[0].y + 0.2])
        self._poly_ed[2] = ti.Vector(
            [self._poly_st[0].x - 0.1, self._poly_st[0].y + 0.2])
        self._poly_ed[3] = ti.Vector(
            [self._poly_st[0].x - 0.2, self._poly_st[0].y + 0.1])
        self._poly_ed[4] = ti.Vector(
            [self._poly_st[0].x - 0.1, self._poly_st[0].y])
        self._poly_ed[5] = ti.Vector([self._poly_st[0].x, self._poly_st[0].y])

        for i in range(4):
            self._polytri_a[i] = self._poly_st[0]
            self._polytri_b[i] = self._poly_ed[i]
            self._polytri_c[i] = self._poly_ed[i + 1]

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

    def clear_all_bodies(self) -> None:
        self._body_list.clear()

    def clear_all_joints(self) -> None:
        self._joint_list.clear()
