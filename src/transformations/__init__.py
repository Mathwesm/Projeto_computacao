"""
Módulo de transformações geométricas
Implementa todas as transformações 3D necessárias usando matrizes homogêneas
"""

from .matrix import Matrix4x4
from .geometric import GeometricTransformations

__all__ = ['Matrix4x4', 'GeometricTransformations']
