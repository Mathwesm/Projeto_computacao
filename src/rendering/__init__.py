"""
Módulo de renderização 3D
Implementa modelos de iluminação e renderização
"""

from .lighting import PhongShading, LambertianShading, GouraudShading, Light, create_shading_model
from .camera import Camera
from .renderer import Renderer

__all__ = ['PhongShading', 'LambertianShading', 'GouraudShading', 'Light', 'Camera', 'Renderer', 'create_shading_model']
