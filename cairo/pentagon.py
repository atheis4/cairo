
class Pentagon(object):
    """
    Pentagons represent the object that will be rendered in the final piece.

    Pentagons have several attributes that uniquely define its position, shape,
    and visibility.

    Attributes:

    Orientation
    -----------
    Pentagons are isosceles: the angle on one of the points is greater than all
    others. The direction that this greatest point faces defines the pentagon's
    orientation. The four different orientations of pentagons: up, down, left,
    and right.

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
    orientation = None

    # The entire pattern exists within a zero-indexed, row and column grid. The
    # top-left is considered the origin.

    # Each pentagon spans more than one row or column. Up and Down pentagons
    # always span two columns, while Left and Right pentagons always span two
    # rows. Whether the pentagon spans move toward or away from the origin is
    # a result of which shape they inhibit, 'alpha' or 'beta'. We will call the
    #
    _dim_map = {
        ('left', 'down'): {'alpha': (-1, 0), 'beta': (0, 1)},
        ('right', 'up'): {'alpha': (0, 1), 'beta': (-1, 0)}
    }

    # Pentagons are uniquely identified by four attributes: their shape,
    # orientation, row, and column. Each of these are hashable values and will
    # be used to tell our program whether the requested pentagon has already
    # been created, or if we need to make it. This allows us to reference the
    # same pentagon object across a single frame layer.

    def __init__(self, shape: str=None):
        # A pentagon always exists relative to a 2-d array of rows and columns.
        # One pentagon may exist in multiple rows and columns at the same time,
        # so long as they follow strict rules about position. Certain types of
        # pentagon--based on orientation--may only exist in the same row or the
        # same column.

        # Up/Down pentagons can only exist in one row, but over two columns.
        # Left/Right pentagons can only exist in one column, but over two rows.
        self.shape = shape

        self._visible = False

    def __repr__(self):
        return (f'<{self.orientation} - row: {self.row}, col: {self.col}, '
                f'shape: {self.shape}>')

    def _create_compound_dimension(self, dimension: int):
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

    @property
    def visible(self):
        return self._visible

    def is_visible(self):
        return self.visible

    def get_unique_key(self):
        """Return the unique key of this pentagon."""
        return self.orientation, self.row, self.col

    @classmethod
    def define_unique_key(cls,
                          orientation: str,
                          shape: str,
                          row: int,
                          col: int):
        """
        Provided an orientation, a shape, a row, and a column, return the
        unique key for all pentagons defined by these attributes.

        Arguments:
            orientation (str):
            shape (str):
            row (int):
            col(int)

        Returns:
            A tuple of (orientation, row, col)
        """
        for orientations in cls._dim_map.keys():
            if orientation in orientations:
                if orientation in ['up', 'down']:
                    dimensions = (
                        row,
                        (col + cls._dim_map[orientations][shape][0],
                         col + cls._dim_map[orientations][shape][1]))
                else:
                    dimensions = (
                        (row + cls._dim_map[orientations][shape][0],
                         row + cls._dim_map[orientations][shape][1]),
                        col
                    )
                return (orientation, *dimensions)

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

    orientation = 'up'

    def __init__(self, shape: str, row: int, col: int):
        super(UpPentagon, self).__init__(shape=shape)
        self.row = row
        self.col = self._create_compound_dimension(dimension=col)


class DownPentagon(Pentagon):

    orientation = 'down'

    def __init__(self, shape: str, row: int, col: int):
        super(DownPentagon, self).__init__(shape=shape)
        self.row = row
        self.col = self._create_compound_dimension(dimension=col)


class LeftPentagon(Pentagon):

    orientation = 'left'

    def __init__(self, shape: str, row: int, col: int):
        super(LeftPentagon, self).__init__(shape=shape)
        self.row = self._create_compound_dimension(dimension=row)
        self.col = col


class RightPentagon(Pentagon):

    orientation = 'right'

    def __init__(self, shape: str, row: int, col: int):
        super(RightPentagon, self).__init__(shape)
        self.row = self._create_compound_dimension(dimension=row)
        self.col = col
