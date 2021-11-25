class Minkowski():
    def __init__(self, pa, pb):
        self._pointa = pa
        self._pointb = pb
        self._result = self._pointa - self._pointb

    def __eq__(self, other):
        return self._pointa == other._pointa and self._pointb == other._pointb

    def __ne__(self, other):
        return not (self._pointa == other._pointa
                    and self._pointb == other._pointb)


class Simplex():
    def __init__(self):
        self._is_contain_origin = False
        self._vertices = []

    def contain_origin(self, strict=False):
        self._is_contain_origin = Simplex.contain_origin_oper(self, strict)
        return self._is_contain_origin

    def insert(self, pos, vertex):
        self._vertices.insert(pos + 1, vertex)

    def contains(self, minkowski):
        for v in self._vertices:
            if v == minkowski:
                return True

        return False

    def last_vertex(self):
        vert_len = len(self._vertices)
        if vert_len == 2:
            return self._vertices[vert_len - 1]._result

        return self._vertices[vert_len - 2]._result

    @staticmethod
    def contain_origin_oper(simplex, strict=False):
        num = len(simplex.vertices())
        if num == 4:
            return GeomAlgo2D.is_triangle_contain_origin(
                simplex._vertices[0]._result, simplex._vertices[1]._result,
                simplex._vertices[2]._result)
        elif num == 2:
            oa = -simplex._vertices[0]._result
            ob = -simplex._vertices[1]._result
            return GeomAlgo2D.is_point_on_segment(oa, ob, [0.0, 0.0])
        else:
            return False


class PenetrationInfo():
    def __init__(self):
        self._normal = Matrix([0.0, 0.0], 'vec')
        self.penetration = 0.0


class PenetrationSource():
    def __init__(self):
        self._a1 = Matrix([0.0, 0.0], 'vec')
        self._a2 = Matrix([0.0, 0.0], 'vec')
        self._b1 = Matrix([0.0, 0.0], 'vec')
        self._b2 = Matrix([0.0, 0.0], 'vec')

class PointPair():
    def __init__(self):
        self._pointa = Matrix([0.0, 0.0], 'vec')
        self._pointb = Matrix([0.0, 0.0], 'vec')

    def __eq__(self, other):
        return self._pointa == other._pointa and self._pointb == other._pointb

    def is_empty(self):
        return self._pointa == Matrix(
            [0.0, 0.0], 'vec') and self._pointb == Matrix([0.0, 0.0], 'vec')


class GJK():
    def __init__(self):
        pass

    @staticmethod
    def gjk(shape_a, shape_b, iter=20):
        pass

    @staticmethod
    def epa(shape_a, shape_b, src, iter=20):
        pass

    @staticmethod
    def dump_info(src):
        pass

    @staticmethod
    def support(shape_a, shape_b, dir):
        pass

    @staticmethod
    def find_edge_closest_to_origin(simplex):
        pass

    @staticmethod
    def find_farthest_point(shape, dir):
        pass

    @staticmethod
    def adjust_simplex(simplex, closest_1, closest_2):
        pass

    @staticmethod
    def calc_direction_by_edge(p1, p2, point_to_origin=True):
        pass

    @staticmethod
    def distance(shape_a, shape_b, iter=20):
        pass

    @staticmethod
    def dump_source(simplex):
        pass

    @staticmethod
    def dump_points(src):
        pass
