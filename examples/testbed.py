from typing import List

import sys
import taichi as ti

# add the TaichiGAME lib to the path
# below code is only needed in dev condition
sys.path.append('../')

from TaichiGAME.scene import Scene
from TaichiGAME.math.matrix import Matrix
from TaichiGAME.dynamics.body import Body
from TaichiGAME.common.config import Config
import TaichiGAME.geometry.shape as sp

ti.init(arch=ti.cpu)

scene = Scene()

data: List[Matrix] = [
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
poly.vertices = data

grd: Body = scene._world.create_body()
grd.shape = edg
grd.pos = Matrix([0.0, 0.0], 'vec')
grd.mass = Config.Max
grd.type = Body.Type.Static
grd.fric = 0.7
grd.restit = 1.0
scene._dbvt.insert(grd)

# bd1: Body = scene._world.create_body()
# bd1.shape = cir
# bd1.pos = Matrix([4.0, 3.0], 'vec')
# bd1.mass = 1
# bd1.type = Body.Type.Dynamic
# bd1.fric = 0.4
# bd1.restit = 0.0
# scene._dbvt.insert(bd1)

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

scene.show()
