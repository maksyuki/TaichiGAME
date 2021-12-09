from abc import ABC, abstractmethod
from enum import IntEnum, unique

import numpy as np


@unique
class JointType(IntEnum):
    BASE = -1
    Distance = 0
    Point = 1
    Rotation = 2
    Orientation = 3
    Pulley = 4
    Prismatic = 5
    Wheel = 6
    Revolute = 7


class Joint(ABC):
    def __init__(self):
        self._active: bool = True
        self._type: JointType = JointType.BASE
        self._id: int = 0

    @abstractmethod
    def prepare(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def solve_velocity(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def solve_position(self, dt: float) -> None:
        raise NotImplementedError

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        self._active = active

    def type(self) -> JointType:
        return self._type

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, val: int) -> None:
        self._id = val

    @staticmethod
    def natural_frequency(freq: float) -> float:
        return 2 * np.pi * freq

    @staticmethod
    def spring_damping_cofficient(mass: float, natural_freq: float,
                                  damping_radio: float) -> float:
        return damping_radio * 2.0 * mass * natural_freq

    @staticmethod
    def spring_stiff(mass: float, natural_freq: float) -> float:
        return mass * natural_freq * natural_freq

    @staticmethod
    def constraint_impulse_mixing(dt: float, stiff: float,
                                  damping: float) -> float:
        cim: float = dt * (dt * stiff + damping)
        return 0.0 if np.isclose(cim, 0.0) else 1.0 / cim

    @staticmethod
    def error_reduction_parameter(dt: float, stiff: float,
                                  damping: float) -> float:
        erp: float = dt * stiff + damping
        return 0.0 if np.isclose(erp, 0.0) else stiff / erp
