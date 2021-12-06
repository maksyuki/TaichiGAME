from taichi.misc.gui import GUI
import taichi as ti


class Scene():
    def __init__(self):
        self.gui: GUI = GUI('TaichiGAME')

    def show(self):
        while self.gui.running:
            self.gui.circle([0.5, 0.5], radius=4)
            for e in self.gui.get_events(ti.GUI.PRESS):
                if e.key == ti.GUI.ESCAPE:
                    exit()

                elif e.key == ti.GUI.UP:
                    print("press up key")

                elif e.key == ti.GUI.DOWN:
                    print("press down key start")

                elif e.key == ti.GUI.LEFT:
                    print("press LEFT key restart")

                elif e.key == ti.GUI.RIGHT:
                    print("press right key")

            self.gui.show()