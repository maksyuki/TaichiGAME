from TaichiGAME.dynamics.joint.joint import JointType
from TaichiGAME.dynamics.joint.pulley import PulleyJoint, PulleyJointPrimitive


class TestPulleyJointPrimitive():
    def test__init__(self):
        dut: PulleyJointPrimitive = PulleyJointPrimitive()
        assert isinstance(dut, PulleyJointPrimitive)


class TestPulleyJoint():
    def test__init__(self):
        dut: PulleyJoint = PulleyJoint()

        assert dut._type == JointType.Pulley
        assert isinstance(dut._prim, PulleyJointPrimitive)

    def test_set_value(self):
        dut: PulleyJoint = PulleyJoint()
        dut.set_value(PulleyJointPrimitive())
        assert isinstance(dut._prim, PulleyJointPrimitive)

    def test_prepare(self):
        assert 1

    def test_solve_velocity(self):
        assert 1

    def test_solve_position(self):
        assert 1
