"""
Constantes do projeto
Valores constantes usados em todo o projeto
"""

import math

# Informações do projeto
VERSION = "1.0.0"
AUTHOR = "Equipe MathShape Quest"
DESCRIPTION = "Jogo Educativo de Computação Gráfica"
GITHUB_URL = "https://github.com/seu-usuario/Projeto_computacao_grafica"

# Constantes matemáticas
EPSILON = 1e-6  # Pequeno valor para comparações de ponto flutuante
PI = math.pi
TWO_PI = 2 * math.pi
HALF_PI = math.pi / 2
DEG_TO_RAD = math.pi / 180
RAD_TO_DEG = 180 / math.pi

# Constantes de renderização
DEFAULT_VERTEX_SIZE = 4
DEFAULT_EDGE_WIDTH = 2
DEFAULT_FACE_ALPHA = 180

# Constantes de física/movimento
GRAVITY = 9.8
DEFAULT_FRICTION = 0.95
MIN_VELOCITY = 0.01

# Constantes de UI
DEFAULT_FONT_SIZE = 24
TITLE_FONT_SIZE = 48
SUBTITLE_FONT_SIZE = 32
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 200
BUTTON_PADDING = 10
UI_ANIMATION_SPEED = 0.15

# Constantes de gameplay
MIN_SCORE = 0
MAX_SCORE = 999999
COMBO_MULTIPLIER = 1.5
PERFECT_BONUS = 200
TIME_BONUS_MULTIPLIER = 10

# Limites de transformação
MAX_SCALE = 10.0
MIN_SCALE = 0.1
MAX_ROTATION_SPEED = 5.0
MAX_TRANSLATION_DISTANCE = 100.0

# Debug
DEBUG_MODE = False
SHOW_FPS = True
SHOW_WIREFRAME = False
SHOW_NORMALS = False
