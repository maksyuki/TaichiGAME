from TaichiGAME.dynamics.joint.rotation import RotationJointPrimitive
from typing import IO, List, Dict, Optional, Tuple, Union

from ..math.matrix import Matrix
from ..dynamics.body import Body
from .joint.joint import Joint
from .joint.distance import DistanceJoint, DistanceJointPrimitive
from .joint.point import PointJoint, PointJointPrimitive
from .joint.pulley import PulleyJoint, PulleyJointPrimitive
from .joint.revolute import RevoluteJoint, RevoluteJointPrimitive
from .joint.rotation import OrientationJoint, OrientationJointPrimitive, RotationJoint


class PhysicsWorld():
    def __init__(self):
        self._gravity: Matrix = Matrix([0.0, -1.0], 'vec')
        self._linear_vel_damping: float = 0.9
        self._ang_vel_damping: float = 0.9
        self._linear_vel_threshold: float = 0.02
        self._ang_vel_threshold: float = 0.02
        self._air_fric_coeff: float = 0.7

        self._bias: float = 0.8
        self._vel_iter: int = 1
        self._pos_iter: int = 1

        self._grav_ena: bool = True
        self._damping_ena: bool = True
        self._body_list: List[Body] = []
        self._joint_list: List[Joint] = []

    def prepare_velocity_constraint(self, dt: float):
        for joint in self._joint_list:
            if joint.active:
                joint.prepare(dt)

    def step_velocity(self, dt: float):
        g: Matrix = self._gravity if self._grav_ena else Matrix([0.0, 0.0],
                                                                'vec')
        lvd: float = 1.0
        avd: float = 1.0

        if self._damping_ena:
            lvd = 1.0 / (1.0 + dt * self._linear_vel_damping)
            avd = 1.0 / (1.0 + dt * self._ang_vel_damping)

        for body in self._body_list:
            if body.type == Body.Type.Static:
                body.vel.clear()
                body.ang_vel = 0.0

            elif body.type == Body.Type.Dynamic:
                body.forces += body.mass * g
                body.vel += body.inv_mass * body.forces * dt
                body.ang_vel += body.inv_inertia * body.torques * dt

                body.vel *= lvd
                body.ang_vel *= avd

            elif body.type == Body.Type.Kinematic:
                body.vel += body.inv_mass * body.forces * dt
                body.ang_vel += body.inv_inertia * body.torques * dt

                body.vel *= lvd
                body.ang_vel *= avd

            elif body.type == Body.Type.Bullet:
                pass

    def solve_velocity_constraint(self, dt: float):
        for joint in self._joint_list:
            if joint.active:
                joint.solve_velocity(dt)

    def stepPosition(self, dt: float):
        for body in self._body_list:
            if body.type == Body.Type.Static:
                pass
            elif body.type == Body.Type.Dynamic:
                body.pos += body.vel * dt
                body.rot += body.ang_vel * dt
                body.forces.clear()
                body.clear_torque()

            elif body.type == Body.Type.Kinematic:
                body.pos += body.vel * dt
                body.rot += body.ang_vel * dt
                body.forces.clear()
                body.clear_torque()

            elif body.type == Body.Type.Bullet:
                pass

    def solve_position_constraint(self, dt: float):
        for joint in self._joint_list:
            if joint.active:
                joint.solve_position(dt)

    @property
    def grav(self) -> Matrix:
        return self._gravity

    @grav.setter
    def grav(self, grav: Matrix):
        self._gravity = grav

    @property
    def lin_vel_damping(self) -> float:
        return self._linear_vel_damping

    @lin_vel_damping.setter
    def lin_vel_damping(self, lin_vel_damping: float):
        self._linear_vel_damping = lin_vel_damping

    @property
    def ang_vel_damping(self) -> float:
        return self._ang_vel_damping

    @ang_vel_damping.setter
    def ang_vel_damping(self, ang_vel_damping: float):
        self._ang_vel_damping = ang_vel_damping

    @property
    def lin_vel_thold(self) -> float:
        return self._linear_vel_threshold

    @lin_vel_thold.setter
    def lin_vel_thold(self, lin_vel_thold: float):
        self._linear_vel_threshold = lin_vel_thold

    @property
    def ang_vel_thold(self) -> float:
        return self._ang_vel_threshold

    @ang_vel_thold.setter
    def ang_vel_thold(self, ang_vel_thold: float):
        self._ang_vel_threshold = ang_vel_thold

    @property
    def air_fric_coeff(self) -> float:
        return self._air_fric_coeff

    @air_fric_coeff.setter
    def air_fric_coeff(self, air_fric_coeff: float):
        self._air_fric_coeff = air_fric_coeff

    @property
    def bias(self) -> float:
        return self._bias

    @bias.setter
    def bias(self, bias: float):
        self._bias = bias

    @property
    def vel_iter(self) -> int:
        return self._vel_iter

    @vel_iter.setter
    def vel_iter(self, vel_iter: int):
        self._vel_iter = vel_iter

    @property
    def pos_iter(self) -> int:
        return self._pos_iter

    @pos_iter.setter
    def pos_iter(self, pos_iter: int):
        self._pos_iter = pos_iter

    @property
    def grav_ena(self) -> bool:
        return self._grav_ena

    @grav_ena.setter
    def grav_ena(self, grav_ena: bool):
        self._grav_ena = grav_ena

    @property
    def damping_ena(self) -> bool:
        return self._damping_ena

    @damping_ena.setter
    def damping_ena(self, damping_ena: bool):
        self._damping_ena = damping_ena

    def create_body(self) -> Body:
        body: Body = Body()
        body.id = 6  # FIXME: need to gen by random module
        self._body_list.append(body)
        return body

    def create_joint(
        self, prim: Union[RotationJointPrimitive, PointJointPrimitive,
                          DistanceJointPrimitive, PulleyJointPrimitive,
                          RevoluteJointPrimitive, OrientationJointPrimitive]
    ) -> Joint:

        joint: Joint = None
        if isinstance(prim, RotationJointPrimitive):
            joint = RotationJoint(prim)
        elif isinstance(prim, PointJointPrimitive):
            joint = PointJoint(prim)
        elif isinstance(prim, DistanceJointPrimitive):
            joint = DistanceJoint(prim)
        elif isinstance(prim, PulleyJointPrimitive):
            joint = PulleyJoint(prim)
        elif isinstance(prim, RevoluteJointPrimitive):
            joint = RevoluteJoint(prim)
        elif isinstance(prim, OrientationJointPrimitive):
            joint = OrientationJoint(prim)

        joint.id = 6  # FIXME:
        self._joint_list.append(joint)
        return joint

    def remove_body(self, body: Body):
        for b in self._body_list:
            if body == b:
                #FIXME:
                self._body_list.remove(body)
                break

    def remove_joint(self, joint: Joint):
        for j in self._joint_list:
            if joint == j:
                #FIXME:
                self._joint_list.remove(joint)

    def clear_all_bodies(self):
        self._body_list.clear()

    def clear_all_joints(self):
        self._joint_list.clear()
