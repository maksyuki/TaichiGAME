class Tree():
    def __init__(self):
        self._fat_expansion_factor = 0.5
        self._root_index = -1.0
        self._tree = []
        self._empty_list = []
        self._body_table = {}

    class Node():
        def __init__(self):
            self._body = None
            self._aabb = AABB()
            self._parent_index = -1
            self._left_index = -1
            self._right_index = -1

        def is_leaf(self):
            return self._left_index == -1 and self._right_index == -1

        def is_branch(self):
            return self._parent_index != -1 and self._left_index != -1 and self._right_index != -1

        def is_root(self):
            return self._parent_index == -1 and self._left_index != -1 and self._right_index != -1

        def is_empty(self):
            return self._aabb.is_empty()

        def clear(self):
            self._body = None
            self._aabb.clear()
            self._parent_index = -1
            self._left_index = -1
            self._right_index = -1

    #FIXME:
    def query(self, body):
        pass

    def raycast(self, start_point, dir):
        result = []
        self._raycast(result, self._root_index, start_point, dir)
        return result

    def generate(self):
        pairs = []
        self._generate(self._root_index, pairs)
        return pairs

    def insert(self, body):
        new_node_index = self._allocate_node()
        self._tree[new_node_index]._body = body
        self._tree[new_node_index]._aabb = AABB.from_body(body)
        self._tree[new_node_index]._aabb.expand(self._fat_expansion_factor)
        self._body_table[body] = new_node_index

        if self._root_index == -1:
            self._root_index = new_node_index
            return

        if self._tree[self._root_index].is_leaf():
            self._root_index = self._merge(new_node_index, self._root_index)
            return

        target_index = self._calc_lowest_cost_node(new_node_index)
        if target_index == self._root_index:
            self._root_index = self._merge(new_node_index, target_index)
            self._balance(self._root_index)
            return

        target_parent_index = self._tree[target_index]._parent_index
        self._separate(target_index, target_parent_index)
        box_index = self._merge(new_node_index, target_index)
        self._join(box_index, target_parent_index)
        self._upgrade(box_index)
        self._balance(self._root_index)

    def remove(self, body):
        is_find = False
        for v in self._body_table.keys():
            if v == body:
                is_find = True
                break

        if not is_find:
            return

        parent_index = self._tree[self._body_table[body]]._parent_index
        if parent_index == -1 and self._tree[self._body_table[body]].is_leaf():
            self._root_index = -1
            self._remove(self._body_table[body])
            del self._body_table[body]
            return

        another_child = self._tree[parent_index]._right_index if self._tree[
            parent_index]._left_index == self._body_table[
                body] else self._tree[parent_index]._left_index
        self._remove(self._body_table[body])
        self._elevate(another_child)
        self._upgrade(another_child)
        del self._body_table[body]

    def clear_all(self):
        self._tree = []
        self._empty_list = []
        self._body_table = {}
        self._root_index = -1

    def update(self, body):
        is_find = False
        for v in self._body_table:
            if v == body:
                is_find = True
                break

        if not is_find:
            return

        thin = AABB.from_body(body)
        thin.expand(0.1)
        if not thin.is_subset(self._tree[self._body_table[body]])._aabb:
            self._extract(self._tree[self._body_table[body]])
            self.insert(body)

    def tree(self):
        return self._tree

    def root_index(self):
        return self._root_index

    def _query_nodes(self, node_index, aabb, res):
        if node_index == -1:
            return

        overlap = self._tree[node_index]._aabb.collide(aabb) or self._tree[
            node_index]._aabb.is_subset(aabb) or aabb.is_subset(
                self._tree[node_index]._aabb)

        if not overlap:
            return

        if self._tree[node_index].is_leaf():
            result.append(self._tree[node_index]._body)
            return

        if self._tree[node_index].is_branch(
        ) or self._tree[node_index].is_root():
            self._query_nodes(self._tree[node_index]._left_index, aabb, result)
            self._query_nodes(self._tree[node_index]._right_index, aabb,
                              result)

    def _accumulate_cost(node_index, box_index, inheritance_cost):
        if self._tree[node_index].is_leaf():
            return inheritance_cost + AABB.unite(
                self._tree[node_index]._aabb,
                self._tree[box_index]._aabb).surface_area()
        return self._delta_cost(node_index, box_index) + inheritance_cost

    # FIXME: final_index need to be returned
    def _traverse_lowest_cost(self, node_index, box_index, cost, final_index):
        if self._tree[box_index].is_leaf(
        ) and not self._tree[box_index].is_root():
            final_index = box_index
            return

        area = self._tree[box_index]._aabb.surface_area()
        union_area = AABB.unite(self._tree[node_index]._aabb,
                                self._tree[box_index]._aabb).surface_area()

        cost = 2.0 * area
        inheritance_cost = 2.0 * (union_area - area)

        left_index = self._tree[box_index]._left_index
        right_index = self._tree[box_index]._right_index
        left_cost = self._accumulate_cost(node_index, left_index)
        right_cost = self._accumulate_cost(node_index, right_index)
        lowest_cost = 0.0
        lowest_const_index = 0

        if cost < left_cost and cost < right_cost:
            final_index = box_index
            return

        if left_cost > right_cost:
            lowest_cost = right_cost
            lowest_const_index = right_index
        else:
            lowest_cost = left_cost
            lowest_const_index = left_index

        final_index = lowest_const_index
        self._traverse_lowest_cost(node_index, lowest_const_index, lowest_cost,
                                   final_index)

    def _raycast(self, result, node_index, p, d):
        if node_index < 0:
            return

        if self._tree[node_index]._aabb.raycast(p, d):
            if self._tree[node_index].is_leaf():
                result.append(self._tree[node_index]._body)
            else:
                self._raycast(result, self._tree[node_index]._left_index, p, d)
                self._raycast(result, self._tree[node_index]._right_index, p,
                              d)

    # FIXME:
    def _generate(self, node_index, pairs):
        pass

    def _extract(self, target_index):
        if target_index == self._root_index:
            self._root_index = -1
            self._body_table[self._tree[target_index]._body] = -1
            self._remove(target_index)
            return

        if self._tree[target_index]._parent_index == self._root_index:
            another_child_index = self._tree[
                self._root_index]._right_index if self._tree[
                    self.
                    _root_index]._left_index == target_index else self._tree[
                        self._root_index]._left_index
            self._separate(target_index, self._root_index)
            self._elevate(another_child_index)
            self._body_table[self._tree[target_index]._body] = -1
            self._remove(target_index)

        parent_index = self._tree[target_index]._parent_index
        another_child_index = self._tree[
            parent_index]._right_index if self._tree[
                parent_index]._left_index == target_index else self._tree[
                    parent_index]._left_index
        self._separate(target_index, parent_index)
        self._elevate(another_child_index)
        self._body_table[self._tree[target_index].body] = -1
        self._remove(target_index)

    def _merge(self, node_index, leaf_index):
        parent_index = self._allocate_node()
        self._tree[leaf_index]._parent_index = parent_index
        self._tree[node_index]._parent_index = parent_index
        self._tree[parent_index]._left_index = leaf_index
        self._tree[parent_index]._right_index = node_index
        self._tree[parent_index]._aabb = AABB.unite(
            self._tree[node_index]._aabb, self._tree[leaf_index]._aabb)
        return parent_index

    def _ll(self, node_index):
        if node_index == -1 or self._tree[node_index].is_root():
            return

        if self._tree[node_index]._parent_index == self._root_index:
            parent_index = self._tree[node_index]._parent_index
            right_index = self._tree[node_index]._right_index
            self._separate(node_index, parent_index)
            self._separate(right_index, node_index)
            self._join(right_index, parent_index)
            self._join(parent_index, node_index)
            self._root_index = node_index
            self._upgrade(parent_index)
            return

        parent_index = self._tree[node_index]._parent_index
        grand_index = self._tree[parent_index]._parent_index
        right_index = self._tree[node_index]._right_index

        self._separate(parent_index, grand_index)
        self._separate(node_index, parent_index)
        self._separate(right_index, node_index)

        self._join(right_index, parent_index)
        self._join(parent_index, node_index)
        self._join(node_index, grand_index)
        self._upgrade(parent_index)

    def _rr(self, node_index):
        if node_index == -1 or self._tree[node_index].is_root():
            return

        if self._tree[node_index]._parent_index == self._root_index:
            parent_index = self._tree[node_index]._parent_index
            left_index = self._tree[node_index]._left_index
            self._separate(node_index, parent_index)
            self._separate(left_index, node_index)
            self._join(left_index, parent_index)
            self._join(parent_index, node_index)
            self._root_index = node_index
            self._upgrade(parent_index)
            return

        parent_index = self._tree[node_index]._parent_index
        grand_index = self._tree[parent_index]._parent_index
        left_index = self._tree[node_index]._left_index

        self._separate(parent_index, grand_index)
        self._separate(node_index, parent_index)
        self._separate(left_index, node_index)
        self._join(left_index, parent_index)
        self._join(parent_index, node_index)
        self._join(node_index, grand_index)
        self._upgrade(parent_index)

    def _balance(self, target_index):
        if target_index == -1 or self._tree[target_index].is_root():
            return
        left_height = self._height(self._tree[target_index]._left_index)
        right_height = self._height(self._tree[target_index]._right_index)
        if np.fabs(left_height - right_height) <= 1:
            return

        if left_height < right_height:
            ll_height = self._height(
                self._tree[self._tree[target_index]._left_index]._left_index)
            lr_height = self._height(
                self._tree[self._tree[target_index]._left_index]._right_index)

            if ll_height < lr_height:
                self._rr(self._tree[
                    self._tree[target_index]._left_index]._right_index)
            else:
                self._ll(self._tree[
                    self._tree[target_index]._left_index]._left_index)

            self._ll(self._tree[target_index]._left_index)
        else:
            rr_height = self._height(
                self._tree[self._tree[target_index]._right_index]._right_index)
            rl_height = self._height(
                self._tree[self._tree[target_index]._right_index]._left_index)

            if rr_height < rl_height:
                self._ll(self._tree[
                    self._tree[target_index]._right_index]._left_index)
            else:
                self._rr(self._tree[
                    self._tree[target_index]._right_index]._right_index)

            self._rr(self._tree[target_index]._right_index)

        self._balance(self._tree[target_index]._left_index)
        self._balance(self._tree[target_index]._right_index)
        self._balance(self._tree[target_index]._parent_index)

    def _separate(self, source_index, parent_index):
        if source_index < 0 or parent_index < 0:
            return

        if self._tree[parent_index]._left_index == source_index:
            self._tree[parent_index]._left_index = -1
        elif self._tree[parent_index]._right_index == source_index:
            self._tree[parent_index]._right_index = -1
        self._tree[source_index]._parent_index = -1

    def _join(self, node_index, box_index):
        if node_index < 0 or box_index < 0:
            return

        if self._tree[box_index]._left_index == -1:
            self._tree[box_index]._left_index = node_index
        elif self._tree[box_index]._right_index == -1:
            self._tree[box_index]._right_index = node_index
        self._tree[node_index]._parent_index = box_index

    def _remove(self, target_index):
        self._tree[target_index].clear()
        self._empty_list.append(target_index)

    def _elevate(self, target_index):
        if self._tree[target_index]._parent_index == self._root_index:
            self._remove(self._root_index)
            self._root_index = target_index
            self._tree[target_index]._parent_index = -1
            return

        parent_index = self._tree[target_index]._parent_index
        grand_index = self._tree[parent_index]._parent_index
        self._separate(target_index, parent_index)
        self._separate(parent_index, grand_index)
        self._join(target_index, grand_index)
        self._remove(parent_index)

    def _upgrade(self, node_index):
        pass

    def _calc_lowest_cost_node(self, node_index):
        lowest_cost = 222222222  #FIXME:
        target_index = -1

        # FIXME: need to return the target index value by ref
        self._traverse_lowest_cost(node_index, self._root_index, lowest_cost,
                                   target_index)
        return target_index

    def _total_cost(self, node_index, leaf_index):
        total_cost = AABB.unite(self._tree[node_index]._aabb,
                                self._tree[leaf_index]._aabb).surface_area()
        current_index = self._tree[leaf_index]._parent_index

        while current_index != -1:
            total_cost += self._delta_cost(node_index, current_index)
            current_index = self._tree[current_index]._parent_index

        return total_cost

    def _delta_cost(self, node_index, box_index):
        return AABB.unite(self._tree[box_index]._aabb,
                          self._tree[node_index]._aabb).surface_area(
                          ) - self._tree[box_index]._aabb.surface_area()

    def _allocate_node(self):
        if not self._empty_list.empty():
            target_index = len(self._empty_list) - 1
            del self._empty_list[target_index]
            return target_index

        self._tree.append(Node())
        return len(self._tree) - 1

    def _height(self, target_index):
        return 0 if target_index < 0 else np.fmax(
            self._height(self._tree[target_index]._left_index),
            self._height(self._tree[target_index]._right_index)) + 1
