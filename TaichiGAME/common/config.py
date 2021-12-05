class Config():
    SimplexMax = 8
    Epsilon = 1e-5
    Max = 1e37
    PositiveMin = 1e-37
    NegativeMin = -Max
    Pi = 3.14159265
    HalfPi = Pi / 2.0
    DoublePi = Pi * 2.0
    ReciprocalOfPi = 0.3183098861
    GeometryEpsilon = 0.00001
    MaxVelocity = 1000.0
    MaxAngularVelocity = 1000.0

    @staticmethod
    def clamp(num: float, low: float, high: float) -> float:
        assert low <= high

        if num < low:
            return low
        elif num > high:
            return high
        else:
            return num