import sys
import taichi as ti

# add the TaichiGAME lib to the path
# below code is only needed in dev condition
sys.path.append('../')

from TaichiGAME.scene import Scene

ti.init(arch=ti.gpu)

scene = Scene()
scene.show()
