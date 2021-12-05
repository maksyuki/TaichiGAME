from typing import AbstractSet, List, Dict, Optional, Tuple

import numpy as np

from TaichiGAME.collision.broad_phase.aabb import AABB
from TaichiGAME.math.matrix import Matrix

class TestAABB():
    def test__init__(self):
        dut: AABB = AABB(2.4, 3.6)
        assert dut._pos == Matrix([0.0, 0.0], 'vec')
        assert np.isclose(dut._width, 2.4)
        assert np.isclose(dut._height, 3.6)

    def test__eq__(self):
        dut1: AABB = AABB(2.3, 4.5)
        dut2: AABB = AABB(2.3, 4.5)
        dut3: AABB = AABB(2.3, 4.8)
        assert dut1 == dut2
        assert not dut1 == dut3

    def test_top_left(self):
        dut1: AABB = AABB(2.4, 3.6)
        assert dut1.top_left == Matrix([-1.2, 1.8], 'vec')

    def test_top_right(self):
        dut1: AABB = AABB(2.4, 3.6)
        assert dut1.top_right == Matrix([1.2, 1.8], 'vec')

    def test_bot_left(self):
        dut1: AABB = AABB(2.4, 3.6)
        assert dut1.bot_left == Matrix([-1.2, -1.8], 'vec')

    def test_bot_right(self):
        dut1: AABB = AABB(2.4, 3.6)
        assert dut1.bot_right == Matrix([1.2, -1.8], 'vec')

    def test_collide(self):
        dut1: AABB = AABB(2.4, 3.6)
        dut2: AABB = AABB(1.2, 1.2)
        dut3: AABB = AABB(1.2, 1.2)
        dut3.pos = Matrix([100.0, 100.0], 'vec')

        assert dut1.collide(dut2)
        assert not dut1.collide(dut3)

    def test_expand(self):
        dut1: AABB = AABB(2.4, 3.6)
        dut1.expand(23)
        assert np.isclose(dut1._width, 25.4)
        assert np.isclose(dut1._height, 26.6)

    def test_scale(self):
        assert 1

    def test_clear(self):
        assert 1

    def test_unite(self):
        dut1: AABB = AABB(2.0, 4.0)
        dut2: AABB = AABB(1.2, 1.2)
        dut3: AABB = AABB(2.0, 4.0)
        dut3.pos = Matrix([10.0, 10.0], 'vec')
        dut4: AABB = AABB(12.0, 14.0)
        dut4.pos = Matrix([5.0, 5.0], 'vec')

        assert dut1.unite(dut2) == dut1
        assert dut1.unite(dut3) == dut4

    def test_surface_area(self):
        assert 1

    def test_volume(self):
        assert 1

    def test_is_subset(self):
        dut1: AABB = AABB(2.0, 4.0)
        dut2: AABB = AABB(1.2, 1.2)

        assert dut2.is_subset(dut1)

    def test_raycast(self):
        assert 1  #FIXME: need to add test case

    def test_from_shape(self):
        assert 1

    def test_from_body(self):
        assert 1

    def test_from_box(self):
        assert 1
