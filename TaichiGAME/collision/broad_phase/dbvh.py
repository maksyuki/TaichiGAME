import numpy as np

from ...math.matrix import Matrix
from ...geometry.gemo_algo import GeomAlgo2D


class DBVH():
    def __init__(self):
        self._root = None
        self._profile = 0
        self._leaf_factor = 0.5
        self._leaves = {}

    class Node():
        def __init__(self):
            pass

        def separate(self, node):
            pass

        def swap(self, src, target):
            pass

        def is_leaf(self):
            pass

        def is_branch(self):
            pass

        def is_root(self):
            pass

        def clear(self):
            pass

    def find(self, body):
        for b in self._leaves.keys():
            if b == body:
                return True
        return False

    def insert(self, body):
        if not self.find(body):
            return

        aabb = AABB.from_body(body)
        aabb.expand(self._leaf_factor)

        if self._root == None:
            self._root = Node(body, aabb)
            self._leaves[body] = self._root

        if self._root.is_leaf() and self._root.is_root():
            self._merge(self._root, aabb, body)
            self._update(self._root)
            return

        target = self._get_cost(None, aabb)
        self._merge(target, aabb, body)
        self._balance(self._root)
        self._update(target)
        for val in self._leaves.values():
            self._update(val)

    def update(self, body):
        assert body != None
        if not self.find(body):
            return

        thin = AABB.from_body(body)
        thin.expand(0.1)
        if not thin.is_subset(self._leaves[body]._aabb):
            node = self.extract(body)
            self._insert(node)

    def extract(self, body):
        pass

    def erase(self, body):
        target = self.extract(body)
        if target == None:
            return

        target._body = None
        target._aabb.clear()
        del self._leaves[body]

    def clean_up(self, node):
        pass

    def root(self):
        return self._root

    def raycast(self, start_point, dir):
        res = []
        self._raycast(res, self._root, start_point, dir)
        return res

    def generate(self):
        self._profile = 0
        res = [Body(), Body()]
        self._generate(self._root, res)
        return res

    def leaves(self):
        return self._leaves

    def query(self, src, nodes, skip_body=None):
        return DBVH.query_nodes(self._root, src, nodes, skip_body)

    @staticmethod
    def query_nodes(node, aabb, nodes, skip_body=None):
        if node == None or not aabb.collide(node._aabb):
            return

        if skip_body != None and node._body == skip_body:
            return

        if node.is_branch() or node.is_root():
            DBVH.query_nodes(node._left, aabb, nodes, skip_body)
            DBVH.query_nodes(node._right, aabb, nodes, skip_body)
            return

        if node.is_leaf():
            nodes.append(node)

    def _raycast(self, res, node, start_point, dir):
        if node == None:
            return

        if node._aabb.raycast(start_point, dir):
            if node.is_leaf():
                res.append(node._body)
            else:
                self._raycast(res, node._left, start_point, dir)
                self._raycast(res, node._right, start_point, dir)

    def _get_cost(self, target, aabb):
        low_cost_node = None
        cost_value = 0
        is_first = True
        for val in self._leaves.values():
            assert val != None
            if val == target:
                continue

            cost = self._total_cost(val, aabb)

            # FIXME: need to simplify the code
            if is_first or cost < cost_value:
                is_first = False
                cost_value = cost
                low_cost_node = val

        return low_cost_node

    def _insert(self, node):
        if node == None:
            return

        aabb = AABB.from_body(node._body)
        aabb.expand(self._leaf_factor)
        node._aabb = aabb

        if self._root == None:
            self._root = node
            return

        if self._root.is_leaf() and self._root.is_root():
            self._merge(self._root, node)
            self._update(self._root)
            return

        if self._root.is_root():
            target = self._get_cost(node, aabb)
            self._merge(target, node)
            self._balance(self._root)

            for val in self._leaves.values():
                if val == node:
                    continue
                self._update(val)

    def _delta_cost(self, node, aabb):
        pass

    def _total_cost(self, node, aabb):  # FIXME: need to return the cost
        pass

    def _merge(self, node, aabb, body):
        assert node != None

        new_node = Node(body, aabb)
        copy = Node(node._body, node._aabb)
        self._leaves[new_node._body] = new_node
        if node.is_leaf():
            self._leaves[node._body] = copy

        node._body = None
        node._aabb = AABB.unite(aabb, node._aabb)
        node._left = copy
        node._right = new_node
        copy._parent = node
        new_node._parent = node

        return node

    def _update(self, parent):
        pass

    def _balance(self, parent):
        pass

    def _generate(self, node, pairs):
        pass

    def _height(self, node):
        pass
