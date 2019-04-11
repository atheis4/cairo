import pytest

from cairo.layer import Layer


def test_default_constructor():
    layer = Layer(init_shape='alpha')
    assert layer.width == 4
    assert layer.height == 4
    assert not layer.layer
    assert not layer.color
    assert layer.opacity == 0.25


def test_constructor():
    layer = Layer(init_shape='beta', width=8, height=12)
    assert layer.width == 8
    assert layer.height == 12
    assert not layer.all_pentagons
    assert not layer.color
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
