from TaichiGAME.math.matrix import Matrix
from TaichiGAME.common.config import Config
from typing import List, Dict, Optional, Tuple

import numpy as np

from ..broad_phase.aabb import AABB
from ...dynamics.body import Body
from ..detector import Detector
from ..broad_phase.dbvh import DBVH


class CCD():
    '''Continuous Collision Detection

    This class is implemented by bisection and re-sampling. Both them are costly.
    '''
    class AABBShot():
        def __init__(self,
                     box: AABB,
                     attr: Body.PhysicsAttribute,
                     t: float = 0.0):
            self._aabb: AABB = box
            self._attr: Body.PhysicsAttribute = attr
            self._time: float = t

    class IndexSection():
        def __init__(self):
            self._forward: int = -1
            self._backward: int = -1

    class CCDPair():
        def __init__(self, time: float = 0.0, target: Body = None):
            self._toi: float = time
            self._body: Optional[Body] = target

    @staticmethod
    def build_trajectory_aabb(
            body: Body,
            dt: float,
            target: Optional[Matrix] = None) -> Tuple[List[AABBShot], AABB]:
        assert body != None

        traj = []  # HACK: add type hint
        res: AABB = AABB()

        start: Body.PhysicsAttribute = body.phy_attr
        start_box: AABB = AABB.from_body(body)

        # run a dt step
        body.step_position(dt)

        # end: Body.PhysicsAttribute= body.phy_attr
        end_box: AABB = AABB.from_body(body)

        if start_box == end_box and start._vel.len_square(
        ) < Config.MaxVelocity and np.fabs(
                start._ang_vel) < Config.MaxAngularVelocity:
            traj.append(CCD.AABBShot(start_box, body.phy_attr, 0))
            traj.append(CCD.AABBShot(end_box, body.phy_attr, dt))
            return (traj, res)

        res.unite(start_box).unite(end_box)
        body.phy_attr = start

        slice: float = 40.0
        step: float = dt / slice
        idx: float = step
        while idx <= dt:
            body.step_position(step)
            aabb: AABB = AABB.from_body(body)
            traj.append(CCD.AABBShot(aabb, body.phy_attr, idx))
            res.unite(aabb)
            idx += step
            if target != None and (aabb.pos - target).len_square() >= (
                    target - start._pos).len_square():
                break

        body.phy_attr = start
        return (traj, res)

    @staticmethod
    def find_broad_phase_root(bodya: Body, traja: List[AABBShot], bodyb: Body,
                              trajb: List[AABBShot],
                              dt: float) -> Optional[IndexSection]:
        assert bodya != None and bodyb != None
        is_bodya_ccd: bool = len(traja) > 2
        is_bodyb_ccd: bool = len(trajb) > 2

        if is_bodya_ccd and is_bodyb_ccd:
            traj1: AABB = AABB.unite(traja[0]._aabb,
                                     traja[len(traja) - 1]._aabb)
            traj2: AABB = AABB.unite(trajb[0]._aabb,
                                     trajb[len(trajb) - 1]._aabb)

            if not traj1.collide(traj2):
                return None

            length: int = np.fmin(len(traja), len(trajb))
            res: CCD.IndexSection = CCD.IndexSection()

            for i in range(length - 1):
                tmp1: AABB = AABB.unite(traja[i]._aabb, traja[i + 1]._aabb)
                tmp2: AABB = AABB.unite(trajb[i]._aabb, trajb[i + 1]._aabb)
                if tmp1.collide(tmp2):
                    res._forward = i
                    break

            return None if res._forward == -1 else res

        elif not is_bodya_ccd or not is_bodyb_ccd:
            traj_static: Optional[List[CCD.AABBShot]] = None
            traj_dynamic: Optional[List[CCD.AABBShot]] = None

            if is_bodya_ccd:
                traj_static = trajb
                traj_dynamic = traja
            elif is_bodyb_ccd:
                traj_static = traja
                traj_dynamic = trajb

            traj1: AABB = AABB.unite(
                traj_static.at(0)._aabb,
                traj_static.at(1)._aabb)
            traj2: AABB = AABB.unite(
                traj_dynamic.at(0)._aabb,
                traj_dynamic.at(len(traj_dynamic) - 1)._aabb)

            if not traj1.collide(traj2):
                return None

            res: CCD.IndexSection = CCD.IndexSection()
            length: int = len(traj_dynamic)
            forward_found: bool = False
            backward_found: bool = False

            j: int = length - 1
            for i in range(length) - 1:
                tmp_forward: AABB = AABB.unite(
                    traj_dynamic.at(i)._aabb,
                    traj_dynamic.at(i + 1)._aabb)

                tmp_backward: AABB = AABB.unite(
                    traj_dynamic.at(j)._aabb,
                    traj_dynamic.at(j - 1)._aabb)

                if tmp_forward.collide(traj1) and not forward_found:
                    res._forward = i
                    forward_found = True

                if tmp_backward.collide(traj1) and not backward_found:
                    res._backward = j
                    backward_found = True

                if forward_found and backward_found:
                    break

                j -= 1

            return None if res._forward == -1 else res

        return None

    @staticmethod
    def find_narrow_phase_root(bodya: Body, traja: List[AABBShot], bodyb: Body,
                               trajb: List[AABBShot], idx: IndexSection,
                               dt: float) -> Optional[float]:
        assert bodya != None and bodyb != None

        is_bodya_ccd: bool = len(traja) > 2
        is_bodyb_ccd: bool = len(trajb) > 2
        if is_bodya_ccd and is_bodyb_ccd:
            return None

        elif not is_bodya_ccd or not is_bodyb_ccd:
            dynamic_body: Body = None
            origin1: Body.PhysicsAttribute = bodya.phy_attr
            origin2: Body.PhysicsAttribute = bodyb.phy_attr

            start_timestep: float = 0.0
            end_timestep: float = 0.0

            if is_bodya_ccd:
                dynamic_body = bodya
                bodya.phy_attr = traja[idx._forward]._attr
                start_timestep = traja[idx._forward]._time
                end_timestep = traja[idx._backward]._time

            elif is_bodyb_ccd:
                dynamic_body = bodyb
                bodyb.phy_attr = trajb[idx._forward]._attr
                start_timestep = trajb[idx._forward]._time
                end_timestep = trajb[idx._backward]._time

            # slice maybe 25~70. It depends on how thin the sticks you set
            slice: float = 30.0
            step: float = (end_timestep - start_timestep) / slice
            forward_steps: float = 0

            last_attr: Body.PhysicsAttribute = Body.PhysicsAttribute()
            is_find: bool = False

            while start_timestep + forward_steps <= end_timestep:
                last_attr = dynamic_body.phy_attr
                dynamic_body.step_position(step)
                forward_steps += step

                res: Optional[bool] = Detector.collide(bodya, bodyb)

                if res != None:
                    forward_steps -= step
                    dynamic_body.phy_attr = last_attr
                    is_find = True
                    break

            if not is_find:
                bodya.phy_attr = origin1
                bodyb.phy_attr = origin2
                return None

            # retracing
            step /= 2.0
            epsilon: float = 0.01

            while start_timestep + forward_steps <= end_timestep:
                last_attr = dynamic_body.phy_attr
                dynamic_body.step_position(step)
                forward_steps += step

                res = Detector.detect(bodya, bodyb)
                if res._is_colliding:
                    if np.fabs(res._penetration) < epsilon:
                        bodya.phy_attr = origin1
                        bodyb.phy_attr = origin2
                        return start_timestep + forward_steps

                    forward_steps -= step
                    dynamic_body.phy_attr = last_attr
                    step /= 2.0

        return None

    @staticmethod
    def query(root: DBVH.Node, body: Optional[Body],
              dt: float) -> Optional[List[CCDPair]]:
        assert root.is_root() and body != None

        query_list: List[CCD.CCDPair] = []
        potential: List[DBVH.Node] = []
        (traj_ccd, aabb_ccd) = CCD.build_trajectory_aabb(body, dt)

        DBVH.query_nodes(root, aabb_ccd, potential, body)

        for elem in potential:
            (traj_elem, aabb_elem) = CCD.build_trajectory_aabb(elem._body, dt)
            (new_ccd_tarj,
             new_aabb) = CCD.build_trajectory_aabb(body, dt,
                                                   elem._body.position())
            res: Optional[CCD.IndexSection] = CCD.find_broad_phase_root(
                body, new_ccd_tarj, elem._body, traj_elem, dt)

            if res != None:
                toi: Optional[float] = CCD.find_narrow_phase_root(
                    body, new_ccd_tarj, elem._body, traj_elem, res, dt)
                if toi != None:
                    query_list.append(CCD.CCDPair(toi, elem._body))

        return query_list if len(query_list) > 0 else None
