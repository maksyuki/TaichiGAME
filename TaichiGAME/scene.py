from taichi.misc.gui import GUI
import taichi as ti
import numpy as np

class Scene():
    def __init__(self):
        self.gui: GUI = GUI('TaichiGAME')

    def show(self):
        while self.gui.running:
            # self.gui.circle([0.5, 0.5], radius=4)
            self.gui.rect([0.1, 0.3], [0.3, 0.1], radius=3, color=0x00FF00)
            self.gui.triangle([0.1, 0.3], [0.1, 0.1], [0.3, 0.1], color=0x008000)
            self.gui.triangle([0.1, 0.3], [0.3, 0.1], [0.3, 0.3], color=0x008000)

            # draw the polygon
            hex_st = np.array([[0.4, 0.4], [0.5, 0.4], [0.6, 0.5], [0.6, 0.6], [0.5, 0.7], [0.4, 0.7], [0.3, 0.6], [0.3, 0.5]])
            hex_ed = np.array([[0.5, 0.4], [0.6, 0.5], [0.6, 0.6], [0.5, 0.7], [0.4, 0.7], [0.3, 0.6], [0.3, 0.5], [0.4, 0.4]])
            self.gui.lines(hex_st, hex_ed, radius=2, color=0x00FF00)

            hex_tri_a = np.array([[0.4, 0.4], [0.4, 0.4], [0.4, 0.4], [0.4, 0.4], [0.4, 0.4], [0.4, 0.4]])
            hex_tri_b = np.array([[0.5, 0.4], [0.6, 0.5], [0.6, 0.6], [0.5, 0.7], [0.4, 0.7], [0.3, 0.6]])
            hex_tri_c = np.array([[0.6, 0.5], [0.6, 0.6], [0.5, 0.7], [0.4, 0.7], [0.3, 0.6], [0.3, 0.5]])
            self.gui.triangles(hex_tri_a, hex_tri_b, hex_tri_c, color=0x008000)
            for e in self.gui.get_events():
                if e.key == ti.GUI.ESCAPE:
                    exit()

                elif e.key == ti.GUI.LMB:
                    print('click left mouse')
                    print('e.type: {0}'.format(e.type))

                elif e.key == ti.GUI.RMB:
                    print('click right mouse')

                elif e.key == ti.GUI.MOVE:
                    print('({0}, {1})'.format(e.pos[0], e.pos[1]))
                    pass

                elif e.key == ti.GUI.WHEEL:
                    print('wheel mouse')
                    print('e.delta: {0}, {1}'.format(e.delta[0], e.delta[1]))

                elif e.key == ti.GUI.UP:
                    print("press up key")

                elif e.key == ti.GUI.DOWN:
                    print("press down key start")

                elif e.key == ti.GUI.LEFT:
                    print("press LEFT key restart")

                elif e.key == ti.GUI.RIGHT:
                    print("press right key")

            self.gui.show()