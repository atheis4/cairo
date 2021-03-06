import random
from typing import List, Optional

from cairo_pentagon import layer, pattern
from cairo_pentagon.utils import constants, randomizer, typing


class Piece:

    # A Piece is comprised of three layers of pentagon patterns.

    _num_layers: int = 3
    _seed: int = 324

    def __init__(self, width: typing.Width = 12, height: typing.Height = 15):
        self.width = width
        self.height = height

        # Three individual Layer objects: A, B, & C.
        self.layers: Optional[List[layer.Layer]] = None

        # Three individual Pattern objects: A, B, & C.
        self.patterns: Optional[List[pattern.Pattern]] = None

        # The color of the background rectangle.
        self.background_color: Optional[typing.Color] = None
        self.randomizer = randomizer.Randomizer(seed=self._seed)

    @property
    def patterns(self) -> Optional[List[pattern.Pattern]]:
        return self._patterns

    @patterns.setter
    def patterns(self, value) -> None:
        self._patterns = value

    @property
    def layers(self) -> Optional[List[layer.Layer]]:
        return self._layers

    @layers.setter
    def layers(self, value) -> None:
        self._layers = value

    def _add_layers(self):
        if self.layers:
            raise RuntimeError("Layers already exist, cannot overwrite.")
        self.layers = []
        for _ in range(3):
            new_layer = layer.Layer(height=self.height, width=self.width)
            new_layer.construct_layer()
            self.layers.append(new_layer)

    def _add_patterns(self):
        if self._patterns:
            raise RuntimeError("Patterns already exist, cannot overwrite.")
        self.patterns = []
        for _ in range(3):
            factory = pattern.SquarePattern.get_subclass_from_spin(
                self.randomizer.get_random_attribute("spin")
            )
            new_pattern = factory(
                origin=self.randomizer.get_origin(height=self.height, width=self.width),
                space=self.randomizer.get_random_attribute("space"),
            )
            self.patterns.append(new_pattern)

    def apply_patterns(self):
        for this_layer, this_pattern in zip(self.layers, self.patterns):
            for pentagon in this_layer.pentagon_map.values():
                pentagon.visibility = this_pattern.apply(pentagon)

    def construct_piece(self, shape: typing.Shape = constants.Shape.ALPHA) -> None:
        pass

    @classmethod
    def manual_build(
        cls,
        height: int,
        width: int,
        layers: List[layer.Layer],
        patterns: List[typing.Pattern],
        background_color: typing.Color,
    ):
        piece = cls(width=width, height=height)
        piece.background_color = background_color
        piece._layers = layers
        piece._patterns = patterns
        piece.apply_patterns()
        return piece
