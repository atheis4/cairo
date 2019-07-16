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
    TODO: complete comment


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

    _orientation: Optional[typing.Orientation] = None

    def __init__(
            self,
            shape: typing.Shape = constants.Shape.ALPHA,
            row: typing.Row = None,
            column: typing.Column = None
    ):
        self.shape: typing.Shape = shape

        self.visibility: typing.Visibility = False
        self.row: Optional[typing.Row] = row
        self.column: Optional[typing.Column] = column

    def __repr__(self) -> str:
        return (
            f'<{self.orientation} - row: {self.row}, col: {self.column}, '
            f'shape: {self.shape}>'
        )

    @property
    def orientation(self):
        return self._orientation

    @property
    def row(self) -> Union[typing.Row, typing.CompoundDimension]:
        return self._row

    @row.setter
    def row(self, value) -> None:
        self._row = value

    @property
    def column(self) -> Union[typing.Column, typing.CompoundDimension]:
        return self._column

    @column.setter
    def column(self, value) -> None:
        self._column = value

    @property
    def visibility(self) -> typing.Visibility:
        return self._visibility

    @visibility.setter
    def visibility(self, value) -> None:
        self._visibility = value

    def is_visible(self) -> typing.Visibility:
        return self.visibility

    @classmethod
    def define_unique_key(
            cls,
            shape: typing.Shape,
            orientation: typing.Orientation,
            row: typing.Dimension,
            column: typing.Dimension
    ) -> typing.Key:
        """
        Provided an orientation, a shape, a row, and a column, return the
        unique key for all pentagons defined by these attributes.

        Arguments:
            shape (typing.Shape):
            orientation (typing.Orientation):
            row (typing.Dimension):
            column(typing.Dimension)

        Returns:
            A Key tuple of (shape, orientation, row, col)
        """
        if orientation in constants.Orientation.VERTICAL:
            dimensions: Tuple[typing.Dimension, typing.Dimension] = (
                row,
                (column + cls._dim_map[shape][orientation][0],
                 column + cls._dim_map[shape][orientation][1])
            )
        else:
            dimensions: Tuple[typing.Dimension, typing.Dimension] = (
                (row + cls._dim_map[shape][orientation][0],
                 row + cls._dim_map[shape][orientation][1]),
                column
            )
        return orientation, dimensions[0], dimensions[1]

    @classmethod
    def get_subclass_from_orientation(cls, orientation: typing.Orientation):
        """
        Return the subclass constructor for the provided orientation.

        Arguments:
            orientation (typing.Orientation):

        Returns:
            Pentagon subclass constructor.
        """
        for pentagon in cls.__subclasses__():
            if getattr(pentagon, 'orientation') == orientation:
                return pentagon


class UpPentagon(Pentagon):
    _orientation: typing.Orientation = constants.Orientation.UP


class DownPentagon(Pentagon):
    _orientation: typing.Orientation = constants.Orientation.DOWN


class LeftPentagon(Pentagon):
    _orientation: typing.Orientation = constants.Orientation.LEFT


class RightPentagon(Pentagon):
    _orientation: typing.Orientation = constants.Orientation.RIGHT
