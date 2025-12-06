"""
Módulo Utils - Utilitários e helpers
Funções auxiliares reutilizáveis em todo o projeto
"""

try:
    from .math_utils import *
    from .color_utils import *
    from .time_utils import *
    from .validators import *
except ImportError:
    from math_utils import *
    from color_utils import *
    from time_utils import *
    from validators import *

__all__ = [
    # Math utils
    'clamp', 'lerp', 'map_range', 'normalize_vector',
    'distance_3d', 'angle_between_vectors',

    # Color utils
    'rgb_to_hex', 'hex_to_rgb', 'interpolate_color',
    'darken_color', 'lighten_color',

    # Time utils
    'format_time', 'get_timestamp', 'Timer',

    # Validators
    'validate_color', 'validate_vector3', 'validate_matrix',
]
