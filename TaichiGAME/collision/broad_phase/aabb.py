from __future__ import annotations
from typing import Optional, Tuple, cast

import numpy as np

from ...common.config import Config
from ...math.matrix import Matrix
from ...geometry.geom_algo import GeomAlgo2D
from ...geometry.shape import Circle, Edge, Ellipse
from ...geometry.shape import Polygon, Shape, ShapePrimitive
from ...dynamics.body import Body
from ..algorithm.gjk import GJK


class AABB():
    def __init__(self, width: float = 0.0, height: float = 0.0):
        self._pos: Matrix = Matrix([0.0, 0.0], 'vec')
        self._width: float = width
        self._height: float = height

    def __eq__(self, other) -> bool:
        return np.isclose(self._width, other._width) and np.isclose(
            self._height, other._height) and self._pos == other._pos

    @property
    def pos(self) -> Matrix:
        return self._pos

    @pos.setter
    def pos(self, pos: Matrix) -> None:
        self._pos = pos

    @property
    def top_left(self) -> Matrix:
        return Matrix([
            -self._width / 2.0 + self._pos.x, self._height / 2.0 + self._pos.y
        ], 'vec')

    @property
    def top_right(self) -> Matrix:
        return Matrix([
            self._width / 2.0 + self._pos.x, self._height / 2.0 + self._pos.y
        ], 'vec')

    @property
    def bot_left(self) -> Matrix:
        return Matrix([
            -self._width / 2.0 + self._pos.x, -self._height / 2.0 + self._pos.y
        ], 'vec')

    @property
    def bot_right(self) -> Matrix:
        return Matrix([
            self._width / 2.0 + self._pos.x, -self._height / 2.0 + self._pos.y
        ], 'vec')

    def collide(self, aabb) -> bool:
        '''check if two aabbs are overlapping

        Parameters
        ----------
        aabb : AABB
            other AABB

        Returns
        -------
        bool
            True: collide, otherwise not
        '''
        return AABB._collide(self, aabb)

    def expand(self, factor: float) -> None:
        AABB._expand(self, factor)

    def scale(self, factor: float) -> None:
        self._width *= factor
        self._height *= factor

    def clear(self) -> None:
        self._pos.clear()
        self._width = 0.0
        self._height = 0.0

    def unite(self, aabb: AABB) -> AABB:
        '''return two AABB union result

        Parameters
        ----------
        aabb : AABB
            other AABB

        Returns
        -------
        AABB
            union AABB
        '''
        return AABB._unite(self, aabb)

    def surface_area(self) -> float:
        return (self._width + self._height) * 2.0

    def volume(self) -> float:
        return self._width * self._height

    def is_subset(self, aabb) -> bool:
        '''check if self is the subset of aabb

        Parameters
        ----------
        aabb : AABB
            ref AABB

        Returns
        -------
        bool
            True: is subset, otherwise not
        '''
        return AABB._is_subset(aabb, self)  # NOTE: the seq is important

    def is_empty(self) -> bool:
        return np.isclose(self._width, 0.0) and np.isclose(
            self._height, 0.0) and self._pos == Matrix([0.0, 0.0], 'vec')

    def raycast(self, start: Matrix, dirn: Matrix) -> bool:
        return AABB._raycast(self, start, dirn)

    @staticmethod
    def from_prim(prim: ShapePrimitive, factor: float = 0.0) -> AABB:
        res: AABB = AABB()
        assert prim._shape is not None

        if prim._shape.type == Shape.Type.Polygon:
            polygon: Polygon = cast(Polygon, prim._shape)
            x_max: float = Config.NegativeMin
            y_max: float = Config.NegativeMin
            x_min: float = Config.Max
            y_min: float = Config.Max
            for v in polygon.vertices:
                vertex: Matrix = Matrix.rotate_mat(prim._rot) * v

                if x_max < vertex.x:
                    x_max = vertex.x

                if x_min > vertex.x:
                    x_min = vertex.x

                if y_max < vertex.y:
                    y_max = vertex.y

                if y_min > vertex.y:
                    y_min = vertex.y

            res._width = np.fabs(x_max - x_min)
            res._height = np.fabs(y_max - y_min)
            res._pos.set_value([(x_max + x_min) / 2.0, (y_max + y_min) / 2.0])

        elif prim._shape.type == Shape.Type.Ellipse:
            ellipse: Ellipse = cast(Ellipse, prim._shape)

            top_dir: Matrix = Matrix([0.0, 1.0], 'vec')
            left_dir: Matrix = Matrix([-1.0, 0.0], 'vec')
            bot_dir: Matrix = Matrix([0.0, -1.0], 'vec')
            right_dir: Matrix = Matrix([1.0, 0.0], 'vec')

            top_dir = Matrix.rotate_mat(-prim._rot) * top_dir
            left_dir = Matrix.rotate_mat(-prim._rot) * left_dir
            bot_dir = Matrix.rotate_mat(-prim._rot) * bot_dir
            right_dir = Matrix.rotate_mat(-prim._rot) * right_dir

            top: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), top_dir)
            left: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), left_dir)
            bot: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), bot_dir)
            right: Matrix = GeomAlgo2D.calc_ellipse_project_on_point(
                ellipse.A(), ellipse.B(), right_dir)

            top = Matrix.rotate_mat(prim._rot) * top
            left = Matrix.rotate_mat(prim._rot) * left
            bot = Matrix.rotate_mat(prim._rot) * bot
            right = Matrix.rotate_mat(prim._rot) * right

            res._height = np.fabs(top.y - bot.y)
            res._width = np.fabs(right.x - left.x)

        elif prim._shape.type == Shape.Type.Circle:
            cir: Circle = cast(Circle, prim._shape)
            res._width = cir.radius * 2.0
            res._height = cir.radius * 2.0

        elif prim._shape.type == Shape.Type.Edge:
            edg: Edge = cast(Edge, prim._shape)
            res._width = np.fabs(edg.start.x - edg.end.x)
            res._height = np.fabs(edg.start.y - edg.end.y)
            res._pos.set_value(
                [edg.start.x + edg.end.x, edg.start.y + edg.end.y])
            res._pos *= 0.5

        elif prim._shape.type == Shape.Type.Curve:
            pass
        elif prim._shape.type == Shape.Type.Point:
            res._width = 1.0
            res._height = 1.0

        elif prim._shape.type == Shape.Type.Capsule:
            p1: Matrix = GJK.find_farthest_point(prim, Matrix([1.0, 0.0],
                                                              'vec'))
            p2: Matrix = GJK.find_farthest_point(prim, Matrix([0.0, 1.0],
                                                              'vec'))

            p1 -= prim._xform
            p2 -= prim._xform
            res._width = p1.x * 2.0
            res._height = p2.y * 2.0
        elif prim._shape.type == Shape.Type.Sector:
            pass

        res._pos += prim._xform
        res.expand(factor)
        return res

    @staticmethod
    def from_body(body: Body, factor: float = 0.0) -> AABB:
        assert body is not None
        assert body.shape is not None

        prim: ShapePrimitive = ShapePrimitive()
        prim._shape = body.shape
        prim._rot = body.rot
        prim._xform = body.pos

        return AABB.from_prim(prim, factor)

    @staticmethod
    def from_box(top_left: Matrix, bot_right: Matrix) -> AABB:
        res: AABB = AABB()
        res._width = bot_right.x - top_left.x
        res._height = top_left.y - bot_right.y
        res._pos = (top_left + bot_right) / 2.0
        return res

    @staticmethod
    def _collide(src: AABB, target: AABB) -> bool:
        '''check if two aabbs are overlapping

        Parameters
        ----------
        src : AABB
            src AABB
        target : AABB
            target AABB

        Returns
        -------
        bool
            True: collide, otherwise not
        '''
        src_top_left: Matrix = src.top_left
        src_bot_right: Matrix = src.bot_right
        tgt_top_left: Matrix = target.top_left
        tgt_bot_right: Matrix = target.bot_right

        return not (src_bot_right.x < tgt_top_left.x
                    or tgt_bot_right.x < src_top_left.x
                    or src_top_left.y < tgt_bot_right.y
                    or tgt_top_left.y < src_bot_right.y)

    @staticmethod
    def _unite(src: AABB, target: AABB, factor: float = 0.0) -> AABB:
        '''return two AABB union result

        Parameters
        ----------
        src : AABB
            source AABB
        target : AABB
            target AABB
        factor : float
            expand factor

        Returns
        -------
        AABB
            union AABB
        '''

        if src.is_empty():
            return target
        elif target.is_empty():
            return src

        src_top_left: Matrix = src.top_left
        src_bot_right: Matrix = src.bot_right
        tgt_top_left: Matrix = target.top_left
        tgt_bot_right: Matrix = target.bot_right

        x_min: float = np.fmin(src_top_left.x, tgt_top_left.x)
        x_max: float = np.fmax(src_bot_right.x, tgt_bot_right.x)
        y_min: float = np.fmin(src_bot_right.y, tgt_bot_right.y)
        y_max: float = np.fmax(src_top_left.y, tgt_top_left.y)

        res: AABB = AABB()
        res._pos.set_value([(x_min + x_max) / 2.0, (y_min + y_max) / 2.0])
        res._width = x_max - x_min
        res._height = y_max - y_min
        res.expand(factor)

        return res

    @staticmethod
    def _is_subset(src: AABB, target: AABB) -> bool:
        '''check if target is the subset of src

        Parameters
        ----------
        src : AABB
            ref AABB
        target : AABB
            dut AABB

        Returns
        -------
        bool
            True: is subset, otherwise not
        '''
        src_top_left: Matrix = src.top_left
        src_bot_right: Matrix = src.bot_right
        tgt_top_left: Matrix = target.top_left
        tgt_bot_right: Matrix = target.bot_right

        x_ck1: bool = src_bot_right.x >= tgt_bot_right.x
        x_ck2: bool = tgt_top_left.x >= src_top_left.x
        y_ck1: bool = src_top_left.y >= tgt_top_left.y
        y_ck2: bool = tgt_bot_right.y >= src_bot_right.y
        return x_ck1 and x_ck2 and y_ck1 and y_ck2

    @staticmethod
    def _expand(aabb: AABB, factor: float = 0.0) -> None:
        aabb._width += factor
        aabb._height += factor

    @staticmethod
    def _raycast(aabb: AABB, start: Matrix, dirn: Matrix) -> bool:
        res: Optional[Tuple[Matrix, Matrix]] = GeomAlgo2D.raycastAABB(
            start, dirn, aabb.top_left, aabb.bot_right)

        if res is None:
            return False

        p1, p2 = res[0], res[1]
        return GeomAlgo2D.is_point_on_AABB(
            p1, aabb.top_left, aabb.bot_right) and GeomAlgo2D.is_point_on_AABB(
                p2, aabb.top_left, aabb.bot_right)
