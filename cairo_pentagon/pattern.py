from typing import Callable, Dict, Optional

from cairo_pentagon import pentagon
from cairo_pentagon.utils import constants, typing

# This object must contain all the data necessary to apply a pattern onto a
# layer object.


class Pattern:

    style: Optional[typing.Pattern] = None
    spin: Optional[typing.Spin] = None

    def __int__(self, origin: Optional[typing.Origin] = None):
        self.origin: Optional[typing.Origin] = origin

    @property
    def row(self):
        return self.origin[1]

    @property
    def column(self):
        return self.origin[0]

    def apply(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class SquarePattern(Pattern):

    style: typing.Pattern = constants.Pattern.SQUARE

    def __init__(self, origin: Optional[typing.Origin] = None):
        super().__init__(origin)

    def apply(self, p: pentagon.Pentagon) -> bool:
        return self._quadrant_map[p.orientation](p)

    @property
    def _quadrant_map(self) -> Dict[typing.Orientation, Callable]:
        raise NotImplementedError

    @classmethod
    def get_subclass_from_spin(cls, spin: typing.Spin):
        """
        Return the subclass constructor for the provided orientation.

        Arguments:
            spin (typing.Spin):

        Returns:
            Square pattern subclass constructor.
        """
        for pattern in cls.__subclasses__():
            if getattr(pattern, 'spin') == spin:
                return pattern


class ClockwiseSquare(SquarePattern):

    spin: typing.Spin = constants.Spin.CLOCKWISE

    def __init__(self, origin: Optional[typing.Origin] = None):
        super().__init__(origin=origin)

    @property
    def _quadrant_map(self) -> Dict[typing.Orientation, Callable]:
        return {
            constants.Orientation.RIGHT: self._quadrant_one,
            constants.Orientation.DOWN: self._quadrant_two,
            constants.Orientation.LEFT: self._quadrant_three,
            constants.Orientation.UP: self._quadrant_four
        }

    def _quadrant_one(self, p) -> bool:
        return (
            p.row < self.row or
            (p.column > self.column and p.row <= self.row)
        )

    def _quadrant_two(self, p) -> bool:
        return (
            p.column > self.column + 1 or
            (p.row > self.row and p.column > self.column)
        )

    def _quadrant_three(self, p) -> bool:
        return (
            p.row > self.row + 1 or
            (p.column <= self.column and p.row > self.row)
        )

    def _quadrant_four(self, p) -> bool:
        return (
            p.column < self.column or
            (p.row <= self.row and p.column <= self.column)
        )


class CounterClockwiseSquare(SquarePattern):

    spin: typing.Spin = constants.Spin.COUNTER_CLOCKWISE

    def __init__(self, origin: Optional[typing.Origin] = None):
        super().__init__(origin=origin)

    @property
    def _quadrant_map(self) -> Dict[typing.Orientation, Callable]:
        return {
            constants.Orientation.UP: self._quadrant_one,
            constants.Orientation.RIGHT: self._quadrant_two,
            constants.Orientation.DOWN: self._quadrant_three,
            constants.Orientation.LEFT: self._quadrant_four
        }

    def _quadrant_one(self, p) -> bool:
        return (
            p.column < self.column + 1 or
            (p.row <= self.row and p.column > self.column)
        )

    def _quadrant_two(self, p) -> bool:
        return (
            p.row > self.row + 1 or
            (p.column > self.column and p.row > self.row)
        )

    def _quadrant_three(self, p) -> bool:
        return (
            p.column < self.column or
            (p.row > self.row and p.column <= self.column)
        )

    def _quadrant_four(self, p) -> bool:
        return (
            p.row < self.row or
            (p.column <= self.column and p.column <= self.column)
        )
