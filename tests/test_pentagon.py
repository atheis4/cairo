import pytest

from cairo_pentagon.pentagon import (
    Pentagon, UpPentagon, DownPentagon, LeftPentagon, RightPentagon
)
from cairo_pentagon.utils import constants


@pytest.mark.parametrize('orientation,subclass',
                         [('up', UpPentagon),
                          ('down', DownPentagon),
                          ('left', LeftPentagon),
                          ('right', RightPentagon)])
def test_formula_constructor(orientation, subclass):
    instance = Pentagon.get_subclass_from_orientation(orientation)
    assert instance == subclass


@pytest.mark.parametrize(
    'orientation,subclass', [
        (constants.Orientation.DOWN, DownPentagon),
        (constants.Orientation.LEFT, LeftPentagon),
        (constants.Orientation.UP, UpPentagon),
        (constants.Orientation.RIGHT, RightPentagon)
    ]
)
def test_constructors(orientation, subclass):
    pentagon = subclass(
        shape=constants.Shape.ALPHA, row=1, column=1
    )
    assert pentagon._orientation == orientation
    assert pentagon._row == 1
    assert pentagon._column == 1


def test_row_property():
    pass


def test_row_setter():
    pass


def test_column_property():
    pass


def test_column_setter():
    pass


def test_visibility_property():
    pass


def test_visibility_setter():
    pass


def test_is_visible():
    pass


def test_define_unique_key():
    pass


