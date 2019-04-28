from typing import Dict, Optional, Tuple, Union


Color = Tuple[int, int, int]

Column = Optional[Union[int, Tuple[int, int]]]

Coordinates = Tuple[int, int]

CompoundDimension = Union[Tuple[int, int], int]

DimensionMap = Dict[Tuple[str, str], Dict[str, Tuple[int, int]]]

Height = int

Key = Tuple[str, Union[int, Tuple[int, int]], Union[Tuple[int, int], int]]

Opacity = float

Orientation = str

Origin = Coordinates

PatternStyle = str

Row = Optional[Union[int, Tuple[int, int]]]

Shape = str

Spin = str

Width = int

Visibility = bool

Dimension = Union[Column, Row, CompoundDimension]
