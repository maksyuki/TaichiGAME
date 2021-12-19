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
    BackgroundColor: int = 0x323232
    OuterLineColor: int = 0x00FF00
    FillColor: int = 0x008000
    AxisPointColor: int = 0x00FF00
    AxisLineColor: int = 0x008000
    AABBLineColor: int = 0xFFFF33
    BodyCenterColor: int = 0x660066
    AngleLineXColor: int = 0x0000FF
    AngleLineYColor: int = 0xFF0000
    QueryRectLineColor: int = 0xFF0000
    QueryRaycasFillColor: int = 0x00CCCC
    QueryRaycasOutLineColor: int = 0x33FFFF
    JointPointColor: int = 0xFF0000
    JointLineColor: int = 0x0000FF

    @staticmethod
    def clamp(num: float, low: float, high: float) -> float:
        assert low <= high

        if num < low:
            return low
        elif num > high:
            return high
        else:
            return num
