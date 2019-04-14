from typing import Any, Dict, Optional, Tuple, Union

from cairo.pentagon import Pentagon


Column = Optional[int, Tuple[int, int]]
CompoundDimension = Union[int, Tuple[int, int]]
DimensionMap = Dict[Tuple[str, str], Dict[str, Tuple[int, int]]]
Key = Tuple[str, Union[int, Tuple[int, int]], Union[Tuple[int, int], int]]
PentagonMap = Optional[Dict[Key, Pentagon]]
Row = Optional[int, Tuple[int, int]]
