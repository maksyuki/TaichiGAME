from TaichiGAME.common.config import Config
from typing import List, Tuple

import numpy as np

from taichi.misc.gui import GUI

from ..math.matrix import Matrix
from ..geometry.shape import Circle, Edge, Polygon, Shape, ShapePrimitive
from ..dynamics.joint.joint import Joint
from ..collision.broad_phase.aabb import AABB
from ..common.camera import Camera


class Render():
    @staticmethod
    def rd_point(gui: GUI, cam: Camera, point: Matrix):
        assert gui != None and cam != None

        view_width: float = cam.viewport.width
        view_height: float = cam.viewport.height

        scrnp: Matrix = cam.world_to_screen(point)
        gui.circle([scrnp.x / view_width, scrnp.y / view_height])

    @staticmethod
    def rd_points(gui: GUI, cam: Camera, points: List[Matrix]):
        assert gui != None and cam != None

        for p in points:
            Render.rd_point(gui, cam, p)

    @staticmethod
    def rd_line(gui: GUI, cam: Camera, p1: Matrix, p2: Matrix):
        assert gui != None and cam != None

        scrnp1: Matrix = cam.world_to_screen(p1)
        scrnp2: Matrix = cam.world_to_screen(p2)

        scrnp1.x /= cam.viewport.width
        scrnp1.y /= cam.viewport.height
        scrnp2.x /= cam.viewport.width
        scrnp2.y /= cam.viewport.height

        gui.line([scrnp1.x, scrnp1.y], [scrnp2.x, scrnp2.y])

    @staticmethod
    def rd_lines(gui: GUI, cam: Camera, lines: List[Tuple[Matrix, Matrix]]):
        assert gui != None and cam != None

        for lin in lines:
            Render.rd_line(gui, cam, lin[0], lin[1])

    @staticmethod
    def rd_shape(gui: GUI, cam: Camera, prim: ShapePrimitive):
        assert gui != None and cam != None

        if prim._shape.type() == Shape.Type.Polygon:
            #[trick] draw polygon by draw multi triangle
            poly: Polygon = prim._shape
            assert len(poly.vertices) >= 3

            outer_line_st: np.ndarray = None
            outer_line_ed: np.ndarray = None
            fill_tri_pa: np.ndarray = None
            fill_tri_pb: np.ndarray = None
            fill_tri_pc: np.ndarray = None

            is_first: bool = True

            # NOTE: the vertices can form a close shape,
            # so the first vertex and last vertex are same
            vert_len: int = len(poly.vertices)
            for i in range(vert_len - 1):
                wordpa: Matrix = Matrix.rotate_mat(
                    prim._rot) * poly.vertices[i] + prim._xform
                scrnpa: Matrix = cam.world_to_screen(wordpa)
                scrnpa.x /= cam.viewport.width
                scrnpa.y /= cam.viewport.height

                wordpb: Matrix = Matrix.rotate_mat(
                    prim._rot) * poly.vertices[i + 1] + prim._xform
                scrnpb: Matrix = cam.world_to_screen(wordpb)
                scrnpb.x /= cam.viewport.width
                scrnpb.y /= cam.viewport.height

                if is_first:
                    is_first = False
                    outer_line_st = np.array([[scrnpa.x, scrnpa.y]])
                    outer_line_st = np.array([[scrnpb.x, scrnpb.y]])
                else:
                    tmpa = np.array([[scrnpa.x, scrnpa.y]])
                    tmpb = np.array([[scrnpb.x, scrnpb.y]])
                    np.concatenate((outer_line_st, tmpa))
                    np.concatenate((outer_line_ed, tmpb))

            fill_tri_pa = np.repeat(np.array([outer_line_st[0]]),
                                    vert_len - 3,
                                    axis=0)
            fill_tri_pb = outer_line_st[1:-1]
            fill_tri_pc = outer_line_st[2:]

            gui.lines(outer_line_st,
                      outer_line_ed,
                      radius=2,
                      color=Config.OuterLineColor)
            gui.triangles(fill_tri_pa,
                          fill_tri_pb,
                          fill_tri_pc,
                          color=Config.FillColor)

        elif prim._shape.type() == Shape.Type.Ellipse:
            pass

        elif prim._shape.type() == Shape.Type.Circle:
            cir: Circle = prim._shape
            scrnp: Matrix = cam.world_to_screen(prim._xform)
            gui.circle([scrnp.x, scrnp.y],
                       radius=cir.radius * cam.meter_to_pixel)

        elif prim._shape.type() == Shape.Type.Curve:
            pass
        elif prim._shape.type() == Shape.Type.Edge:
            edg: Edge = prim._shape
            Render.rd_point(gui, cam, edg.start + prim._xform)
            Render.rd_point(gui, cam, edg.end + prim._xform)
            Render.rd_line(gui, cam, edg.start + prim._xform,
                           edg.end + prim._xform)

            center: Matrix = (edg.start + edg.end) / 2.0
            center += prim._xform
            Render.rd_line(gui, cam, center, center + 0.1 * edg.normal)

        elif prim._shape.type() == Shape.Type.Capsule:
            pass
        elif prim._shape.type() == Shape.Type.Sector:
            pass

    @staticmethod
    def rd_aabb(gui: GUI, cam: Camera, aabb: AABB):
        assert gui != None and cam != None

        top_left: Matrix = cam.world_to_screen(aabb.top_left)
        top_left.x /= cam.viewport.width
        top_left.y /= cam.viewport.height

        bot_right: Matrix = cam.world_to_screen(aabb.bot_right)
        bot_right.x /= cam.viewport.width
        bot_right.y /= cam.viewport.height

        gui.rect([top_left.x, top_left.y], [bot_right.x, bot_right.y])

    @staticmethod
    def rd_joint(gui, joint: Joint):
        pass