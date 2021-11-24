class AABB():
    def __init__(self):
        pass

    def __eq__(self, other):
        pass

    def top_left(self):
        pass

    def top_right(self):
        pass

    def bottom_left(self):
        pass

    def bottom_right(self):
        pass

    def collide(self, aabb):
        pass

    def expand(self, factor):
        pass

    def scale(self, factor):
        pass

    def unite(self, aabb):
        pass

    def surface_area(self):
        pass

    def volume(self):
        pass

    def is_subset(self, aabb):
        pass

    def is_empty(self):
        pass

    def raycast(self, start_point, dir):
        pass

    @staticmethod
    def from_shape(shape, factor=0.0):
        pass

    @staticmethod
    def from_body(body, factor=0.0):
        pass

    @staticmethod
    def from_box(top_left, bottom_right):
        pass

    @staticmethod
    def collide_det(src, target):
        pass

    @staticmethod
    def unite_oper(src, target, factor=0.0):
        pass

    @staticmethod
    def is_subset_det(src, target):
        pass

    @staticmethod
    def expand_oper(aabb, factor=0.0):
        pass

    @staticmethod
    def raycast_oper(aabb, start_point, dir):
        pass
