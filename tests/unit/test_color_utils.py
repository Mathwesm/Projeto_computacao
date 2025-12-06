"""
Testes para utilitários de cores
"""

import pytest
from src.utils.color_utils import (
    rgb_to_hex, hex_to_rgb, interpolate_color,
    darken_color, lighten_color, normalize_color
)


class TestColorUtils:
    """Testes para funções de manipulação de cores"""

    def test_rgb_to_hex(self):
        """Testa conversão RGB para hexadecimal"""
        assert rgb_to_hex((255, 0, 0)) == '#ff0000'
        assert rgb_to_hex((0, 255, 0)) == '#00ff00'
        assert rgb_to_hex((0, 0, 255)) == '#0000ff'
        assert rgb_to_hex((255, 255, 255)) == '#ffffff'

    def test_hex_to_rgb(self):
        """Testa conversão hexadecimal para RGB"""
        assert hex_to_rgb('#ff0000') == (255, 0, 0)
        assert hex_to_rgb('#00ff00') == (0, 255, 0)
        assert hex_to_rgb('#0000ff') == (0, 0, 255)
        assert hex_to_rgb('ffffff') == (255, 255, 255)

    def test_interpolate_color(self):
        """Testa interpolação de cores"""
        black = (0, 0, 0)
        white = (255, 255, 255)

        result = interpolate_color(black, white, 0.0)
        assert result == black

        result = interpolate_color(black, white, 1.0)
        assert result == white

        result = interpolate_color(black, white, 0.5)
        assert result == (127, 127, 127)

    def test_darken_color(self):
        """Testa escurecimento de cores"""
        color = (100, 100, 100)
        darker = darken_color(color, 0.5)
        assert all(d < c for d, c in zip(darker, color))

    def test_lighten_color(self):
        """Testa clareamento de cores"""
        color = (100, 100, 100)
        lighter = lighten_color(color, 1.5)
        assert all(l > c for l, c in zip(lighter, color))

    def test_normalize_color(self):
        """Testa normalização de cores"""
        color_int = (255, 128, 0)
        color_float = normalize_color(color_int, 'float')
        assert all(0 <= c <= 1 for c in color_float)

        color_back = normalize_color(color_float, 'int')
        assert color_back == color_int
