from typing import Dict, Optional, Tuple

from cairo_pentagon.pentagon import Pentagon
from cairo_pentagon.utils import constants, typing


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
    _shape_to_pentagons: Dict[typing.Shape, Tuple[typing.Orientation]] = {
        constants.Shape.ALPHA: (
            constants.Orientation.DOWN,
            constants.Orientation.LEFT,
            constants.Orientation.UP,
            constants.Orientation.RIGHT
        ),
        constants.Shape.BETA: (
            constants.Orientation.RIGHT,
            constants.Orientation.DOWN,
            constants.Orientation.LEFT,
            constants.Orientation.UP
        )
    }
    _shape_shift: Dict[typing.Shape, typing.Shape] = {
        constants.Shape.ALPHA: constants.Shape.BETA,
        constants.Shape.BETA: constants.Shape.ALPHA
    }

    def __init__(
            self,
            init_shape: typing.Shape = constants.Shape.ALPHA,
            width: typing.Width = constants.DEFAULT_WIDTH,
            height: typing.Height = constants.DEFAULT_HEIGHT,
            color: typing.Color = constants.Colors.RED,
            opacity: typing.Opacity = constants.DEFAULT_OPACITY
    ):
        self._init_shape: typing.Shape = init_shape
        self.width: typing.Width = width
        self.height: typing.Height = height

        self._pentagon_map: Optional[Dict[typing.Key, Pentagon]] = None

        # rendering characteristics
        self.color: typing.Color = color
        self.opacity: typing.Opacity = opacity

    @property
    def pentagon_map(self) -> Dict[typing.Key, Pentagon]:
        return self._pentagon_map

    @pentagon_map.setter
    def pentagon_map(self, value: Optional[Dict[typing.Key, Pentagon]]) -> None:
        self._pentagon_map = value

    @property
    def shape(self) -> typing.Shape:
        return self._init_shape

    def construct_layer(self) -> None:
        """Create the pentagon_map of unique key to pentagon objects."""
        if self._pentagon_map:
            raise RuntimeError(
                "A mapping for this layer already exists, cannot construct a "
                "new one."
            )
        self._pentagon_map: Dict[typing.Key, Pentagon] = {}

        curr_shape: typing.Shape = self.shape

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

    def _construct_cell(
            self,
            shape: typing.Shape,
            row: typing.Row,
            column: typing.Column
    ) -> None:
        """Create a new cell to add to our row."""
        for orientation in self._shape_to_pentagons[shape]:
            # Check to see if the pentagon has already been made. If it isn't,
            # create it and add it to the pentagon map.
            key: typing.Key = Pentagon.define_unique_key(
                orientation=orientation,
                shape=shape,
                row=row,
                column=column
            )
            if key not in self._pentagon_map:
                # Get the class constructor for the pentagon we need to build.
                factory = Pentagon.get_subclass_from_orientation(orientation)
                # Build the pentagon.
                pentagon: Pentagon = factory(
                    shape=shape,
                    row=row,
                    column=column
                )
                # Add to our dict of unique key to pentagon.
                self._pentagon_map.update({key: pentagon})

    def reset(self):
        self.pentagon_map = None
