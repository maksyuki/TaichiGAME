from TaichiGAME.common.random import RandomGenerator


class TestRandom():
    def test_unique(self):
        dut1: int = RandomGenerator.unique()
        dut2: int = RandomGenerator.unique()
        assert dut1 == 1001
        assert dut2 == 1002

    def test_pop(self):
        dut1: int = RandomGenerator.unique()
        dut2: int = RandomGenerator.unique()
        RandomGenerator.pop(dut2)
        dut3: int = RandomGenerator.unique()
        dut4: int = RandomGenerator.unique()
        print(dut1)
        assert dut1 == 1003
        assert dut2 == 1004
        assert dut3 == 1004
        assert dut4 == 1005