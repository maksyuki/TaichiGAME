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
            traj1 = AABB.unite(trajectory1[0]._aabb,
                               trajectory1[len(trajectory1) - 1]._aabb)
            traj2 = AABB.unite(trajectory2[0]._aabb,
                               trajectory2[len(trajectory2) - 1]._aabb)

            if not traj1.collide(traj2):
                return None

            length = len(trajectory2) if len(trajectory1) > len(
                trajectory2) else len(trajectory1)
            result = IndexSection()

            for i in range(length - 1):
                tmp1 = AABB.unite(trajectory1[i]._aabb,
                                  trajectory1[i + 1]._aabb)
                tmp2 = AABB.unite(trajectory2[i]._aabb,
                                  trajectory2[i + 1]._aabb)
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

            traj1 = AABB.unite(
                traj_static.at(0)._aabb,
                traj_static.at(1)._aabb)
            traj2 = AABB.unite(
                traj_dynamic.at(0)._aabb,
                traj_dynamic.at(len(traj_dynamic) - 1)._aabb)

            if not traj1.collide(traj2):
                return None

            result = IndexSection()
            length = len(traj_dynamic)
            forward_found = False
            backward_found = False

            j = length - 1
            for i in range(length) - 1:
                tmp_forward = AABB.unite(
                    traj_dynamic.at(i)._aabb,
                    traj_dynamic.at(i + 1)._aabb)
                tmp_backward = AABB.unite(
                    traj_dynamic.at(j)._aabb,
                    traj_dynamic.at(j - 1)._aabb)

                if tmp_forward.collide(traj1) and not forward_found:
                    result._forward = i
                    forward_found = True

                if tmp_backward.collide(traj1) and not backward_found:
                    result._backward = _join
                    backward_found = True

                if forward_found and backward_found:
                    break

                j -= 1

            return None if result._forward == -1 else result

        return None

    @staticmethod
    def find_narrow_phase_root(body1, trajectory1, body2, trajectory2, index,
                               dt):
        assert body1 != None and body2 != None

        is_body1_ccd = len(trajectory1) > 2
        is_body2_ccd = len(trajectory2) > 2
        if is_body1_ccd and is_body2_ccd:
            return None

        elif not is_body1_ccd or not is_body2_ccd:
            dynamic_body = None
            origin1 = body1.phsics_attribute()
            origin2 = body2.phsics_attribute()

            start_timestep = 0.0
            end_timestep = 0.0

            if is_body1_ccd:
                dynamic_body = body1
                body1.set_physics_attribute(
                    trajectory1[index._forward]._attribute)
                start_timestep = trajectory1[index._forward]._time
                end_timestep = trajectory1[index._backward]._time

            elif is_body2_ccd:
                dynamic_body = body2
                body2.set_physics_attribute(
                    trajectory2[index._forward]._attribute)
                start_timestep = trajectory2[index._forward]._time
                end_timestep = trajectory2[index._backward]._time

            val_slice = 30.0
            step = (end_timestep - start_timestep) / val_slice
            forward_steps = 0
            last_attribute = Body.physic_attribute()
            is_find = False

            while start_timestep + forward_steps <= end_timestep:
                last_attribute = dynamic_body.physic_attribute()
                dynamic_body.step_position(step)
                forward_steps += step

                result = Detector.collide(body1, body2)
                #FIXME:
                if result != None:
                    forward_steps -= step
                    dynamic_body.set_physics_attribute(last_attribute)
                    is_find = True
                    break

            if not is_find:
                body1.set_physics_attribute(origin1)
                body2.set_physics_attribute(origin2)
                return None

            step /= 2.0
            epsilon = 0.0
            while start_timestep + forward_steps <= end_timestep:
                last_attribute = dynamic_body.physic_attribute()
                dynamic_body.step_position(step)
                forward_steps += step

                result = Detector.detect(body1, body2)
                if result.is_colliding:
                    if np.fabs(result._penetration) < epsilon:
                        body1.set_physics_attribute(origin1)
                        body2.set_physics_attribute(origin2)
                        return start_timestep + forward_steps

                    forward_steps -= step
                    dynamic_body.set_physics_attribute(last_attribute)
                    step /= 2.0

        return None

    @staticmethod
    def query(root, body, dt):
        assert root.is_root() and body != None

        (trajectory_ccd, aabb_ccd) = self.build_trajectory_aabb(body, dt)
        query_list = []
        potential = []
        DBVH._query_nodes(root, aabb_ccd, potential, body)

        for elem in potential:
            (trajectory_element,
             aabb_element) = self.build_trajectory_aabb(elem._body, dt)
            (new_ccd_tarjectory,
             new_aabb) = self.build_trajectory_aabb(body,
                                                    elem._body.position(), dt)
            result = self.find_broad_phase_root(body, new_ccd_tarjectory,
                                                elem._body, trajectory_element,
                                                dt)

            if result != None:
                toi = self.find_narrow_phase_root(body, new_ccd_tarjectory,
                                                  elem._body,
                                                  trajectory_element, result,
                                                  dt)
                if toi != None:
                    query_list.append(CCDPair(toi, elem._body))

        return query_list if not query_list.empty() else None
