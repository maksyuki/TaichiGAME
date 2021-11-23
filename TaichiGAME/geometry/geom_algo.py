import numpy as np

from ..math.matrix import Matrix


class GeomAlgo2D():
    def __init__(self):
        pass

    @staticmethod
    def is_collinear(pa, pb, pc):
        return np.isclose((pa - pb).cross(pa - pc), [0.0, 0.0]).all()

    @staticmethod
    def judge_range(val, low, high):
        return val >= low and val <= high

    @staticmethod
    def is_fuzzy_collinear(pa, pb, target_point):
        x_min = np.fmin(pa.val[0], pb.val[0])
        x_max = np.fmax(pa.val[0], pb.val[0])
        y_min = np.fmin(pa.val[1], pb.val[1])
        y_max = np.fmax(pa.val[1], pb.val[1])
        return GeomAlgo2D.judge_range(target_point.val[0], x_min,
                                      x_max) and GeomAlgo2D.judge_range(
                                          target_point.val[1], y_min, y_max)

    @staticmethod
    def is_point_on_segment(pa, pb, target_point):
        return GeomAlgo2D.is_collinear(
            pa, pb, target_point) and GeomAlgo2D.is_fuzzy_collinear(
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

    @staticmethod
    def triangle_centroid(pa, pb, pc):
        return (pa + pb + pc) / 3.0

    @staticmethod
    def triangle_area(pa, pb, pc):
        return np.fabs(Matrix.cross_product(pa - pb, pa - pc) / 2.0)

    #TODO: need to focus on the vertices format
    @staticmethod
    def calc_center(vertices):
        if len(vertices) >= 4:
            pos = Matrix([0.0, 0.0], 'vec')
            tot_area = 0
            for i in range(len(vertices) - 1):
                p1 = i + 1
                p2 = i + 2
                if p1 == len(vertices) - 2:
                    break

                tri_area = GeomAlgo2D.triangle_area(vertices[0], vertices[p1],
                                                    vertices[p2])
                tri_centroid = GeomAlgo2D.triangle_centroid(
                    vertices[0], vertices[p1], vertices[p2])
                pos += tri_centroid * tri_area
                tot_area += tri_area

            pos /= tot_area
            return pos
        else:
            return Matrix([0.0, 0.0], 'vec')

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

    @staticmethod
    def is_point_on_same_side(edge_point1, edge_point2, ref_point,
                              target_point):
        u = edge_point1 - edge_point2
        v = ref_point - edge_point1
        w = target_point - edge_point1
        d1 = u.cross(v)
        d2 = u.cross(w)
        return np.sign(d1) == np.sign(d2)
