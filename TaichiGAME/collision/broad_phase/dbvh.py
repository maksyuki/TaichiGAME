from typing import List, Dict, Optional, SupportsRound, TYPE_CHECKING, Tuple

import numpy as np

from ...math.matrix import Matrix
from ...geometry.geom_algo import GeomAlgo2D
from ...dynamics.body import Body
from ..broad_phase.aabb import AABB


class DBVH():
    '''Dynamic Bounding Volume Hierarchy
    This is implemented by traditional binary search tree
    '''
    class Node():
        def __init__(self, body: Body = None, aabb: AABB = None):
            self._parent = None
            self._left = None
            self._right = None
            self._body: Optional[Body] = body
            self._aabb: AABB = aabb

        def separate(self, node):
            if node == None:
                return

            if node.is_leaf() and node.is_root():
                return

            if node == self._left:
                self._left = None
                node._parent = None
                self._aabb = self._right._aabb
            elif node == self._right:
                self._right = None
                node._parent = None
                self._aabb = self._left._aabb

        def swap(self, src, target):
            if src == self._left:
                self.separate(self._left)
                target._parent = self
                self._left = target

            elif src == self._right:
                self.separate(self._right)
                target._parent = self
                self._right = target

        def is_leaf(self) -> bool:
            return self._left == None and self._right == None

        def is_branch(self) -> bool:
            return self._left != None and self._right != None and self._parent != None

        def is_root(self) -> bool:
            return self._parent == None

        def clear(self) -> bool:
            self._body = None
            self._aabb.clear()

    def __init__(self):
        self._root: Optional[DBVH.Node] = None
        self._profile: float = 0.0
        self._leaf_factor: float = 0.5
        self._leaves: Dict[Body, DBVH.Node] = {}

    def find(self, body: Body) -> bool:
        for b in self._leaves.keys():
            if b == body:
                return True
        return False

    def insert(self, body: Body):
        if not self.find(body):
            return

        aabb: AABB = AABB.from_body(body)
        aabb.expand(self._leaf_factor)

        if self._root == None:
            self._root = DBVH.Node(body, aabb)
            self._leaves[body] = self._root
            return

        if self._root.is_leaf() and self._root.is_root():
            self._merge(self._root, aabb, body)
            self._update(self._root)
            return

        target = self._get_cost(None, aabb)  #FIXME: is right func?
        self._merge(target, aabb, body)
        self._balance(self._root)
        self._update(target)
        for val in self._leaves.values():
            self._update(val)

    def update(self, body: Body):
        assert body != None

        if not self.find(body):
            return

        thin: AABB = AABB.from_body(body)
        thin.expand(0.1)
        if not thin.is_subset(self._leaves[body]._aabb):
            node = self.extract(body)
            self._insert(node)

    def extract(self, body: Body):
        if not self.find(body):
            return None

        source: DBVH.Node = self._leaves[body]
        parent: DBVH.Node = source._parent
        parent.separate(source)

        if source.is_root() and source.is_leaf() and len(self._leaves) < 2:
            self._root = None
            return source

        child: DBVH.Node = self._moveup(parent)
        self._balance(child._parent)
        self._update(child._parent)
        return source

    def erase(self, body: Body):
        target: Optional[DBVH.Node] = self.extract(body)
        if target == None:
            return

        target._body = None
        target._aabb.clear()
        # FIXME:
        # del target
        del self._leaves[body]

    def clean_up(self, node: Optional[Node]):
        if node == None:
            return

        self.clean_up(node._left)
        self.clean_up(node._right)

        # FIXME:
        # del node
        node = None

    def root(self) -> Optional[Node]:
        return self._root

    def raycast(self, start: Matrix, dir: Matrix) -> List[Body]:
        res: List[Body] = []
        self._raycast(res, self._root, start, dir)
        return res

    def generate(self) -> List[Tuple[Body, Body]]:
        self._profile = 0.0
        res: List[Tuple[Body, Body]] = []
        self._generate(self._root, res)
        return res

    def leaves(self) -> Dict[Body, Node]:
        return self._leaves

    def query(self, src: AABB, nodes: List[Node], skip_body: Body = None):
        DBVH.query_nodes(self._root, src, nodes, skip_body)

    @staticmethod
    def query_nodes(node: Node,
                    aabb: AABB,
                    nodes: List[Node],
                    skip_body: Body = None):
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

    def _raycast(self, res: List[Body], node: Optional[Node], start: Matrix,
                 dir: Matrix):
        if node == None:
            return

        if node._aabb.raycast(start, dir):
            if node.is_leaf():
                res.append(node._body)
            else:
                self._raycast(res, node._left, start, dir)
                self._raycast(res, node._right, start, dir)

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

    def _moveup(self, branch):
        pass

    def _insert(self, node: Optional[Node]):
        if node == None:
            return

        aabb: AABB = AABB.from_body(node._body)
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
            target: Optional[DBVH.Node] = self._get_cost(node, aabb)
            self._merge(target, node)
            self._balance(self._root)

            for val in self._leaves.values():
                if val == node:
                    continue
                self._update(val)

    def _delta_cost(self, node: Optional[Node], aabb: AABB) -> float:
        if node == None:
            return 0.0

        if node.is_leaf():
            return AABB.unite(node._aabb, aabb).surface_area()

        return AABB.unite(node._aabb,
                          aabb).surface_area() - node._aabb.surface_area()

    def _total_cost(self, node: Optional[Node],
                    aabb: AABB) -> float:  # FIXME: need to return the cost
        if node == None:
            return None

        cost: float = 0.0
        tmp: float = self._delta_cost(node, aabb)
        cost += tmp
        return cost + self._total_cost(node._parent, aabb)

    #FIXME: tow params version is not impl
    def _merge(self, node: Optional[Node], aabb: AABB, body: Body) -> Node:
        assert node != None

        new_node: DBVH.Node = DBVH.Node(body, aabb)
        copy: DBVH.Node = DBVH.Node(node._body, node._aabb)

        self._leaves[new_node._body] = new_node
        if node.is_leaf():
            self._leaves[node._body] = copy

        node._body = None
        node._aabb = AABB.unite(aabb, node._aabb)
        node._left = copy
        node._right = new_node
        copy._parent = node
        new_node._parent = node

        return new_node

    def _update(self, parent: Optional[Node]):
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

    def _balance(self, node: Optional[Node]):
        if node == None:
            return

        left_height: int = self._height(node._left)
        right_height: int = self._height(node._right)
        if np.fabs(left_height - right_height) <= 1:
            return

        # left unbalance
        if left_height > right_height:
            ll_height: int = self._height(node._left._left)
            lr_height: int = self._height(node._left._right)

            if ll_height < lr_height:
                self._RR(node._left._right)
            else:
                self._LL(node._left._left)

            self._LL(node._left)

        # right unbalance
        else:
            rr_height: int = self._height(node._right._right)
            rl_height: int = self._height(node._right._left)
            if rr_height < rl_height:
                self._LL(node._right._left)
            else:
                self._RR(node._right._right)
            self._RR(node._right)

        self._balance(node._left)
        self._balance(node._right)
        self._balance(node._parent)

    #FIXME: two overlad impl
    def _generate(self, node, pairs):
        pass

    def _height(self, node: Optional[Node]) -> int:
        return 0 if node == None else np.fmax(self._height(node._left),
                                              self._height(node._right)) + 1
