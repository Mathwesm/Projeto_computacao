"""
Testes para utilitários matemáticos
"""

import pytest
import numpy as np
from src.utils.math_utils import (
    clamp, lerp, map_range, normalize_vector,
    distance_3d, angle_between_vectors
)


class TestMathUtils:
    """Testes para funções matemáticas utilitárias"""

    def test_clamp(self):
        """Testa função clamp"""
        assert clamp(5, 0, 10) == 5
        assert clamp(-5, 0, 10) == 0
        assert clamp(15, 0, 10) == 10
        assert clamp(5.5, 0, 10) == 5.5

    def test_lerp(self):
        """Testa interpolação linear"""
        assert lerp(0, 10, 0.0) == 0
        assert lerp(0, 10, 1.0) == 10
        assert lerp(0, 10, 0.5) == 5
        assert abs(lerp(0, 100, 0.25) - 25) < 0.001

    def test_map_range(self):
        """Testa mapeamento de intervalos"""
        assert map_range(5, 0, 10, 0, 100) == 50
        assert map_range(0, 0, 10, 0, 100) == 0
        assert map_range(10, 0, 10, 0, 100) == 100

    def test_normalize_vector(self):
        """Testa normalização de vetores"""
        v = normalize_vector([3, 4, 0])
        assert abs(np.linalg.norm(v) - 1.0) < 1e-6
        assert abs(v[0] - 0.6) < 1e-6
        assert abs(v[1] - 0.8) < 1e-6

    def test_distance_3d(self):
        """Testa cálculo de distância 3D"""
        p1 = [0, 0, 0]
        p2 = [3, 4, 0]
        assert distance_3d(p1, p2) == 5.0

        p1 = [1, 2, 3]
        p2 = [1, 2, 3]
        assert distance_3d(p1, p2) == 0.0

    def test_angle_between_vectors(self):
        """Testa cálculo de ângulo entre vetores"""
        v1 = [1, 0, 0]
        v2 = [0, 1, 0]
        angle = angle_between_vectors(v1, v2)
        assert abs(angle - np.pi/2) < 1e-6

        v1 = [1, 0, 0]
        v2 = [1, 0, 0]
        angle = angle_between_vectors(v1, v2)
        assert abs(angle) < 1e-6
