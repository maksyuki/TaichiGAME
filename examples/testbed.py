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


class BroadPhaseDetect(Frame):
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


def tb_collision():
    tri_data: List[Matrix] = [
        Matrix([4.0, 4.0], 'vec'),
        Matrix([3.0, 3.0], 'vec'),
        Matrix([3.0, 1.0], 'vec'),
        Matrix([4.0, 4.0], 'vec')
    ]

    poly_data: List[Matrix] = [
        Matrix([4.0, 4.0], 'vec'),
        Matrix([3.0, 3.0], 'vec'),
        Matrix([3.0, 1.0], 'vec'),
        Matrix([6.0, 2.0], 'vec'),
        Matrix([4.0, 4.0], 'vec')
    ]

    edg: sp.Edge = sp.Edge()
    edg.set_value(Matrix([-10.0, 0.0], 'vec'), Matrix([10.0, 0.0], 'vec'))

    cir: sp.Circle = sp.Circle(1)

    poly: sp.Polygon = sp.Polygon()
    poly.vertices = poly_data

    tri: sp.Polygon = sp.Polygon()
    tri.vertices = tri_data

    cap: sp.Capsule = sp.Capsule(3.5, 1.5)
    rec: sp.Rectangle = sp.Rectangle(4.0, 2.0)

    # set the body config
    grd: Body = scene._world.create_body()
    grd.shape = edg
    grd.pos = Matrix([0.0, 0.0], 'vec')
    grd.mass = Config.Max
    grd.type = Body.Type.Static
    grd.fric = 0.7
    grd.restit = 1.0
    scene._dbvt.insert(grd)

    bd1: Body = scene._world.create_body()
    bd1.shape = cir
    bd1.pos = Matrix([4.0, 3.0], 'vec')
    bd1.mass = 1
    bd1.type = Body.Type.Dynamic
    bd1.fric = 0.4
    bd1.restit = 0.0
    scene._dbvt.insert(bd1)

    bd2: Body = scene._world.create_body()
    bd2.shape = poly
    bd2.pos = Matrix([0.0, 4.0], 'vec')
    # bd2.rot = 3.14 / 3
    bd2.mass = 1
    # bd2.torques = 60
    bd2.type = Body.Type.Dynamic
    bd2.fric = 0.4
    bd2.restit = 0.0
    scene._dbvt.insert(bd2)

    bd3: Body = scene._world.create_body()
    bd3.shape = tri
    bd3.pos = Matrix([3.0, 4.0], 'vec')
    # bd3.rot = 3.14 / 3
    bd3.mass = 1
    # bd3.torques = 60
    bd3.type = Body.Type.Dynamic
    bd3.fric = 0.4
    bd3.restit = 0.0
    scene._dbvt.insert(bd3)

    bd4: Body = scene._world.create_body()
    bd4.shape = cap
    bd4.pos = Matrix([-3.0, 4.0], 'vec')
    # bd4.rot = 3.14 / 3
    bd4.mass = 1
    # bd4.torques = 60
    bd4.type = Body.Type.Dynamic
    bd4.fric = 0.4
    bd4.restit = 0.0
    scene._dbvt.insert(bd4)

    bd5: Body = scene._world.create_body()
    bd5.shape = rec
    bd5.pos = Matrix([-3.0, -2.0], 'vec')
    bd4.rot = 3.14 / 3
    bd5.mass = 1
    # bd4.torques = 60
    bd5.type = Body.Type.Dynamic
    bd5.fric = 0.4
    bd5.restit = 0.0
    scene._dbvt.insert(bd5)


broad_phase: BroadPhaseDetect = BroadPhaseDetect()
broad_phase.load()
scene.show(broad_phase.render)
