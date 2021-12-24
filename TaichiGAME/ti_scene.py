import numpy as np
import taichi as ti

from .common.config import Config
from .common.ti_viewport import Viewport


@ti.data_oriented
class Scene():
    def __init__(self, name: str, width: int = 1280, height: int = 720):
        self._gui = ti.GUI(name,
                           res=(width, height),
                           background_color=Config.BackgroundColor)

        # viewport system
        self._viewport = Viewport(ti.Vector([0, height]), ti.Vector([width,
                                                                     0]))
        self._origin: ti.Vector = ti.Vector(
            [self._viewport.width / 2.0, self._viewport.height / 2.0])
        self._xform: ti.Vector = ti.Vector([0.0, 0.0])
        # zoom system
        self._meter_to_pixel: float = 33.0
        self._pixel_to_meter: float = 1 / self._meter_to_pixel
        self._target_meter_to_pixel: float = 53.0
        self._target_pixel_to_meter: float = 1 / self._target_meter_to_pixel
        self._restit: float = 2.0
        self._delta_time: float = 15.0
        # axis system
        self._axis_p_cnt: int = 10
        self._axis_p_list = ti.Vector.field(2,
                                            float,
                                            shape=4 * self._axis_p_cnt)
        self._axis_lin_st = ti.Vector.field(2, float, shape=2)
        self._axis_lin_ed = ti.Vector.field(2, float, shape=2)

    def render(self) -> None:
        self.smooth_scale()
        self.render_axis()

    @ti.func
    def world_to_screen(self, world, scale):
        origin = ti.Vector(
            [self._origin.x + self._xform.x, self._origin.y + self._xform.y])

        vw = self._viewport.width
        vh = self._viewport.height

        resx = (origin.x + world.x * scale) / vw
        resy = (origin.y + world.y * scale) / vh
        return ti.Vector([resx, resy])

    @ti.kernel
    def gen_axis_data(self, scale: float):
        tmp = ti.Vector([0.0, 0.0])
        for i in range(-self._axis_p_cnt, self._axis_p_cnt + 1):
            tmp = self.world_to_screen(ti.Vector([i * 1.0, 0.0]), scale)
            self._axis_p_list[(i + self._axis_p_cnt) * 2] = tmp

            tmp = self.world_to_screen(ti.Vector([0.0, i * 1.0]), scale)
            self._axis_p_list[(i + self._axis_p_cnt) * 2 + 1] = tmp

        self._axis_lin_st[0] = self._axis_p_list[0]
        self._axis_lin_st[1] = self._axis_p_list[1]
        self._axis_lin_ed[0] = self._axis_p_list[4 * self._axis_p_cnt - 2]
        self._axis_lin_ed[1] = self._axis_p_list[4 * self._axis_p_cnt - 1]

    def render_axis(self) -> None:
        self.gen_axis_data(self._meter_to_pixel)

        self._gui.circles(self._axis_p_list.to_numpy(),
                          radius=2,
                          color=Config.AxisPointColor)

        self._gui.lines(begin=self._axis_lin_st.to_numpy(),
                        end=self._axis_lin_ed.to_numpy(),
                        color=Config.AxisLineColor)

    def handle_wheel_evt(self, delta: float) -> None:
        if delta > 0:
            self.meter_to_pixel += self.meter_to_pixel / 4
        else:
            self.meter_to_pixel -= self.meter_to_pixel / 4

    def show(self):
        while self._gui.running:

            for e in self._gui.get_events():
                if e.key == ti.GUI.ESCAPE:
                    exit()

                elif e.key == ti.GUI.SPACE and e.type == ti.GUI.RELEASE:
                    pass

                elif e.key == ti.GUI.LMB:
                    pass

                elif e.key == ti.GUI.RMB:
                    pass

                elif e.key == ti.GUI.MOVE:
                    pass

                elif e.key == ti.GUI.WHEEL:
                    self.handle_wheel_evt(e.delta[1])
                    # print('meter to pixel: ', self.meter_to_pixel)

                elif e.key == ti.GUI.UP:
                    print("press up key")

                elif e.key == ti.GUI.DOWN:
                    pass

                elif e.key == ti.GUI.LEFT and e.type == ti.GUI.RELEASE:
                    pass

                elif e.key == ti.GUI.RIGHT and e.type == ti.GUI.RELEASE:
                    pass

            self.render()
            self._gui.show()

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

    def smooth_scale(self) -> None:
        # calc the 'meter to pixel' scale according
        # to the 'target meter to pixel' set from
        # the wheel event smooth animation
        inv_dt: float = 1.0 / self._delta_time
        scale: float = self._target_meter_to_pixel - self._meter_to_pixel
        if np.fabs(scale) < 0.1 or self._meter_to_pixel < 1.0:
            self._meter_to_pixel = self._target_meter_to_pixel
        else:
            self._meter_to_pixel -= (1.0 -
                                     ti.exp(self._restit * inv_dt)) * scale

        self._pixel_to_meter = 1.0 / self._meter_to_pixel
