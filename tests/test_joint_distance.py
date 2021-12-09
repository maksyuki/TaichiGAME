import numpy as np

from TaichiGAME.dynamics.joint.distance import DistanceConstraint
from TaichiGAME.dynamics.joint.distance import DistanceJointPrimitive
from TaichiGAME.dynamics.joint.distance import DistanceConstraintPrimitive
from TaichiGAME.math.matrix import Matrix


class TestDistanceJointPrimitive():
    def test__init__(self):
        dut: DistanceJointPrimitive = DistanceJointPrimitive()

        assert dut._bodya is None
        assert dut._local_pointa == Matrix([0.0, 0.0], 'vec')
        assert dut._target_point == Matrix([0.0, 0.0], 'vec')
        assert dut._normal == Matrix([0.0, 0.0], 'vec')

        assert np.isclose(dut._bias_factor, 0.3)
        assert np.isclose(dut._bias, 0)
        assert np.isclose(dut._dist_min, 0)
        assert np.isclose(dut._dist_max, 0)
        assert np.isclose(dut._eff_mass, 0)
        assert np.isclose(dut._accum_impulse, 0)


class TestDistanceConstraintPrimitive():
    def test_DistanceConstraintPrimitive(self):
        dut: DistanceConstraintPrimitive = DistanceConstraintPrimitive()

        assert dut._bodya is None
        assert dut._bodyb is None
        assert dut._nearest_pa == Matrix([0.0, 0.0], 'vec')
        assert dut._nearest_pb == Matrix([0.0, 0.0], 'vec')
        assert dut._ra == Matrix([0.0, 0.0], 'vec')
        assert dut._rb == Matrix([0.0, 0.0], 'vec')
        assert dut._bias == Matrix([0.0, 0.0], 'vec')
        assert dut._eff_mass == Matrix([0.0, 0.0, 0.0, 0.0])
        assert dut._impulse == Matrix([0.0, 0.0], 'vec')
        assert np.isclose(dut._force_max, 200)


class TestDistanceJoint():
    def test__init__(self):
        dut: DistanceConstraint = DistanceConstraint()

        assert isinstance(dut._prim, DistanceConstraintPrimitive)
        assert np.isclose(dut._factor, 0.1)

    def test_set_value(self):
        assert 1

    def test_prepare(self):
        assert 1

    def test_solve_velocity(self):
        assert 1

    def test_solve_position(self):
        assert 1

    def test_prim(self):
        assert 1


class TestDistanceConstraint():
    def test__init__(self):
        assert 1

    def test_prepare(self):
        assert 1

    def test_solve_velocity(self):
        assert 1

    def test_set_value(self):
        assert 1

    def test_solve_position(self):
        assert 1

    def test_prim(self):
        assert 1
