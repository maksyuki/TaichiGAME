import numpy as np
from TaichiGAME.geometry.shape import Circle

from TaichiGAME.math.matrix import Matrix
from TaichiGAME.dynamics.body import Body


class TestBody():
    def test_Body_Type(self):
        assert Body.Type.Kinematic.value == 0
        assert Body.Type.Static.value == 1
        assert Body.Type.Dynamic.value == 2
        assert Body.Type.Bullet.value == 3

    def test_PhysicsAttribute__init__(self):
        dut: Body.PhysicsAttribute = Body.PhysicsAttribute()
        assert dut._pos == Matrix([0.0, 0.0], 'vec')
        assert dut._vel == Matrix([0.0, 0.0], 'vec')
        assert np.isclose(dut._rot, 0)
        assert np.isclose(dut._ang_vel, 0)

    def test_PhysicsAttribute_step(self):
        dut: Body.PhysicsAttribute = Body.PhysicsAttribute()
        dut._vel.x = 1.0
        dut._vel.y = 2.0
        dut._ang_vel = 1.0
        dut.step(6)
        assert dut._pos == Matrix([6.0, 12.0], 'vec')
        assert np.isclose(dut._rot, 6)

    def test_init__(self):
        assert 1

    def test_pos(self):
        dut: Body = Body()
        assert dut.pos == Matrix([0.0, 0.0], 'vec')

    def test_vel(self):
        dut: Body = Body()
        assert dut.vel == Matrix([0.0, 0.0], 'vec')

    def test_rot(self):
        dut: Body = Body()
        assert np.isclose(dut.rot, 0)

    def test_ang_vel(self):
        dut: Body = Body()
        assert np.isclose(dut.ang_vel, 0)

    def test_forces(self):
        dut: Body = Body()
        assert dut.forces == Matrix([0.0, 0.0], 'vec')

    def test_torques(self):
        dut: Body = Body()
        assert np.isclose(dut.torques, 0)

    def test_clear_torques(self):
        dut: Body = Body()
        dut.torques = 23.4
        assert np.isclose(dut.torques, 23.4)
        dut.clear_torque()
        assert np.isclose(dut.torques, 0)

    def test_mass(self):
        dut: Body = Body()
        assert np.isclose(dut.mass, 0)
        dut.shape = Circle()
        dut.mass = 23.4
        assert np.isclose(dut.mass, 23.4)
        assert np.isclose(dut._inv_mass, 1 / 23.4)

    def test_inertia(self):
        dut: Body = Body()
        assert np.isclose(dut.inertia, 0)

    def test_fric(self):
        dut: Body = Body()
        assert np.isclose(dut.fric, 0.2)

    def test_sleep(self):
        dut: Body = Body()
        assert not dut.sleep

    def test_inv_mass(self):
        dut: Body = Body()
        assert np.isclose(dut.inv_mass, 0)

    def test_inv_inertia(self):
        dut: Body = Body()
        assert np.isclose(dut.inv_inertia, 0)

    def test_phy_attr(self):
        dut: Body = Body()
        phy1: Body.PhysicsAttribute = Body.PhysicsAttribute()

        phy1._rot = 2.2
        phy1._ang_vel = 3.6
        dut.phy_attr = phy1

        assert np.isclose(dut.rot, 2.2)
        assert np.isclose(dut.ang_vel, 3.6)

    def test_step_position(self):
        dut: Body = Body()
        dut.vel = Matrix([1.0, 2.0], 'vec')
        dut.ang_vel = 1.0
        dut.step_position(6)

        assert dut.pos == Matrix([6, 12], 'vec')
        assert np.isclose(dut.rot, 6)

    def test_apply_impulse(self):
        dut: Body = Body()
        dut.shape = Circle()
        dut.vel = Matrix([1.0, 2.0], 'vec')
        dut.ang_vel = 1.0
        dut.mass = 10
        print(dut.vel.shape)
        dut.apply_impulse(Matrix([1.0, 1.0], 'vec'), Matrix([1.0, 1.0], 'vec'))
        print(dut.vel.shape)
        print(dut.vel)

        print(dut.ang_vel)
        assert dut.vel == Matrix([1.1, 2.1], 'vec')
        assert np.isclose(dut.ang_vel, 1)

    def test_to_local_point(self):
        dut: Body = Body()
        dut.rot = np.pi / 4
        dut.pos = Matrix([0.0, 0.0], 'vec')
        tmp = dut.to_local_point(Matrix([1.0, 1.0], 'vec'))
        assert tmp == Matrix([1.414213, 0], 'vec')

    def test_to_world_point(self):
        dut: Body = Body()
        dut.rot = np.pi / 4
        dut.pos = Matrix([0.0, 0.0], 'vec')
        tmp = dut.to_local_point(Matrix([1.414213, 0], 'vec'))
        print(tmp)
        assert tmp == Matrix([1, -1], 'vec')

    def test_to_actual_point(self):
        dut: Body = Body()
        dut.rot = np.pi / 4
        tmp = dut.to_actual_point(Matrix([1, 1], 'vec'))
        print(tmp)
        assert tmp == Matrix([0, 1.41421], 'vec')

    def test_id(self):
        dut: Body = Body()
        dut.id = 6
        assert dut.id == 6

    def test_bitmask(self):
        dut: Body = Body()
        dut.bitmask = 6
        assert dut.bitmask == 6

    def test_restit(self):
        dut: Body = Body()
        dut.restit = 6.4
        assert np.isclose(dut.restit, 6.4)

    # NOTE: need to add more body type
    def test_calc_inertia(self):
        dut: Body = Body()
        dut.shape = Circle(6)
        dut.mass = 1
        print(dut.inertia)
        assert np.isclose(dut.inertia, 18)
