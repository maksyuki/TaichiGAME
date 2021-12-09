from __future__ import annotations
from enum import IntEnum, unique
from typing import Optional, Type, TypeVar

import numpy as np

from ..common.config import Config
from ..math.matrix import Matrix
from ..geometry.shape import Capsule, Ellipse
from ..geometry.shape import Polygon, Sector, Shape, Circle


class Body():
    @unique
    class Type(IntEnum):
        Kinematic: int = 0
        Static: int = 1
        Dynamic: int = 2
        Bullet: int = 3

    class PhysicsAttribute():
        def __init__(self):
            self._pos: Matrix = Matrix([0.0, 0.0], 'vec')
            self._vel: Matrix = Matrix([0.0, 0.0], 'vec')
            self._rot: float = 0.0
            self._ang_vel: float = 0.0

        def step(self, dt: float) -> None:
            self._pos += self._vel * dt
            self._rot += self._ang_vel * dt

    U = TypeVar('U', bound=Shape)

    def __init__(self):
        self._id: int = 0
        self._bitmask: int = 1

        self._mass: float = 0.0
        self._inv_mass: float = 0.0
        self._inertia: float = 0.0
        self._inv_inertia: float = 0.0

        self._phy_attr = Body.PhysicsAttribute()
        self._forces: Matrix = Matrix([0.0, 0.0], 'vec')
        self._torques: float = 0.0

        self._shape: Optional[Type[Body.U]] = None
        self._type = Body.Type.Static

        self._sleep: bool = False
        self._fric: float = 0.2
        self._restit: float = 0.0

    @property
    def pos(self) -> Matrix:
        return self._phy_attr._pos

    @pos.setter
    def pos(self, pos: Matrix) -> None:
        self._phy_attr._pos = pos

    @property
    def vel(self) -> Matrix:
        return self._phy_attr._vel

    @vel.setter
    def vel(self, vel: Matrix) -> None:
        self._phy_attr._vel = vel

    @property
    def rot(self) -> float:
        return self._phy_attr._rot

    @rot.setter
    def rot(self, rot: float) -> None:
        self._phy_attr._rot = rot

    @property
    def ang_vel(self) -> float:
        return self._phy_attr._ang_vel

    @ang_vel.setter
    def ang_vel(self, ang_vel: float) -> None:
        self._phy_attr._ang_vel = ang_vel

    @property
    def forces(self) -> Matrix:
        return self._forces

    @forces.setter
    def forces(self, forces: Matrix) -> None:
        self._forces = forces

    @property
    def torques(self) -> float:
        return self._torques

    @torques.setter
    def torques(self, tor: float) -> None:
        self._torques = tor

    def clear_torque(self) -> None:
        self._torques = 0.0

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self.calc_inertia()

    # NOTE: need to achieve type hint
    @property
    def type(self):
        return self._type

    # NOTE: need to achieve type hint
    @type.setter
    def type(self, val):
        self._type = val

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass: float) -> None:
        self._mass = mass

        if np.isclose(mass, Config.Max):
            self._inv_mass = 0.0
        else:
            self._inv_mass = 0.0 if np.isclose(mass, 0) else 1.0 / mass

        self.calc_inertia()

    @property
    def inertia(self) -> float:
        return self._inertia

    # FIXME: if import AABB, will trigger loop import err
    # USE AABB.from_body static method
    # def aabb(self, factor: float = 1.0) -> AABB:
    #     prim: ShapePrimitive = ShapePrimitive()
    #     prim._xform = self._phy_attr._pos
    #     prim._rot = self._phy_attr._rot
    #     prim._shape = self._shape
    #     return AABB.from_prim(prim, factor)

    @property
    def fric(self) -> float:
        return self._fric

    @fric.setter
    def fric(self, fric: float) -> None:
        self._fric = fric

    @property
    def sleep(self) -> bool:
        return self._sleep

    @sleep.setter
    def sleep(self, sleep: bool) -> None:
        self._sleep = sleep

    @property
    def inv_mass(self) -> float:
        return self._inv_mass

    @property
    def inv_inertia(self) -> float:
        return self._inv_inertia

    @property
    def phy_attr(self) -> PhysicsAttribute:
        return self._phy_attr

    @phy_attr.setter
    def phy_attr(self, info: PhysicsAttribute):
        self._phy_attr = info

    def step_position(self, dt: float) -> None:
        self._phy_attr._pos += self._phy_attr._vel * dt
        self._phy_attr._rot += self._phy_attr._ang_vel * dt

    def apply_impulse(self, impulse: Matrix, r: Matrix) -> None:
        self._phy_attr._vel += impulse * self._inv_mass
        self._phy_attr._ang_vel += self._inv_inertia * r.cross(impulse)

    def to_local_point(self, point: Matrix) -> Matrix:
        return Matrix.rotate_mat(-self._phy_attr._rot) * (point -
                                                          self._phy_attr._pos)

    def to_world_point(self, point: Matrix) -> Matrix:
        return Matrix.rotate_mat(
            self._phy_attr._rot) * point + self._phy_attr._pos

    def to_actual_point(self, point: Matrix) -> Matrix:
        return Matrix.rotate_mat(self._phy_attr._rot) * point

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, val: int) -> None:
        self._id = val

    @property
    def bitmask(self) -> int:
        return self._bitmask

    @bitmask.setter
    def bitmask(self, bitmask: int):
        self._bitmask = bitmask

    @property
    def restit(self) -> float:
        return self._restit

    @restit.setter
    def restit(self, restit: float):
        self._restit = restit

    # NOTE: need to achieve type hint
    def calc_inertia(self):
        assert self._shape is not None
        shape_type = self._shape.type

        if shape_type == Shape.Type.Circle:
            cir: Circle = self._shape
            self._inertia = self._mass * cir.radius * cir.radius / 2.0

        elif shape_type == Shape.Type.Polygon:
            polygon: Polygon = self._shape
            center: Matrix = polygon.center()

            sum1: float = 0.0
            sum2: float = 0.0
            for i in range(len(polygon.vertices) - 1):
                n1: Matrix = polygon.vertices[i] - center
                n2: Matrix = polygon.vertices[i + 1] - center
                cross: float = np.fabs(n1.cross(n2))
                dot: float = n2.dot(n2) + n2.dot(n1) + n1.dot(n1)
                sum1 += cross * dot
                sum2 += cross

            self._inertia = self._mass * (1.0 / 6.0) * sum1 / sum2

        elif shape_type == Shape.Type.Ellipse:
            ellipse: Ellipse = self._shape
            a: float = ellipse.A()
            b: float = ellipse.B()
            self._inertia = self._mass * (a * a + b * b) * (1.0 / 5.0)

        elif shape_type == Shape.Type.Capsule:
            capsule: Capsule = self._shape
            r: float = 0.0
            h: float = 0.0
            mass_s: float = 0.0
            inertia_s: float = 0.0
            mass_c: float = 0.0
            inertia_c: float = 0.0
            volume: float = 0.0

            if capsule.width >= capsule.height:
                r = capsule.height / 2.0
                h = capsule.width - capsule.height

            else:
                r = capsule.width / 2.0
                h = capsule.height - capsule.width

            volume = np.pi * r * r + h * 2 * r
            rho: float = self._mass / volume
            mass_s = rho * np.pi * r * r
            mass_c = rho * h * 2.0 * r
            inertia_c = (1.0 / 12.0) * mass_c * (h * h + (2.0 * r) * (2.0 * r))
            inertia_s = mass_s * r * r * 0.5
            self._inertia = inertia_c + inertia_s + mass_s * (
                3.0 * r + 2.0 * h) * h / 8.0

        elif shape_type == Shape.Type.Sector:
            sector: Sector = self._shape
            self._inertia = self._mass * (
                sector.span - np.sin(sector.span)
            ) * sector.radius * sector.radius / 4.0 * sector.span

        if np.isclose(self._mass, Config.Max):
            self._inv_inertia = 0.0
        else:
            self._inv_inertia = 1.0 / self._inertia if not np.isclose(
                self._inertia, 0) else 0.0
