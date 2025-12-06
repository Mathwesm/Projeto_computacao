"""
Script de teste para verificar todos os módulos do projeto
"""

import sys
import os

# Configura encoding para UTF-8 no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("TESTE DE MODULOS - MathShape Quest")
print("=" * 60)
print()

# Teste 1: Transformações
print("1. Testando transformações geométricas...")
try:
    from transformations import Matrix4x4, GeometricTransformations

    # Cria uma matriz de translação
    mat = Matrix4x4.translation(1, 2, 3)
    print("   ✓ Matrix4x4 OK")

    # Testa transformação
    transform = GeometricTransformations()
    transform.translate(1, 0, 0)
    transform.rotate_y(45)
    transform.scale_uniform(2)
    print("   ✓ GeometricTransformations OK")
    print("   ✓ Transformações: PASSOU")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print()

# Teste 2: Renderização
print("2. Testando renderização e iluminação...")
try:
    import traceback
    from rendering import Light, PhongShading, LambertianShading, GouraudShading
    from rendering import Camera, Renderer

    # Cria luz
    light = Light([0, 10, 0])
    print("   ✓ Light OK")

    # Cria modelos de iluminação
    phong = PhongShading()
    lambert = LambertianShading()
    gouraud = GouraudShading()
    print("   ✓ Modelos de iluminação OK")

    # Testa câmera
    camera = Camera([5, 2, 5], [0, 0, 0])
    camera.orbit(0.1, 0.1)
    print("   ✓ Camera OK")

    # Testa renderer
    renderer = Renderer(800, 600)
    print("   ✓ Renderer OK")

    print("   ✓ Renderização: PASSOU")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    traceback.print_exc()
    sys.exit(1)

print()

# Teste 3: Objetos 3D
print("3. Testando objetos 3D...")
try:
    from objects import Cube, Sphere, Pyramid, Cylinder, Torus

    # Cria objetos
    cube = Cube()
    sphere = Sphere()
    pyramid = Pyramid()
    cylinder = Cylinder()
    torus = Torus()

    print(f"   ✓ Cubo: {len(cube.vertices)} vértices")
    print(f"   ✓ Esfera: {len(sphere.vertices)} vértices")
    print(f"   ✓ Pirâmide: {len(pyramid.vertices)} vértices")
    print(f"   ✓ Cilindro: {len(cylinder.vertices)} vértices")
    print(f"   ✓ Torus: {len(torus.vertices)} vértices")

    # Testa transformações no cubo
    cube.translate(1, 0, 0)
    cube.rotate_y(45)
    cube.scale_uniform(1.5)

    print("   ✓ Objetos 3D: PASSOU")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print()

# Teste 4: Lógica do jogo
print("4. Testando lógica do jogo...")
try:
    from game_logic import Player, Puzzle, PuzzleType, Level, LevelManager

    # Testa player
    player = Player()
    player.add_score(100)
    print(f"   ✓ Player OK (Score: {player.score})")

    # Testa puzzle
    puzzle = Puzzle(PuzzleType.TRANSFORMATION, difficulty=1)
    print(f"   ✓ Puzzle OK (Tipo: {puzzle.type.value})")

    # Testa level manager
    level_manager = LevelManager()
    print(f"   ✓ LevelManager OK ({level_manager.get_total_levels()} níveis)")

    current_level = level_manager.get_current_level()
    print(f"   ✓ Nível atual: {current_level.name}")

    print("   ✓ Lógica do jogo: PASSOU")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print()

# Teste 5: Interface
print("5. Testando interface...")
try:
    from ui import Button, Menu, MenuState, HUD

    # Testa componentes (sem pygame.init())
    print("   ✓ Button importado OK")
    print("   ✓ Menu importado OK")
    print("   ✓ HUD importado OK")

    print("   ✓ Interface: PASSOU")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print()

# Teste 6: Config
print("6. Testando configurações...")
try:
    from core.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
    from core.config import TRANSFORMATIONS, SHADING_MODELS
    from core.constants import VERSION, AUTHOR

    print(f"   ✓ Resolução: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    print(f"   ✓ FPS: {FPS}")
    print(f"   ✓ Transformações: {len(TRANSFORMATIONS)}")
    print(f"   ✓ Modelos de iluminação: {len(SHADING_MODELS)}")
    print(f"   ✓ Versão: {VERSION}")

    print("   ✓ Configurações: PASSOU")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("TODOS OS TESTES PASSARAM! ✓")
print("=" * 60)
print()
print("O jogo está pronto para ser executado!")
print("Execute: python src/main.py")
print()
