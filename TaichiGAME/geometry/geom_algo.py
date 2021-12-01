import copy
from functools import cmp_to_key
from os import DirEntry, fpathconf, stat
from typing import Any, List, Tuple, Optional

import numpy as np
from numpy.core.fromnumeric import sort
from numpy.core.function_base import geomspace

from ..math.matrix import Matrix


class GeomAlgo2D():
    class Clipper():
        @staticmethod
        def sutherland_hodgment_polygon_clipping(
                polygon: List[Matrix],
                clip_region: List[Matrix]) -> List[Matrix]:
            '''Sutherland Hodgman Polygon Clipping
            All points is stored in counter clock winding.
            By convention:
               p0 -> idx1 -> idx2 -> p0 constructs a triangle

            Parameters
            ----------
            polygon : List[Matrix]
                original polygon
            clip_region : List[Matrix]
                ref clip polygon

            Returns
            -------
            List[Matrix]
                clipped polygon
            '''
            res: List[Matrix] = copy.deepcopy(polygon)
            clip_len: int = len(clip_region)
            for i in range(clip_len - 1):
                clipa: Matrix = clip_region[i]
                clipb: Matrix = clip_region[i+1]
                clipdir: Matrix = clip_region[1] if i + 2 == clip_len else clip_region[i+2]

                is_same_side: List[bool] = []
                poly_len: int = len(res)
                for j in range(poly_len):
                    is_same_side.append(GeomAlgo2D.is_point_on_same_side(clipa, clipb, clipdir, res[j]))

                new_polygon: List[Matrix] = []
                for j in range(1, poly_len):
                    last_inside: bool = is_same_side[j-1]
                    cur_inside: bool = is_same_side[j]

                    # last inside and cur outside
                    if last_inside and not cur_inside:
                        # push last point
                        new_polygon.append(res[j-1])
                        # push intersection point
                        new_polygon.append(GeomAlgo2D.line_intersection(clipa,clipb, res[j-1], res[j]))
                    elif not last_inside and cur_inside:
                        # push intersection point first
                        new_polygon.append(GeomAlgo2D.line_intersection(clipa,clipb, res[j-1], res[j]))
                    elif not last_inside and not cur_inside:
                        pass
                    elif last_inside and cur_inside:
                        new_polygon.append(res[j-1])
                
                res = copy.deepcopy(new_polygon)
                res.append(res[0])

            return res

    @staticmethod
    def is_collinear(pa: Matrix, pb: Matrix, pc: Matrix) -> bool:
        '''check if point pa, pb, pc are collinear

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        bool
            True: collinear False: not collinear
        '''
        return np.isclose((pa - pb).cross(pa - pc), [0.0, 0.0]).all()

    @staticmethod
    def judge_range(val: float, low: float, high: float) -> bool:
        return val >= low and val <= high

    @staticmethod
    def is_fuzzy_collinear(pa: Matrix, pb: Matrix, target: Matrix) -> bool:
        '''check if the target point is in rectangle which diag is pa-pb

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        target : Matrix
            target point

        Returns
        -------
        bool
            True: in range False: no in range
        '''
        x_min = np.fmin(pa._val[0], pb._val[0])
        x_max = np.fmax(pa._val[0], pb._val[0])
        y_min = np.fmin(pa._val[1], pb._val[1])
        y_max = np.fmax(pa._val[1], pb._val[1])
        return GeomAlgo2D.judge_range(target._val[0], x_min,
                                      x_max) and GeomAlgo2D.judge_range(
                                          target._val[1], y_min, y_max)

    @staticmethod
    def is_point_on_segment(pa: Matrix, pb: Matrix, target: Matrix) -> bool:
        '''check if the target point is on line segment pa-pb

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        target : Matrix
            target point

        Returns
        -------
        bool
            True: on segment False: not on
        '''
        return GeomAlgo2D.is_collinear(
            pa, pb, target) and GeomAlgo2D.is_fuzzy_collinear(pa, pb, target)

    @staticmethod
    def is_fuzzy_point_on_segment(pa: Matrix, pb: Matrix, target: Matrix) -> bool:
        return np.isclose(GeomAlgo2D.point_to_line_segment(pa, pb, target), 0)

    @staticmethod
    def line_segment_intersection(pa: Matrix, pb: Matrix, pc: Matrix, pd: Matrix) -> Matrix:
        pass
    
    @staticmethod
    def line_intersection(pa: Matrix, pb: Matrix, pc: Matrix, pd: Matrix) -> Optional[Matrix]:
        '''check if line pa-pb and pc-pd is intersection
        if yes, return the intersection point
        https://blog.csdn.net/qq_45735851/article/details/114434281

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c
        pd : Matrix
            point d

        Returns
        -------
        Optional[Matrix]
            if insect, return insect point, otherwise return None
        '''
        linea: Matrix = pb - pa # w
        lineb: Matrix = pd - pc # v
        if np.isclose(Matrix.cross_product(linea, lineb), 0):
            return None

        u: Matrix = pc - pa
        t: float = Matrix.cross_product(linea, u) / Matrix.cross_product(lineb, linea)
        res: Matrix = Matrix([pc._val[0]+t*lineb._val[0], pc._val[1]+t*lineb._val[1]], 'vec')

        return res
        
    @staticmethod
    def triangle_circum_center(pa: Matrix, pb: Matrix, pc: Matrix) -> Optional[Matrix]:
        '''calc the circum-circle center from triangle pa-pb-pc

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        Optional[Matrix]
            If pa-pb-pc form triangle, return circum-circle center, otherwise None
        '''
        if np.isclose(GeomAlgo2D.triangle_area(pa, pb, pc), 0):
            return None
        
        # 2 * (x2 - x1) * x + 2 * (y2 - y1) y = x2 ^ 2 + y2 ^ 2 - x1 ^ 2 - y1 ^ 2
        # 2 * (x3 - x2) * x + 2 * (y3 - y2) y = x3 ^ 2 + y3 ^ 2 - x2 ^ 2 - y2 ^ 2
        val11: float = 2.0 * (pb._val[0] - pa._val[0])
        val12: float = 2.0 * (pb._val[1] - pa._val[1])
        val21: float = 2.0 * (pc._val[0] - pb._val[0])
        val22: float = 2.0 * (pc._val[1] - pb._val[1])
        coef_mat: Matrix = Matrix([val11, val12, val21, val22])
        equal_val: Matrix = Matrix([pb.len_square() - pa.len_square(), pc.len_square() - pb.len_square()], 'vec')

        return coef_mat.invert() * equal_val

    @staticmethod
    def triangle_inscribed_center(pa: Matrix, pb: Matrix, pc: Matrix) -> Optional[Matrix]:
        '''calc the inscribed-circle center from triangle pa-pb-pc

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        Optional[Matrix]
            If pa-pb-pc form triangle, return inscribed-circle center, otherwise None
        '''
        if np.isclose(GeomAlgo2D.triangle_area(pa, pb, pc), 0):
            return None

        ab_len: float = (pb - pa).len()
        bc_len: float = (pc - pb).len()
        ca_len: float = (pc - pa).len()
        return (ab_len * pc + bc_len * pa + ca_len * pb) / (ab_len + bc_len + ca_len)


    @staticmethod
    def calc_circum_center(pa: Matrix, pb: Matrix, pc: Matrix) -> Optional[Tuple[Matrix, float]]:
        '''return the circum-circle's center and radius from triangle pa-pb-pc

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        Optional[Tuple[Matrix, float]]
            If can, return the (center, radius), otherwise None
        '''
        if np.isclose(GeomAlgo2D.triangle_area(pa, pb, pc), 0):
            return None

        center: Matrix = GeomAlgo2D.triangle_circum_center(pa, pb, pc)
        radius: float = (center - pa).len()
        return (center, radius)

    @staticmethod
    def calc_inscribed_center(pa: Matrix, pb: Matrix, pc: Matrix) -> Optional[Tuple[Matrix, float]]:
        '''return the inscribed-circle's center and radius from triangle pa-pb-pc

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        Optional[Tuple[Matrix, float]]
            If can, return the (center, radius), otherwise None
        '''
        area: float = GeomAlgo2D.triangle_area(pa, pb, pc)
        if np.isclose(area, 0):
            return None

        center: Matrix = GeomAlgo2D.triangle_inscribed_center(pa, pb, pc)

        ab_len: float = (pb - pa).len()
        bc_len: float = (pc - pb).len()
        ca_len: float = (pc - pa).len()
        radius: float = 2.0 * area / (ab_len + bc_len + ca_len)

        return (center, radius)

    @staticmethod
    def is_convex_polygon(vertices: List[Matrix]) -> bool:
        '''check if the polygon is convex

        Parameters
        ----------
        vertices : List[Matrix]
            polygon's points

        Returns
        -------
        bool
            True: is convex, False: not is
        '''
        
        num: float = len(vertices)
        if num == 4:
            return True

        for i in range(num - 1):
            ab: Matrix = vertices[i+1] - vertices[i]
            ac: Matrix = vertices[i+2] - vertices[i] if i + 2 != num else vertices[1] - vertices[i]

            if Matrix.cross_product(ab, ac) < 0:
                return False

        return True

    @staticmethod
    def graham_scan_cmp(a: Matrix, b: Matrix) -> int:
        first_val1: float = np.arctan2(a._val[1], a._val[0])
        first_val2: float = np.arctan2(b._val[1], b._val[0])
        if  not np.isclose(first_val1, first_val2):
            if first_val1 < first_val2:
                return -1
            elif first_val1 > first_val2:
                return 1
        else:
            second_val1: float = a._val[0]
            second_val2: float = b._val[0]
            if not np.isclose(second_val1, second_val2):
                if second_val1 < second_val2:
                    return -1
                elif second_val1 > second_val2:
                    return 1
        

    @staticmethod
    def graham_scan(vertices: List[Matrix]) -> List[Matrix]:
        '''Convex hull algorithm: Graham Scan. Given a series of points,
        find the convex polygon that can contains all of these points.

        Parameters
        ----------
        vertices : List[Matrix]
            polygon's points

        Returns
        -------
        List[Matrix]
            convex polygon's point
        '''
        sort_vert: List[Matrix] = copy.deepcopy(vertices)
        sort_vert.sort(vertices, key=cmp_to_key(GeomAlgo2D.graham_scan_cmp))

        stack: List[int] = []
        check_idx: int = 2
        stack.append(0)
        stack.append(1)
        while True:
            i: int = stack[-2]
            j: int = stack[-1]
            if j == 0:
                break
                
            if check_idx >= len(sort_vert):
                check_idx = 0

            ab: Matrix = sort_vert[j] - sort_vert[i]
            ac: Matrix = sort_vert[check_idx] - sort_vert[i]

            if ab.cross(ac) < 0:
                stack.pop()
            stack.append(check_idx)
            check_idx += 1

        res: List[Matrix] = []
        for idx in stack:
            res.append(sort_vert[idx])

        return res

    @staticmethod
    def point_to_line_segment(pa: Matrix, pb: Matrix, pc: Matrix) -> Optional[Matrix]:
        '''calculate point on line segment pa-pb that is the shortest length to pc

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        Optional[Matrix]
            shortest-dis point to the segment, otherwise None
        '''
        
        if pa == pb:
            return None

        if GeomAlgo2D.is_collinear(pa, pb, pc):
            return pc

        ac: Matrix = pc - pa
        ab_normal: Matrix = (pb - pa).normal()
        ac_proj: Matrix = ab_normal.dot(ac) * ab_normal
        op_proj: Matrix = pa + ac_proj

        if GeomAlgo2D.is_fuzzy_collinear(pa, pb, op_proj):
            return op_proj

        return pb if (pc - pa).len_square() > (pc - pb).len_squre() else pa


    @staticmethod
    def shortest_length_point_of_ellipse(a: float, b: float, pc: Matrix) -> Optional[Matrix]:
        '''calculate point on ellipse that is the shortest length 
        to pc(aka projection point)

        Parameters
        ----------
        a : float
            semi-major axis len
        b : float
            semi-minor axis len
        pc : Matrix
            target point

        Returns
        -------
        Optional[Matrix]
            shortest-dis point to the ellipse, otherwise None
        '''
        
        if np.isclose(a, 0) or np.isclose(b, 0):
            return None

        if np.isclose(pc._val[0], 0):
            return Matrix([0.0, b], 'vec') if pc._val[1] > 0 else Matrix([0.0, -b], 'vec')

        if np.isclose(pc._val[1], 0):
            return Matrix([a, 0.0], 'vec') if pc._val[0] > 0 else Matrix([-a, 0.0], 'vec')

        x_left: float = 0.0
        x_right: float = 0.0
        t0: Matrix = Matrix([0.0, 0.0], 'vec')
        t1: Matrix = Matrix([0.0, 0.0], 'vec')
        sgn: int = 1 if pc._val[1] > 0 else -1

        if pc._val[0] < 0:
            x_left = -a
            x_right = 0.0
        else:
            x_left = 0.0
            x_right = a

        iter_val: int = 0
        while True:
            iter_val += 1

            tmp_x0: float = (x_left + x_right) * 0.5
            tmp_y0: float = sgn * np.sqrt(b**2 - (b / a)**2 * tmp_x0**2)
            t0.set_value([tmp_x0, tmp_y0])

            tmp_x1: float = tmp_x0 + 1
            tmp_y1: float = (b**2 - (b / a)**2 * tmp_x1 * tmp_x0) / tmp_y0
            t1.set_value([tmp_x1, tmp_y1])

            t0t1: Matrix = t1 - t0
            t0p: Matrix = pc - t0

            res: float = t0t1.dot(t0p)
            if np.isclose(np.fabs(res), 0.0):
                break

            if res > 0:
                x_left = tmp_x0
            else:
                x_right = tmp_x0

        return t0



    @staticmethod
    def triangle_centroid(pa: Matrix, pb: Matrix, pc: Matrix) -> Matrix:
        '''calculate the centroid of the triangle

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        Matrix
            centroid point
        '''
        return (pa + pb + pc) / 3.0

    @staticmethod
    def triangle_area(pa: Matrix, pb: Matrix, pc: Matrix) -> float:
        '''calculate the area of the triangle

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        float
            triangle area
        '''
        return np.fabs(Matrix.cross_product(pa - pb, pa - pc) / 2.0)

    #NOTE: need to focus on the vertices format
    @staticmethod
    def calc_mass_center(vertices: List[Matrix]) -> Matrix:
        '''calculate the mass center of the convex polygon

        Parameters
        ----------
        vertices : List[Matrix]
            polygon's points

        Returns
        -------
        Matrix
            mass center
        '''

        vert_len: float = len(vertices)
        if vert_len >= 4:
            pos: Matrix = Matrix([0.0, 0.0], 'vec')
            tot_area: float = 0.0

            for i in range(vert_len - 1):
                idx1: int = i + 1
                idx2: int = i + 2
                if idx1 == vert_len - 2:
                    break

                tri_area: float = GeomAlgo2D.triangle_area(vertices[0], vertices[idx1],
                                                    vertices[idx2])
                tri_centroid: Matrix = GeomAlgo2D.triangle_centroid(
                    vertices[0], vertices[idx1], vertices[idx2])

                pos += tri_centroid * tri_area
                tot_area += tri_area

            pos /= tot_area

            return pos
        else:
            return Matrix([0.0, 0.0], 'vec')

    @staticmethod #FIXME: need to understand the algorithm
    def shortest_length_line_segment_ellipse(a: float, b: float, pc: Matrix, pd: Matrix) -> Tuple[Matrix, Matrix]:
        '''calculate two points on line segment and ellipse respectively.
        The length of two points is the shortest distance of line segment and ellipse

        Parameters
        ----------
        a : float
            semi-major axis len
        b : float
            semi-minor axis len
        pc : Matrix
            line segment point c
        pd : Matrix
            line segment point d

        Returns
        -------
        Tuple[Matrix, Matrix]
            the return data
        '''
        
        res_segm: Matrix = Matrix([0.0, 0.0], 'vec')
        res_elli: Matrix = Matrix([0.0, 0.0], 'vec')

        #FIXME: can write helper func
        if np.isclose(pc._val[1], pd._val[1]):
            if not ((pc._val[0] > 0 and pd._val[0] > 0) or (pc._val[0] < 0 and pd._val[0] < 0)):
                res_elli.set_value([0.0, b if pc._val[1] > 0 else -b])
                res_segm.set_value([0.0, pc._val[1]])
            else:
                tmp: float = np.fmin(np.fabs(pc._val[0]), np.fabs(pd._val[0]))
                res_segm.set_value([tmp, pc._val[1]])
                res_elli = GeomAlgo2D.shortest_length_point_of_ellipse(a, b, res_segm)
        elif np.isclose(pc._val[0], pd._val[0]):
            if not ((pc._val[1] > 0 and pd._val[1] > 0) or (pc._val[1] < 0 and pd._val[1] < 0)):
                res_elli.set_value([a if pc._val[0] > 0 else -a, 0.0])
                res_segm.set_value([pc._val[0], 0.0])
            else:
                tmp: float = np.fmin(np.fabs(pc._val[1]), np.fabs(pd._val[1]))
                res_segm.set_value([pc._val[0], tmp])
                res_elli = GeomAlgo2D.shortest_length_point_of_ellipse(a, b, res_segm)
        else:
            k: float = (pd._val[1] - pc._val[1]) / (pd._val[0] - pc._val[0])
            k2: float = k * k
            a2:float = a**2
            b2:float = b**2
            f_x2: float = (k2 * a2 * a2 / b2) / (1 + a2 * k2 / b2)
            f_y2: float = b2 - b2 * f_x2 / a2
            f_x: float = np.sqrt(f_x2)
            f_y: float = np.sqrt(f_y2)
            f: Matrix = Matrix([0.0, 0.0], 'vec')
            pcpd: Matrix = (pd - pc).normal()

            # Check which quadrant does nearest point fall in
            f_arr: List[Matrix] = []
            f_arr.append(Matrix([f_x, f_y], 'vec'))
            f_arr.append(Matrix([-f_x, f_y], 'vec'))
            f_arr.append(Matrix([-f_x, -f_y], 'vec'))
            f_arr.append(Matrix([f_x, -f_y], 'vec'))

            min_val: float = Matrix.cross_product(pcpd, f_arr[0] - pc)
            for i in range(1, 4):
                tmp_val: float = Matrix.cross_product(pcpd, f_arr[i] - pc)
                if tmp_val < min_val:
                    f = f_arr[i] #BUG: the f is not the one define before
                    min_val = tmp_val
            
            pcf: Matrix = f - pc
            pc_fp: Matrix = pcpd * pcpd.dot(pcf)
            f_proj: Matrix = pc + pc_fp

            if GeomAlgo2D.is_fuzzy_collinear(a, b, f_proj):
                res_elli = f
                res_segm = f_proj
            else:
                pc_p = GeomAlgo2D.shortest_length_point_of_ellipse(a, b, pc)
                pd_p = GeomAlgo2D.shortest_length_point_of_ellipse(a, b, pd)

                if (pc - pc_p).len_square() > (pd - pd_p).len_square():
                    res_elli = pd_p
                    res_segm = pd
                else:
                    res_elli = pc_p
                    res_segm = pc

        return (res_elli, res_segm)

    @staticmethod
    def raycast(pa: Matrix, dir: Matrix, pc: Matrix, pd: Matrix) -> Optional[Matrix]:
        '''calculate point on line segment pc-pd, if point 'pa' can cast ray in 'dir' 
        direction on line segment pc-pd.

        Parameters
        ----------
        pa : Matrix
            ray start point
        dir : Matrix
            ray direction
        pc : Matrix
            line segment point a
        pd : Matrix
            line segment point b

        Returns
        -------
        Optional[Matrix]
            If exist, return raycast point, otherwise None
        '''
        
        denominator: float = (pa._val[0] - dir._val[0]) * (pc._val[1] - pd._val[1]) - (pa._val[1] - dir._val[1]) * (pc._val[0] - pd._val[0])

        if np.isclose(denominator, 0):
            return None

        t: float = ((pa._val[0] - pc._val[0]) * (pc._val[1] - pd._val[1]) - (pa._val[1] - pc._val[1]) * (pc._val[0] - pd._val[0])) / denominator
        u: float = ((dir._val[0] - pa._val[0]) * (pa._val[1] - pc._val[1]) - (dir._val[1] - pa._val[1]) * (pa._val[0] - pc._val[0])) / denominator

        if t >= 0 and 0 <= u <= 1.0:
            return Matrix([pa._val[0] + t * (dir._val[0] - pa._val[0]), pa._val[1] + t * (dir._val[1] - pa._val[1])], 'vec')
        
        return None

    @staticmethod
    def raycastAABB(pa: Matrix, dir: Matrix, top_left: Matrix, bot_right: Matrix) -> Optional[Tuple[Matrix, Matrix]]:
        '''calculate point on  AABB, if point 'pa' can cast ray in 'dir' 
        direction on AABB.

        Parameters
        ----------
        pa : Matrix
            ray start point
        dir : Matrix
            ray direction
        top_left : Matrix
            AABB top left point
        bot_right : Matrix
            AABB bot right point

        Returns
        -------
        Optional[Matrix]
            If exist, return raycast point, otherwise None
        '''

        x_min: float = top_left._val[0]
        y_min: float = bot_right._val[1]
        x_max: float = bot_right._val[0]
        y_max: float = top_left._val[1]
        tx_min: float = 0.0
        ty_min: float= 0.0
        tx_max: float = 0.0
        ty_max: float = 0.0
        tx_enter: float  = 0.0
        tx_exit: float = 0.0
        ty_enter: float = 0.0
        ty_exit: float = 0.0
        t_enter: float = 0.0
        t_exit: float = 0.0

        if np.isclose(dir._val[0], 0) and not np.isclose(dir._val[1], 0):
            ty_min = (y_min - pa._val[1]) / dir._val[1]
            ty_max = (y_max - pa._val[1]) / dir._val[1]
            t_enter = np.fmin(ty_min, ty_max)
            t_exit = np.fmax(ty_min, ty_max)
        elif not np.isclose(dir._val[0], 0) and np.isclose(dir._val[1], 0):
            tx_min = (x_min - pa._val[0]) / dir._val[0]
            tx_max = (x_max - pa._val[0]) / dir._val[0]
            t_enter = np.fmin(tx_min, tx_max)
            t_exit = np.fmax(tx_min, tx_max)
        else:
            tx_min = (x_min - pa._val[0]) / dir._val[0]
            tx_max = (x_max - pa._val[0]) / dir._val[0]
            ty_min = (y_min - pa._val[1]) / dir._val[1]
            ty_max = (y_max - pa._val[1]) / dir._val[1]
            tx_enter = np.fmin(tx_min, tx_max)
            tx_exit = np.fmax(tx_min, tx_max)
            ty_enter = np.fmin(ty_min, ty_max)
            ty_exit = np.fmax(ty_min, ty_max)
            t_enter = np.fmax(tx_enter, ty_enter)
            t_exit = np.fmin(tx_exit, ty_exit)
    
        if t_enter < 0 and t_exit < 0:
            return None
        
        enter: Matrix = pa + t_enter * dir
        exit: Matrix = pa + t_exit * dir

        return (enter, exit)


    @staticmethod
    def is_point_on_AABB(pa: Matrix, top_left: Matrix, bot_right: Matrix) -> bool:
        '''check if the pa is in the AABB

        Parameters
        ----------
        pa : Matrix
            target point
        top_left : Matrix
            AABB top left point
        bot_right : Matrix
            AABB bottom right point

        Returns
        -------
        bool
            True: is in AABB False: is not
        '''
        
        return GeomAlgo2D.judge_range(pa._val[0], top_left._val[0], bot_right._val[0]) and GeomAlgo2D.judge_range(pa._val[1], bot_right._val[1], top_left._val[1])

    @staticmethod
    def rotate(pa: Matrix, center: Matrix, radian: float) -> Matrix:
        '''rotate point 'pa' around point 'center' by radian

        Parameters
        ----------
        pa : Matrix
            source point
        center : Matrix
            center point
        radian : float
            rotate radian

        Returns
        -------
        Matrix
            result point
        '''
        
        return Matrix.rotate_mat(radian) * (pa - center) + center


    @staticmethod
    def calc_ellipse_project_on_point(a: float, b: float, dir: Matrix) -> Matrix:
        '''calculate the projection axis of ellipse in user-define direction.
        return the maximum point in ellipse

        Parameters
        ----------
        a : float
            semi-major axis len
        b : float
            semi-minor axis len
        dir : Matrix
            user define direction

        Returns
        -------
        Matrix
            maximum point
        '''
        
        res: Matrix = Matrix([0.0, 0.0], 'vec')

        if np.isclose(dir._val[0], 0):
            sgn: int = -1 if dir._val[1] < 0 else 1
            res.set_value([0.0, sgn * b])
        elif np.isclose(dir._val[1], 0):
            sgn: int = -1 if dir._val[0] < 0 else 1
            res.set_value([sgn * a, 0.0])
        else:
            k = dir._val[1] / dir._val[0]
            # line offset constant 
            a2 = a**2
            b2 = b**2
            k2 = k**2
            d = np.sqrt((a2 + b2 * k2) / k2)
            if Matrix.dot_product(Matrix([0.0, d], 'vec'), dir) < 0:
                d = d * -1

            x1 = k * d - (b2 * k2 * k * d) / (a2 + b2 * k2)
            y1 = (b2 * k2 * d) / (a2 + b2 * k2)
            res.set(x1, y1)

        return res

    @staticmethod
    def calc_capsule_project_on_point(width: float, height: float, dir: Matrix) -> Matrix:
        '''calculate the projection axis of capsule in user-define direction.
        return the maximum point in capsule

        Parameters
        ----------
        width : float
            capsule width
        height : float
            capsule height
        dir : Matrix
            user define direction

        Returns
        -------
        Matrix
            maximum point
        '''
        
        res: Matrix = Matrix([0.0, 0.0], 'vec')
        if width > height:
            radius: float = height / 2.0
            offset: float = width / 2.0 - radius if dir._val[0] >= 0 else radius - width / 2.0
            res = dir.normal() * radius
            res._val[0] += offset
        else:
            radius: float = width / 2.0
            offset: float = height / 2.0 - radius if dir._val[1] >= 0 else radius - height / 2.0
            res = dir.normal() * radius
            res._val[1] += offset

        return res

    @staticmethod
    def calc_sector_project_on_point(start: float, span: float, radius: float, dir: Matrix) -> Matrix:
        '''calculate the projection axis of sector in user-define direction.
        return the maximum point in sector

        Parameters
        ----------
        start : float
            start radian
        span : float
            span radian(delta radian)
        radius : float
            radius value
        dir : Matrix
            user define direction

        Returns
        -------
        Matrix
            maximum point
        '''

        res: Matrix = Matrix([0.0, 0.0], 'vec')

        def _clamp_radian(radian: float) -> float:
            _res: float = radian
            _res -= np.floor(_res / np.pi * 2) * np.pi * 2

            if _res < 0:
                _res += np.pi * 2
            
            return _res
        
        clamp_start: float = _clamp_radian(start)
        clamp_end: float = _clamp_radian(start + span)
        origin_start: float = _clamp_radian(start - np.pi / 2.0)
        origin_end: float = _clamp_radian(start + span + np.pi / 2.0)
        origin_theta: float = dir.theta()
        theta: float = _clamp_radian(origin_theta)

        if origin_start > origin_end:
            # does not fall in zero area
            if not GeomAlgo2D.judge_range(theta, origin_end, origin_start):
                if theta > origin_start:
                    theta = origin_theta

                # clamp theta to sector area
                res = Matrix.rotate_mat(np.clip(theta, clamp_start, clamp_end)) * Matrix([1.0, 0.0], 'vec') * radius

        elif origin_start < origin_end:
            if GeomAlgo2D.judge_range(origin_theta, origin_start, origin_end):
                res = Matrix.rotate_mat(np.clip(theta, clamp_start, clamp_end)) * Matrix([1.0, 0.0], 'vec') * radius

        if np.isclose(origin_start, origin_end):
            if not np.isclose(theta, origin_start):
                if theta > origin_start:
                    theta = origin_theta
                
                if clamp_start > clamp_end:
                    res = Matrix.rotate_mat(np.clip(theta, clamp_start - np.pi * 2.0, clamp_end)) * Matrix([1.0, 0.0], 'vec') * radius
                else:
                    res = Matrix.rotate_mat(np.clip(theta, clamp_start, clamp_end)) * Matrix([1.0, 0.0], 'vec') * radius

        return res
        

    @staticmethod
    def is_triangle_contain_origin(pa: Matrix, pb: Matrix, pc: Matrix) -> bool:
        '''check if the origin point is in the triangle

        Parameters
        ----------
        pa : Matrix
            point a
        pb : Matrix
            point b
        pc : Matrix
            point c

        Returns
        -------
        bool
            True: origin point is in triangle, otherwise not
        '''
        
        ra: float = (pb - pa).cross(-pa)
        rb: float = (pc - pb).cross(-pb)
        rc: float = (pa - pc).cross(-pc)
        return (ra >= 0 and rb >= 0 and rc >= 0) or (ra <= 0 and rb <= 0 and rc <= 0)

    @staticmethod
    def is_point_on_same_side(edgp1: Matrix, edgp2: Matrix, ref: Matrix, target: Matrix) -> bool:
        '''check if the target and ref point is on edgep1-edgep2 same side

        Parameters
        ----------
        edgp1 : Matrix
            edge point 1
        edgp2 : Matrix
            edge point 2
        ref : Matrix
            ref point
        target : Matrix
            target point

        Returns
        -------
        bool
            True: is on same side, otherwise not
        '''

        u = edgp1 - edgp2
        v = ref - edgp1
        w = target - edgp1
        d1 = u.cross(v)
        d2 = u.cross(w)
        return np.sign(d1) == np.sign(d2)
