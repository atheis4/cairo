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

    _pattern_style: Optional[str] = None

    def __int__(
            self,
            origin: typing.Origin = None,
            shape: str = Shape.ALPHA,
            spin: str = Spin.CLOCKWISE
    ):
        self.origin: Optional[typing.Origin] = origin
        self.spin: Optional[str] = spin


class SquarePattern(Pattern):

    _pattern_style: Optional[str] = 'square'

    def __init__(
            self,
            origin: Optional[typing.Origin] = None,
            spin: Optional[str] = None
    ):
        super().__init__(origin, spin)

    def _setup(self):


    def apply(self, pentagon_map: Dict[typing.Key, Pentagon]):
        for key, pentagon in pentagon_map:
            pass
