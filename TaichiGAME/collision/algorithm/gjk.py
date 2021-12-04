class Minkowski():
    def __init__(self, pa, pb):
        self._pa = pa
        self._pb = pb
        self._result = self._pa - self._pb

    def __eq__(self, other):
        return self._pa == other._pa and self._pb == other._pb

    def __ne__(self, other):
        return not (self._pa == other._pa
                    and self._pb == other._pb)


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
        self._pa = Matrix([0.0, 0.0], 'vec')
        self._pb = Matrix([0.0, 0.0], 'vec')

    def __eq__(self, other):
        return self._pa == other._pa and self._pb == other._pb

    def is_empty(self):
        return self._pa == Matrix(
            [0.0, 0.0], 'vec') and self._pb == Matrix([0.0, 0.0], 'vec')


class GJK():
    def __init__(self):
        pass

    @staticmethod
    def gjk(shape_a, shape_b, iter_val=20):
        simplex = Simplex()
        is_found = False
        direction = shape_a._xform - shape_b._xform

        if direction == Matrix([0.0, 0.0], 'vec'):
            direction.set_value([1.0, 1.0])

        diff = self.support(shape_a, shape_b, direction)
        simplex._vertices.append(diff)
        direction.negate()

        removed = []
        for i in range(iter_val):
            diff = self.support(shape_a, shape_b, direction)
            simplex._vertices.append(diff)
            if len(simplex._vertices == 3):
                simplex._vertices.append(simplex._vertices[0])

            if simplex.last_vertex().dot(direction) <= 0:
                break

            if simplex.contain_origin(True):
                is_found = True
                break

            (index1, index2) = self.find_edge_closest_to_origin(simplex)
            direction = calc_direction_by_edge(
                simplex._vertices[index1]._result,
                simplex._vertices[index2]._result, True)

            result = self.adjust_simplex(simplex, index1, index2)

            if result != None:
                for v in removed:
                    if v == result:
                        break

                removed.append(result)

        return (is_found, simplex)

    @staticmethod
    def epa(shape_a, shape_b, src, iter_val=20):
        edge = Simplex()
        simplex = src
        normal = Matrix([0.0, 0.0], 'vec')
        p = Minkowski()

        for i in rnage(iter_val):
            (index1, index2) = self.find_edge_closest_to_origin(simplex)
            normal = self.calc_direction_by_edge(
                simplex._vertices[index1]._result,
                simplex._vertices[index2]._result, False).normal()

            if GeomAlgo2D.is_point_on_segment(
                    simplex._vertices[index1]._result,
                    simplex._vertices[index2]._result, [0.0, 0.0]):
                normal.negate()

            p = self.support(shape_a, shape_b, normal)

            if simplex.contains(p):
                break

            simplex.insert(index1, p)

        return simplex

    @staticmethod
    def dump_info(src):
        result = PenetrationInfo()
        edge1 = src._a1 - src._b1
        edge2 = src._a2 - src._b2
        normal = calc_direction_by_edge(edge1, edge2, False).normal()
        origin_to_edge = np.fabs(normal.dot(edge1))
        result.normal = normal.negate()
        result.penetration = origin_to_edge
        return res

    @staticmethod
    def support(shape_a, shape_b, dir):
        return Minkowski(self.find_farthest_point(shape_a, dir),
                         find_farthest_point(shape_b, -dir))

    @staticmethod
    def find_edge_closest_to_origin(simplex):
        index1 = 0
        index2 = 0
        min_dist = 2222222222  # FIXME:

        if len(simplex._vertices) == 2:
            return (0, 1)

        # FIXME: need to improve perf
        for i in range(len(simplex.vertices) - 1):
            a = simplex._vertices[i]._result
            b = simplex._vertices[i + 1]._result

            p = GeomAlgo2D.point_to_line_segment(a, b, [0.0, 0.0])
            projection = p.len()

            if min_dist > projection:
                index1 = i
                index2 = i + 1
                min_dist = projection
            elif np.isclose(min_dist, projection):
                length1 = a.len_square() + b.len_square()
                length2 = simplex._vertices[index1]._result.len_square(
                ) + simplex._vertices[index2]._result.len_square()

                if length1 < length2:
                    index1 = i
                    index2 = i + 1

        return (index1, index2)

    @staticmethod
    def find_farthest_point(shape, dir):
        pass

    @staticmethod
    def adjust_simplex(simplex, closest_1, closest_2):
        if len(simplex._vertices) == 4:
            index = -1
            for i in range(simplex._vertices - 1):
                if i != closest_1 and i != closest_2:
                    index = i

            target = simplex._vertices[index]
            del simplex._vertices[index]
            del simplex._vertices[len(simplex._vertices) - 1]
            return target

        return None

    @staticmethod
    def calc_direction_by_edge(p1, p2, point_to_origin=True):
        ao = -1 * p1
        ab = p2 - p1
        perpendicular_of_ab = ab.perpendicular()

        if (Matrix.dot_product(ao, perpendicular_of_ab) < 0 and point_to_origin
            ) or (Matrix.dot_product(ao, perpendicular_of_ab) > 0
                  and not point_to_origin):
            perpendicular_of_ab.negate()

        return perpendicular_of_ab

    @staticmethod
    def distance(shape_a, shape_b, iter_val=20):
        result = PointPair()
        simplex = Simplex()
        direction = shape_b._xform - shape_a._xform

        m = self.support(shape_a, shape_b, direction)
        simplex._vertices.append(m)
        direction.negate()
        for i in range(iter_val):
            direction = self.calc_direction_by_edge(
                simplex._vertices[0]._result, simplex._vertices[1]._result,
                True)
            m = self.support(shape_a, shape_b, direction)

            if simplex.contains(m):
                break

            simplex._vertices.append(m)
            simplex._vertices.append(simplex._vertices[0])
            (index1, index2) = self.find_edge_closest_to_origin(simplex)
            self.adjust_simplex(simplex, index1, index2)

        return self.dump_points(self.dump_source(simplex))

    @staticmethod
    def dump_source(simplex):
        result = PenetrationSource
        (index1, index2) = self.find_edge_closest_to_origin(simplex)
        result._a1 = simplex._vertices[index1]._pa
        result._a2 = simplex._vertices[index2]._pa
        result._b1 = simplex._vertices[index1]._pb
        result._b2 = simplex._vertices[index2]._pb
        return result

    @staticmethod
    def dump_points(src):
        result = PointPair()
        a_s1 = src._a1
        b_s1 = src._a2
        a_s2 = src._b1
        b_s2 = src._b2

        a = src._a1 - src._b1
        b = src._a2 - src._b2
        l = b - a
        ll = l.dot(l)
        la = l.dot(a)
        lambda2 = -la / ll
        lambda1 = 1 - lambda2

        result._pa.set_value(lambda1 * a_s1 + lambda2 * b_s1)
        result._pb.set_value(lambda1 * a_s2 + lambda2 * b_s2)

        if l == Matrix([0.0, 0.0], 'vec') or lambda2 < 0:
            result._pa.set_value(a_s1)
            result._pb.set_value(a_s2)

        if lambda1 < 0:
            result._pa.set_value(b_s1)
            result._pb.set_value(b_s2)

        return result
