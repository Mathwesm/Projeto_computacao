"""
Módulo Core - Componentes centrais do jogo
Contém configurações, constantes e exceções personalizadas
"""

try:
    from .config import *
    from .constants import *
    from .exceptions import *
    from .logger import get_logger, setup_logger
except ImportError:
    from config import *
    from constants import *
    from exceptions import *
    from logger import get_logger, setup_logger

__all__ = [
    # Config
    'WINDOW_WIDTH', 'WINDOW_HEIGHT', 'FPS', 'TITLE',
    'BLACK', 'WHITE', 'RED', 'GREEN', 'BLUE', 'YELLOW',
    'BG_COLOR', 'UI_BG_COLOR', 'TEXT_COLOR',
    'SHADING_MODELS', 'TRANSFORMATIONS',

    # Constants
    'VERSION', 'AUTHOR', 'DESCRIPTION',
    'EPSILON', 'PI', 'TWO_PI',

    # Exceptions
    'GameException', 'RenderException', 'TransformationException',

    # Logger
    'get_logger', 'setup_logger'
]
