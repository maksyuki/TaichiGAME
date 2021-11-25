


class Minkowski():
    def __init__(self):
        pass
    
    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

class Simplex():
    def __init__(self):
        self._is_contain_origin = False
    
    def contain_origin(self, strict=False):
        pass

    def insert(self, pos, vertex):
        pass

    def contains(self, minkowski):
        pass

    def last_vertex(self):
        pass

class PenetrationInfo():
    def __init__(self):
        self._normal = Matrix([0.0, 0.0], 'vec')
        self.penetration = 0.0

class PenetrationSource():
    def __init__(self):
        pass

class PointPair():
    def __init__(self):
        pass
    
    def __eq__(self, other):
        pass

    def is_empty(self):
        pass

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
    def distance(shape_a, shape_b, iter=20)
        pass

    @staticmethod
    def dump_source(simplex):
        pass

    @staticmethod
    def dump_points(src):
        pass