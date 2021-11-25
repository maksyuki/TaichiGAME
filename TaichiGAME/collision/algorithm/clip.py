
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
        pass

    @staticmethod
    def find_clip_edge(vertices, index, normal):
        pass

    @staticmethod
    def dump_clip_edge(shape, vertices, normal):
        pass

    @staticmethod
    def recognize(shape_a, shape_b, normal):
        pass
    
    @staticmethod
    def clip(clip_edge_a, clip_edge_b, normal):
        pass