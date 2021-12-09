import numpy as np

from TaichiGAME.dynamics.body import Body
from TaichiGAME.dynamics.joint.joint import JointType
from TaichiGAME.dynamics.joint.rotation import OrientationJointPrimitive, RotationJoint
from TaichiGAME.dynamics.joint.rotation import RotationJointPrimitive
from TaichiGAME.math.matrix import Matrix


class TestRotationJointPrimitive():
    def test__init__(self):
        dut: RotationJointPrimitive = RotationJointPrimitive()

        assert isinstance(dut._bodya, Body)
        assert isinstance(dut._bodyb, Body)
        assert np.isclose(dut._ref_rot, 0)
        assert np.isclose(dut._eff_mass, 0)
        assert np.isclose(dut._bias, 0)


class TestOrientationJointPrimitive():
    def test__init__(self):
        dut: OrientationJointPrimitive = OrientationJointPrimitive()

        assert isinstance(dut._bodya, Body)
        assert dut._target_point == Matrix([0.0, 0.0], 'vec')
        assert np.isclose(dut._ref_rot, 0)
        assert np.isclose(dut._eff_mass, 0)
        assert np.isclose(dut._bias, 0)


class TestRotationJoint():
    def test__init__(self):
        dut: RotationJoint = RotationJoint()

        assert dut._type == JointType.Rotation
        assert isinstance(dut._prim, RotationJointPrimitive)
        assert np.isclose(dut._factor, 0.2)

    def test_set_value(self):
        dut: RotationJoint = RotationJoint()
        tmp: RotationJointPrimitive = RotationJointPrimitive()
        tmp._bias = 0.66
        dut.set_value(tmp)

        assert isinstance(dut._prim, RotationJointPrimitive)

    def test_prepare(self):
        assert 1

    def test_solve_velocity(self):
        assert 1

    def test_solve_position(self):
        assert 1

    def test_prim(self):
        dut: RotationJoint = RotationJoint()

        assert isinstance(dut.prim(), RotationJointPrimitive)
