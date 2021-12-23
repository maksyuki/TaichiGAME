from typing import List
import sys

import numpy as np
import taichi as ti

# add the TaichiGAME lib to the path
# below code is only needed in dev condition
sys.path.append('../')

import TaichiGAME as ng

ti.init(arch=ti.cpu)

scene = ng.Scene('TaichiGAME testbed')


class FrameBroadPhaseDetect(ng.Frame):
    def load(self) -> None:
        tri_data: List[ng.Matrix] = [
            ng.Matrix([-1.0, 1.0], 'vec'),
            ng.Matrix([0.0, -2.0], 'vec'),
            ng.Matrix([1.0, -1.0], 'vec'),
            ng.Matrix([-1.0, 1.0], 'vec'),
        ]

        poly_data: List[ng.Matrix] = [
            ng.Matrix([0.0, 4.0], 'vec'),
            ng.Matrix([-3.0, 3.0], 'vec'),
            ng.Matrix([-4.0, 0.0], 'vec'),
            ng.Matrix([-3.0, -3.0], 'vec'),
            ng.Matrix([0.0, -4.0], 'vec'),
            ng.Matrix([3.0, -3.0], 'vec'),
            ng.Matrix([4.0, 0.0], 'vec'),
            ng.Matrix([3.0, 3.0], 'vec'),
            ng.Matrix([0.0, 4.0], 'vec')
        ]

        rect: ng.Rectangle = ng.Rectangle(0.5, 0.5)
        cir: ng.Circle = ng.Circle(0.5)
        cap: ng.Capsule = ng.Capsule(1.5, 0.5)
        tri: ng.Polygon = ng.Polygon()
        tri.vertices = tri_data
        poly: ng.Polygon = ng.Polygon()
        poly.vertices = poly_data

        tri.scale(0.5)
        poly.scale(0.1)

        rng: np.random._generator.Generator = np.random.default_rng(seed=6)

        bd: ng.Body = ng.Body()
        tmpx: float = 0.0
        tmpy: float = 0.0
        cnt: np.ndarray = np.array([])
        for i in range(101):
            bd = scene._world.create_body()
            tmpx = -10 + rng.random() * 20.0
            tmpy = -6 + rng.random() * 12.0
            bd.pos = ng.Matrix([tmpx, tmpy], 'vec')

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
            bd.type = ng.Body.Type.Static
            scene._dbvt.insert(bd)

    def render(self) -> None:
        # render the query rectangle range
        ng.Render.rd_rect(
            scene._gui,
            scene._cam.world_to_screen(ng.Matrix([-4.0, 4.0], 'vec')),
            scene._cam.world_to_screen(ng.Matrix([4.0, -4.0], 'vec')),
            color=ng.Config.QueryRectLineColor)

        query_region: ng.AABB = ng.AABB(8, 8)
        query_body_list: List[ng.Body] = scene._dbvt.query(query_region)

        for bd in query_body_list:
            scene._cam.render_aabb(scene._gui, ng.AABB.from_body(bd))


class FrameRaycast(ng.Frame):
    def load(self) -> None:
        tri_data: List[ng.Matrix] = [
            ng.Matrix([-1.0, 1.0], 'vec'),
            ng.Matrix([0.0, -2.0], 'vec'),
            ng.Matrix([1.0, -1.0], 'vec'),
            ng.Matrix([-1.0, 1.0], 'vec')
        ]

        poly_data: List[ng.Matrix] = [
            ng.Matrix([0.0, 4.0], 'vec'),
            ng.Matrix([-3.0, 3.0], 'vec'),
            ng.Matrix([-4.0, 0.0], 'vec'),
            ng.Matrix([-3.0, -3.0], 'vec'),
            ng.Matrix([0.0, -4.0], 'vec'),
            ng.Matrix([3.0, -3.0], 'vec'),
            ng.Matrix([4.0, 0.0], 'vec'),
            ng.Matrix([3.0, 3.0], 'vec'),
            ng.Matrix([0.0, 4.0], 'vec')
        ]

        rect: ng.Rectangle = ng.Rectangle(0.5, 0.5)
        cir: ng.Circle = ng.Circle(0.5)
        cap: ng.Capsule = ng.Capsule(1.5, 0.5)
        tri: ng.Polygon = ng.Polygon()
        tri.vertices = tri_data
        poly: ng.Polygon = ng.Polygon()
        poly.vertices = poly_data

        tri.scale(0.5)
        poly.scale(0.1)

        rng: np.random._generator.Generator = np.random.default_rng(seed=6)

        bd: ng.Body = ng.Body()
        tmpx: float = 0.0
        tmpy: float = 0.0
        cnt: np.ndarray = np.array([])
        for i in range(101):
            bd = scene._world.create_body()
            tmpx = -10 + rng.random() * 20.0
            tmpy = -6 + rng.random() * 12.0
            bd.pos = ng.Matrix([tmpx, tmpy], 'vec')

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
            bd.type = ng.Body.Type.Static
            scene._dbvt.insert(bd)

    def render(self) -> None:
        st: ng.Matrix = ng.Matrix([0.0, 0.0], 'vec')
        dirn: ng.Matrix = scene._mouse_pos.normal()

        ng.Render.rd_line(scene._gui,
                          scene._cam.world_to_screen(st),
                          scene._cam.world_to_screen(dirn * 10.0),
                          color=0xFF0000)
        query_body_list: List[ng.Body] = scene._dbvt.raycast(st, dirn)

        prim: ng.ShapePrimitive = ng.ShapePrimitive()
        for bd in query_body_list:
            prim._rot = bd.rot
            prim._xform = bd.pos
            prim._shape = bd.shape
            ng.Render.rd_shape(scene._gui, prim, scene._cam.world_to_screen,
                               scene._cam.meter_to_pixel,
                               ng.Config.QueryRaycasFillColor,
                               ng.Config.QueryRaycasOutLineColor)


class FrameBitmask(ng.Frame):
    def load(self) -> None:
        rect: ng.Rectangle = ng.Rectangle(1.0, 1.0)
        edg: ng.Edge = ng.Edge()
        edg.set_value(ng.Matrix([-10.0, 0.0], 'vec'),
                      ng.Matrix([10.0, 0.0], 'vec'))

        mask: int = 0x01
        for i in range(3):
            grd: ng.Body = scene._world.create_body()
            grd.shape = edg
            grd.pos = ng.Matrix([0.0, -3.0 + i * 3.0], 'vec')
            grd.fric = 0.9
            grd.bitmask = mask
            grd.restit = 0
            grd.mass = ng.Config.Max
            grd.type = ng.Body.Type.Static
            mask <<= 1
            scene._dbvt.insert(grd)

        mask = 0x01
        for i in range(3):
            bd: ng.Body = scene._world.create_body()
            bd.shape = rect
            bd.pos = ng.Matrix([i * 3.0, 6.0], 'vec')
            bd.fric = 0.9
            bd.bitmask = mask
            bd.restit = 0.0
            bd.mass = 1
            bd.type = ng.Body.Type.Dynamic
            mask <<= 1
            scene._dbvt.insert(bd)

    def render(self) -> None:
        pass


class FrameCollision(ng.Frame):
    def load(self) -> None:
        edg: ng.Edge = ng.Edge()
        edg.set_value(ng.Matrix([-10.0, 0.0], 'vec'),
                      ng.Matrix([10.0, 0.0], 'vec'))
        cap: ng.Capsule = ng.Capsule(2.0, 1.0)

        grd: ng.Body = scene._world.create_body()
        grd.shape = edg
        grd.pos = ng.Matrix([0.0, 0.0], 'vec')
        grd.mass = ng.Config.Max
        grd.type = ng.Body.Type.Static
        grd.fric = 0.7
        grd.restit = 1.0
        scene._dbvt.insert(grd)

        bd: ng.Body = scene._world.create_body()
        bd.shape = cap
        bd.pos = ng.Matrix([0.0, 6.0], 'vec')
        bd.rot = np.pi / 4
        bd.mass = 1
        bd.type = ng.Body.Type.Dynamic
        bd.fric = 0.4
        bd.restit = 0.0
        scene._dbvt.insert(bd)

    def render(self) -> None:
        pass


# BUG: some restit will lead to some enormous bias
class FrameRestitution(ng.Frame):
    def load(self) -> None:
        cir: ng.Circle = ng.Circle(1.0)
        edg: ng.Edge = ng.Edge()
        edg.set_value(ng.Matrix([-100.0, 0.0], 'vec'),
                      ng.Matrix([100.0, 0.0], 'vec'))

        grd: ng.Body = scene._world.create_body()
        grd.shape = edg
        grd.mass = ng.Config.Max
        grd.restit = 1.0
        grd.fric = 0.9
        grd.pos = ng.Matrix([0.0, 0.0], 'vec')
        grd.type = ng.Body.Type.Static
        scene._dbvt.insert(grd)

        for i in range(10):
            bd: ng.Body = scene._world.create_body()
            bd.shape = cir
            bd.mass = 10
            bd.fric = 0.1
            bd.restit = i / 10.0
            bd.pos = ng.Matrix([i * 2.5 - 10.0, 10.0], 'vec')
            bd.type = ng.Body.Type.Dynamic
            scene._dbvt.insert(bd)

    def render(self) -> None:
        pass


class FrameFriction(ng.Frame):
    def load(self) -> None:
        edg: ng.Edge = ng.Edge()
        edg.set_value(ng.Matrix([0.0, 0.0], 'vec'),
                      ng.Matrix([10.0, 0.0], 'vec'))
        ramp: ng.Edge = ng.Edge()
        ramp.set_value(ng.Matrix([-10.0, 4.0], 'vec'),
                       ng.Matrix([0.0, 0.0], 'vec'))
        rect: ng.Rectangle = ng.Rectangle(0.5, 0.5)

        for i in range(3):
            grd: ng.Body = scene._world.create_body()
            grd.shape = edg
            grd.fric = 0.1
            grd.mass = ng.Config.Max
            grd.pos = ng.Matrix([0, i * 3.0], 'vec')
            grd.restit = 0.0
            grd.type = ng.Body.Type.Static

            ram_grd: ng.Body = scene._world.create_body()
            ram_grd.shape = ramp
            ram_grd.fric = 0.1
            ram_grd.mass = ng.Config.Max
            ram_grd.pos = ng.Matrix([0, i * 3.0], 'vec')
            ram_grd.restit = 0.0
            ram_grd.type = ng.Body.Type.Static

            scene._dbvt.insert(grd)
            scene._dbvt.insert(ram_grd)

        for i in range(1, 4):
            cube: ng.Body = scene._world.create_body()
            cube.shape = rect
            cube.fric = i * 0.3
            cube.mass = 1
            cube.pos = ng.Matrix([-5.0, i * 3.5], 'vec')
            cube.restit = 0.0
            cube.type = ng.Body.Type.Dynamic
            scene._dbvt.insert(cube)

    def render(self) -> None:
        pass


class FrameStack(ng.Frame):
    def load(self) -> None:
        edg: ng.Edge = ng.Edge()
        edg.set_value(ng.Matrix([-100.0, 0.0], 'vec'),
                      ng.Matrix([100.0, 0.0], 'vec'))
        rect: ng.Rectangle = ng.Rectangle(1.0, 1.0)
        grd: ng.Body = scene._world.create_body()
        grd.shape = edg
        grd.pos = ng.Matrix([0.0, 0.0], 'vec')
        grd.mass = ng.Config.Max
        grd.type = ng.Body.Type.Static
        scene._dbvt.insert(grd)

        offset: float = 0.0
        max: int = 4
        for i in range(max):
            for j in range(max - i):
                bd: ng.Body = scene._world.create_body()
                bd.pos = ng.Matrix([-10.0 + j * 1.1 + offset, i * 1.8 + 2.0],
                                   'vec')
                bd.shape = rect
                bd.rot = 0.0
                bd.mass = 0.2
                bd.type = ng.Body.Type.Dynamic
                bd.fric = 0.8
                bd.restit = 0.0
                scene._dbvt.insert(bd)

            offset += 0.5

    def render(self) -> None:
        pass


# BUG: some impl error
class FrameBridge(ng.Frame):
    def load(self) -> None:
        brick: ng.Rectangle = ng.Rectangle(1.5, 0.5)
        edg: ng.Edge = ng.Edge()
        edg.set_value(ng.Matrix([-100.0, 0.0], 'vec'),
                      ng.Matrix([100.0, 0], 'vec'))

        rect: ng.Body = scene._world.create_body()
        rect.shape = brick
        rect.pos = ng.Matrix([-15.0, 0.0], 'vec')
        rect.rot = 0.0
        rect.mass = 1.0
        rect.restit = 0.2
        rect.fric = 0.01
        rect.type = ng.Body.Type.Dynamic

        grd: ng.Body = scene._world.create_body()
        grd.shape = edg
        grd.pos = ng.Matrix([0.0, -15.0], 'vec')
        grd.mass = ng.Config.Max
        grd.type = ng.Body.Type.Static
        scene._dbvt.insert(grd)

        ppm: ng.PointJointPrimitive = ng.PointJointPrimitive()
        revol: ng.RevoluteJointPrimitive = ng.RevoluteJointPrimitive()

        half: float = brick.width / 2.0
        ppm._bodya = rect
        ppm._local_pointa.set_value([-half, 0.0])
        ppm._target_point.set_value([-15.0 - half, 0.0])
        ppm._damping_radio = 0.1
        ppm._freq = 1000
        ppm._force_max = 10000
        scene._world.create_joint(ppm)

        cnt: int = 20
        scene._dbvt.insert(rect)

        for i in range(1, cnt):
            rect2: ng.Body = scene._world.create_body()
            rect2.shape = brick
            rect2.pos = ng.Matrix([-15.0 + i * brick.width * 1.2, 0.0], 'vec')
            rect2.rot = 0.0
            rect2.mass = 1.0
            rect2.fric = 0.01
            rect2.type = ng.Body.Type.Dynamic

            scene._dbvt.insert(rect2)
            revol._bodya = rect
            revol._bodyb = rect2
            revol._local_pointa.set_value([half + brick.width * 0.1, 0.0])
            revol._local_pointb.set_value([-half - brick.width * 0.1, 0.0])
            revol._damping_radio = 0.8
            revol._freq = 10.0
            revol._force_max = 10000
            scene._world.create_joint(revol)
            rect = rect2

        ppm._bodya = rect2
        ppm._local_pointa.set_value([0.75, 0.0])
        ppm._target_point.set_value(
            rect2.to_world_point(ng.Matrix([0.75, 0.0], 'vec')))
        ppm._damping_radio = 0.1
        ppm._freq = 1000.0
        ppm._force_max = 10000.0
        scene._world.create_joint(ppm)

    def render(self) -> None:
        pass


class FrameDomino(ng.Frame):
    def load(self) -> None:
        floor: ng.Rectangle = ng.Rectangle(15.0, 0.5)
        rect: ng.Rectangle = ng.Rectangle(0.5, 0.5)
        brick: ng.Rectangle = ng.Rectangle(0.3, 3.0)
        edg: ng.Edge = ng.Edge()
        edg.set_value(ng.Matrix([-100.0, 0.0], 'vec'),
                      ng.Matrix([100.0, 0.0], 'vec'))

        grd: ng.Body = scene._world.create_body()
        grd.shape = edg
        grd.type = ng.Body.Type.Static
        grd.mass = ng.Config.Max
        grd.pos = ng.Matrix([0.0, 0.0], 'vec')
        grd.fric = 0.1
        grd.restit = 0.0
        scene._dbvt.insert(grd)

        tile: ng.Body = scene._world.create_body()
        tile.shape = floor
        tile.type = ng.Body.Type.Static
        tile.mass = ng.Config.Max
        tile.fric = 0.1
        tile.restit = 0.0
        tile.rot = np.pi / 180 * 15
        tile.pos = ng.Matrix([4.0, 8.0], 'vec')
        scene._dbvt.insert(tile)

        tile = scene._world.create_body()
        tile.shape = floor
        tile.type = ng.Body.Type.Static
        tile.mass = ng.Config.Max
        tile.fric = 0.1
        tile.restit = 0.0
        tile.rot = np.pi / 180 * -15
        tile.pos = ng.Matrix([-4.0, 4.0], 'vec')
        scene._dbvt.insert(tile)

        tile = scene._world.create_body()
        tile.shape = floor
        tile.type = ng.Body.Type.Static
        tile.mass = ng.Config.Max
        tile.fric = 0.1
        tile.restit = 0.0
        tile.rot = 0.0
        tile.pos = ng.Matrix([-5.0, 10.0], 'vec')
        scene._dbvt.insert(tile)

        for i in range(9):
            card: ng.Body = scene._world.create_body()
            card.shape = brick
            card.mass = 10
            card.fric = 0.1
            card.restit = 0.0
            card.type = ng.Body.Type.Dynamic
            card.pos = ng.Matrix([-10.0 + i * 1.2, 12.0], 'vec')
            scene._dbvt.insert(card)

        pendulum: ng.Body = scene._world.create_body()
        pendulum.shape = rect
        pendulum.mass = 2.0
        pendulum.fric = 0.1
        pendulum.type = ng.Body.Type.Dynamic
        pendulum.pos = ng.Matrix([-16.0, 16.0], 'vec')
        scene._dbvt.insert(pendulum)

        djp: ng.DistanceJointPrimitive = ng.DistanceJointPrimitive()
        djp._bodya = pendulum
        djp._local_pointa.set_value([0.0, 0.0])
        djp._dist_min = 1.0
        djp._dist_max = 4.0
        djp._target_point.set_value([-12.0, 16.0])
        scene._world.create_joint(djp)

        # ojp: OrientationJointPrimitive = OrientationJointPrimitive()
        # ojp._target_point.set_value([-12.0, 16.0])
        # ojp._bodya = pendulum
        # ojp._ref_rot = 0.0
        # scene._world.create_joint(ojp)

    def render(self) -> None:
        pass


frame_broad_phase = FrameBroadPhaseDetect()
frame_raycast = FrameRaycast()
frame_bitmask = FrameBitmask()
frame_collision = FrameCollision()
frame_restitution = FrameRestitution()
frame_fricitoin = FrameFriction()
frame_stack = FrameStack()
frame_bridge = FrameBridge()
frame_domino = FrameDomino()

scene.register_frame(frame_broad_phase)
scene.register_frame(frame_raycast)
scene.register_frame(frame_bitmask)
scene.register_frame(frame_collision)
scene.register_frame(frame_restitution)
scene.register_frame(frame_fricitoin)
scene.register_frame(frame_stack)
scene.register_frame(frame_domino)
scene.init_frame()

scene.show()
