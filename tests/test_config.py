from typing import List, Dict, Optional, Tuple

import numpy as np
from TaichiGAME.common.config import Config


class TestConfig():
    def test_clamp(self):
        low_limit: float = 1.4
        high_limit: float = 5.7

        dut: float = Config.clamp(23, low_limit, high_limit)
        assert np.isclose(dut, high_limit)

        dut = Config.clamp(-3, low_limit, high_limit)
        assert np.isclose(dut, low_limit)

        dut = Config.clamp(2.8, low_limit, high_limit)
        assert np.isclose(dut, 2.8)

        dut = Config.clamp(1.3911111111, low_limit, high_limit)
        assert np.isclose(dut, low_limit)