from typing import Callable, Dict, Iterable, Optional, Tuple, Union


Color = Tuple[int, int, int]

Column = Optional[Union[int, Tuple[int, int]]]

CoordinateMap = Dict[str, Dict[str, Callable[[Iterable[int]], int]]]

Coordinates = Tuple[int, int]

CompoundDimension = Union[Tuple[int, int], int]

DimensionMap = Dict[str, Dict[str, Coordinates]]

Height = int

Key = Tuple[str, Union[int, Tuple[int, int]], Union[Tuple[int, int], int]]

Opacity = float

Orientation = str

Origin = Coordinates

Pattern = str

Row = Optional[Union[int, Tuple[int, int]]]

Shape = str

Spin = str

Width = int

Visibility = bool

Dimension = Union[Column, Row, CompoundDimension]
