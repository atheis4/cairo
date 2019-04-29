from typing import Optional, Tuple, Union

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


    Simple and Compound Dimensions
    ------------------------------
    Each pentagon spans across either the row or column dimension.

    Up and Down pentagons exist within a single row, but span two columns. For
    these pentagons, the row is represented by a single int and the column is
    represented by a tuple of ints (compound).

    While Left and Right pentagons exist within one column and span two rows.
    The column is represented by a single int and the row is represented by a
    tuple of ints (compound).


    Key
    ---
    Pentagons are uniquely identified by four attributes: shape, orientation,
    row, and column. Each of these are hashable values and will be used to tell
    our program whether the requested pentagon has already been created, or if
    we need to make it. This allows us to reference the same pentagon object
    across a single frame layer.
    """
    _dim_map: typing.DimensionMap = {
        constants.Shape.ALPHA: {
            constants.Orientation.DOWN: constants.DimensionalOffset.NEGATIVE,
            constants.Orientation.LEFT: constants.DimensionalOffset.NEGATIVE,
            constants.Orientation.UP: constants.DimensionalOffset.POSITIVE,
            constants.Orientation.RIGHT: constants.DimensionalOffset.POSITIVE
        },
        constants.Shape.BETA: {
            constants.Orientation.RIGHT: constants.DimensionalOffset.NEGATIVE,
            constants.Orientation.DOWN: constants.DimensionalOffset.POSITIVE,
            constants.Orientation.LEFT: constants.DimensionalOffset.POSITIVE,
            constants.Orientation.UP: constants.DimensionalOffset.NEGATIVE
        }
    }

    _coord_map: typing.CoordinateMap = {
        constants.Shape.ALPHA: {
            constants.Orientation.DOWN: max,
            constants.Orientation.LEFT: max,
            constants.Orientation.UP: min,
            constants.Orientation.RIGHT: min
        },
        constants.Shape.BETA: {
            constants.Orientation.RIGHT: max,
            constants.Orientation.DOWN: min,
            constants.Orientation.LEFT: min,
            constants.Orientation.UP: max
        }
    }

    orientation: Optional[typing.Orientation] = None

    def __init__(self, shape: typing.Shape = constants.Shape.ALPHA):
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
        return (
            dimension + self._dim_map[self.shape][self.orientation][0],
            dimension + self._dim_map[self.shape][self.orientation][1]
        )

    def get_unique_key(self) -> typing.Key:
        """Return the unique key of this pentagon."""
        return self.orientation, self.row, self.col

    def coordinates_from_key(self, key: typing.Key) -> typing.Coordinates:
        """
        Return coordinates from a pentagon key.

        Arguments:
            key (typing.Key):

        Returns:
            A Coordinate tuple of (row, col)
        """
        orientation, row, column = key
        if orientation in [
            constants.Orientation.UP, constants.Orientation.DOWN
        ]:
            coordinates: typing.Coordinates = (
                row,
                self._coord_map[self.shape][orientation](column)
            )
        else:
            coordinates: typing.Coordinates = (
                self._coord_map[self.shape][orientation](row),
                column
            )
        return coordinates

    @classmethod
    def define_unique_key(
            cls,
            shape: typing.Shape,
            orientation: typing.Orientation,
            row: typing.Dimension,
            col: typing.Dimension
    ) -> typing.Key:
        """
        Provided an orientation, a shape, a row, and a column, return the
        unique key for all pentagons defined by these attributes.

        Arguments:
            shape (typing.Shape):
            orientation (typing.Orientation):
            row (typing.Dimension):
            col(typing.Dimension)

        Returns:
            A Key tuple of (shape, orientation, row, col)
        """
        if orientation in [
            constants.Orientation.UP, constants.Orientation.DOWN
        ]:
            dimensions: Tuple[typing.Dimension, typing.Dimension] = (
                row,
                (col + cls._dim_map[shape][orientation][0],
                 col + cls._dim_map[shape][orientation][1]))
        else:
            dimensions: Tuple[typing.Dimension, typing.Dimension] = (
                (row + cls._dim_map[shape][orientation][0],
                 row + cls._dim_map[shape][orientation][1]),
                col
            )
        return orientation, dimensions[0], dimensions[1]

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
