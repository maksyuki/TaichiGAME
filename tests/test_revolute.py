import numpy as np
from TaichiGAME.dynamics.joint.joint import JointType

from TaichiGAME.dynamics.joint.revolute import RevoluteJoint
from TaichiGAME.dynamics.joint.revolute import RevoluteJointPrimitive
from TaichiGAME.math.matrix import Matrix


class TestRevoluteJointPrimitive():
    def test__init__(self):
        dut: RevoluteJointPrimitive = RevoluteJointPrimitive()

        assert dut._bodya is None
        assert dut._bodyb is None
        assert dut._local_pointa == Matrix([0.0, 0.0], 'vec')
        assert dut._local_pointb == Matrix([0.0, 0.0], 'vec')
        assert np.isclose(dut._damping, 0)
        assert np.isclose(dut._stiff, 0)
        assert np.isclose(dut._freq, 8)
        assert np.isclose(dut._force_max, 5000)
        assert np.isclose(dut._damping_radio, 0.2)
        assert np.isclose(dut._gamma, 0)
        assert dut._bias == Matrix([0.0, 0.0], 'vec')
        assert dut._eff_mass == Matrix([0.0, 0.0], 'vec')
        assert dut._impulse == Matrix([0.0, 0.0], 'vec')


class TestRevoluteJoint():
    def test__init__(self):
        dut: RevoluteJoint = RevoluteJoint()

        assert dut._type == JointType.Revolute
        assert isinstance(dut._prim, RevoluteJointPrimitive)

    def test_set_value(self):
        dut: RevoluteJoint = RevoluteJoint()
        tmp: RevoluteJointPrimitive = RevoluteJointPrimitive()
        tmp._bias = 0.66
        dut.set_value(tmp)

        assert np.isclose(dut._prim._bias, 0.66)

    def test_prepare(self):
        assert 1

    def test_solve_velocity(self):
        assert 1

    def test_solve_position(self):
        assert 1

    def test_prim(self):
        dut: RevoluteJoint = RevoluteJoint()

        assert isinstance(dut.prim(), RevoluteJointPrimitive)