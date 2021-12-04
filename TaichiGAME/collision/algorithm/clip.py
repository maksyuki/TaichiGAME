class ContactGenerator():
    class ClipEdge():
        def __init__(self):
            self._p1 = Matrix([0.0, 0.0], 'vec')
            self._p2 = Matrix([0.0, 0.0], 'vec')
            self._normal = Matrix([0.0, 0.0], 'vec')

        def is_empty(self):
            return self._p1.is_origin() and self._p2.is_origin()

    @staticmethod
    def dump_vertices(prim):
        vertices = []
        shape = prim._shape
        shape_type = shape.type()

        if shape_type == Shape.Type.Capsule:
            vertices = shape.box_vertices()

        elif shape_type == Shape.Type.Polygon:
            vertices = shape.box_vertices()

        elif shape_type == Shape.Type.Edge:
            vertices.append(shape.start_point())
            vertices.append(shape.end_point())

        elif shape_type == Shape.Type.Sector:
            vertices = shape.vertices()

        vertices = [prim.translate(v) for v in vertices]
        return vertices

    @staticmethod
    def find_clip_edge(vertices, index, normal):
        edge1 = ClipEdge()
        edge2 = ClipEdge()
        edge1._p2 = vertices[index]
        edge2._p1 = vertices[index]

        if index == 0:
            edge1._p1 = vertices[len(vertices) - 2]
            edge2._p2 = vertices[index + 1]

        elif index == len(vertices) - 1:
            edge1._p1 = vertices[index - 1]
            edge2._p2 = vertices[1]
        else:
            edge1._p1 = vertices[index - 1]
            edge2._p2 = vertices[index + 1]

        final_edge = ClipEdge()
        if np.fabs((edge1._p2 - edge1._p1).dot(normal)) >= np.fabs(
            (edge2._p2 - edge2._p1).dot(normal)):
            final_edge = edge2
            p = (edge2._p2 - edge2._p1).normal().perpendicular()
            if GeomAlgo2D.is_point_on_same_side(edge2._p1, edge2._p2,
                                                edge1._p1, edge2._p1 + p):
                final_edge._normal = p
            else:
                final_edge._normal = -p
        else:
            final_edge = edge1
            p = (edge1._p2 - edge1._p1).normal().perpendicular()
            if GeomAlgo2D.is_point_on_same_side(edge1._p1, edge1._p2,
                                                edge2._p1, edge1._p1 + p):
                final_edge._normal = p
            else:
                final_edge._normal = -p

        return final_edge

    @staticmethod
    def dump_clip_edge(shape, vertices, normal):
        edge = ClipEdge()

        if len(vertices) == 2:
            edge._p1 = vertices[0]
            edge._p2 = vertices[1]

            if shape._shape.type() == Shape.Type.Edge:
                edge._normal = shape.normal()

        else:
            support, index = GJK.find_farthest_point(vertices, normal)
            edge = self.find_clip_edge(vertices, index, normal)

        return edge

    @staticmethod
    def recognize(shape_a, shape_b, normal):
        type_a = shape_a._shape.type()
        type_b = shape_b._shape.type()
        if type_a == Shape.Type.Point or type_a == Shape.Type.Circle or type_a == Shape.Type.Ellipse or type_b == Shape.Type.Point or type_b == Shape.Type.Circle or type_b == Shape.Type.Ellipse:
            return (ClipEdge, ClipEdge)

        vertices_a = self.dump_vertices(shape_a)
        vertices_b = self.dump_vertices(shape_b)
        edge_a = self.dump_clip_edge(shape_a, vertices_a, -normal)
        edge_b = self.dump_clip_edge(shape_b, vertices_b, -normal)

        return (edge_a, edge_b)

    @staticmethod
    def clip(clip_edge_a, clip_edge_b, normal):
        result = []
        if clip_edge_a.is_empty() or clip_edge_b.is_empty():
            return result

        d1 = Matrix(clip_edge_a._p1 - clip_edge_a._p2).dot(normal)
        d2 = Matrix(clip_edge_b._p1 - clip_edge_b._p2).dot(normal)
        reference_edge = clip_edge_a
        incident_edge = clip_edge_b
        swap = False

        if np.fabs(d1) > np.fabs(d2):
            reference_edge = clip_edge_b
            incident_edge = clip_edge_a
            swap = True

        u = (reference_edge._p2 - reference_edge._p1).normal()
        ref_anchor1 = u.perpendicular() + reference_edge._p1

        if not GeomAlgo2D.is_point_on_same_side(
                reference_edge._p1, ref_anchor1, reference_edge._p2,
                incident_edge._p1):
            incident_edge._p1 = GeomAlgo2D.line_intersection(
                reference_edge._p1, ref_anchor1, incident_edge._p1,
                incident_edge._p2)

        if not GeomAlgo2D.is_point_on_same_side(
                reference_edge._p1, ref_anchor1, reference_edge._p2,
                incident_edge._p2):
            incident_edge._p2 = GeomAlgo2D.line_intersection(
                reference_edge._p1, ref_anchor1, incident_edge._p1,
                incident_edge._p2)

        u.negate()
        if not GeomAlgo2D.is_point_on_same_side(
                reference_edge._p2, ref_anchor2, reference_edge._p1,
                incident_edge._p1):
            incident_edge._p1 = GeomAlgo2D.line_intersection(
                reference_edge._p2, ref_anchor2, incident_edge._p1,
                incident_edge._p2)

        if not GeomAlgo2D.is_point_on_same_side(
                reference_edge._p2, ref_anchor2, reference_edge._p1,
                incident_edge._p2):
            incident_edge._p2 = GeomAlgo2D.line_intersection(
                reference_edge._p2, ref_anchor2, incident_edge._p1,
                incident_edge._p2)

        ref_anchor3 = (reference_edge._p2 +
                       reference_edge._p1) / 2.0 + reference_edge._normal

        p1_on_clip_area = GeomAlgo2D.is_point_on_same_side(
            reference_edge._p1, reference_edge._p2, ref_anchor3,
            incident_edge._p1)
        p2_on_clip_area = GeomAlgo2D.is_point_on_same_side(
            reference_edge._p1, reference_edge._p2, ref_anchor3,
            incident_edge._p2)

        if not (p1_on_clip_area and p2_on_clip_area):
            return result

        if p1_on_clip_area and not p2_on_clip_area:
            incident_edge._p2 = GeomAlgo2D.line_intersection(
                reference_edge._p1, reference_edge._p2, incident_edge._p1,
                incident_edge._p2)

        if not p1_on_clip_area and p2_on_clip_area:
            incident_edge._p1 = GeomAlgo2D.line_intersection(
                reference_edge._p1, reference_edge._p2, incident_edge._p1,
                incident_edge._p2)

        pp1 = GeomAlgo2D.point_to_line_segment(reference_edge._p1,
                                               reference_edge._p2,
                                               incident_edge._p1)
        pp2 = GeomAlgo2D.point_to_line_segment(reference_edge._p1,
                                               reference_edge._p2,
                                               incident_edge._p2)

        pair1 = PointPair()
        pair2 = PointPair()

        if not swap:
            pair1._pa = pp1
            pair1._pb = incident_edge._p1
            pair2._pa = pp2
            pair2._pb = incident_edge._p2
        else:
            pair1._pa = incident_edge._p1
            pair1._pb = pp1
            pair2._pa = incident_edge._p2
            pair2._pb = pp2

        result.append(pair1)
        result.append(pair2)
        return result
