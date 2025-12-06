"""
Configurações do jogo MathShape Quest
"""

# Configurações da janela
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "MathShape Quest - Aventura das Formas Geométricas"

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Cores do tema
BG_COLOR = (60, 70, 100)  # Fundo mais claro
UI_BG_COLOR = (70, 80, 120)
UI_BORDER_COLOR = (120, 140, 220)
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = YELLOW
SUCCESS_COLOR = GREEN
ERROR_COLOR = RED
WARNING_COLOR = YELLOW

# Configurações de renderização 3D
NEAR_PLANE = 0.1
FAR_PLANE = 1000.0
FOV = 90  # Field of view em graus
ENABLE_BACKFACE_CULLING = False  # Se False, mostra bases dos objetos

# Configurações de iluminação
AMBIENT_LIGHT = 0.2
LIGHT_POSITION = [0, 10, -10]
LIGHT_COLOR = [1.0, 1.0, 1.0]
LIGHT_INTENSITY = 1.0

# Configurações de câmera
CAMERA_DISTANCE = 5
CAMERA_HEIGHT = 2
CAMERA_ROTATION_SPEED = 0.02
CAMERA_ZOOM_SPEED = 0.1

# Configurações de gameplay
MAX_LIVES = 3
POINTS_PER_CORRECT = 100
POINTS_PER_LEVEL = 500
TIME_LIMIT = 300  # segundos

# Modelos de iluminação disponíveis
SHADING_MODELS = {
    'PHONG': 'Phong',
    'LAMBERTIAN': 'Lambertiano',
    'GOURAUD': 'Gouraud'
}

# Transformações disponíveis
TRANSFORMATIONS = {
    'TRANSLATE': 'Translação',
    'ROTATE': 'Rotação',
    'SCALE': 'Escala',
    'REFLECT': 'Reflexão',
    'SHEAR': 'Distorção'
}
