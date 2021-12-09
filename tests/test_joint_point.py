import numpy as np
from TaichiGAME.dynamics.body import Body
from TaichiGAME.dynamics.joint.joint import JointType

from TaichiGAME.dynamics.joint.point import PointJoint, PointJointPrimitive
from TaichiGAME.math.matrix import Matrix


class TestPointJointPrimitive():
    def test__init__(self):
        dut: PointJointPrimitive = PointJointPrimitive()

        assert isinstance(dut._bodya, Body)
        assert dut._local_pointa == Matrix([0.0, 0.0], 'vec')
        assert dut._target_point == Matrix([0.0, 0.0], 'vec')
        assert dut._normal == Matrix([0.0, 0.0], 'vec')

        assert np.isclose(dut._damping, 0)
        assert np.isclose(dut._stiff, 0)
        assert np.isclose(dut._freq, 8)
        assert np.isclose(dut._force_max, 1000)
        assert np.isclose(dut._damping_radio, 1)
        assert np.isclose(dut._gamma, 0)
        assert dut._bias == Matrix([0.0, 0.0], 'vec')
        assert dut._eff_mass == Matrix([0.0, 0.0], 'vec')
        assert dut._impulse == Matrix([0.0, 0.0], 'vec')


class TestPointJoint():
    def test__init__(self):
        dut: PointJoint = PointJoint()
        assert dut._type == JointType.Point
        assert isinstance(dut._prim, PointJointPrimitive)
        assert np.isclose(dut._factor, 0.22)

    def test_set_value(self):
        dut: PointJoint = PointJoint()
        tmp: PointJointPrimitive = PointJointPrimitive()
        tmp._impulse = 0.66
        dut.set_value(tmp)

        assert np.isclose(dut._prim._impulse, 0.66)

    def test_prepare(self):
        assert 1

    def test_solve_velocity(self):
        assert 1

    def test_solve_position(self):
        # NOTE: solve position is not achieved
        assert 1

    def test_prim(self):
        dut: PointJoint = PointJoint()

        assert isinstance(dut.prim(), PointJointPrimitive)
