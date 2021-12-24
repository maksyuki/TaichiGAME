import sys
import taichi as ti

# add the TaichiGAME lib to the path
# below code is only needed in dev condition
sys.path.append('../')

from TaichiGAME.ti_scene import Scene

ti.init(arch=ti.gpu, excepthook=True)

scene = Scene('GPU Testbed')

scene.show()
