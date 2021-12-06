
from typing import List, Dict, Optional, Tuple

import numpy as np

from TaichiGAME.collision.broad_phase.dbvh import DBVH

class TestDBVH():
    def test_node__init__(self):
        dut: DBVH.Node = DBVH.Node()
        assert dut._parent == None
        assert dut._left == None
        assert dut._right == None
        assert dut._body == None
        assert dut._aabb == None

    def test_node_separete(self):
        dut1: DBVH.Node = DBVH.Node()
        dut2: DBVH.Node = DBVH.Node()
        dut3: DBVH.Node = DBVH.Node()

        dut1.separate(None)
        dut1.separate(dut2)

        dut1._left = dut2
        dut1._right = dut3
        dut2._parent = dut1
        
        assert dut1._left == dut2
        assert dut2._parent == dut1
        dut1.separate(dut2)
        assert dut1._left == None
        assert dut2._parent == None

    def test_node_swap(self):
        dut1: DBVH.Node = DBVH.Node()
        dut2: DBVH.Node = DBVH.Node()
        dut3: DBVH.Node = DBVH.Node()

        dut1._left = dut2
        assert dut1._left == dut2
        dut1._right = dut3
        dut1.swap(dut2, dut3)
        assert dut1._left == dut3
        assert dut3._parent == dut1

    def test_node_is_leaf(self):
        dut1: DBVH.Node = DBVH.Node()
        dut2: DBVH.Node = DBVH.Node()
        dut3: DBVH.Node = DBVH.Node()

        dut1._left = dut2
        dut1._right = dut3

        assert not dut1.is_leaf()
        assert dut2.is_leaf()
        assert dut3.is_leaf()

    def test_node_is_branch(self):
        dut1: DBVH.Node = DBVH.Node()
        dut2: DBVH.Node = DBVH.Node()
        dut3: DBVH.Node = DBVH.Node()
        dut4: DBVH.Node = DBVH.Node()
        dut5: DBVH.Node = DBVH.Node()

        dut1._left = dut2
        dut1._right = dut3
        dut2._parent = dut1
        dut3._parent = dut1

        dut2._left = dut4
        dut2._right = dut5
        dut4._parent = dut2
        dut5._parent = dut2

        assert not dut1.is_branch()
        assert dut2.is_branch()
        assert not dut3.is_branch()

    def test_node_is_root(self):
        dut1: DBVH.Node = DBVH.Node()
        dut2: DBVH.Node = DBVH.Node()

        dut1._left = dut2
        dut2._parent = dut1
        assert dut1.is_root()

    def test_node_clear(self):
        dut1: DBVH.Node = DBVH.Node()
        dut2: DBVH.Node = DBVH.Node()
        dut3: DBVH.Node = DBVH.Node()

        dut1._left = dut2
        dut1._right = dut3
        dut2._parent = dut1

        assert dut1._left == dut2
        assert dut1._right == dut3
        dut1.clear()
        assert dut1._body == None

    def test__init__(self):
        dut: DBVH = DBVH()
        assert dut._root == None
        assert np.isclose(dut._profile, 0)
        assert np.isclose(dut._leaf_factor, 0.5)
        