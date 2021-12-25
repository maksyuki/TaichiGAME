from typing import Optional, Union, List, cast

import taichi as ti

from ..dynamics.body import Body
from .joint.joint import Joint
from ..common.random import RandomGenerator
from ..geometry.shape import Capsule, Circle, Edge, Polygon, Shape


@ti.data_oriented
class PhysicsWorld():
    def __init__(self, body_len: int = 60):
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
        # 1: kinematic 2: static 3: dynamic
        self._phy_type = ti.field(int, shape=self._body_len)
        # 1: circle 2: Edge 3: triangle 4: rect 5: pentagon
        # 6: hexagon 7: capsule
        self._shape_type = ti.field(int, shape=self._body_len)
        # circle
        self._cirpos = ti.Vector.field(2, float, shape=self._body_len)
        self._scirpos = ti.Vector.field(2, float, shape=self._body_len)
        self._cir_rad = ti.field(float, shape=self._body_len)
        self._scir_rad = ti.field(float, shape=self._body_len)
        # edge
        self._edgpos = ti.Vector.field(2, float, shape=self._body_len)
        self._sedgpos = ti.Vector.field(2, float, shape=self._body_len)
        self._edg_st = ti.Vector.field(2, float, shape=self._body_len)
        self._edg_sst = ti.Vector.field(2, float, shape=self._body_len)
        self._edg_ed = ti.Vector.field(2, float, shape=self._body_len)
        self._edg_sed = ti.Vector.field(2, float, shape=self._body_len)

        # polygon triangle
        self._poly_tripos = ti.Vector.field(2, float, shape=self._body_len)
        self._poly_trist = ti.Vector.field(2, float, shape=(self._body_len, 3))
        self._poly_tried = ti.Vector.field(2, float, shape=(self._body_len, 3))
        self._poly_trisst = ti.Vector.field(2,
                                            float,
                                            shape=(self._body_len, 3))
        self._poly_trised = ti.Vector.field(2,
                                            float,
                                            shape=(self._body_len, 3))
        self._poly_tri_a = ti.Vector.field(2, float, shape=(self._body_len, 1))
        self._poly_tri_b = ti.Vector.field(2, float, shape=(self._body_len, 1))
        self._poly_tri_c = ti.Vector.field(2, float, shape=(self._body_len, 1))

        # polygon rect
        self._poly_recpos = ti.Vector.field(2, float, shape=self._body_len)
        self._poly_recst = ti.Vector.field(2, float, shape=(self._body_len, 4))
        self._poly_reced = ti.Vector.field(2, float, shape=(self._body_len, 4))
        self._poly_recsst = ti.Vector.field(2,
                                            float,
                                            shape=(self._body_len, 4))
        self._poly_recsed = ti.Vector.field(2,
                                            float,
                                            shape=(self._body_len, 4))

        self._poly_rec_a = ti.Vector.field(2, float, shape=(self._body_len, 2))
        self._poly_rec_b = ti.Vector.field(2, float, shape=(self._body_len, 2))
        self._poly_rec_c = ti.Vector.field(2, float, shape=(self._body_len, 2))

        # polygon pen
        self._poly_penpos = ti.Vector.field(2, float, shape=self._body_len)
        self._poly_penst = ti.Vector.field(2, float, shape=(self._body_len, 5))
        self._poly_pened = ti.Vector.field(2, float, shape=(self._body_len, 5))
        self._poly_pensst = ti.Vector.field(2,
                                            float,
                                            shape=(self._body_len, 5))
        self._poly_pensed = ti.Vector.field(2,
                                            float,
                                            shape=(self._body_len, 5))

        self._poly_pen_a = ti.Vector.field(2, float, shape=(self._body_len, 3))
        self._poly_pen_b = ti.Vector.field(2, float, shape=(self._body_len, 3))
        self._poly_pen_c = ti.Vector.field(2, float, shape=(self._body_len, 3))

        # capsule
        self._cap_pos = ti.Vector.field(2, float, shape=self._body_len)
        self._cap_width = ti.field(float, shape=self._body_len)
        self._cap_height = ti.field(float, shape=self._body_len)
        self._cap_c1 = ti.Vector.field(2, float, shape=self._body_len)
        self._cap_c2 = ti.Vector.field(2, float, shape=self._body_len)
        self._cap_p = ti.Vector.field(2, float, shape=(self._body_len, 4))
        self._cap_rec_a = ti.Vector.field(2, float, shape=(self._body_len, 2))
        self._cap_rec_b = ti.Vector.field(2, float, shape=(self._body_len, 2))
        self._cap_rec_c = ti.Vector.field(2, float, shape=(self._body_len, 2))

        self._vel = ti.Vector.field(2, float, shape=self._body_len)
        self._rot = ti.field(float, shape=self._body_len)
        self._ang_vel = ti.field(float, shape=self._body_len)
        self._force = ti.Vector.field(2, float, shape=self._body_len)
        self._torque = ti.field(float, shape=self._body_len)

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
            self._phy_type[i] = self._body_list[i].type + 1
            self._vel[i] = ti.Vector(
                [self._body_list[i].vel.x, self._body_list[i].vel.y])
            self._rot[i] = self._body_list[i].rot
            self._ang_vel[i] = self._body_list[i].ang_vel
            self._force[i] = ti.Vector(
                [self._body_list[i].forces.x, self._body_list[i].forces.y])
            self._torque[i] = self._body_list[i].torques

            pos = ti.Vector(
                [self._body_list[i].pos.x, self._body_list[i].pos.y])
            if self._body_list[i].shape.type == Shape.Type.Circle:
                cir: Circle = cast(Circle, self._body_list[i].shape)
                self._shape_type[i] = 1
                self._cirpos[i] = pos
                self._cir_rad[i] = cir.radius

            elif self._body_list[i].shape.type == Shape.Type.Edge:
                edg: Edge = cast(Edge, self._body_list[i].shape)
                self._shape_type[i] = 2
                self._edg_st[i] = ti.Vector([edg.start.x, edg.start.y])
                self._edg_ed[i] = ti.Vector([edg.end.x, edg.end.y])

            elif self._body_list[i].shape.type == Shape.Type.Polygon:
                poly: Polygon = cast(Polygon, self._body_list[i].shape)
                vert_len: int = len(poly.vertices)
                assert vert_len >= 4

                if vert_len == 4:
                    self._shape_type[i] = 3
                    self._poly_tripos[i] = pos
                    for j in range(3):
                        self._poly_trist[i, j] = ti.Vector(
                            [poly.vertices[j].x, poly.vertices[j].y])
                        self._poly_tried[i, j] = ti.Vector(
                            [poly.vertices[j + 1].x, poly.vertices[j + 1].y])

                elif vert_len == 5:
                    self._shape_type[i] = 4
                    self._poly_recpos[i] = pos
                    for j in range(4):
                        self._poly_recst[i, j] = ti.Vector(
                            [poly.vertices[j].x, poly.vertices[j].y])
                        self._poly_reced[i, j] = ti.Vector(
                            [poly.vertices[j + 1].x, poly.vertices[j + 1].y])

                elif vert_len == 6:
                    self._shape_type[i] = 5
                    self._poly_penpos[i] = pos
                    for j in range(5):
                        self._poly_penst[i, j] = ti.Vector(
                            [poly.vertices[j].x, poly.vertices[j].y])
                        self._poly_pened[i, j] = ti.Vector(
                            [poly.vertices[j + 1].x, poly.vertices[j + 1].y])

                elif vert_len == 7:
                    self._shape_type[i] = 6

            elif self._body_list[i].shape.type == Shape.Type.Capsule:
                self._shape_type[i] = 7
                self._cap_pos[i] = pos
                cap: Capsule = cast(Capsule, self._body_list[i].shape)
                self._cap_width[i] = cap.width
                self._cap_height[i] = cap.height

    @ti.kernel
    def step_velocity(self, dt: float):
        lvd = 1.0 / (1.0 + dt * self._linear_vel_damping)
        avd = 1.0 / (1.0 + dt * self._ang_vel_damping)
        g = self._grav

        for i in range(self._body_len):
            if self._phy_type[i] == -1:
                self._vel[i] = ti.Vector([0.0, 0.0])
                self._ang_vel[i] = 0.0

            elif self._phy_type[i] == 0:
                self._force[i] = self._force[i] + self._mass[i] * g
                self._vel[
                    i] = self._vel[i] + self._force[i] / self._mass[i] * dt
                self._ang_vel[i] = self._ang_vel[
                    i] + self._torque[i] / self._inertia[i] * dt

                self._vel[i] = self._vel[i] * lvd
                self._ang_vel[i] = self._ang_vel[i] * avd

            elif self._phy_type[i] == 1:
                self._vel[
                    i] = self._vel[i] + self._force[i] / self._mass[i] * dt
                self._ang_vel[i] = self._ang_vel[
                    i] + self._torque[i] / self._inertia[i] * dt

                self._vel[i] = self._vel[i] * lvd
                self._ang_vel[i] = self._ang_vel[i] * avd

    @ti.kernel
    def step_position(self, dt: float):
        for i in range(self._body_len):
            if self._phy_type[i] == 0:
                pass

            elif self._phy_type[i] == 1 or self._phy_type[i] == 3:
                # self._pos[i] = self._pos[i] + self._vel[i] * dt
                self._rot[i] = self._rot[i] + self._ang_vel[i] * dt
                self._force[i] = ti.Vector([0.0, 0.0])
                self._torque[i] = 0.0

    def clear_all_bodies(self) -> None:
        self._body_list.clear()

    def clear_all_joints(self) -> None:
        self._joint_list.clear()
