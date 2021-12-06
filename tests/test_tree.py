from typing import List, Dict, Optional, Tuple

import numpy as np

from TaichiGAME.collision.broad_phase.tree import Tree
from TaichiGAME.collision.broad_phase.aabb import AABB

class TestTree():
    def test_node__init__(self):
        dut: Tree.Node = Tree.Node()

        assert dut._body == None
        assert isinstance(dut._aabb, AABB)
        assert dut._parent_idx == -1
        assert dut._left_idx == -1
        assert dut._right_idx == -1

    def test_node_is_leaf(self):
        dut1: Tree.Node = Tree.Node()
        dut2: Tree.Node = Tree.Node()
        dut3: Tree.Node = Tree.Node()

        # suppose dutx's id is same as x
        dut1._left_idx = 2
        dut1._right_idx = 3
        assert not dut1.is_leaf()
        assert dut2.is_leaf()
        assert dut3.is_leaf()

    def test_node_is_branch(self):
        dut1: Tree.Node = Tree.Node()
        dut2: Tree.Node = Tree.Node()
        dut3: Tree.Node = Tree.Node()

        # suppose dutx's id is same as x
        dut1._left_idx = 2
        dut1._right_idx = 3
        dut2._parent_idx = 1
        dut2._left_idx = 4
        dut2._right_idx = 5

        assert not dut1.is_branch()
        assert dut2.is_branch()
        assert not dut3.is_branch()

    def test_node_is_root(self):
        dut1: Tree.Node = Tree.Node()
        dut2: Tree.Node = Tree.Node()
        dut3: Tree.Node = Tree.Node()

        # suppose dutx's id is same as x
        dut1._left_idx = 2
        dut1._right_idx = 3
        dut2._parent_idx = 1
        dut2._left_idx = 4
        dut2._right_idx = 5

        assert dut1.is_root()
        assert not dut2.is_root()
        assert not dut3.is_root()

    def test_node_is_empty(self):
        dut: Tree.Node = Tree.Node()
        assert dut.is_empty()

    def test_node_clear(self):
        dut1: Tree.Node = Tree.Node()

        # suppose dutx's id is same as x
        dut1._left_idx = 2
        dut1._right_idx = 3
        assert dut1._left_idx == 2
        assert dut1._right_idx == 3

        dut1.clear()
        assert dut1._left_idx == -1
        assert dut1._right_idx == -1

    def test__init__(self):
        dut: Tree = Tree()

        assert np.isclose(dut._fat_expansion_factor, 0.5)
        assert dut._root_idx == -1
        assert len(dut._tree) == 0
        assert len(dut._empty_list) == 0
        assert len(dut._body_table) == 0

    def test_query(self):
        assert 1

    def test_raycast(self):
        assert 1

    def test_generate(self):
        assert 1

    def test_inert(self):
        assert 1

    def test_remove(self):
        assert 1

    def test_clear_all(self):
        assert 1

    def test_update(self):
        assert 1

    def test_tree(self):
        assert 1

    def test_root_index(self):
        assert 1

    def test__query_nodes(self):
        assert 1

    def test__traverse_lowest_cost(self):
        assert 1

    def test__raycast(self):
        assert 1

    def test__generate(self):
        assert 1

    def test__generate2(self):
        assert 1

    def test__extract(self):
        assert 1

    def test__merge(self):
        assert 1

    def test___ll(self):
        assert 1

    def test__rr(self):
        assert 1

    def test__balance(self):
        assert 1

    def test__separate(self):
        assert 1

    def test__join(self):
        assert 1

    def test__remove(self):
        assert 1

    def test__elevate(self):
        assert 1

    def test__upgrade(self):
        assert 1

    def test__calc_lowest_cost_node(self):
        assert 1

    def test__total_cost(self):
        assert 1

    def test__delta_cost(self):
        assert 1

    def test__allocate_node(self):
        assert 1

    def test__height(self):
        assert 1