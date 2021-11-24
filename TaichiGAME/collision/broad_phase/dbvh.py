import numpy as np

from ...math.matrix import Matrix
from ...geometry.gemo_algo import GeomAlgo2D
from ...geometry.shape import *

class DBVH():
    def __init__(self):
        pass
    
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
    
    def insert(self, body):
        pass

    def update(self, body):
        pass
    
    def extract(self, body):
        pass

    def erease(self, body):
        pass

    def clean_up(self, node):
        pass

    def root(self):
        pass

    def raycast(self, start_point, dir):
        pass
    
    def generate(self):
        pass

    def leaves(self):
        pass
    
    def query(self, src, nodes, skip_body=None):
        pass

    @staticmethod
    def query_nodes(node, src, nodes, skip_body=None):
        pass
    
    def _raycast(self, res, node, start_point, dir):
        pass

    def _insert(self, node):
        pass

    def _delta_cost(self, node, aabb):
        pass

    def _total_cost(self, node, aabb, cost):
        pass

    def _merge(self, node, aabb, body):
        pass

    def _update(self, parent):
        pass

    def _balance(self, parent):
        pass

    def _generate(self, node, pairs):
        pass

    def _height(self, node):
        pass
        