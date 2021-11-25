import numpy as np

from .gjk import Simplex
from .gjk import Minkowski
from ...math.matrix import Matrix


class MPR():
    def __init__(self):
        pass

    @staticmethod
    def discover(self, shape_a, shape_b):
        simplex = Simplex()
        center_a = Matrix.rotate_mat(
            shape_a._rotation) * shape_a._shape.center()
        center_b = Matrix.rotate_mat(
            shape_b._rotation) * shape_b._shape.center()
        origin = shape_b._transform - shape_a._transform
        v0 = Minkowski(center_a + shape_a._transform,
                       center_b + shape_b._transform)
        direction = center_b - center_a + origin

        if np.isclose(direction.val[0], 0) and np.isclose(direction.val[1], 0):
            direction.set_value([1.0, 1.0])

        v1 = GJK.support(shape_a, shape_b, direction)
        direction = GJK.calc_direction_by_edge(v0._result, v1._result, True)
        v2 = GJK.support(shape_a, shape_b, direction)
        simplex._vertices.append(v0)
        simplex._vertices.append(v1)
        simplex._vertices.append(v2)

        return (center_b - center_a + origin, simplex)

    @staticmethod
    def refine(self, shape_a, shape_b, src, center_to_origin, iter_val=50):
        simplex = src
        is_colliding = False
        v1 = Matrix([0.0, 0.0], 'vec')
        v2 = Matrix([0.0, 0.0], 'vec')
        direction = Matrix([0.0, 0.0], 'vec')

        for i in range(iter_val):
            v1 = simplex._vertices[1]._result
            v2 = simplex._vertices[2]._result
            direction = GJK.calc_direction_by_edge(v1, v2, True)

            if (direction.dot(center_to_origin) < 0):
                direction.negate()
                is_colliding = True

            new_vertex = GJK.support(shape_a, shape_b, direction)

            if v1 == new_vertex._result or v2 == new_vertex.result:
                break

            dist13 = GeomAlgo2D.point_to_line_segment(v1, new_vertex,
                                                      [0.0, 0.0]).len_square()
            dist23 = GeomAlgo2D.point_to_line_segment(v2, new_vertex,
                                                      [0.0, 0.0]).len_square()

            if dist13 < dist23:
                simplex._vertices[2] = new_vertex
            else:
                simplex._vertices[1] = new_vertex

        return (is_colliding, simplex)
