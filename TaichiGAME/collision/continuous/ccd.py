class CCD():
    def __init__(self):
        broad_phase_trajectory = []

    class AABBShot():
        def __init__(self, box, attr, t=0):
            self._aabb = box
            self._attribute = attr
            self._time = t

    class IndexSection():
        def __init__(self):
            self._forward = -1
            self._backward = -1

    class CCDPair():
        def __init__(self, time=0.0, target=None):
            self._toi = time
            self._body = target
    
    # FIXME:
    @staticmethod
    def build_trajectory_aabb(body, dt):
        assert body != None
    
    @staticmethod
    def find_broad_phase_root(body1, trajectory1, body2, trajectory2, dt):
        assert body1 != None and body2 != None
        is_body1_ccd = len(trajectory1) > 2
        is_body2_ccd = len(trajectory2) > 2
        
        if is_body1_ccd and is_body2_ccd:
                traj1 = AABB.unite(trajectory1[0]._aabb, trajectory1[len(trajectory1)-1]._aabb)
                traj2 = AABB.unite(trajectory2[0]._aabb, trajectory2[len(trajectory2)-1]._aabb)

                if not traj1.collide(traj2):
                    return None
                
                length = len(trajectory2) if len(trajectory1) > len(trajectory2) else len(trajectory1)
                result = IndexSection()

                for i in range(length - 1):
                    tmp1 = AABB.unite(trajectory1[i]._aabb, trajectory1[i+1]._aabb)
                    tmp2 = AABB.unite(trajectory2[i]._aabb, trajectory2[i+1]._aabb)
                    if tmp1.collide(tmp2):
                        result._forward = i
                        break
                    
                return None if result._forward == -1 else result
        elif not is_body1_ccd or not is_body2_ccd:
            traj_static = None
            traj_dynamic = None

            if is_body1_ccd:
                traj_static = trajectory2
                traj_dynamic = trajectory1
            elif is_body2_ccd:
                traj_static = trajectory1
                traj_dynamic = trajectory2
            
            traj1 = AABB.unite(traj_static.at(0)._aabb, traj_static.at(1)._aabb)
            traj2 = AABB.unite(traj_dynamic.at(0)._aabb, traj_dynamic.at(len(traj_dynamic) - 1)._aabb)

            if not traj1.collide(traj2):
                return None

            result = IndexSection()
            length = len(traj_dynamic)
            forward_found = False
            backward_found = False
            



    @staticmethod
    def find_narrow_phase_root(body1, traj1, body2, traj2, index, dt):
        pass

    @staticmethod
    def query(root, body, dt):
        pass
    
