from ..math.matrix import Matrix

class GeomAlgo2D():
    def __init__(self):
        pass

    def is_collinear(self, pa, pb, pc):
        pass

    def is_point_on_segment(self, pa, pb, pc):
        pass

    def line_segment_intersection(self, pa, pb, pc, pd):
        pass

    def line_intersection(self, pa, pb, pc, pd):
        pass

    def triangle_circum_center(self, pa, pb, pc):
        pass

    def triangle_inscribed_center(self, pa, pb, pc):
        pass

    def calc_circum_center(self, pa, pb, pc):
        pass

    def calc_inscribed_center(self, pa, pb, pc):
        pass

    def is_convex_polygon(self, vertices):
        pass

    def graham_scan(self, vertices):
        pass

    def point_to_line_segment(self, pa, pb, pc):
        pass

    def shortest_length_point_of_ellipse(self, pa, pb, pc):
        pass

    def triangle_centroid(self, pa, pb, pc):
        pass

    def triangle_area(self, pa, pb, pc):
        pass

    def calc_center(self, vertices):
        pass

    def shortest_length_line_segment__ellipse(self, pa, pb, pc, pd):
        pass

    def raycast(self, pa, dir, pb, pc):
        pass

    def raycastAABB(self, pa, dir, pb, pc):
        pass

    def is_point_on_AABB(self, pa, top_left, bottom_right):
        pass

    def rotate(self, pa, center, angle):
        pass

    def calc_ellipse_project_on_point(self, va, vb, dir):
        pass

    def calc_capsule_project_on_point(self, width, height, dir):
        pass

    def calc_sector_project_on_point(self, start_radian, span_radian, dir):
        pass

    def is_triangle_contain_origin(self, pa, pb, pc):
        pass

    def is_point_on_same_side(self, pa, pb, ref_point, target_point):
        pass
