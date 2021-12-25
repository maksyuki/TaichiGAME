from TaichiGAME.common.random import RandomGenerator


class TestRandom():
    def test_unique(self):
        dut1: int = RandomGenerator.unique()
        dut2: int = RandomGenerator.unique()
        assert dut1 == 1
        assert dut2 == 2

    def test_pop(self):
        dut1: int = RandomGenerator.unique()
        dut2: int = RandomGenerator.unique()
        RandomGenerator.pop(dut2)
        dut3: int = RandomGenerator.unique()
        dut4: int = RandomGenerator.unique()
        print(dut1)
        assert dut1 == 3
        assert dut2 == 4
        assert dut3 == 4
        assert dut4 == 5
