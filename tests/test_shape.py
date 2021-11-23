import numpy as np
from TaichiGAME.geometry.shape import Point

class TestShape():
    def test_point(self):
        p1 = Point()
        assert np.isclose(p1._pos.val[0], 0)
        assert np.isclose(p1._pos.val[1], 0)