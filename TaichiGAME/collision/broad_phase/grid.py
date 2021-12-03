from typing import List, Dict, Optional, Tuple

import numpy as np

from ...math.matrix import Matrix
from .aabb import AABB


class UniformGrid():
    def __init__(self):
        self._grid_size: float = 1.0

    def generate(self) -> List[Tuple[Matrix, Matrix]]:
        pass

    def raycast(self, p: Matrix, d: Matrix) -> Matrix:
        pass

    def update(self, body):
        pass

    def insert(self, body):
        pass

    def remove(self, body):
        pass
