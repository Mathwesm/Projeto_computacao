"""
Testes de integração para transformações geométricas
"""

import pytest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from transformations import Matrix4x4, GeometricTransformations


class TestTransformationsIntegration:
    """Testes de integração para sistema de transformações"""

    def test_combined_transformations(self):
        """Testa combinação de múltiplas transformações"""
        transform = GeometricTransformations()

        # Aplica transformações
        transform.translate(1, 2, 3)
        transform.rotate_y(45)
        transform.scale_uniform(2)

        # Verifica que a matriz foi modificada
        identity = Matrix4x4.identity()
        assert not np.array_equal(transform.matrix.data, identity.data)

    def test_transformation_order_matters(self):
        """Verifica que a ordem das transformações importa"""
        # Primeira ordem: translate -> rotate
        transform1 = GeometricTransformations()
        transform1.translate(5, 0, 0)
        transform1.rotate_y(90)

        # Segunda ordem: rotate -> translate
        transform2 = GeometricTransformations()
        transform2.rotate_y(90)
        transform2.translate(5, 0, 0)

        # As matrizes devem ser diferentes
        assert not np.array_equal(transform1.matrix.data, transform2.matrix.data)

    def test_reset_transformation(self):
        """Testa reset das transformações"""
        transform = GeometricTransformations()

        # Aplica transformações
        transform.translate(1, 2, 3)
        transform.rotate_x(45)
        transform.scale(2, 2, 2)

        # Reset
        transform.reset()

        # Deve voltar à identidade
        identity = Matrix4x4.identity()
        assert np.array_equal(transform.matrix.data, identity.data)
