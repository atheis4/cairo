from typing import List

from cairo.pentagon import Pentagon


class Layer(object):
    """
    Container for one layer of Pentagon objects.

    A layer is series of nested nd.arrays representing rows filled with
    columns, or cells, of Pentagon objects.

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
    _shape_to_pentagons = {
        'alpha': ('down', 'left', 'up', 'right'),
        'beta': ('right', 'down', 'left', 'up')
    }
    # Simple switch to control the 'mirror' effect of the pattern
    _shape_switch = {'alpha': 'beta', 'beta': 'alpha'}

    def __init__(self, init_shape: str='alpha', width: int=4, height: int=4):
        self._init_shape = init_shape
        self.width = width
        self.height = height

        self.layer = None
        self._pentagon_map = None

        # One of 'red' (255, 0, 0), 'green' (0, 255, 0), or 'blue' (0, 0, 255).
        self.color = None

        self.opacity = 0.25

    @property
    def shape(self):
        return self._init_shape

    def construct_layer(self):
        # Check to see if we already have a layer on this object, raise if so.
        if self.layer is not None:
            raise RuntimeError(
                "layer already exists, cannot construct a new one."
            )
        self._pentagon_map = {}

        self.layer = []

        curr_shape = self.shape
        curr_height, curr_width = 0, 0

        while curr_height < self.height:
            # Create the row
            new_row = []

            # while curr_width < self.width:
            #     # Add a single cell to the new row
            #     new_row.append(self._construct_cell(shape=shape,
            #                                         row=curr_height,
            #                                         col=curr_width))
            #     # add one to current width and flip the shape when finished
            #     # constructing a cell. If we have finished constructing an
            #     # entire row, i.e. if curr_width == self.width, then we don't
            #     # flip the shape. Just as cells alternate shape within a row,
            #     # they must also alternate within each column. For this reason
            #     # we keep the same shape when beginning to make a new row.
            #     curr_width += 1
            #
            #     if curr_width != self.width:
            #         shape = self._shape_switch[shape]

            # Add all of the cells with shapes equal to init_shape first.
            self._add_to_row(new_row, curr_shape, curr_height, curr_width, 2)
            # Then go through and add all of the remaining cells.
            # self._add_to_row(new_row, curr_shape, curr_height, curr_width, 1)

            self.layer.append(new_row)
            # reset curr_width to 0 and add one to curr_height when finished
            # constructing a row.
            curr_width = 0
            curr_height += 1

    def _add_to_row(self, row, shape, height, width, increment=2):
        """
        Modifies the row provided, adding each cell of pentagons either
        alternating shape cells or creating each one in order.

        If increment is 2, all cells for the provided shape will be created
        first. If increment is 1, then it will alternate shapes while creating
        cells for the row.
        """
        while width < self.width:
            row.append(
                self._construct_cell(shape=shape, row=height, col=width)
            )
            if increment == 1:
                shape = self._shape_switch[shape]
            width += increment

    def _construct_cell(self, shape: str, row: int, col: int):
        """Create a new cell to add to our row."""
        cell = []
        for orientation in self._shape_to_pentagons[shape]:
            # Check to see if the pentagon has already been made. If it is
            # already made, we must reference the existing object and add it a
            # second time to the layer list, while excluding it from the
            # pentagon map.
            key = Pentagon.define_unique_key(orientation=orientation,
                                             shape=shape, row=row, col=col)
            pentagon = self._pentagon_map.get(key)
            if not pentagon:
                # Get the class constructor for the pentagon we need to build.
                factory = Pentagon.get_subclass_from_orientation(orientation)
                # Build the pentagon.
                pentagon = factory(shape=shape, row=row, col=col)
                # Add to our dict of unique key to pentagon.
                unique_key = (pentagon.orientation, pentagon.row, pentagon.col)
                self._pentagon_map.update({unique_key: pentagon})
            # TODO: I'm not sure we need the list representation of layers if
            # TODO: we have the pentagon_map... We could use map.keys() to
            # TODO: intuit all of the coordinates we need to render a layer.
            cell.append(pentagon)
        return cell

    def flat_pentagons(self):
        return [
            pentagon for row in self.layer for col in row for pentagon in col
        ]

    def apply_pattern(self, pattern=None, origin=None, color=None):
        # Create a pattern to apply to the layer
        pass


layer = Layer(init_shape='alpha')
layer.construct_layer()