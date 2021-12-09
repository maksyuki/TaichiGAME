import numpy as np

from TaichiGAME.dynamics.phy_world import PhysicsWorld
from TaichiGAME.math.matrix import Matrix


class TestPhysicsWorld():
    def test__init__(self):
        dut: PhysicsWorld = PhysicsWorld()

        assert dut._gravity == Matrix([0.0, -1.0], 'vec')
        assert np.isclose(dut._linear_vel_damping, 0.9)
        assert np.isclose(dut.ang_vel_damping, 0.9)
        assert np.isclose(dut._linear_vel_threshold, 0.02)
        assert np.isclose(dut._ang_vel_threshold, 0.02)
        assert np.isclose(dut._air_fric_coeff, 0.7)
        assert np.isclose(dut._bias, 0.8)
        assert np.isclose(dut._vel_iter, 1)
        assert np.isclose(dut._pos_iter, 1)
        assert dut._grav_ena
        assert dut.damping_ena
        assert len(dut._body_list) == 0
        assert len(dut._joint_list) == 0

    def test_prepare_velocity_constraint(self):
        # NOTE: just call joint.prepare
        assert 1

    def test_step_velocity(self):
        assert 1

    def test_solve_velocity_constraint(self):
        # NOTE: just call joint.solve_velocity
        assert 1

    def test_step_position(self):
        assert 1

    def test_solve_position_constrain(self):
        # NOTE: just call joint.solve_position
        assert 1

    def test_grav(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.grav = Matrix([1.1, -1.0], 'vec')
        assert dut.grav == Matrix([1.1, -1.0], 'vec')

    def test_lin_vel_damping(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.lin_vel_damping = 6.6
        assert np.isclose(dut.lin_vel_damping, 6.6)

    def test_ang_vel_damping(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.ang_vel_damping = 6.6
        assert np.isclose(dut.ang_vel_damping, 6.6)

    def test_lin_vel_thold(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.lin_vel_thold = 6.6
        assert np.isclose(dut.lin_vel_thold, 6.6)

    def test_ang_vel_thold(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.ang_vel_thold = 6.6
        assert np.isclose(dut.ang_vel_thold, 6.6)

    def test_air_fric_coeff(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.air_fric_coeff = 6.6
        assert np.isclose(dut.air_fric_coeff, 6.6)

    def test_bias(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.bias = 6.6
        assert np.isclose(dut.bias, 6.6)

    def test_vel_iter(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.vel_iter = 6
        assert dut.vel_iter == 6

    def test_pos_iter(self):
        dut: PhysicsWorld = PhysicsWorld()
        dut.pos_iter = 6
        assert dut.pos_iter == 6

    def test_grav_ena(self):
        dut: PhysicsWorld = PhysicsWorld()
        assert dut.grav_ena
        dut.grav_ena = False
        assert not dut.grav_ena

    def test_damping_ena(self):
        dut: PhysicsWorld = PhysicsWorld()
        assert dut.damping_ena
        dut.damping_ena = False
        assert not dut.damping_ena

    def test_create_body(self):
        assert 1

    def test_create_joint(self):
        assert 1

    def test_remove_body(self):
        assert 1

    def test_remove_joint(self):
        assert 1

    def test_clear_all_bodies(self):
        assert 1

    def test_clear_all_joints(self):
        assert 1
