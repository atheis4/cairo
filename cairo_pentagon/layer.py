from typing import Any, Dict, Optional, Tuple, Union

from cairo_pentagon.pentagon import Pentagon
from cairo_pentagon.pattern import Pattern
from cairo_pentagon.utils.constants import Orientation, Shape
from cairo_pentagon.utils import typing


class Layer:
    """
    Container for one layer of Pentagon objects.

    A layer is a mapping of orientation, row, and column values to their unique
    Pentagon objects.

    Pentagon's are arranged in a 'shape': either 'alpha' or 'beta'.
    Each shape/cell is made up of four separate orientations of pentagon:
    'up', 'down', 'left', 'right'. 'Alpha' and 'beta' shapes maintain different
    orders of orientation.

    'alpha': 'down', 'left', 'up', 'right'
    'beta': 'right', 'down', 'left', 'up'

    These two shapes will selectively alternate as the layer is constructed to
    build the Cairo Pentagon pattern.
    """
    # Replace with the Pentagon subtypes: Up, Down, Left, Right
    _shape_to_pentagons: Dict[str, Dict[str, Tuple[str]]] = {
        Shape.ALPHA: (
            Orientation.DOWN,
            Orientation.LEFT,
            Orientation.UP,
            Orientation.RIGHT
        ),
        Shape.BETA: (
            Orientation.RIGHT,
            Orientation.DOWN,
            Orientation.LEFT,
            Orientation.UP
        )
    }
    # Simple switch to control the 'mirror' effect of the pattern
    _shape_shift: Dict[str, str] = {
        Shape.ALPHA: Shape.BETA, Shape.BETA: Shape.ALPHA
    }

    def __init__(
            self,
            init_shape: str = Shape.ALPHA,
            width: int = 4,
            height: int = 4
    ):
        self._init_shape: str = init_shape
        self.width: int = width
        self.height: int = height

        self._pentagon_map: typing.PentagonMap = None

        # pattern object
        self.pattern: Optional[Pattern] = None

        # rendering characteristics
        self.color: Optional[Tuple[int, int, int]] = None
        self.opacity: float = 0.25

    @property
    def pattern(self) -> Pattern:
        return self._pattern

    @pattern.setter
    def pattern(self, value) -> None:
        self._pattern = value

    @property
    def shape(self) -> str:
        return self._init_shape

    def construct_layer(self):
        # Check to see if we already have a pentagon mapping on this object,
        # raise if so.
        if self._pentagon_map is not None:
            raise RuntimeError(
                "A mapping for this layer already exists, cannot construct a "
                "new one."
            )
        self._pentagon_map: typing.PentagonMap = {}

        curr_shape: str = self.shape

        for curr_height in range(self.height):
            # Create the row.
            # Add all of the cells with shapes equal to init_shape first.
            # The starting column value of an even-indexed height is zero for
            # the initial shape and one for an odd-indexed heights.
            start, stop, step = curr_height % 2, self.width, 2
            for curr_width in range(start, stop, step):
                self._construct_cell(curr_shape, curr_height, curr_width)

        # Switch the shape and iterate again to complete the layer.
        curr_shape = self._shape_shift[curr_shape]

        for curr_height in range(self.height):
            # The starting column value of an even-indexed height is one for
            # the secondary shape and zero for odd-indexed heights.
            start, stop, step = 1 if curr_height % 2 == 0 else 0, self.width, 2
            for curr_width in range(start, stop, step):
                self._construct_cell(curr_shape, curr_height, curr_width)

    def _construct_cell(self, shape: str, row: int, col: int):
        """Create a new cell to add to our row."""
        for orientation in self._shape_to_pentagons[shape]:
            # Check to see if the pentagon has already been made. If it isn't,
            # create it and add it to the pentagon map.
            key = Pentagon.define_unique_key(
                orientation=orientation,
                shape=shape,
                row=row,
                col=col
            )
            pentagon = self._pentagon_map.get(key)
            if not pentagon:
                # Get the class constructor for the pentagon we need to build.
                factory = Pentagon.get_subclass_from_orientation(orientation)
                # Build the pentagon.
                pentagon = factory(shape=shape, row=row, col=col)
                # Add to our dict of unique key to pentagon.
                unique_key: Tuple[str, Any, Any] = (
                    pentagon.orientation, pentagon.row, pentagon.col
                )
                self._pentagon_map.update({unique_key: pentagon})

    def all_pentagons(self):
        return list(self._pentagon_map.values())

    def apply(self, pattern: Pattern) -> None:
        """
        Apply a pattern to the layer.
        """
        self.pattern = pattern

    def reset(self):
        pass


layer = Layer(init_shape=Shape.ALPHA)
layer.construct_layer()