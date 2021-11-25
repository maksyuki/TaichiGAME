
class ContactGenerator():
    class ClipEdge():
        def __init__(self):
            self._p1 = Matrix([0.0, 0.0], 'vec')
            self._p2 = Matrix([0.0, 0.0], 'vec')
            self._normal = Matrix([0.0, 0.0], 'vec')

        def is_empty(self):
            return self._p1.is_origin() and self._p2.is_origin()
    
    @staticmethod
    def dump_vertices(primitive):
        vertices = []
        shape = primitive._shape
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


        vertices = [primitive.translate(v) for v in vertices]
        return vertices

    @staticmethod
    def find_clip_edge(vertices, index, normal):
        edge1 = ClipEdge()
        edge2 = ClipEdge()
        edge1._p2 = vertices[index]
        edge2._p1 = vertices[index]

        if index == 0:
            edge1._p1 = vertices[len(vertices)-2]
            edge2._p2 = vertices[index+1]

        elif index == len(vertices) - 1:
            edge1._p1 = vertices[index-1]
            edge2._p2 = vertices[1]
        else:
            edge1._p1 = vertices[index-1]
            edge2._p2 = vertices[index+1]

        final_edge = ClipEdge()
        if np.fabs((edge1._p2 - edge1._p1).dot(normal)) >= np.fabs((edge2._p2 - edge2._p1).dot(normal)):
            final_edge = edge2
            p = (edge2._p2 - edge2._p1).normal().perpendicular()
            if GeomAlgo2D.is_point_on_same_side(edge2._p1, edge2._p2, edge1._p1, edge2._p1 + p):
                final_edge._normal = p
            else:
                final_edge._normal = -p
        else:
            final_edge = edge1
            p = (edge1._p2 - edge1._p1).normal().perpendicular()
            if GeomAlgo2D.is_point_on_same_side(edge1._p1, edge1._p2, edge2._p1, edge1._p1 + p):
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

        # d1 = 