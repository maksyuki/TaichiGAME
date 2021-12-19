from typing import List
import sys

import numpy as np
import taichi as ti

# add the TaichiGAME lib to the path
# below code is only needed in dev condition
sys.path.append('../')

from TaichiGAME.scene import Scene
from TaichiGAME.frame import Frame
from TaichiGAME.math.matrix import Matrix
from TaichiGAME.dynamics.body import Body
from TaichiGAME.common.config import Config
from TaichiGAME.render.render import Render
from TaichiGAME.collision.broad_phase.aabb import AABB
import TaichiGAME.geometry.shape as sp

ti.init(arch=ti.cpu)

scene = Scene()


class FrameBroadPhaseDetect(Frame):
    def load(self) -> None:
        tri_data: List[Matrix] = [
            Matrix([-1.0, 1.0], 'vec'),
            Matrix([0.0, -2.0], 'vec'),
            Matrix([1.0, -1.0], 'vec'),
            Matrix([-1.0, 1.0], 'vec'),
        ]

        poly_data: List[Matrix] = [
            Matrix([0.0, 4.0], 'vec'),
            Matrix([-3.0, 3.0], 'vec'),
            Matrix([-4.0, 0.0], 'vec'),
            Matrix([-3.0, -3.0], 'vec'),
            Matrix([0.0, -4.0], 'vec'),
            Matrix([3.0, -3.0], 'vec'),
            Matrix([4.0, 0.0], 'vec'),
            Matrix([3.0, 3.0], 'vec'),
            Matrix([0.0, 4.0], 'vec')
        ]

        rect: sp.Rectangle = sp.Rectangle(0.5, 0.5)
        cir: sp.Circle = sp.Circle(0.5)
        cap: sp.Capsule = sp.Capsule(1.5, 0.5)
        tri: sp.Polygon = sp.Polygon()
        tri.vertices = tri_data
        poly: sp.Polygon = sp.Polygon()
        poly.vertices = poly_data

        tri.scale(0.5)
        poly.scale(0.1)

        rng: np.random._generator.Generator = np.random.default_rng(seed=6)

        bd: Body = Body()
        tmpx: float = 0.0
        tmpy: float = 0.0
        cnt: np.ndarray = np.array([])
        for i in range(101):
            bd = scene._world.create_body()
            tmpx = -10 + rng.random() * 20.0
            tmpy = -6 + rng.random() * 12.0
            bd.pos = Matrix([tmpx, tmpy], 'vec')

            cnt = rng.integers(low=0, high=5, size=1)
            if cnt[0] == 0:
                bd.shape = rect
            elif cnt[0] == 1:
                bd.shape = cir
            elif cnt[0] == 2:
                bd.shape = tri
            elif cnt[0] == 3:
                bd.shape = poly
            elif cnt[0] == 4:
                bd.shape = cap

            bd.rot = -np.pi + rng.random() * np.pi
            bd.mass = 1
            bd.type = Body.Type.Static
            scene._dbvt.insert(bd)

    def render(self) -> None:
        # render the query rectangle range
        Render.rd_rect(scene._gui,
                       scene._cam.world_to_screen(Matrix([-4.0, 4.0], 'vec')),
                       scene._cam.world_to_screen(Matrix([4.0, -4.0], 'vec')),
                       color=Config.QueryRectLineColor)

        query_region: AABB = AABB(8, 8)
        query_body_list: List[Body] = scene._dbvt.query(query_region)

        for bd in query_body_list:
            scene._cam.render_aabb(scene._gui, AABB.from_body(bd))


class FrameRaycast(Frame):
    def load(self) -> None:
        tri_data: List[Matrix] = [
            Matrix([-1.0, 1.0], 'vec'),
            Matrix([0.0, -2.0], 'vec'),
            Matrix([1.0, -1.0], 'vec'),
            Matrix([-1.0, 1.0], 'vec')
        ]

        poly_data: List[Matrix] = [
            Matrix([0.0, 4.0], 'vec'),
            Matrix([-3.0, 3.0], 'vec'),
            Matrix([-4.0, 0.0], 'vec'),
            Matrix([-3.0, -3.0], 'vec'),
            Matrix([0.0, -4.0], 'vec'),
            Matrix([3.0, -3.0], 'vec'),
            Matrix([4.0, 0.0], 'vec'),
            Matrix([3.0, 3.0], 'vec'),
            Matrix([0.0, 4.0], 'vec')
        ]

        rect: sp.Rectangle = sp.Rectangle(0.5, 0.5)
        cir: sp.Circle = sp.Circle(0.5)
        cap: sp.Capsule = sp.Capsule(1.5, 0.5)
        tri: sp.Polygon = sp.Polygon()
        tri.vertices = tri_data
        poly: sp.Polygon = sp.Polygon()
        poly.vertices = poly_data

        tri.scale(0.5)
        poly.scale(0.1)

        rng: np.random._generator.Generator = np.random.default_rng(seed=6)

        bd: Body = Body()
        tmpx: float = 0.0
        tmpy: float = 0.0
        cnt: np.ndarray = np.array([])
        for i in range(101):
            bd = scene._world.create_body()
            tmpx = -10 + rng.random() * 20.0
            tmpy = -6 + rng.random() * 12.0
            bd.pos = Matrix([tmpx, tmpy], 'vec')

            cnt = rng.integers(low=0, high=5, size=1)
            if cnt[0] == 0:
                bd.shape = rect
            elif cnt[0] == 1:
                bd.shape = cir
            elif cnt[0] == 2:
                bd.shape = tri
            elif cnt[0] == 3:
                bd.shape = poly
            elif cnt[0] == 4:
                bd.shape = cap

            bd.rot = -np.pi + rng.random() * np.pi
            bd.mass = 1
            bd.type = Body.Type.Static
            scene._dbvt.insert(bd)

    def render(self) -> None:
        st: Matrix = Matrix([0.0, 0.0], 'vec')
        dirn: Matrix = scene._mouse_pos.normal()

        Render.rd_line(scene._gui,
                       scene._cam.world_to_screen(st),
                       scene._cam.world_to_screen(dirn * 10.0),
                       color=0xFF0000)
        query_body_list: List[Body] = scene._dbvt.raycast(st, dirn)

        prim: sp.ShapePrimitive = sp.ShapePrimitive()
        for bd in query_body_list:
            prim._rot = bd.rot
            prim._xform = bd.pos
            prim._shape = bd.shape
            Render.rd_shape(scene._gui, prim, scene._cam.world_to_screen,
                            scene._cam.meter_to_pixel,
                            Config.QueryRaycasFillColor,
                            Config.QueryRaycasOutLineColor)


class FrameBitmask(Frame):
    def load(self) -> None:
        rect: sp.Rectangle = sp.Rectangle(1.0, 1.0)
        edg: sp.Edge = sp.Edge()
        edg.set_value(Matrix([-10.0, 0.0], 'vec'), Matrix([10.0, 0.0], 'vec'))

        mask: int = 0x01
        for i in range(3):
            grd: Body = scene._world.create_body()
            grd.shape = edg
            grd.pos = Matrix([0.0, -3.0 + i * 3.0], 'vec')
            grd.fric = 0.9
            grd.bitmask = mask
            grd.restit = 0
            grd.mass = Config.Max
            grd.type = Body.Type.Static
            mask <<= 1
            scene._dbvt.insert(grd)

        mask = 0x01
        for i in range(3):
            bd: Body = scene._world.create_body()
            bd.shape = rect
            bd.pos = Matrix([i * 3.0, 6.0], 'vec')
            bd.fric = 0.9
            bd.bitmask = mask
            bd.restit = 0.0
            bd.mass = 1
            bd.type = Body.Type.Dynamic
            mask <<= 1
            scene._dbvt.insert(bd)

    def render(self) -> None:
        pass


class FrameCollision(Frame):
    def load(self) -> None:
        edg: sp.Edge = sp.Edge()
        edg.set_value(Matrix([-10.0, 0.0], 'vec'), Matrix([10.0, 0.0], 'vec'))
        cap: sp.Capsule = sp.Capsule(2.0, 1.0)

        grd: Body = scene._world.create_body()
        grd.shape = edg
        grd.pos = Matrix([0.0, 0.0], 'vec')
        grd.mass = Config.Max
        grd.type = Body.Type.Static
        grd.fric = 0.7
        grd.restit = 1.0
        scene._dbvt.insert(grd)

        bd: Body = scene._world.create_body()
        bd.shape = cap
        bd.pos = Matrix([0.0, 6.0], 'vec')
        bd.rot = np.pi / 4
        bd.mass = 1
        bd.type = Body.Type.Dynamic
        bd.fric = 0.4
        bd.restit = 0.0
        scene._dbvt.insert(bd)

    def render(self) -> None:
        pass


# BUG: some restit will lead to some enormous bias
class FrameRestitution(Frame):
    def load(self) -> None:
        cir: sp.Circle = sp.Circle(1.0)
        edg: sp.Edge = sp.Edge()
        edg.set_value(Matrix([-100.0, 0.0], 'vec'), Matrix([100.0, 0.0],
                                                           'vec'))

        grd: Body = scene._world.create_body()
        grd.shape = edg
        grd.mass = Config.Max
        grd.restit = 1.0
        grd.fric = 0.9
        grd.pos = Matrix([0.0, 0.0], 'vec')
        grd.type = Body.Type.Static
        scene._dbvt.insert(grd)

        for i in range(10):
            bd: Body = scene._world.create_body()
            bd.shape = cir
            bd.mass = 10
            bd.fric = 0.1
            bd.restit = i / 10.0
            bd.pos = Matrix([i * 2.5 - 10.0, 10.0], 'vec')
            bd.type = Body.Type.Dynamic
            scene._dbvt.insert(bd)

    def render(self) -> None:
        pass


frame_broad_phase: FrameBroadPhaseDetect = FrameBroadPhaseDetect()
frame_raycast: FrameRaycast = FrameRaycast()
frame_bitmask: FrameBitmask = FrameBitmask()
frame_collision: FrameCollision = FrameCollision()
frame_restitution: FrameRestitution = FrameRestitution()

# frame_broad_phase.load()
# frame_raycast.load()
# frame_bitmask.load()
# frame_collision.load()
frame_restitution.load()
scene.show(frame_restitution.render)
