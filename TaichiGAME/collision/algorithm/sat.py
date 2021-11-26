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
        assert shape_a._shape.type() == Shape.Type.Circle
        assert shape_b._shape.type() == Shape.Type.Capsule
        result = SATResult
        return result

    @staticmethod
    def circle_vs_sector(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Circle
        assert shape_b._shape.type() == Shape.Type.Sector
        result = SATResult
        return result

    @staticmethod
    def circle_vs_edge(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Circle
        assert shape_b._shape.type() == Shape.Type.Edge

        result = SATResult
        circle = shape_a._shape
        edge = shape_b._shape

        actual_start = shape_b._transform + edge.start_point()
        actual_end = shape_b._transform + edge.end()
        normal = (actual_start - actual_end).normal()

        if (actual_start - shape_a._transform).dot(normal) < 0 and (
                actual_end - shape_b._transform).dot(normal) < 0:
            normal.negate()

        projected_point = GeomAlgo2D.point_to_line_segment(
            actual_start, actual_end, shape_a._transform)
        diff = projected_point - shape_a._transform
        result._normal = diff.normal()
        length = diff.len()
        result._is_colliding = length < circle.radius()
        result._penetration = circle.radius() - length

        result._contact_pair[
            0]._pointa = shape_a._transform + circle.radius() * result._normal
        result._contact_pair[0]._pointb = projected_point
        result._contact_pair_count += 1
        return result

    @staticmethod
    def circle_vs_circle(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Circle
        assert shape_b._shape.type() == Shape.Type.Circle

        result = SATResult()
        circle_a = shape_a._shape
        circle_b = shape_b._shape

        ba = shape_a._transform - shape_b._transform
        dp = circle_a.radius() + circle_b.radius()
        length = ba.len()

        if length <= dp:
            result._normal = ba.normal()
            result._penetration = dp - length
            result._is_colliding = True
            result._contact_pair[
                0]._pointa = shape_a._transform - circle_a.radius(
                ) * result._normal
            result._contact_pair[
                0]._pointb = shape_b._transform - circle_b.radius(
                ) * result._normal
            result._contact_pair_count += 1

        return result

    @staticmethod
    def circle_vs_polygon(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Circle
        assert shape_b._shape.type() == Shape.Type.Polygon

        circle_a = shape_a._shape
        polygon_b = shape_b._shape
        colliding_axis = 0
        result = SATResult()

        len_min = 2222222222  #FIXME:
        closest = Matrix([0.0, 0.0], 'vec')

        for elem in polygon_b.vertices():
            vertex = shape_b.translate(elem)
            length = (vertex - shape_a._transform).len_square()
            if len_min > length:
                len_min = length
                closest = vertex

        normal = closest.normal()
        segment_circle = SAT._axis_projection(shape_a, circle_a, normal)
        segment_polygon = SAT._axis_projection(shape_b, circle_b, normal)

        (final_segment,
         length) = ProjectSegment.intersect(segment_circle, segment_polygon)

        if length > 0:
            colliding_axis += 1

        if result._penetration > length:
            result._penetration = length
            result._normal = normal

        circle_point = ProjectPoint()
        polygon_point = ProjectPoint()
        circle_point = final_segment._val_max if segment_circle._val_max == final_segment._val_max else final_segment._val_min
        polygon_point = final_segment._val_max if segment_polygon._val_max == final_segment._val_max else final_segment._val_min

        segment = ProjectSegment()
        on_polygon = False

        for i in range(len(polygon_b) - 1):
            v1 = shape_b.translate(polygon_b.vertices()[i])
            v2 = shape_b.translate(polygon_b.vertices())[i + 1]
            edge = v1 - v2
            normal = edge.perpendicular().normal()

            segment_c = SAT._axis_projection(shape_a, circle_a, normal)
            segment_p = SAT._axis_projection(shape_b, polygon_b, normal)

            (tmp_segment,
             tmp_length) = ProjectSegment.intersect(segment_c, segment_p)
            if tmp_length > 0:
                colliding_axis += 1

            if result._penetration > tmp_length and tmp_length > 0:
                result._penetration = tmp_length
                result._normal = normal
                segment = tmp_segment
                circle_point = tmp_segment._val_min if segment_c._val_max == tmp_segment._val_max else tmp_segment._val_min

        if colliding_axis == len(polygon_b.vertices()):
            result._is_colliding = True

        result._contact_pair[0]._pointa = circle_point._vertex
        result._contact_pair[
            0]._pointb = circle_point._vertex + -result._normal * result._penetration
        result._contact_pair_count += 1

        return result

    @staticmethod
    def polygon_helper(polygon_a, polygon_b):
        polya = polygon_a._shape
        polyb = polygon_b._shape

        final_normal = Matrix([0.0, 0.0], 'vec')
        len_min = 222222222  #FIXME:
        colliding_axis = 0
        segment = ProjectSegment()
        target_a_point = ProjectPoint()
        target_b_point = ProjectPoint()

        for i in range(len(polya.vertices()) - 1):
            v1 = polygon_a.translate(polya.vertices())[i]
            v2 = polygon_b.translate(polya.vertices())[i + 1]
            edge = v1 - v2
            normal = edge.perpendicular().normal()

            segment_a = SAT._axis_projection(polygon_a, polya, normal)
            segment_b = SAT._axis_projection(polygon_b, polyb, normal)

            (final_segment,
             length) = ProjectSegment.intersect(segment_a, segment_b)
            if length > 0:
                colliding_axis += 1

            polya_point = ProjectPoint
            polyb_point = ProjectPoint
            polya_point = final_segment._val_max if segment_a._val_max == final_segment._val_max else final_segment._val_min
            polyb_point = final_segment._val_max if segment_b._val_max == final_segment._val_max else final_segment._val_min

            if len_min > length:
                len_min = length
                final_normal = normal
                target_a_point = polya_point
                target_b_point = polyb_point

        return (final_normal, len_min, colliding_axis, target_a_point,
                target_b_point)

    @staticmethod
    def polygon_vs_polygon(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Polygon
        assert shape_b._shape.type() == Shape.Type.Polygon

        polya = shape_a._shape
        polyb = shape_b._shape

        result = SATResult
        (normal1, length1, axis1, polya_point1,
         polyb_point1) = SAT.polygon_helper(shape_a, shape_b)
        (normal2, length2, axis2, polyb_point2,
         polya_point2) = SAT.polygon_helper(shape_b, shape_a)

        if axis1 + axis2 == len(polya.vertices()) + len(polyb.vertices()) - 2:
            result._is_colliding = True

        if length1 < length2:
            result._penetration = length1
            result._normal = normal1
        else:
            result._penetration = length2
            result.normal = normal2

    @staticmethod
    def polygon_vs_edge(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Polygon
        assert shape_b._shape.type() == Shape.Type.Edge
        return SATResult()

    @staticmethod
    def polygon_vs_capsule(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Polygon
        assert shape_b._shape.type() == Shape.Type.Capsule
        return SATResult()

    @staticmethod
    def polygon_vs_sector(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Polygon
        assert shape_b._shape.type() == Shape.Type.Sector
        return SATResult()

    @staticmethod
    def capsule_vs_edge(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Capsule
        assert shape_b._shape.type() == Shape.Type.Edge
        return SATResult()

    @staticmethod
    def capsule_vs_capsule(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Capsule
        assert shape_b._shape.type() == Shape.Type.Capsule
        return SATResult()

    @staticmethod
    def capsule_vs_sector(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Capsule
        assert shape_b._shape.type() == Shape.Type.Sector
        return SATResult()

    @staticmethod
    def sector_vs_sector(shape_a, shape_b):
        assert shape_a._shape.type() == Shape.Type.Sector
        assert shape_b._shape.type() == Shape.Type.Sector
        return SATResult()

    @staticmethod
    def _axis_projection(shape, fixme, normal):
        pass
