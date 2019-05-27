from typing import List, Optional

from cairo_pentagon import layer, pattern
from cairo_pentagon.utils import constants, typing


class Piece:

    # A Piece is comprised of three layers of pentagon patterns.

    _num_layers: int = 3
    _seed: int = 324

    def __init__(
            self,
            width: typing.Width = 12,
            height: typing.Height = 15
    ):
        self.width = width
        self.height = height

        # Three individual Layer objects: A, B, & C.
        self._layers: Optional[List[layer.Layer]] = None

        # Three individual Pattern objects: A, B, & C.
        self._patterns: Optional[List[pattern.Pattern]] = None

        # The color of the background rectangle.
        self.background_color: Optional[typing.Color] = None

    def _add_layers(self):
        pass

    def _add_patterns(self):
        pass

    def _apply_patterns(self):
        pass

    def construct_piece(
            self,
            shape: typing.Shape = constants.Shape.ALPHA
    ) -> None:
        for i in range(self._num_layers):
            self._layers[i] = layer.Layer(
                init_shape=shape,
                width=self.width,
                height=self.height,

            )
