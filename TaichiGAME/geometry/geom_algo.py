import numpy as np

from ..math.matrix import Matrix


class GeomAlgo2D():
    def __init__(self):
        pass

    def is_collinear(self, pa, pb, pc):
        return np.isclose((pa - pb).cross(pa - pc), 0)

    def is_fuzzy_collinear(self, pa, pb, target_point):
        return target_point.val[0] >= np.min(
            pa.val[0], pb.val[0]) and target_point.val[0] <= np.max(
                pa.val[0], pb.val[0]) and target_point.val[1] >= np.min(
                    pa.val[1], pb.val[1]) and target_point.val[1] <= np.max(
                        pa.val[1], pb.val[1])

    def is_point_on_segment(self, pa, pb, target_point):
        return self.is_collinear(pa, pb,
                                 target_point) and self.is_fuzzy_collinear(
                                     pa, pb, target_point)

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
        return (pa + pb + pc) / 3.0

    def triangle_area(self, pa, pb, pc):
        return np.fabs(Matrix.cross_product(pa - pb, pa - pc) / 2.0)

    #TODO: need to focus on the vertices format
    def calc_center(self, vertices):
        if len(vertices) >= 4:
            pos = Matrix([0, 0], 'vec')
            tot_area = 0
            for i in range(len(vertices) - 1):
                p1 = i + 1
                p2 = i + 2
                if p1 == len(vertices) - 2:
                    break

                tri_area = self.triangle_area(vertices[0], vertices[p1],
                                              vertices[p2])
                tri_centroid = self.triangle_centroid(vertices[0],
                                                      vertices[p1],
                                                      vertices[p2])
                pos += tri_centroid * tri_area
                tot_area += tri_area

            pos /= tot_area
            return pos
        else:
            return Matrix([0, 0], 'vec')

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

    def is_point_on_same_side(self, edge_point1, edge_point2, ref_point,
                              target_point):
        u = edge_point1 - edge_point2
        v = ref_point - edge_point1
        w = target_point - edge_point1
        d1 = u.cross(v)
        d2 = u.cross(w)
        return np.sign(d1) == np.sign(d2)
