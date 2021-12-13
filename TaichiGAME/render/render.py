from typing import Callable, List, Optional, Tuple, cast
import numpy as np

import taichi as ti
try:
    from taichi.ui.gui import GUI
except ImportError:
    from taichi.misc.gui import GUI

from ..math.matrix import Matrix
from ..geometry.shape import Circle, Edge, Polygon, Shape, ShapePrimitive
from ..dynamics.joint.joint import Joint
from ..collision.broad_phase.aabb import AABB
from ..common.config import Config


class Render():
    @staticmethod
    def rd_point(gui: GUI,
                 point: Matrix,
                 color: int = ti.rgb_to_hex([1.0, 1.0, 1.0]),
                 radius: int = 2) -> None:
        assert gui is not None
        assert 0 <= point.x <= 1.0
        assert 0 <= point.y <= 1.0
        gui.circle([point.x, point.y], color, radius)

    @staticmethod
    def rd_points(gui: GUI,
                  points: List[Matrix],
                  color: int = ti.rgb_to_hex([1.0, 1.0, 1.0]),
                  radius: int = 2) -> None:
        assert gui is not None

        for p in points:
            Render.rd_point(gui, p, color, radius)

    @staticmethod
    def rd_line(gui: GUI,
                p1: Matrix,
                p2: Matrix,
                color: int = ti.rgb_to_hex([1.0, 1.0, 1.0]),
                radius: int = 1) -> None:
        assert gui is not None
        assert 0 <= p1.x <= 1.0
        assert 0 <= p1.y <= 1.0
        assert 0 <= p2.x <= 1.0
        assert 0 <= p2.y <= 1.0

        gui.line([p1.x, p1.y], [p2.x, p2.y], radius, color)

    @staticmethod
    def rd_lines(gui: GUI,
                 lines: List[Tuple[Matrix, Matrix]],
                 color: int = ti.rgb_to_hex([1.0, 1.0, 1.0]),
                 radius: int = 1) -> None:
        assert gui is not None

        for lin in lines:
            Render.rd_line(gui, lin[0], lin[1], radius, color)

    @staticmethod
    def rd_shape(
        gui: GUI,
        prim: ShapePrimitive,
        world_to_screen: Callable[[Matrix], Matrix],
        vp_width: float,
        vp_height,
        meter_to_pixel: float,
        color: int = ti.rgb_to_hex([1.0, 1.0, 1.0])
    ) -> None:
        assert gui is not None
        assert prim._shape is not None

        if prim._shape.type == Shape.Type.Polygon:
            # [trick] draw polygon by draw multi triangle
            poly: Polygon = cast(Polygon, prim._shape)
            assert len(poly.vertices) >= 3

            outer_line_st: Optional[np.ndarray] = None
            outer_line_ed: Optional[np.ndarray] = None
            fill_tri_pa: Optional[np.ndarray] = None
            fill_tri_pb: Optional[np.ndarray] = None
            fill_tri_pc: Optional[np.ndarray] = None

            is_first: bool = True

            # NOTE: the vertices can form a close shape,
            # so the first vertex and last vertex are same
            vert_len: int = len(poly.vertices)
            for i in range(vert_len - 1):
                wordpa: Matrix = Matrix.rotate_mat(
                    prim._rot) * poly.vertices[i] + prim._xform
                scrnpa: Matrix = world_to_screen(wordpa)
                scrnpa.x /= vp_width
                scrnpa.y /= vp_height

                wordpb: Matrix = Matrix.rotate_mat(
                    prim._rot) * poly.vertices[i + 1] + prim._xform
                scrnpb: Matrix = world_to_screen(wordpb)
                scrnpb.x /= vp_width
                scrnpb.y /= vp_height

                if is_first:
                    is_first = False
                    outer_line_st = np.array([[scrnpa.x, scrnpa.y]]) * 220.0
                    outer_line_ed = np.array([[scrnpb.x, scrnpb.y]]) * 220.0
                else:
                    tmpa = np.array([[scrnpa.x, scrnpa.y]]) * 220.0
                    tmpb = np.array([[scrnpb.x, scrnpb.y]]) * 220.0
                    outer_line_st = np.concatenate((outer_line_st, tmpa))
                    outer_line_ed = np.concatenate((outer_line_ed, tmpb))

            assert outer_line_st is not None
            assert outer_line_ed is not None

            fill_tri_pa = np.repeat(np.array([outer_line_st[0]]),
                                    vert_len - 3,
                                    axis=0)
            fill_tri_pb = outer_line_st[1:-1]
            fill_tri_pc = outer_line_st[2:]

            print('poly ver:')
            for v in poly.vertices:
                print(v)
            print('end')

            print(f'line_len: {len(outer_line_st)}')
            for v in outer_line_st:
                print(v)

            gui.lines(outer_line_st,
                      outer_line_ed,
                      radius=2,
                      color=Config.OuterLineColor)
            gui.triangles(fill_tri_pa,
                          fill_tri_pb,
                          fill_tri_pc,
                          color=Config.FillColor)

        elif prim._shape.type == Shape.Type.Ellipse:
            raise NotImplementedError

        elif prim._shape.type == Shape.Type.Circle:
            cir: Circle = cast(Circle, prim._shape)
            scrnp: Matrix = world_to_screen(prim._xform)
            gui.circle([scrnp.x, scrnp.y],
                       color,
                       radius=cir.radius * meter_to_pixel)

        elif prim._shape.type == Shape.Type.Curve:
            raise NotImplementedError

        elif prim._shape.type == Shape.Type.Edge:
            edg: Edge = cast(Edge, prim._shape)
            tmp1: Matrix = world_to_screen(edg.start + prim._xform)
            tmp2: Matrix = world_to_screen(edg.end + prim._xform)
            Render.rd_point(gui, tmp1, Config.AxisPointColor)
            Render.rd_point(gui, tmp2, Config.AxisPointColor)
            Render.rd_line(gui, tmp1, tmp2, Config.AxisLineColor)

            center: Matrix = edg.center()
            center += prim._xform
            Render.rd_line(gui, world_to_screen(center),
                           world_to_screen(center + edg.normal * 0.1),
                           Config.AxisLineColor)

        elif prim._shape.type == Shape.Type.Capsule:
            raise NotImplementedError

        elif prim._shape.type == Shape.Type.Sector:
            raise NotImplementedError

    @staticmethod
    def rd_aabb(gui: GUI, aabb: AABB) -> None:
        assert gui is not None
        assert 0 <= aabb.top_left.x <= 1.0
        assert 0 <= aabb.top_left.y <= 1.0
        assert 0 <= aabb.bot_right.x <= 1.0
        assert 0 <= aabb.bot_right.y <= 1.0

        gui.rect([aabb.top_left.x, aabb.top_left.y],
                 [aabb.bot_right.x, aabb.bot_right.y])

    @staticmethod
    def rd_joint(gui, joint: Joint) -> None:
        raise NotImplementedError
