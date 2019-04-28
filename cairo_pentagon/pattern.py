from typing import Dict, Optional

from cairo_pentagon.pentagon import Pentagon
from cairo_pentagon.utils.constants import Shape, Spin
from cairo_pentagon.utils import typing

# This object must contain all the data necessary to apply a pattern onto a
# layer object.

# What should this look like? Which objects are interacting where to turn the
# individual pentagon's visibility off and on?

# If all a pattern object is doing is turning certain pentagons off and on,
# then all it needs are the keys of the dictionary to turn off.

# potential: linear transformations.
# A 90 degree rotation counter clockwise is representable as a linear
# transformation where the vector is multiplied by [[0, 1], [-1, 0]] * [x, y]
# [[a, c], [b, d]][x, y] = x * [a, c] + y * [b, d] = [ax + by, cx + dy]


class Pattern:

    _pattern_style: Optional[typing.PatternStyle] = None

    def __int__(
            self,
            origin: typing.Origin = None,
            shape: typing.Shape = Shape.ALPHA,
            spin: typing.Spin = Spin.CLOCKWISE
    ):
        self.origin: Optional[typing.Origin] = origin
        self.spin: Optional[typing.Spin] = spin

    def apply(self, *args, **kwargs) -> None:
        raise NotImplementedError


class SquarePattern(Pattern):

    _pattern_style: typing.PatternStyle = 'square'

    def __init__(
            self,
            origin: Optional[typing.Origin] = None,
            spin: Optional[typing.Spin] = None
    ):
        super().__init__(origin, spin)

    def apply(self, pentagon_map: Dict[typing.Key, Pentagon]) -> None:
        for key, pentagon in pentagon_map.items():
            orientation, row, col = key

