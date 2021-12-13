from __future__ import annotations
from typing import List, Dict, Optional, Union, Tuple

import numpy as np

from ...math.matrix import Matrix
from ...common.config import Config
from ...dynamics.body import Body
from ..broad_phase.aabb import AABB


class Tree():
    '''Dynamic Bounding Volume Tree
    This is implemented by dynamic array-arranged.
    '''
    class Node():
        def __init__(self):
            self._body: Optional[Body] = None
            self._aabb: AABB = AABB()
            self._parent_idx: int = -1
            self._left_idx: int = -1
            self._right_idx: int = -1

        def is_leaf(self) -> bool:
            return self._left_idx == -1 and self._right_idx == -1

        def is_branch(self) -> bool:
            child_ck: bool = self._left_idx != -1 and self._right_idx != -1
            return self._parent_idx != -1 and child_ck

        def is_root(self) -> bool:
            child_ck: bool = self._left_idx != -1 and self._right_idx != -1
            return self._parent_idx == -1 and child_ck

        def is_empty(self) -> bool:
            return self._aabb.is_empty()

        def clear(self) -> None:
            self._body = None
            self._aabb.clear()
            self._parent_idx = -1
            self._left_idx = -1
            self._right_idx = -1

    def __init__(self):
        self._fat_expansion_factor: float = 0.5
        self._root_idx: int = -1
        self._tree: List[Tree.Node] = []
        self._empty_list: List[int] = []
        self._body_table: Dict[Body, int] = {}

    def query(self, val: Union[Body, AABB]) -> List[Body]:
        res: List[Body] = []
        aabb: Optional[AABB] = None

        if isinstance(val, Body):
            aabb = AABB.from_body(val)
        elif isinstance(val, AABB):
            aabb = val

        assert aabb is not None
        self._query_nodes(self._root_idx, aabb, res)
        return res

    def raycast(self, start: Matrix, dirn: Matrix) -> List[Body]:
        res: List[Body] = []
        self._raycast(res, self._root_idx, start, dirn)
        return res

    def generate(self) -> List[Tuple[Body, Body]]:
        pairs: List[Tuple[Body, Body]] = []
        self._generate(self._root_idx, pairs)
        return pairs

    def insert(self, body: Body) -> None:
        new_node_idx: int = self._allocate_node()
        self._tree[new_node_idx]._body = body
        self._tree[new_node_idx]._aabb = AABB.from_body(body)
        self._tree[new_node_idx]._aabb.expand(self._fat_expansion_factor)
        self._body_table[body] = new_node_idx

        if self._root_idx == -1:
            self._root_idx = new_node_idx
            return

        if self._tree[self._root_idx].is_leaf():
            self._root_idx = self._merge(new_node_idx, self._root_idx)
            return

        # calc cost
        target_idx: int = self._calc_lowest_cost_node(new_node_idx)
        if target_idx == self._root_idx:
            self._root_idx = self._merge(new_node_idx, target_idx)
            self._balance(self._root_idx)
            return

        target_parent_idx: int = self._tree[target_idx]._parent_idx
        self._separate(target_idx, target_parent_idx)
        box_idx: int = self._merge(new_node_idx, target_idx)
        self._join(box_idx, target_parent_idx)
        self._upgrade(box_idx)
        self._balance(self._root_idx)

    def remove(self, body: Body) -> None:
        is_find: bool = False
        for v in self._body_table:
            if v == body:
                is_find = True
                break

        if not is_find:
            return

        parent_idx: int = self._tree[self._body_table[body]]._parent_idx
        if parent_idx == -1 and self._tree[self._body_table[body]].is_leaf():
            self._root_idx = -1
            self._remove(self._body_table[body])
            del self._body_table[body]
            return

        another_child: int = self._tree[parent_idx]._right_idx if self._tree[
            parent_idx]._left_idx == self._body_table[body] else self._tree[
                parent_idx]._left_idx
        self._remove(self._body_table[body])
        self._elevate(another_child)
        self._upgrade(another_child)
        del self._body_table[body]

    def clear_all(self) -> None:
        self._tree = []
        self._empty_list = []
        self._body_table = {}
        self._root_idx = -1

    def update(self, body: Body) -> None:
        is_find: bool = False
        for v in self._body_table:
            if v == body:
                is_find = True
                break

        if not is_find:
            return

        thin: AABB = AABB.from_body(body)
        thin.expand(0.1)
        if not thin.is_subset(self._tree[self._body_table[body]]._aabb):
            self._extract(self._body_table[body])
            self.insert(body)

    def tree(self) -> List[Node]:
        return self._tree

    def root_index(self) -> int:
        return self._root_idx

    def _query_nodes(self, node_idx: int, aabb: AABB, res: List[Body]):
        if node_idx == -1:
            return

        overlap: bool = self._tree[node_idx]._aabb.collide(aabb) or self._tree[
            node_idx]._aabb.is_subset(aabb) or aabb.is_subset(
                self._tree[node_idx]._aabb)

        if not overlap:
            return

        if self._tree[node_idx].is_leaf():
            tmp: Optional[Body] = self._tree[node_idx]._body
            assert tmp is not None
            res.append(tmp)
            return

        if self._tree[node_idx].is_branch() or self._tree[node_idx].is_root():
            self._query_nodes(self._tree[node_idx]._left_idx, aabb, res)
            self._query_nodes(self._tree[node_idx]._right_idx, aabb, res)

    # NOTE: now use the List to return the var
    def _traverse_lowest_cost(self, node_idx: int, box_idx: int,
                              cost: List[float], final_idx: List[int]) -> None:
        def _accumulate_cost(node_idx: int, box_idx: int) -> float:
            if self._tree[node_idx].is_leaf():
                return inherit_cost + AABB.unite(
                    self._tree[node_idx]._aabb,
                    self._tree[box_idx]._aabb).surface_area()

            return self._delta_cost(node_idx, box_idx) + inherit_cost

        if self._tree[box_idx].is_leaf() and not self._tree[box_idx].is_root():
            final_idx[0] = box_idx
            return

        area: float = self._tree[box_idx]._aabb.surface_area()
        union_area: float = AABB.unite(
            self._tree[node_idx]._aabb,
            self._tree[box_idx]._aabb).surface_area()

        cost[0] = 2.0 * area
        inherit_cost: float = 2.0 * (union_area - area)

        left_idx: int = self._tree[box_idx]._left_idx
        right_idx: int = self._tree[box_idx]._right_idx
        left_cost: float = _accumulate_cost(node_idx, left_idx)
        right_cost: float = _accumulate_cost(node_idx, right_idx)
        lowest_cost: float = 0.0
        lowest_const_idx: int = 0

        if cost[0] < left_cost and cost[0] < right_cost:
            final_idx[0] = box_idx
            return

        if left_cost > right_cost:
            lowest_cost = right_cost
            lowest_const_idx = right_idx
        else:
            lowest_cost = left_cost
            lowest_const_idx = left_idx

        final_idx[0] = lowest_const_idx
        self._traverse_lowest_cost(node_idx, lowest_const_idx, [lowest_cost],
                                   final_idx)

    def _raycast(self, res: List[Body], node_idx: int, p: Matrix,
                 d: Matrix) -> None:
        if node_idx < 0:
            return

        if self._tree[node_idx]._aabb.raycast(p, d):
            if self._tree[node_idx].is_leaf():
                tmp: Optional[Body] = self._tree[node_idx]._body
                assert tmp is not None
                res.append(tmp)
            else:
                self._raycast(res, self._tree[node_idx]._left_idx, p, d)
                self._raycast(res, self._tree[node_idx]._right_idx, p, d)

    def _generate(self, node_idx: int, pairs: List[Tuple[Body, Body]]) -> None:
        if node_idx < 0 or self._tree[node_idx].is_leaf():
            return

        left_idx: int = self._tree[node_idx]._left_idx
        right_idx: int = self._tree[node_idx]._right_idx
        res: bool = self._tree[left_idx]._aabb.collide(
            self._tree[right_idx]._aabb)

        if res:
            self._generate2(left_idx, right_idx, pairs)

        self._generate(left_idx, pairs)
        self._generate(right_idx, pairs)

    def _generate2(self, left_idx: int, right_idx: int,
                   pairs: List[Tuple[Body, Body]]) -> None:
        if left_idx < 0 or right_idx < 0:
            return

        left_aabb: AABB = self._tree[left_idx]._aabb
        right_aabb: AABB = self._tree[right_idx]._aabb
        res: bool = left_aabb.collide(right_aabb) or left_aabb.is_subset(
            right_aabb) or right_aabb.is_subset(left_aabb)

        if not res:
            return

        if self._tree[left_idx].is_leaf() and self._tree[right_idx].is_leaf():
            tmpl: Optional[Body] = self._tree[left_idx]._body
            tmpr: Optional[Body] = self._tree[right_idx]._body
            assert tmpl is not None
            assert tmpr is not None

            if tmpl.bitmask & tmpr.bitmask:
                # if AABB of A & B overlap
                if AABB.from_body(tmpl).collide(AABB.from_body(tmpr)):
                    pairs.append((tmpl, tmpr))

        if self._tree[left_idx].is_leaf() and self._tree[right_idx].is_branch(
        ):
            self._generate2(left_idx, self._tree[right_idx]._left_idx, pairs)
            self._generate2(left_idx, self._tree[right_idx]._right_idx, pairs)

        if self._tree[right_idx].is_leaf() and self._tree[left_idx].is_branch(
        ):
            self._generate2(right_idx, self._tree[left_idx]._left_idx, pairs)
            self._generate2(right_idx, self._tree[left_idx]._right_idx, pairs)

        if self._tree[left_idx].is_branch(
        ) and self._tree[right_idx].is_branch():
            self._generate2(self._tree[left_idx]._left_idx, right_idx, pairs)
            self._generate2(self._tree[left_idx]._right_idx, right_idx, pairs)

    def _extract(self, target_idx: int) -> None:
        another_child_index: int = -1
        tmp: Optional[Body] = None

        if target_idx == self._root_idx:
            self._root_idx = -1

            tmp = self._tree[target_idx]._body
            assert tmp is not None
            self._body_table[tmp] = -1
            self._remove(target_idx)
            return

        if self._tree[target_idx]._parent_idx == self._root_idx:
            another_child_index = self._tree[
                self._root_idx]._right_idx if self._tree[
                    self._root_idx]._left_idx == target_idx else self._tree[
                        self._root_idx]._left_idx

            self._separate(target_idx, self._root_idx)
            self._elevate(another_child_index)

            tmp = self._tree[target_idx]._body
            assert tmp is not None
            self._body_table[tmp] = -1
            self._remove(target_idx)
            return

        parent_idx: int = self._tree[target_idx]._parent_idx
        another_child_index = self._tree[parent_idx]._right_idx if self._tree[
            parent_idx]._left_idx == target_idx else self._tree[
                parent_idx]._left_idx

        self._separate(target_idx, parent_idx)
        self._elevate(another_child_index)

        tmp = self._tree[target_idx]._body
        assert tmp is not None
        self._body_table[tmp] = -1
        self._remove(target_idx)

    def _merge(self, node_idx: int, leaf_idx: int) -> int:
        parent_idx: int = self._allocate_node()
        self._tree[leaf_idx]._parent_idx = parent_idx
        self._tree[node_idx]._parent_idx = parent_idx
        self._tree[parent_idx]._left_idx = leaf_idx
        self._tree[parent_idx]._right_idx = node_idx
        self._tree[parent_idx]._aabb = AABB.unite(self._tree[node_idx]._aabb,
                                                  self._tree[leaf_idx]._aabb)
        return parent_idx

    def _ll(self, node_idx: int) -> None:
        if node_idx == -1 or self._tree[node_idx].is_root():
            return

        parent_idx: int = -1
        grand_idx: int = -1
        right_idx: int = -1
        if self._tree[node_idx]._parent_idx == self._root_idx:
            parent_idx = self._tree[node_idx]._parent_idx
            right_idx = self._tree[node_idx]._right_idx
            self._separate(node_idx, parent_idx)
            self._separate(right_idx, node_idx)
            self._join(right_idx, parent_idx)
            self._join(parent_idx, node_idx)
            self._root_idx = node_idx
            self._upgrade(parent_idx)
            return

        parent_idx = self._tree[node_idx]._parent_idx
        grand_idx = self._tree[parent_idx]._parent_idx
        right_idx = self._tree[node_idx]._right_idx

        self._separate(parent_idx, grand_idx)
        self._separate(node_idx, parent_idx)
        self._separate(right_idx, node_idx)

        self._join(right_idx, parent_idx)
        self._join(parent_idx, node_idx)
        self._join(node_idx, grand_idx)
        self._upgrade(parent_idx)

    def _rr(self, node_idx: int) -> None:
        if node_idx == -1 or self._tree[node_idx].is_root():
            return

        parent_idx: int = -1
        grand_idx: int = -1
        left_idx: int = -1
        if self._tree[node_idx]._parent_idx == self._root_idx:
            parent_idx = self._tree[node_idx]._parent_idx
            left_idx = self._tree[node_idx]._left_idx
            self._separate(node_idx, parent_idx)
            self._separate(left_idx, node_idx)
            self._join(left_idx, parent_idx)
            self._join(parent_idx, node_idx)
            self._root_idx = node_idx
            self._upgrade(parent_idx)
            return

        parent_idx = self._tree[node_idx]._parent_idx
        grand_idx = self._tree[parent_idx]._parent_idx
        left_idx = self._tree[node_idx]._left_idx

        self._separate(parent_idx, grand_idx)
        self._separate(node_idx, parent_idx)
        self._separate(left_idx, node_idx)
        self._join(left_idx, parent_idx)
        self._join(parent_idx, node_idx)
        self._join(node_idx, grand_idx)
        self._upgrade(parent_idx)

    def _balance(self, target_idx: int) -> None:
        if target_idx == -1 or self._tree[target_idx].is_leaf():
            return

        left_height: int = self._height(self._tree[target_idx]._left_idx)
        right_height: int = self._height(self._tree[target_idx]._right_idx)
        if np.fabs(left_height - right_height) <= 1:
            return

        # left unbalance
        if left_height > right_height:
            ll_height: int = self._height(
                self._tree[self._tree[target_idx]._left_idx]._left_idx)
            lr_height: int = self._height(
                self._tree[self._tree[target_idx]._left_idx]._right_idx)

            # LR case
            if ll_height < lr_height:
                self._rr(
                    self._tree[self._tree[target_idx]._left_idx]._right_idx)
            else:
                self._ll(
                    self._tree[self._tree[target_idx]._left_idx]._left_idx)

            self._ll(self._tree[target_idx]._left_idx)

        else:  # right unbalance
            rr_height: int = self._height(
                self._tree[self._tree[target_idx]._right_idx]._right_idx)
            rl_height: int = self._height(
                self._tree[self._tree[target_idx]._right_idx]._left_idx)

            # RL case
            if rr_height < rl_height:
                self._ll(
                    self._tree[self._tree[target_idx]._right_idx]._left_idx)
            else:
                self._rr(
                    self._tree[self._tree[target_idx]._right_idx]._right_idx)

            self._rr(self._tree[target_idx]._right_idx)

        self._balance(self._tree[target_idx]._left_idx)
        self._balance(self._tree[target_idx]._right_idx)
        self._balance(self._tree[target_idx]._parent_idx)

    def _separate(self, source_idx: int, parent_idx: int) -> None:
        if source_idx < 0 or parent_idx < 0:
            return

        if self._tree[parent_idx]._left_idx == source_idx:
            self._tree[parent_idx]._left_idx = -1
        elif self._tree[parent_idx]._right_idx == source_idx:
            self._tree[parent_idx]._right_idx = -1
        self._tree[source_idx]._parent_idx = -1

    def _join(self, node_idx: int, box_idx: int) -> None:
        if node_idx < 0 or box_idx < 0:
            return

        if self._tree[box_idx]._left_idx == -1:
            self._tree[box_idx]._left_idx = node_idx
        elif self._tree[box_idx]._right_idx == -1:
            self._tree[box_idx]._right_idx = node_idx
        self._tree[node_idx]._parent_idx = box_idx

    def _remove(self, target_idx: int) -> None:
        self._tree[target_idx].clear()
        self._empty_list.append(target_idx)

    def _elevate(self, target_idx: int) -> None:
        if self._tree[target_idx]._parent_idx == self._root_idx:
            self._remove(self._root_idx)
            self._root_idx = target_idx
            self._tree[target_idx]._parent_idx = -1
            return

        parent_idx: int = self._tree[target_idx]._parent_idx
        grand_idx: int = self._tree[parent_idx]._parent_idx
        self._separate(target_idx, parent_idx)
        self._separate(parent_idx, grand_idx)
        self._join(target_idx, grand_idx)
        self._remove(parent_idx)

    def _upgrade(self, node_idx: int) -> None:
        if node_idx < 0 or self._tree[node_idx].is_leaf():
            return

        self._tree[node_idx]._aabb = AABB.unite(
            self._tree[self._tree[node_idx]._left_idx]._aabb,
            self._tree[self._tree[node_idx]._right_idx]._aabb)

        self._upgrade(self._tree[node_idx]._parent_idx)

    def _calc_lowest_cost_node(self, node_idx: int) -> int:
        lowest_cost: List[float] = [Config.Max]
        target_idx: List[int] = [-1]

        # start traverse lowest cost node
        # the lowest_cost is not returned
        self._traverse_lowest_cost(node_idx, self._root_idx, lowest_cost,
                                   target_idx)
        return target_idx[0]

    def _total_cost(self, node_idx: int, leaf_idx: int) -> float:
        total_cost: float = AABB.unite(
            self._tree[node_idx]._aabb,
            self._tree[leaf_idx]._aabb).surface_area()
        cur_idx: int = self._tree[leaf_idx]._parent_idx

        while cur_idx != -1:
            total_cost += self._delta_cost(node_idx, cur_idx)
            cur_idx = self._tree[cur_idx]._parent_idx

        return total_cost

    def _delta_cost(self, node_idx: int, box_idx: int) -> float:
        return AABB.unite(self._tree[box_idx]._aabb,
                          self._tree[node_idx]._aabb).surface_area(
                          ) - self._tree[box_idx]._aabb.surface_area()

    def _allocate_node(self) -> int:
        if len(self._empty_list) > 0:
            return self._empty_list.pop()

        self._tree.append(Tree.Node())
        return len(self._tree) - 1

    def _height(self, target_idx: int) -> int:
        return 0 if target_idx < 0 else np.fmax(
            self._height(self._tree[target_idx]._left_idx),
            self._height(self._tree[target_idx]._right_idx)) + 1
