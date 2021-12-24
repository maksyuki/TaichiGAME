import taichi as ti


class Viewport():
    '''the viewport of the render, the origin is bottom left of
        the screen
        '''
    def __init__(self,
                 top_left: ti.Vector = ti.Vector([0.0, 720.0]),
                 bot_right: ti.Vector = ti.Vector([1280.0, 0.0])):

        assert top_left.x < bot_right.x
        assert top_left.y > bot_right.y

        self._top_left: ti.Vector = top_left
        self._bot_right: ti.Vector = bot_right

    @property
    def width(self) -> float:
        return self._bot_right.x - self._top_left.x

    @width.setter
    def width(self, width: float) -> None:
        self._bot_right.x = self._top_left.x + width

    @property
    def height(self) -> float:
        return self._top_left.y - self._bot_right.y

    @height.setter
    def height(self, height: float) -> None:
        self._top_left.y = self._bot_right.y + height

    def set_value(self, width: float, height: float):
        self.width = width
        self.height = height
