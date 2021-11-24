class Tree():
    def __init__(self):
        pass

    class Node():
        def __init__(self):
            pass

        def is_leaf(self):
            pass

        def is_branch(self):
            pass

        def is_root(self):
            pass

        def is_empty(self):
            pass

        def clear(self):
            pass

    def query(self, body):
        pass

    def raycast(self, start_point, dir):
        pass

    def generate(self):
        pass

    def insert(self, body):
        pass

    def remove(self, body):
        pass

    def clear_all(self):
        pass

    def update(self, body):
        pass

    def tree(self):
        pass

    def root_index(self):
        pass

    def _query_nodes(self, node_index, aabb, res):
        pass

    def _traverse_lowest_cost(self, node_index, box_index, cost, final_index):
        pass

    def _raycast(self, res, node_index, p, d):
        pass

    def _generate(self, node_index, pairs):
        pass

    def _extract(self, target_index):
        pass

    def _merge(self, node_index, leaf_index):
        pass

    def _ll(self, node_index):
        pass

    def _rr(self, node_index):
        pass

    def _balance(self, target_index):
        pass

    def _separate(self, source_index, parent_index):
        pass

    def _join(self, node_index, box_index):
        pass

    def _remove(self, target_index):
        pass

    def _elevate(self, target_index):
        pass

    def _upgrade(self, node_index):
        pass

    def _calc_lowest_cost_node(self, node_index):
        pass

    def _total_cost(self, node_index, leaf_index):
        pass

    def _delta_cost(self, node_index, box_index):
        pass

    def _allocate_node(self):
        pass

    def height(self, target_index):
        pass
