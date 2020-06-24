"""
Contains an object to return random items for generating a work of art.
"""
import random
from typing import Any, Optional

from cairo_pentagon.utils import constants


_SEED = 324


class Randomizer:

    _attribute_map = {
        "spin": constants.Spin.SPINS,
        "shape": constants.Shape.SHAPES,
        "space": constants.Space.SPACES,
    }
    _colors = [constants.Colors.RED, constants.Colors.GREEN, constants.Colors.BLUE]

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed if seed else _SEED
        random.seed(self.seed)
        random.shuffle(self._colors)

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, value: int) -> None:
        self._seed = value

    def get_random_attribute(self, attribute: str) -> Any:
        return random.choice(self._attribute_map[attribute])

    def get_color(self):
        if not self._colors:
            raise RuntimeError("All colors have been exhausted.")
        return self._colors.pop()

    @staticmethod
    def get_origin(height: int, width: int):
        row = random.randint(0, height)
        column = random.randint(0, width)
        return row, column
