import pytest

from cairo_pentagon.layer import Layer
from cairo_pentagon.utils import constants


def test_default_constructor():
    layer = Layer(init_shape='alpha')
    assert layer.width == 4
    assert layer.height == 4
    assert not layer.pentagon_map
    assert layer.color == constants.Colors.RED
    assert layer.opacity == 0.25


def test_constructor():
    layer = Layer(init_shape='beta', width=8, height=12, color=(0, 255, 0))
    assert layer.width == 8
    assert layer.height == 12
    assert not layer.pentagon_map
    assert layer.color == constants.Colors.GREEN
    assert layer.opacity == 0.25


@pytest.mark.parametrize('shape', ['alpha', 'beta'])
def test_shape_property(shape):
    layer = Layer(init_shape=shape, width=4, height=6)
    assert layer.shape == shape


def test_construct_layer():
    # A layer of width = 1 and height = 1 should be a single cell comprised of
    # four pentagons.
    layer = Layer(init_shape='alpha', width=1, height=1)
    layer.construct_layer()
    assert len(layer.pentagon_map) == 4
    # The following keys should all exist in the pentagon map.
    keys = [
        (constants.Orientation.DOWN, 0, (-1, 0)),
        (constants.Orientation.LEFT, (-1, 0), 0),
        (constants.Orientation.UP, 0, (0, 1)),
        (constants.Orientation.RIGHT, (0, 1), 0)
    ]
    assert all(key in layer.pentagon_map for key in keys)
