from __future__ import annotations
from typing import Union

import taichi as ti

from TaichiGAME.dynamics.phy_world import PhysicsWorld
from TaichiGAME.math.matrix import Matrix

try:
    from taichi.ui.gui import GUI  # for taichi >= 0.8.7
except ImportError:
    print('taichi < 0.8.7 import gui \'from taichi.misc._gui\'')
    print('so feel free for this import error')
    from taichi.misc._gui import GUI

import numpy as np

from .common.camera import Camera


class Scene():
    def __init__(self):
        self._gui: GUI = GUI('TaichiGAME')
        # the physics world, all sim is run in physics world
        self._world: PhysicsWorld = PhysicsWorld()
        # the view camera, all viewport scale is in camera
        self._cam: Camera = Camera()

        self._world.grav = Matrix([0.0, -9.8], 'vec')
        self._world._linear_vel_damping = 0.1
        self._world.air_fric_coeff = 0.8
        self._world.ang_vel_damping = 0.1
        self._world.damping_ena = True
        self._world.pos_iter = 8
        self._world.vel_iter = 6

        # the right-mouse btn drag move flag(change viewport)
        self._mouse_viewport_move: bool = False

        self.radius = self._gui.slider('Radius', 1, 50, step=1)
        self.xcoor = self._gui.label('X-coordinate')
        self.okay = self._gui.button('OK')
        self.xcoor.value = 0.5
        self.radius.value = 10

    def physics_sim(self) -> None:
        pass

    def render(self) -> None:
        # self._gui.circle([0.5, 0.5], radius=4)
        self._gui.rect([0.1, 0.3], [0.3, 0.1], radius=3, color=0x00FF00)
        self._gui.triangle([0.1, 0.3], [0.1, 0.1], [0.3, 0.1], color=0x008000)
        self._gui.triangle([0.1, 0.3], [0.3, 0.1], [0.3, 0.3], color=0x008000)

        # draw the polygon
        hex_st = np.array([[0.4, 0.4], [0.5, 0.4], [0.6, 0.5], [0.6, 0.6],
                           [0.5, 0.7], [0.4, 0.7], [0.3, 0.6], [0.3, 0.5]])
        hex_ed = np.array([[0.5, 0.4], [0.6, 0.5], [0.6, 0.6], [0.5, 0.7],
                           [0.4, 0.7], [0.3, 0.6], [0.3, 0.5], [0.4, 0.4]])
        self._gui.lines(hex_st, hex_ed, radius=2, color=0x00FF00)

        hex_tri_a = np.array([[0.4, 0.4], [0.4, 0.4], [0.4, 0.4], [0.4, 0.4],
                              [0.4, 0.4], [0.4, 0.4]])
        hex_tri_b = np.array([[0.5, 0.4], [0.6, 0.5], [0.6, 0.6], [0.5, 0.7],
                              [0.4, 0.7], [0.3, 0.6]])
        hex_tri_c = np.array([[0.6, 0.5], [0.6, 0.6], [0.5, 0.7], [0.4, 0.7],
                              [0.3, 0.6], [0.3, 0.5]])
        self._gui.triangles(hex_tri_a, hex_tri_b, hex_tri_c, color=0x008000)

    def handle_left_mouse_event(self, state: Union[GUI.PRESS, GUI.RELEASE],
                                x: float, y: float) -> None:

        if state == GUI.PRESS:
            assert x == 0.5
            assert y == 0.5
        else:
            assert x == 0.5
            assert y == 0.5

    def handle_right_mouse_event(self, state: Union[GUI.PRESS,
                                                    GUI.RELEASE]) -> None:
        if state == GUI.PRESS:
            self._mouse_viewport_move = True
        else:
            self._mouse_viewport_move = False

    def handle_mouse_move_event(self, state: Union[GUI.PRESS, GUI.RELEASE],
                                x: float, y: float) -> None:

        if self._mouse_viewport_move:
            print('press right key+move')
        else:
            pass

    def handle_wheel_event(self, y: float) -> None:
        # NOTE: need to set the sef._cam  the value scale
        # zoom in
        if y > 0:
            print('zoom in')
        else:
            print('zoom out')

    def show(self) -> None:
        while self._gui.running:
            self.physics_sim()
            self.render()

            for e in self._gui.get_events():
                if e.key == ti.GUI.ESCAPE:
                    exit()

                elif e.key == ti.GUI.LMB:
                    self.handle_left_mouse_event(e.type, e.pos[0], e.pos[1])

                elif e.key == ti.GUI.RMB:
                    self.handle_right_mouse_event(e.type)

                elif e.key == ti.GUI.MOVE:
                    self.handle_mouse_move_event(e.type, e.pos[0], e.pos[1])

                elif e.key == ti.GUI.WHEEL:
                    self.handle_wheel_event(e.delta[1])

                elif e.key == ti.GUI.UP:
                    print("press up key")

                elif e.key == ti.GUI.DOWN:
                    print("press down key start")

                elif e.key == ti.GUI.LEFT:
                    print("press LEFT key restart")

                elif e.key == ti.GUI.RIGHT:
                    print("press right key")
                elif e.key == 'a':
                    self.xcoor.value -= 0.05
                elif e.key == 'd':
                    self.xcoor.value += 0.05
                elif e.key == 's':
                    self.radius.value -= 1
                elif e.key == 'w':
                    self.radius.value += 1
                elif e.key == self.okay:
                    print('OK clicked')

            self._gui.circle((self.xcoor.value, 0.5), radius=self.radius.value)
            self._gui.show()
