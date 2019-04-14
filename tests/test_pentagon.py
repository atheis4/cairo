import pytest
import random

from cairo_pentagon.pentagon import (
    Pentagon, UpPentagon, DownPentagon, LeftPentagon, RightPentagon
)


@pytest.mark.parametrize('orientation_to_class',
                         [('up', UpPentagon),
                          ('down', DownPentagon),
                          ('left', LeftPentagon),
                          ('right', RightPentagon)])
def test_formula_constructor(orientation_to_class):
    shape = orientation_to_class[0]
    subclass = orientation_to_class[1]

    instance = Pentagon.get_subclass_from_orientation(shape)
    assert instance == subclass


# There are three attributes that determine a correct answer for the private
# method being tested: the orientation, the shape, and the 'fixed' dimension.
@pytest.mark.parametrize('dynamic_dim', range(random.randint(0, 10)))
def test_compound_dimension_assignment_alpha(dynamic_dim):
    # test all alpha shapes
    results = ((dynamic_dim, dynamic_dim + 1), (dynamic_dim - 1, dynamic_dim))
    shape = 'alpha'
    # Test up pentagon dynamic column
    up = UpPentagon(shape=shape, row=0, col=dynamic_dim)
    assert up.col == results[0]

    # Test down pentagon dynamic column
    down = DownPentagon(shape=shape, row=0, col=dynamic_dim)
    assert down.col == results[1]

    # Test left pentagon dynamic column
    left = LeftPentagon(shape=shape, row=dynamic_dim, col=0)
    assert left.row == results[1]

    # Test right pentagon dynamic column
    right = RightPentagon(shape=shape, row=dynamic_dim, col=0)
    assert right.row == results[0]


@pytest.mark.parametrize('dynamic_dim', range(random.randint(0, 10)))
def test_compound_dimension_assignment_beta(dynamic_dim):
    # test all beta shapes
    shape = 'beta'
    results = ((dynamic_dim - 1, dynamic_dim), (dynamic_dim, dynamic_dim + 1))

    # Test up pentagon dynamic column
    up = UpPentagon(shape=shape, row=0, col=dynamic_dim)
    assert up.col == results[0]

    # Test down pentagon dynamic column
    down = DownPentagon(shape=shape, row=0, col=dynamic_dim)
    assert down.col == results[1]

    # Test left pentagon dynamic column
    left = LeftPentagon(shape=shape, row=dynamic_dim, col=0)
    assert left.row == results[1]

    # Test right pentagon dynamic column
    right = RightPentagon(shape=shape, row=dynamic_dim, col=0)
    assert right.row == results[0]


@pytest.mark.parametrize('shape', ['alpha', 'beta'])
@pytest.mark.parametrize('orientation', ['down', 'left', 'up', 'right'])
@pytest.mark.parametrize('row', range(random.randint(0, 10)))
@pytest.mark.parametrize('col', range(random.randint(0, 10)))
def test_get_unique_key(shape, orientation, row, col):
    # Use the classmethod to get the unique key.
    unique_key = Pentagon.define_unique_key(orientation=orientation,
                                            shape=shape,
                                            row=row,
                                            col=col)
    # Create the pentagon that corresponds to the unique key
    pentagon = Pentagon.get_subclass_from_orientation(orientation)(shape=shape,
                                                                   row=row,
                                                                   col=col)
    # Ensure they are equal
    assert pentagon.get_unique_key() == unique_key
