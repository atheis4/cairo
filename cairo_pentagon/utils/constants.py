from typing import List

from cairo_pentagon.utils import typing


class Colors:
    BLUE: typing.Color = (0, 0, 255)
    GREEN: typing.Color = (0, 255, 0)
    RED: typing.Color = (255, 0, 0)

    RGB: List[typing.Color] = [RED, GREEN, BLUE]


class DimensionalOffset:
    POSITIVE: typing.Coordinates = (0, 1)
    NEGATIVE: typing.Coordinates = (-1, 0)


class Orientation:
    UP: typing.Orientation = 'up'
    DOWN: typing.Orientation = 'down'
    LEFT: typing.Orientation = 'left'
    RIGHT: typing.Orientation = 'right'

    VERTICAL: List[typing.Orientation] = [UP, DOWN]
    HORIZONTAL: List[typing.Orientation] = [LEFT, RIGHT]


class Pattern:
    SQUARE = 'square'


class Shape:
    ALPHA: typing.Shape = 'alpha'
    BETA: typing.Shape = 'beta'


class Space:
    POSITIVE: typing.Shape = 'positive'
    NEGATIVE: typing.Shape = 'negative'


class Spin:
    CLOCKWISE: typing.Spin = 'clockwise'
    COUNTER_CLOCKWISE: typing.Spin = 'counter_clockwise'


DEFAULT_OPACITY: typing.Opacity = 0.25
DEFAULT_HEIGHT: typing.Height = 4
DEFAULT_WIDTH: typing.Width = 4
