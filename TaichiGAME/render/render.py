from typing import List, Tuple

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
            poly: Polygon = prim._shape
            assert len(poly.vertices) >= 3

            if len(poly.vertices) == 3:
                pass  # triangle
            elif len(poly.vertices) == 4:
                for p in poly.vertices:
                    wordp: Matrix = Matrix.rotate_mat(
                        prim._rot) * p + prim._xform
                    scrnp: Matrix = cam.world_to_screen(wordp)

            else:
                pass  #[trick] draw polygon by draw multi triangle

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