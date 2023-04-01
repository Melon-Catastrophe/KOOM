import arcade
from planar import Vec2     # For 2D vectors

class Ray():
    def __init__(self):
        self._startPos = Vec2(0, 0)
        self._endPos =  Vec2(0, 0)
        self._color = arcade.color.YELLOW
        self._distance = 0

    def __init__(self, startPos, endPos):
        assert type(startPos) == Vec2
        assert type(endPos) == Vec2

        self._startPos = startPos
        self._endPos = endPos
        self._color = arcade.color.YELLOW
        self._distance = arcade.get_distance(startPos.x, startPos.y, endPos.x, endPos.y)

    def draw(self):
        arcade.draw_line(self._startPos.x, self._startPos.y, self._endPos.x, self._endPos.y, self._color)

    def get_distance(self):
        return self._distance

    def get_end_y(self):
        return self._endPos.y