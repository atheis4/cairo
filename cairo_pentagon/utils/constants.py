from enum import Enum
from typing import List

from cairo_pentagon.utils import typing


class Colors(Enum):
    BLUE: typing.Color = (0, 0, 255)
    GREEN: typing.Color = (0, 255, 0)
    RED: typing.Color = (255, 0, 0)


class DimensionalOffset(Enum):
    POSITIVE: typing.Coordinates = (0, 1)
    NEGATIVE: typing.Coordinates = (-1, 0)


class Orientation(Enum):
    UP: typing.Orientation = 'up'
    DOWN: typing.Orientation = 'down'
    LEFT: typing.Orientation = 'left'
    RIGHT: typing.Orientation = 'right'
    VERTICAL: List[typing.Orientation] = [UP, DOWN]
    HORIZONTAL: List[typing.Orientation] = [LEFT, RIGHT]


class Pattern(Enum):
    SQUARE = 'square'


class Shape(Enum):
    ALPHA: typing.Shape = 'alpha'
    BETA: typing.Shape = 'beta'
    SHAPES: List[typing.Shape] = [ALPHA, BETA]


class Space(Enum):
    POSITIVE: typing.Shape = 'positive'
    NEGATIVE: typing.Shape = 'negative'
    SPACES: List[typing.Shape] = [POSITIVE, NEGATIVE]


class Spin(Enum):
    CLOCKWISE: typing.Spin = 'clockwise'
    COUNTER_CLOCKWISE: typing.Spin = 'counter_clockwise'
    SPINS: List[typing.Spin] = [CLOCKWISE, COUNTER_CLOCKWISE]


DEFAULT_OPACITY: typing.Opacity = 0.25
DEFAULT_HEIGHT: typing.Height = 4
DEFAULT_WIDTH: typing.Width = 4
