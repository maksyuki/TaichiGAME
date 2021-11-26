

class ProjectPoint():
    def __init__(self):
        self._vertex = Matrix([0.0, 0.0], 'vec')
        self._value = 0.0
        self._index = -1.0

    def __eq__(self):
        pass

class ProjectEdge():
    def __init__(self):
        self._vertex1 = Matrix([0.0, 0.0], 'vec')
        self._vertex2 = Matrix([0.0, 0.0], 'vec')

class ProjectSegment():
    def __init__(self):
        self._val_min = ProjectPoint()
        self._val_max = ProjectPoint()

    @staticmethod
    def intersect(s1, s2):
        pass

class SATResult():
    def __init__(self):
        self._contact_pair = []
        self._contact_pair_count = 0
        self._normal = Matrix([0.0, 0.0], 'vec')
        self._penetration = 0.0
        self._is_colliding = False

class SAT():
    def __init__(self):
        pass

    @staticmethod
    def circle_vs_capsule(shape_a, shape_b):
        pass

    @staticmethod
    def circle_vs_sector(shape_a, shape_b):
        pass

    @staticmethod
    def circle_vs_edge(shape_a, shape_b):
        pass

    @staticmethod
    def circle_vs_circle(shape_a,shape_b):
        pass

    @staticmethod
    def circle_vs_polygon(shape_a, shape_b):
        pass

    @staticmethod
    def polygon_vs_polygon(shape_a, shape_b):
        pass

    @staticmethod
    def polygon_vs_edge(shape_a, shape_b):
        pass

    @staticmethod
    def polygon_vs_capsule(shape_a, shape_b):
        pass

    @staticmethod
    def polygon_vs_sector(shape_a, shape_b):
        pass

    @staticmethod
    def capsule_vs_edge(shape_a, shape_b):
        pass
    
    @staticmethod
    def capsule_vs_capsule(shape_a, shape_b):
        pass

    @staticmethod
    def capsule_vs_sector(shape_a, shape_b):
        pass

    @staticmethod
    def sector_vs_sector(shape_a, shape_b):
        pass

    @staticmethod
    def _axis_projection(shape, fixme, normal)