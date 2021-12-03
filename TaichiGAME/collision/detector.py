class Collsion():
    def __init__(self):
        self._is_colliding = False
        self._bodya = None
        self._bodyb = None
        self._contact_list = []
        self._normal = Matrix([0.0, 0.0], 'vec')
        self._penetration = 0.0


class Detector():
    def __init__(self):
        pass

    @staticmethod
    def collide(bodya, bodyb):
        assert bodya != None and bodyb != None
        shapea = ShapePrimitive()
        shapeb = ShapePrimitive()

        shapea._shape = bodya.shape()
        shapea._rot = bodya.rotation()
        shapea._xform = bodya.position()

        shapeb._shape = bodyb.shape()
        shapeb._rot = bodyb.rotation()
        shapeb._xform = bodyb.position()

        (is_colliding, simplex) = GJK.gjk(shapea, shapeb)
        if shapea._xform == shapeb._xform and not is_colliding:
            is_colliding = simplex.contain_origin(True)

        return is_colliding

    @staticmethod
    def detect(bodya, bodyb):
        result = Collsion()

        if bodya == None or bodyb == None:
            return result

        if bodya == bodyb:
            return result

        if bodya.id() > bodyb.id():
            tmp = bodya
            bodya = bodyb
            bodyb = tmp

        result._bodya = bodya
        result._bodyb = bodyb

        shapea = ShapePrimitive()
        shapeb = ShapePrimitive()

        shapea._shape = bodya.shape()
        shapea._rot = bodya.rotation()
        shapea._xform = bodya.position()

        shapeb._shape = bodyb.shape()
        shapeb._rot = bodyb.rotation()
        shapeb._xform = bodyb.position()

        (is_colliding, simplex) = GJK.gjk(shapea, shapeb)
        if shapea._xform == shapeb._xform and not is_colliding:
            is_colliding = simplex.contain_origin(True)

        result._is_colliding = is_colliding
        if is_colliding:
            old_simplex = simplex
            simpelx = GJK.epa(shapea, shapeb, simplex)
            source = GJK.dump_source()

            info = GJK.dump_info()
            result._normal = info._normal
            result._penetration = info._penetration

            (clip_edge_a,
             clip_edge_b) = ContactGenerator.recognize(shapa, shape,
                                                       info._normal)
            pair_list = ContactGenerator.clip(clip_edge_a, clip_edge_b,
                                              info._normal)

            val_pass = False
            for elem in pair_list:
                # FIXME:
                if (elem._pointa - elem._pointb).len_square(
                ) == result._penetration * result._penetration:
                    val_pass = True

                if val_pass:
                    result._contact_list = pair_list
                else:
                    result._contact_list.append(GJK.dump_points(source))

            assert len(result._contact_list) != 3
            return result

    @staticmethod
    def distance(bodya, bodyb):
        result = PointPair()
        if bodya == None or bodyb == None:
            return result

        if bodya == bodyb:
            return result

        shapea = ShapePrimitive()
        shapeb = ShapePrimitive()

        shapea._shape = bodya.shape()
        shapea._rot = bodya.rotation()
        shapea._xform = bodya.position()

        shapeb._shape = bodyb.shape()
        shapeb._rot = bodyb.rotation()
        shapeb._xform = bodyb.position()
        return GJK.distance(shapea, shapeb)
