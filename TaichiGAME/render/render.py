from typing import List, Tuple

from ..math.matrix import Matrix
from ..geometry.shape import ShapePrimitive
from ..dynamics.joint.joint import Joint
from ..collision.broad_phase.aabb import AABB


class Render():
    @staticmethod
    def rd_point(gui, point: Matrix):
        pass

    @staticmethod
    def rd_points(gui, points: List[Matrix]):
        pass

    @staticmethod
    def rd_line(gui, p1: Matrix, p2: Matrix):
        pass

    @staticmethod
    def rd_lines(gui, lines: List[Tuple[Matrix, Matrix]]):
        pass

    @staticmethod
    def rd_shape(gui, prim: ShapePrimitive):
        pass

    @staticmethod
    def rd_aabb(gui, aabb: AABB):
        pass

    @staticmethod
    def rd_joint(gui, joint: Joint):
        pass