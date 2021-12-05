from typing import List, Dict, Optional, Tuple

import numpy as np

from ...math.matrix import Matrix
from ..body import Body
from .joint import Joint, JointType


class PulleyJointPrimitive():
    def __init__(self):
        pass


class PulleyJoint(Joint):
    def __init__(self, prim: PulleyJointPrimitive = PulleyJointPrimitive()):
        self._type: JointType = JointType.Pulley
        self._prim: PulleyJointPrimitive = prim

    def set_value(self, prim: PulleyJointPrimitive):
        self._prim = prim

    def prepare(self, dt: float):
        pass

    def solve_velocity(self, dt: float):
        pass

    def solve_position(self, dt: float):
        pass