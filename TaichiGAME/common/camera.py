from __future__ import annotations
from typing import List, Optional

from TaichiGAME.geometry.shape import Circle, Edge, Polygon, ShapePrimitive

try:
    from taichi.ui.gui import GUI  # for taichi >= 0.8.7
except ImportError:
    print('taichi < 0.8.7 import gui \'from taichi.misc._gui\'')
    print('so feel free for this import error')
    from taichi.misc._gui import GUI

import numpy as np

from ..common.config import Config
from ..render.render import Render
from ..math.matrix import Matrix
from ..dynamics.phy_world import PhysicsWorld
from ..dynamics.body import Body
from ..dynamics.constraint.contact import ContactMaintainer
from ..collision.broad_phase.dbvh import DBVH


class Camera():
    class Viewport():
        '''the viewport of the render, the origin is bottom left of
        the screen
        '''
        def __init__(self,
                     top_left: Matrix = Matrix([0.0, 720.0], 'vec'),
                     bot_right: Matrix = Matrix([1280.0, 0.0], 'vec')):

            assert top_left.x < bot_right.x
            assert top_left.y > bot_right.y

            self._top_left: Matrix = top_left
            self._bot_right: Matrix = bot_right

        @property
        def width(self) -> float:
            return self._bot_right.x - self._top_left.x

        @width.setter
        def width(self, width: float) -> None:
            self._bot_right.x = self._top_left.x + width

        @property
        def height(self) -> float:
            return self._top_left.y - self._bot_right.y

        @height.setter
        def height(self, height: float) -> None:
            self._top_left.y = self._bot_right.y + height

        def set_value(self, width: float, height: float):
            self.width = width
            self.height = height

    def __init__(self):
        self._visible: bool = True
        self._aabb_visible: bool = False
        self._joint_visible: bool = False
        self._body_visible: bool = False
        self._axis_visible: bool = True
        self._dbvh_visible: bool = False
        self._tree_visible: bool = False
        self._grid_scale_line_visible: bool = False
        self._rotation_line_visible: bool = False
        self._center_visible: bool = False
        self._contact_visible: bool = False

        self._meter_to_pixel: float = 33.0
        self._pixel_to_meter: float = 1 / self._meter_to_pixel

        self._target_meter_to_pixel: float = 53.0  # 1920x1080[80] -> 1280x720[53]
        self._target_pixel_to_meter: float = 1 / self._target_meter_to_pixel

        self._transform: Matrix = Matrix([0.0, 0.0], 'vec')
        self._origin: Matrix = Matrix([0.0, 0.0], 'vec')
        self._viewport = Camera.Viewport()

        self._world: Optional[PhysicsWorld] = None
        self._target_body: Optional[Body] = None
        self._dbvh: Optional[DBVH] = None
        #  self._tree: Optional[Tree] = None
        self._maintainer: Optional[ContactMaintainer] = None

        self._zoom_factor: float = 1.0
        self._restit: float = 2.0
        self._delta_time: float = 15.0
        self._axis_point_count: int = 20

    # render factory method
    def render(self, gui: GUI) -> None:
        if self.visible:
            # assert self.world is not None

            # calc the 'meter to pixel' scale according
            # to the 'target meter to pixel' set from
            # the wheel event smooth animation
            inv_dt: float = 1.0 / self._delta_time
            scale: float = self._target_meter_to_pixel - self._meter_to_pixel
            if np.fabs(scale) < 0.1 or self._meter_to_pixel < 1.0:
                self._meter_to_pixel = self._target_meter_to_pixel
            else:
                self._meter_to_pixel -= (1.0 -
                                         np.exp(self._restit * inv_dt)) * scale

            if self.body_visible:
                self.render_body(gui)

            if self.joint_visible:
                self.render_joint(gui)

            if self.axis_visible:
                self.render_axis(gui)

            if self.aabb_visible:
                self.render_aabb(gui)

            if self.dbvh_visible:
                # self.render_dbvh(gui, self._)
                raise NotImplementedError

            if self.tree_visible:
                raise NotImplementedError

            if self.grid_scale_line_visible:
                self.render_grid_scale_line(gui)

            if self.contact_visible:
                self.render_contact(gui)

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool) -> None:
        self._visible = visible

    @property
    def aabb_visible(self) -> bool:
        return self._aabb_visible

    @aabb_visible.setter
    def aabb_visible(self, visible: bool) -> None:
        self._aabb_visible = visible

    @property
    def joint_visible(self) -> bool:
        return self._joint_visible

    @joint_visible.setter
    def joint_visible(self, visible: bool) -> None:
        self._joint_visible = visible

    @property
    def body_visible(self) -> bool:
        return self._body_visible

    @body_visible.setter
    def body_visible(self, visible: bool) -> None:
        self._body_visible = visible

    @property
    def axis_visible(self) -> bool:
        return self._axis_visible

    @axis_visible.setter
    def axis_visible(self, visible: bool) -> None:
        self._axis_visible = visible

    @property
    def dbvh_visible(self) -> bool:
        return self._dbvh_visible

    @dbvh_visible.setter
    def dbvh_visible(self, visible: bool) -> None:
        self._dbvh_visible = visible

    @property
    def tree_visible(self) -> bool:
        return self._tree_visible

    @tree_visible.setter
    def tree_visible(self, visible: bool) -> None:
        self._tree_visible = visible

    @property
    def grid_scale_line_visible(self) -> bool:
        return self._grid_scale_line_visible

    @grid_scale_line_visible.setter
    def grid_scale_line_visible(self, visible: bool) -> None:
        self._grid_scale_line_visible = visible

    @property
    def rot_line_visible(self) -> bool:
        return self._rotation_line_visible

    @rot_line_visible.setter
    def rot_line_visible(self, visible: bool) -> None:
        self._rotation_line_visible = visible

    @property
    def center_visible(self) -> bool:
        return self._center_visible

    @center_visible.setter
    def center_visible(self, visible: bool) -> None:
        self._center_visible = visible

    @property
    def contact_visible(self) -> bool:
        return self._contact_visible

    @contact_visible.setter
    def contact_visible(self, visible: bool) -> None:
        self._contact_visible = visible

    @property
    def meter_to_pixel(self) -> float:
        return self._meter_to_pixel

    @meter_to_pixel.setter
    def meter_to_pixel(self, val: float) -> None:
        # set the target 'meter_to_pixel' value
        # when in render,
        # clamp the scale value
        if val < 1.0:
            self._target_meter_to_pixel = 1.0
            self._target_pixel_to_meter = 1.0
            return

        self._target_meter_to_pixel = val
        self._target_pixel_to_meter = 1.0 / val

    @property
    def transform(self) -> Matrix:
        return self._transform

    @transform.setter
    def transform(self, trans: Matrix) -> None:
        self._transform = trans

    @property
    def world(self) -> PhysicsWorld:
        assert self._world is not None
        return self._world

    @world.setter
    def world(self, world: PhysicsWorld) -> None:
        self._world = world

    @property
    def target_body(self) -> Body:
        assert self._target_body is not None
        return self._target_body

    @target_body.setter
    def target_body(self, body: Body) -> None:
        self._target_body = body

    @property
    def zoom_factor(self) -> float:
        return self._zoom_factor

    @zoom_factor.setter
    def zoom_factor(self, factor: float) -> None:
        self._zoom_factor = factor

    @property
    def viewport(self) -> Viewport:
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: Viewport) -> None:
        self._viewport = viewport

        tmp: List[float] = []
        tmp.append(
            (self._viewport._top_left.x + self._viewport._bot_right.x) * 0.5)
        tmp.append(
            (self._viewport._top_left.y + self._viewport._bot_right.y) * 0.5)
        self._origin.set_value(tmp)

    def world_to_screen(self, pos: Matrix) -> Matrix:
        orign: Matrix = Matrix([
            self._origin.x + self._transform.x,
            self._origin.y + self._transform.y
        ], 'vec')

        # taichi axis system is radio-based
        view_width: float = self.viewport.width
        view_height: float = self.viewport.height

        tmpx: float = (orign.x + pos.x * self._meter_to_pixel) / view_width
        tmpx = Config.clamp(tmpx, 0.0, 1.0)
        tmpy: float = (orign.y + pos.y * self._meter_to_pixel) / view_height
        tmpy = Config.clamp(tmpy, 0.0, 1.0)
        return Matrix([tmpx, tmpy], 'vec')

    def screen_to_world(self, pos: Matrix) -> Matrix:
        orign: Matrix = Matrix([
            self._origin.x + self._transform.x,
            self._origin.y + self._transform.y
        ], 'vec')

        view_width: float = self.viewport.width
        view_height: float = self.viewport.height

        res: Matrix = Matrix([0.0, 0.0], 'vec')
        res.x = pos.x * view_width
        res.y = pos.y * view_height
        res -= orign
        res *= self._pixel_to_meter

        return res

    @property
    def dbvh(self) -> DBVH:
        assert self._dbvh is not None
        return self._dbvh

    @dbvh.setter
    def dbvh(self, dbvh: DBVH) -> None:
        self._dbvh = dbvh

    # @property
    # def tree(self) -> Tree:
    #     return self._tree

    # @tree.setter
    # def tree(self, tree: Tree):
    #     self._tree = tree

    @property
    def delta_time(self) -> float:
        return self._delta_time

    @delta_time.setter
    def delta_time(self, time: float) -> None:
        self._delta_time = time

    @property
    def maintainer(self) -> ContactMaintainer:
        assert self._maintainer is not None
        return self._maintainer

    @maintainer.setter
    def maintainer(self, maintainer: ContactMaintainer) -> None:
        self._maintainer = maintainer

    def render_body(self, gui: GUI) -> None:
        prim: ShapePrimitive = ShapePrimitive()
        cir: Circle = Circle(2)
        edg: Edge = Edge()
        edg.start = Matrix([-3.0, -1.0], 'vec')
        edg.end = Matrix([3.0, -1.0], 'vec')

        dataa: List[Matrix] = [
            Matrix([4.0, 4.0], 'vec'),
            Matrix([3.0, 3.0], 'vec'),
            Matrix([3.0, 1.0], 'vec'),
            Matrix([6.0, 2.0], 'vec'),
            Matrix([4.0, 4.0], 'vec')
        ]

        poly: Polygon = Polygon()
        poly.vertices = dataa
        # prim._shape = cir
        # prim._shape = poly
        prim._shape = edg
        prim._xform = Matrix([2.0, 2.0], 'vec')
        prim._rot = 0.0
        Render.rd_shape(gui, prim, self.world_to_screen, self.viewport.width,
                        self.viewport.height, self.meter_to_pixel,
                        Config.FillColor)

    def render_joint(self, gui: GUI) -> None:
        raise NotImplementedError

    def render_axis(self, gui: GUI) -> None:
        axis_points: List[Matrix] = []

        for i in range(-self._axis_point_count, self._axis_point_count + 1):
            tmp: Matrix = self.world_to_screen(Matrix([0.0, i * 1.0], 'vec'))
            axis_points.append(tmp)
            tmp = self.world_to_screen(Matrix([i * 1.0, 0.0], 'vec'))
            axis_points.append(tmp)

        Render.rd_points(gui, axis_points, Config.AxisPointColor)
        Render.rd_line(gui,
                       axis_points[0],
                       axis_points[-2],
                       color=Config.AxisLineColor)
        Render.rd_line(gui,
                       axis_points[1],
                       axis_points[-1],
                       color=Config.AxisLineColor)

    def render_aabb(self, gui: GUI) -> None:
        raise NotImplementedError

    def render_tree(self, gui: GUI, node_idx: int) -> None:
        raise NotImplementedError

    def render_contact(self, gui: GUI) -> None:
        raise NotImplementedError

    def render_grid_scale_line(self, gui: GUI) -> None:
        raise NotImplementedError

    def render_dbvh(self, gui: GUI, node: DBVH.Node) -> None:
        raise NotImplementedError
