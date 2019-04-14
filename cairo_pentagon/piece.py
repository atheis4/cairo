from cairo_pentagon.layer import Layer
from cairo_pentagon.pattern import Pattern


class Piece:

    # A Piece is comprised of three layers of pentagon patterns.

    _seed = 324

    def __init__(self, width: int = 12, height: int = 15):
        self.width = width
        self.height = height

        # Three individual Layer objects: A, B, & C.
        self._a_layer = None
        self._b_layer = None
        self._c_layer = None

        # Three individual Pattern objects: A, B, & C.
        # TODO: What does a pattern applied to a layer look like? When does it
        # TODO: occur in the program?
        self._a_pattern = None
        self._b_pattern = None
        self._c_pattern = None

        # The order of the layers
        self.layering = None

        # The color of the background rectangle.
        self.background_color = None

    @property
    def a_layer(self):
        if self._a_layer is None:
            raise RuntimeError(
                "Piece needs to be constructed before layers can be accessed. "
                "Call Piece.construct_piece() first."
            )
        return self._a_layer

    @a_layer.setter
    def a_layer(self, value: Layer):
        self._a_layer = value

    @property
    def a_pattern(self):
        return self._a_pattern

    @a_pattern.setter
    def a_pattern(self, value: Pattern):
        self._a_pattern = value

    @property
    def b_layer(self):
        if self._c_layer is None:
            raise RuntimeError(
                "Piece needs to be constructed before layers can be accessed. "
                "Call Piece.construct_piece() first."
            )
        return self._c_layer

    @b_layer.setter
    def b_layer(self, value: Layer):
        self._b_layer = value

    @property
    def b_pattern(self):
        return self._b_pattern

    @b_pattern.setter
    def b_pattern(self, value: Pattern):
        self._b_pattern = value

    @property
    def c_layer(self):
        if self._c_layer is None:
            raise RuntimeError(
                "Piece needs to be constructed before layers can be accessed. "
                "Call Piece.construct_piece() first."
            )
        return self._c_layer

    @c_layer.setter
    def c_layer(self, value: Layer):
        self._c_layer = value

    @property
    def c_pattern(self):
        return self._c_pattern

    @c_pattern.setter
    def c_pattern(self, value: Pattern):
        self._c_pattern = value

    def construct_piece(self, shape='alpha'):
        for layer_name in ['a_layer', 'b_layer', 'c_layer']:
            new_layer = Layer(shape, self.width, self.height)
            new_layer.construct_layer()
            new_layer.apply(pattern=None, origin=None, color=None)
            setattr(self, layer_name, new_layer)
