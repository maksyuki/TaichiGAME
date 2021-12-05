from enum import IntEnum, unique
from typing import List, Dict, Optional, Tuple

import numpy as np


@unique
class JointType(IntEnum):
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
        self._active: bool = True
        self._type: Optional[JointType] = None
        self._id: int = 0

    def prepare(self, dt: float):
        pass

    def solve_velocity(self, dt: float):
        pass

    def solve_position(self, dt: float):
        pass
    
    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool):
        self._active = active

    def type(self) -> JointType:
        return self._type

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @staticmethod
    def natural_frequency(freq: float) -> float:
        return 2 * np.pi * freq

    @staticmethod
    def spring_damping_cofficient(mass: float, natural_freq: float, damping_radio: float) -> float:
        return damping_radio * 2.0 * mass * natural_freq

    @staticmethod
    def spring_stiff(mass: float, natural_freq: float) -> float:
        return mass * natural_freq * natural_freq

    @staticmethod
    def constraint_impulse_mixing(dt: float, stiff: float, damping: float) -> float:
        cim: float = dt * (dt * stiff + damping)
        return 0.0 if np.isclose(cim, 0.0) else 1.0 / cim

    @staticmethod
    def error_reduction_parameter(dt: float, stiff: float, damping: float) -> float:
        erp: float = dt * stiff + damping
        return 0.0 if np.isclose(erp, 0.0) else stiff / erp
