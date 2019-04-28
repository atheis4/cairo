from typing import Any, Dict, Optional, Tuple, Union

from cairo_pentagon.utils.constants import Orientation, Shape
from cairo_pentagon.utils import constants, typing


class Pentagon:
    """
    Pentagons represent the object that will be rendered in the final piece.

    Pentagons have several attributes which uniquely define its position, shape,
    and orientation.

    Attributes:

    Orientation
    -----------
    Pentagons are isosceles: the angle on one of the points is greater than all
    others. The direction that this greatest-angled point faces defines the
    pentagon's orientation. The four different orientations of pentagons: up,
    down, left, and right.

    Shape
    -----

    Fixed and Dynamic Dimension
    ---------------------------
    Each pentagon spans across either the row or column dimension. Up and Down
    pentagons exist within a single row, but span two columns. So for these
    pentagons, the row is the fixed dimension and the column is the dynamic
    dimension. While Left and Right pentagons exist within one column and span
    two rows.
    """
    # TODO: Since this is the actual object being rendered, it needs to have
    # knowledge of its visibility, color, and opacity.

    # One of 'up', 'down', 'left', 'right' - defined as subclass attribute
    # Pentagons are not equilateral and have a 'larger' point. Orientation
    # refers to the direction that this fifth, larger point is directed.
    orientation: Optional[typing.Orientation] = None

    # The entire pattern exists within a zero-indexed, row and column grid. The
    # top-left is considered the origin.

    # Each pentagon spans more than one row or column. Up and Down pentagons
    # always span two columns, while Left and Right pentagons always span two
    # rows. Whether the pentagon spans move toward or away from the origin is
    # a result of which shape they inhibit, 'alpha' or 'beta'.
    _dim_map: typing.DimensionMap = {
        (constants.Orientation.DOWN, constants.Orientation.LEFT): {
            constants.Shape.ALPHA: constants.DimensionalOffset.NEGATIVE,
            constants.Shape.BETA: constants.DimensionalOffset.POSITIVE
        },
        (constants.Orientation.RIGHT, constants.Orientation.UP): {
            constants.Shape.ALPHA: constants.DimensionalOffset.POSITIVE,
            constants.Shape.BETA: constants.DimensionalOffset.NEGATIVE
        }
    }

    # Pentagons are uniquely identified by four attributes: their shape,
    # orientation, row, and column. Each of these are hashable values and will
    # be used to tell our program whether the requested pentagon has already
    # been created, or if we need to make it. This allows us to reference the
    # same pentagon object across a single frame layer.

    def __init__(self, shape: typing.Shape = constants.Shape.ALPHA):
        # A pentagon always exists relative to a 2-d array of rows and columns.
        # One pentagon may exist in multiple rows and columns at the same time,
        # so long as they follow strict rules about position. Certain types of
        # pentagon--based on orientation--may only exist in the same row or the
        # same column.

        # Up/Down pentagons can only exist in one row, but over two columns.
        # Left/Right pentagons can only exist in one column, but over two rows.
        self.shape: typing.Shape = shape

        self.visible: typing.Visibility = False
        self.row: Optional[typing.Row] = None
        self.col: Optional[typing.Column] = None

    def __repr__(self) -> str:
        return (
            f'<{self.orientation} - row: {self.row}, col: {self.col}, shape: '
            f'{self.shape}>'
        )

    @property
    def row(self) -> Union[typing.Row, typing.CompoundDimension]:
        return self._row

    @row.setter
    def row(self, value) -> None:
        self._row = value

    @property
    def col(self) -> Union[typing.Column, typing.CompoundDimension]:
        return self._col

    @col.setter
    def col(self, value) -> None:
        self._col = value

    @property
    def visible(self) -> typing.Visibility:
        return self._visible

    @visible.setter
    def visible(self, value) -> None:
        self._visible = value

    def is_visible(self) -> typing.Visibility:
        return self.visible

    def _create_compound_dimension(
            self,
            dimension: typing.Dimension
    ) -> typing.CompoundDimension:
        """
        Creates the set of values for the 'compound' dimension (either row or
        column).

        Up and Down pentagons span more than one column, while Left and Right
        pentagons span more than one row.

        Arguments:
            dimension (int): represents either the column or row value to be
                'split' into a set of two column or row values.

        Returns:
            Set of two integers representing the two rows or two columns that
            the shape exists within.
        """
        for orientations in self._dim_map.keys():
            if self.orientation in orientations:
                return (
                    dimension + self._dim_map[orientations][self.shape][0],
                    dimension + self._dim_map[orientations][self.shape][1]
                )

    def get_unique_key(self) -> typing.Key:
        """Return the unique key of this pentagon."""
        return self.orientation, self.row, self.col

    @classmethod
    def define_unique_key(
            cls,
            orientation: typing.Orientation,
            shape: typing.Shape,
            row: typing.Dimension,
            col: typing.Dimension
    ) -> typing.Key:
        """
        Provided an orientation, a shape, a row, and a column, return the
        unique key for all pentagons defined by these attributes.

        Arguments:
            orientation (typing.Orientation):
            shape (typing.Shape):
            row (typing.Dimension):
            col(typing.Dimension)

        Returns:
            A tuple of (orientation, row, col)
        """
        for orientations in cls._dim_map.keys():
            if orientation in orientations:
                if orientation in [Orientation.UP, Orientation.DOWN]:
                    dimensions: Tuple[typing.Dimension, typing.Dimension] = (
                        row,
                        (col + cls._dim_map[orientations][shape][0],
                         col + cls._dim_map[orientations][shape][1]))
                else:
                    dimensions: Tuple[typing.Dimension, typing.Dimension] = (
                        (row + cls._dim_map[orientations][shape][0],
                         row + cls._dim_map[orientations][shape][1]),
                        col
                    )
                return (orientation, *dimensions)

    @classmethod
    def coordinates_from_key(cls, key: typing.Key) -> typing.Coordinates:


    @classmethod
    def get_subclass_from_orientation(cls, orientation: str):
        """
        Return the subclass constructor for the provided orientation.

        Arguments:
            orientation (str):

        Returns:
            Pentagon subclass constructor.
        """
        for pentagon in cls.__subclasses__():
            if pentagon.orientation == orientation:
                return pentagon


class UpPentagon(Pentagon):

    orientation: typing.Orientation = constants.Orientation.UP

    def __init__(
            self,
            shape: typing.Shape,
            row: typing.Row,
            col: typing.CompoundDimension
    ):
        super().__init__(shape=shape)
        self.row: typing.Row = row
        self.col: typing.CompoundDimension = self._create_compound_dimension(
            dimension=col
        )


class DownPentagon(Pentagon):

    orientation: typing.Orientation = constants.Orientation.DOWN

    def __init__(
            self,
            shape: typing.Shape,
            row: typing.Row,
            col: typing.CompoundDimension
    ):
        super().__init__(shape=shape)
        self.row: typing.Row = row
        self.col: typing.CompoundDimension = self._create_compound_dimension(
            dimension=col
        )


class LeftPentagon(Pentagon):

    orientation: typing.Orientation = constants.Orientation.LEFT

    def __init__(
            self,
            shape: typing.Shape,
            row: typing.CompoundDimension,
            col: typing.Column
    ):
        super().__init__(shape=shape)
        self.row: typing.CompoundDimension = self._create_compound_dimension(
            dimension=row
        )
        self.col: typing.Column = col


class RightPentagon(Pentagon):

    orientation: typing.Orientation = constants.Orientation.RIGHT

    def __init__(
            self,
            shape: typing.Shape,
            row: typing.CompoundDimension,
            col: typing.Column
    ):
        super().__init__(shape)
        self.row: typing.CompoundDimension = self._create_compound_dimension(
            dimension=row
        )
        self.col: typing.Column = col
