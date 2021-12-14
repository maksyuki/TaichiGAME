from typing import List

import sys
import taichi as ti

# add the TaichiGAME lib to the path
# below code is only needed in dev condition
sys.path.append('../')

from TaichiGAME.scene import Scene
from TaichiGAME.math.matrix import Matrix
from TaichiGAME.dynamics.body import Body
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
poly: sp.Polygon = sp.Polygon()
poly.vertices = data

grd: Body = scene._world.create_body()
grd.shape = edg
grd.pos = Matrix([0.0, 0.0], 'vec')
scene._dbvt.insert(grd)

bd: Body = scene._world.create_body()
bd.shape = poly
bd.pos = Matrix([0.0, 4.0], 'vec')
# bd.rot = 3.14 / 3

scene._dbvt.insert(bd)
scene.show()
