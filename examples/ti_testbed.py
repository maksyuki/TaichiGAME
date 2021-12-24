import sys
import numpy as np
import taichi as ti

# add the TaichiGAME lib to the path
# below code is only needed in dev condition
sys.path.append('../')

import TaichiGAME as ng

from TaichiGAME.ti_scene import Scene

ti.init(arch=ti.gpu, excepthook=True)

scene = Scene('GPU Testbed')


class FrameBroadPhaseDetect(ng.Frame):
    def load(self) -> None:
        tri_data = [
            ng.Matrix([-1.0, 1.0], 'vec'),
            ng.Matrix([0.0, -2.0], 'vec'),
            ng.Matrix([1.0, -1.0], 'vec'),
            ng.Matrix([-1.0, 1.0], 'vec'),
        ]

        # poly_data: List[ng.Matrix] = [
        #     ng.Matrix([0.0, 4.0], 'vec'),
        #     ng.Matrix([-3.0, 3.0], 'vec'),
        #     ng.Matrix([-4.0, 0.0], 'vec'),
        #     ng.Matrix([-3.0, -3.0], 'vec'),
        #     ng.Matrix([0.0, -4.0], 'vec'),
        #     ng.Matrix([3.0, -3.0], 'vec'),
        #     ng.Matrix([4.0, 0.0], 'vec'),
        #     ng.Matrix([3.0, 3.0], 'vec'),
        #     ng.Matrix([0.0, 4.0], 'vec')
        # ]

        rect: ng.Rectangle = ng.Rectangle(0.5, 0.5)
        cir: ng.Circle = ng.Circle(0.5)
        cap: ng.Capsule = ng.Capsule(1.5, 0.5)
        tri: ng.Polygon = ng.Polygon()
        tri.vertices = tri_data
        # poly: ng.Polygon = ng.Polygon()
        # poly.vertices = poly_data

        tri.scale(0.5)
        # poly.scale(0.1)

        rng = np.random.default_rng(seed=6)

        bd = ng.Body()
        tmpx: float = 0.0
        tmpy: float = 0.0
        cnt = np.array([])
        for i in range(101):
            # bd = scene._world.create_body()
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
                # bd.shape = poly
                pass
            elif cnt[0] == 4:
                bd.shape = cap

            bd.rot = -np.pi + rng.random() * np.pi
            bd.mass = 1
            bd.type = ng.Body.Type.Static
            # scene._dbvt.insert(bd)

    def render(self) -> None:
        pass
        # render the query rectangle range
        # ng.Render.rd_rect(
        #     scene._gui,
        #     scene._cam.world_to_screen(ng.Matrix([-4.0, 4.0], 'vec')),
        #     scene._cam.world_to_screen(ng.Matrix([4.0, -4.0], 'vec')),
        #     color=ng.Config.QueryRectLineColor)

        # query_region = ng.AABB(8, 8)
        # query_body_list = scene._dbvt.query(query_region)

        # for bd in query_body_list:
        #     scene._cam.render_aabb(scene._gui, ng.AABB.from_body(bd))


scene.show()
