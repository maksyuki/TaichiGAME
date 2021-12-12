class Config():
    SimplexMax: int = 8
    Epsilon: float = 1e-5
    Max: float = 1e37
    PositiveMin: float = 1e-37
    NegativeMin: float = -Max
    Pi: float = 3.14159265
    HalfPi: float = Pi / 2.0
    DoublePi: float = Pi * 2.0
    ReciprocalOfPi: float = 0.3183098861
    GeometryEpsilon: float = 0.00001
    MaxVelocity: float = 1000.0
    MaxAngularVelocity: float = 1000.0
    # render
    OuterLineColor: int = 0x00FF00
    FillColor: int = 0x008000
    AxisPointColor: int = 0x00FF00
    AxisLineColor: int = 0x008000

    @staticmethod
    def clamp(num: float, low: float, high: float) -> float:
        assert low <= high

        if num < low:
            return low
        elif num > high:
            return high
        else:
            return num
