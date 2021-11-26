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
            if node == None:
                return

            if node.is_leaf() and node.is_root():
                return

            if node == self._left:
                self._left = None
                node._parent = None
                aabb = self._right._aabb
            elif node == self._right:
                self._right = None
                node._parent = None
                aabb = self._left._aabb

        def swap(self, src, target):
            if src == self._left:
                self.separate(self._left)
                target._parent = self
                self._left = target

            elif src == self._right:
                self.separate(self._right)
                target._parent = self
                self._right = target

        def is_leaf(self):
            return self._left == None and self._right == None

        def is_branch(self):
            return self._left != None and self._right != None and self._parent != None

        def is_root(self):
            return self._parent == None

        def clear(self):
            self._body = None
            self._aabb.clear()

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
        if node == None:
            return

        self.clean_up(node._left)
        self.clean_up(node._right)

        node = None

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
        if node == None:
            return 0

        if node.is_leaf():
            return AABB.unite(node._aabb, aabb).surface_area()

        return AABB.unite(node._aabb,
                          aabb).surface_area() - node._aabb.surface_area()

    def _total_cost(self, node, aabb):  # FIXME: need to return the cost
        if node == None:
            return None

        cost = 0.0
        tmp = self._delta_cost(node, aabb)
        cost += tmp
        return cost + self._total_cost(node._parent, aabb)

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
        if parent == None:
            return

        if parent.is_branch() or parent.is_root():
            parent._aabb = AABB.unite(parent._left._aabb, parent._right._aabb)

        self._update(parent._parent)

    def _LL(self, node):
        if node == None or node.is_root():
            return

        if node._parent == self._root:
            parent = node._parent
            right = node._right
            parent._left = right
            node._parent = None

            node._right = parent
            right._parent = parent
            parent._parent = node
            self._root = node

        parent = node._parent
        right = node._right
        garnd_parent = parent._parent
        node._parent = garnd_parent

        if parent == garnd_parent._left:
            garnd_parent._left = node
        else:
            garnd_parent._right = node

        node._right = parent
        parent._parent = node
        parent._left = right
        right._parent = parent

    def _RR(self, node):
        if node == None or node.is_root():
            return

        if node._parent == self._root:
            parent = node._parent
            left = node._left
            parent._right = left
            node._parent = None

            node._left = parent
            left._parent = parent
            parent._parent = node
            self._root = node
            return

        parent = node._parent
        left = node._left
        garnd_parent = parent._parent

        node._parent = garnd_parent
        if parent == garnd_parent._right:
            garnd_parent._right = node
        else:
            garnd_parent._left = node

        node._left = parent
        parent._parent = node

        parent._right = left
        left._parent = parent

    def _balance(self, node):
        if node == None:
            return

        left_height = self._height(node._left)
        right_height = self._height(node._right)
        if np.fabs(left_height - right_height) <= 1:
            return

        if left_height > right_height:
            ll_height = self._height(node._left._left)
            lr_height = self._height(node._left._right)

            if ll_height < lr_height:
                self._RR(node._left._right)
            else:
                self._LL(node._left._right)

            self._LL(node._left)
        else:
            rr_height = self._height(node._right._right)
            rl_height = self._height(node._right._left)
            if rr_height < rl_height:
                self._LL(node._right._left)
            else:
                self._RR(node._right._right)
            self._RR(node._right)

        self._balance(node._left)
        self._balance(node._right)
        self._balance(node._parent)

    #FIXME:
    def _generate(self, node, pairs):
        pass

    def _height(self, node):
        return 0 if node == None else np.fmax(self._height(node._left),
                                              self._height(node._right)) + 1
