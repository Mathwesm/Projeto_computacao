"""
Loop principal do jogo MathShape Quest
"""

import pygame
import sys
from enum import Enum

try:
    from .core.config import *
    from .rendering import Camera, Renderer, Light, create_shading_model
    from .game_logic import Player, LevelManager
    from .ui import Menu, MenuState, HUD, Tutorial
except ImportError:
    from core.config import *
    from rendering import Camera, Renderer, Light, create_shading_model
    from game_logic import Player, LevelManager
    from ui import Menu, MenuState, HUD, Tutorial


class GameState(Enum):
    """Estados do jogo"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"  # Tela de Game Over com opções
    TRAINING = "training"  # Modo de treino livre
    TUTORIAL = "tutorial"  # Tela de tutorial/como jogar


class Game:
    """Classe principal do jogo"""

    def __init__(self):
        """Inicializa o jogo"""
        pygame.init()

        # Configuração da janela
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(TITLE)

        # Clock para FPS
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        # Estado do jogo
        self.state = GameState.MENU

        # Componentes do jogo
        self.player = Player()
        self.level_manager = LevelManager()
        self.menu = Menu(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.hud = HUD(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.tutorial = Tutorial(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Renderização 3D
        self.renderer = Renderer(self.window_width, self.window_height)
        self.renderer.set_surface(self.screen)

        # Câmera
        self.camera = Camera(
            position=[CAMERA_DISTANCE, CAMERA_HEIGHT, CAMERA_DISTANCE],
            target=[0, 0, 0],
            fov=FOV,
            aspect=self.window_width / self.window_height
        )

        # Luz
        self.light = Light(
            position=LIGHT_POSITION,
            color=LIGHT_COLOR,
            intensity=LIGHT_INTENSITY
        )

        # Modelo de iluminação atual
        self.shading_models = {
            'phong': create_shading_model('phong'),
            'lambertian': create_shading_model('lambertian'),
            'gouraud': create_shading_model('gouraud')
        }
        self.current_shading = 'phong'

        # Input do mouse
        self.mouse_dragging = False
        self.last_mouse_pos = None

        # Puzzle atual
        self.current_puzzle_index = 0

        # Sistema de tentativas
        self.wrong_attempts = 0
        self.max_wrong_attempts = 4
        self.current_actions = []  # Ações do jogador para o puzzle atual

        # Auto-rotação dos objetos
        self.auto_rotate = True
        self.rotation_speed = 0.5

        # Modo treino
        self.training_shapes = []
        self.current_shape_index = 0
        self.available_shapes = ['cube', 'pyramid', 'sphere', 'cylinder', 'torus']

    def run(self):
        """Loop principal do jogo"""
        while self.running:
            # Delta time
            self.dt = self.clock.tick(FPS) / 1000.0

            # Eventos
            self.handle_events()

            # Update
            self.update()

            # Draw
            self.draw()

            # Atualiza display
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Processa eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Eventos de teclado
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

            # Eventos de mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    # Tutorial - processa cliques nos botões
                    if self.state == GameState.TUTORIAL:
                        action = self.tutorial.handle_click(event.pos)
                        if action == 'back':
                            self.state = GameState.MENU
                            self.menu.state = MenuState.MAIN  # Garante que volte ao menu principal
                    else:
                        self.mouse_dragging = True
                        self.last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
                    self.last_mouse_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_dragging and (self.state == GameState.PLAYING or self.state == GameState.TRAINING):
                    self.handle_camera_drag(event.pos)

            # Scroll do mouse (zoom)
            elif event.type == pygame.MOUSEWHEEL:
                if self.state == GameState.PLAYING or self.state == GameState.TRAINING:
                    self.camera.zoom(-event.y * CAMERA_ZOOM_SPEED)

    def handle_keydown(self, key):
        """Processa teclas pressionadas"""
        # F11 - Toggle fullscreen (funciona em qualquer estado)
        if key == pygame.K_F11:
            self.toggle_fullscreen()
            return

        if self.state == GameState.TRAINING:
            # ESC - Voltar ao menu
            if key == pygame.K_ESCAPE:
                self.state = GameState.MENU

            # Tab ou Setas - Trocar forma
            elif key == pygame.K_TAB or key == pygame.K_RIGHT:
                self.next_shape()
            elif key == pygame.K_LEFT:
                self.previous_shape()

            # Teclas numéricas (6-0) para selecionar forma diretamente
            elif key == pygame.K_6:
                self.set_shape(0)  # Cubo
            elif key == pygame.K_7:
                self.set_shape(1)  # Pirâmide
            elif key == pygame.K_8:
                self.set_shape(2)  # Esfera
            elif key == pygame.K_9:
                self.set_shape(3)  # Cilindro
            elif key == pygame.K_0:
                self.set_shape(4)  # Torus

            # Transformações (mesmas teclas do jogo normal)
            elif key == pygame.K_1:
                self.apply_training_transformation('translate')
            elif key == pygame.K_2:
                self.apply_training_transformation('rotate')
            elif key == pygame.K_3 or key == pygame.K_PLUS or key == pygame.K_EQUALS:
                self.apply_training_transformation('scale_up')
            elif key == pygame.K_MINUS:
                self.apply_training_transformation('scale_down')
            elif key == pygame.K_4:
                self.apply_training_transformation('reflect')
            elif key == pygame.K_5:
                self.apply_training_transformation('shear')

            # Modelos de iluminação
            elif key == pygame.K_q:
                self.change_shading_model('lambertian')
            elif key == pygame.K_w:
                self.change_shading_model('phong')
            elif key == pygame.K_e:
                self.change_shading_model('gouraud')

            # Toggle auto-rotação
            elif key == pygame.K_r:
                self.auto_rotate = not self.auto_rotate

            # Toggle controles
            elif key == pygame.K_c:
                self.hud.toggle_controls()

        elif self.state == GameState.PLAYING:
            # ESC - Pausar
            if key == pygame.K_ESCAPE:
                self.pause_game()

            # Transformações (teclas 1-5)
            elif key == pygame.K_1:
                self.apply_transformation('translate')
            elif key == pygame.K_2:
                self.apply_transformation('rotate')
            elif key == pygame.K_3:
                self.apply_transformation('scale_up')
            elif key == pygame.K_4:
                self.apply_transformation('reflect')
            elif key == pygame.K_5:
                self.apply_transformation('shear')

            # Escala com + e - (mais intuitivo)
            elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
                self.apply_transformation('scale_up')
            elif key == pygame.K_MINUS:
                self.apply_transformation('scale_down')

            # Modelos de iluminação (Q, W, E)
            elif key == pygame.K_q:
                self.change_shading_model('lambertian')
            elif key == pygame.K_w:
                self.change_shading_model('phong')
            elif key == pygame.K_e:
                self.change_shading_model('gouraud')

            # Dica (H)
            elif key == pygame.K_h:
                self.show_hint()

            # Toggle controles (C)
            elif key == pygame.K_c:
                self.hud.toggle_controls()

            # Toggle auto-rotação (R)
            elif key == pygame.K_r:
                self.auto_rotate = not self.auto_rotate

        elif self.state == GameState.PAUSED:
            if key == pygame.K_ESCAPE:
                self.resume_game()

    def handle_camera_drag(self, current_pos):
        """Processa arrastar da câmera"""
        if self.last_mouse_pos is None:
            self.last_mouse_pos = current_pos
            return

        dx = current_pos[0] - self.last_mouse_pos[0]
        dy = current_pos[1] - self.last_mouse_pos[1]

        # Orbita a câmera
        self.camera.orbit(
            -dx * CAMERA_ROTATION_SPEED,
            -dy * CAMERA_ROTATION_SPEED
        )

        self.last_mouse_pos = current_pos

    def update(self):
        """Atualiza lógica do jogo"""
        if self.state == GameState.MENU:
            self.update_menu()
        elif self.state == GameState.PLAYING:
            self.update_playing()
        elif self.state == GameState.PAUSED:
            self.update_paused()
        elif self.state == GameState.GAME_OVER:
            self.update_game_over()
        elif self.state == GameState.TRAINING:
            self.update_training()
        elif self.state == GameState.TUTORIAL:
            pass  # Tutorial não precisa de update

    def update_menu(self):
        """Atualiza menu"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.menu.update(mouse_pos, mouse_pressed)

        if action == 'start_game':
            self.start_game()
        elif action == 'start_training':
            self.start_training()
        elif action == 'show_tutorial':
            self.state = GameState.TUTORIAL
            self.tutorial.current_page = 0  # Reseta para primeira página
            self.menu.state = MenuState.MAIN  # Garante que o menu volte ao estado principal
        elif action == 'quit':
            self.running = False
        elif action and action.startswith('select_level_'):
            level_num = int(action.split('_')[-1])
            self.start_game(level_num - 1)

    def update_playing(self):
        """Atualiza gameplay"""
        # Verifica se ainda tem vidas (proteção contra game over)
        if self.player.lives <= 0:
            return

        # Auto-rotação dos objetos
        if self.auto_rotate:
            level = self.level_manager.get_current_level()
            if level:
                for shape in level.shapes:
                    shape.rotate_y(self.rotation_speed)

        # Verifica se o nível foi completo
        level = self.level_manager.get_current_level()
        if level and level.is_completed():
            self.complete_level()

    def update_paused(self):
        """Atualiza menu de pausa"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.menu.update(mouse_pos, mouse_pressed)

        if action == 'resume':
            self.resume_game()
        elif action == 'restart':
            self.restart_level()
        elif action == 'main_menu':
            self.state = GameState.MENU
            self.menu.state = MenuState.MAIN  # Garante que volte ao menu principal
        elif action == 'next_level':
            self.next_level()

    def update_game_over(self):
        """Atualiza tela de game over"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.menu.update(mouse_pos, mouse_pressed)

        if action == 'restart_level':
            # Reseta o jogador com 3 vidas e recomeça o nível atual
            self.player.lives = 3
            self.restart_level()
        elif action == 'main_menu':
            # Reseta tudo e volta para o menu
            self.player.reset()
            self.level_manager.current_level_index = 0
            self.state = GameState.MENU

    def draw(self):
        """Desenha tudo"""
        if self.state == GameState.MENU:
            self.menu.draw(self.screen)
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()  # Desenha jogo em baixo
            self.menu.draw(self.screen)  # Menu por cima
        elif self.state == GameState.GAME_OVER:
            self.draw_game()  # Desenha jogo em baixo (desfocado)
            self.menu.draw(self.screen)  # Tela de Game Over por cima
        elif self.state == GameState.TRAINING:
            self.draw_training()
        elif self.state == GameState.TUTORIAL:
            self.tutorial.draw(self.screen)

    def draw_game(self):
        """Desenha o gameplay"""
        # Limpa a tela
        self.renderer.clear(BG_COLOR)

        # Pega nível atual
        level = self.level_manager.get_current_level()
        if not level:
            return

        # Renderiza objetos 3D
        shading_model = self.shading_models[self.current_shading]

        for shape in level.shapes:
            vertices = shape.get_vertices()
            faces = shape.get_faces()
            normals = shape.get_normals()
            color = shape.get_color()

            self.renderer.draw_mesh(
                vertices,
                faces,
                normals,
                self.camera,
                shading_model,
                self.light,
                color
            )

        # Desenha HUD
        current_puzzle = self.get_current_puzzle()
        # Usa o número de ações executadas como tentativas
        attempts_count = len(self.current_actions)

        # Número de ações necessárias para o puzzle
        required_actions = 0
        if current_puzzle and current_puzzle.type.value == 'sequence':
            required_actions = current_puzzle.data.get('required_actions', len(current_puzzle.solution.get('sequence', [])))

        self.hud.draw(
            self.screen,
            self.player,
            level,
            current_puzzle,
            shading_model,
            self.dt,
            attempts_count,
            required_actions
        )

    # ==================== AÇÕES DO JOGO ====================

    def start_game(self, level_index=0):
        """Inicia o jogo"""
        self.state = GameState.PLAYING
        self.level_manager.goto_level(level_index)
        self.player.current_level = level_index
        self.current_puzzle_index = 0

        # Reseta tentativas
        self.wrong_attempts = 0
        self.current_actions = []

        # Reseta câmera
        self.camera = Camera(
            position=[CAMERA_DISTANCE, CAMERA_HEIGHT, CAMERA_DISTANCE],
            target=[0, 0, 0],
            fov=FOV,
            aspect=WINDOW_WIDTH / WINDOW_HEIGHT
        )

    def pause_game(self):
        """Pausa o jogo"""
        self.state = GameState.PAUSED
        self.menu.set_state(MenuState.PAUSE)

    def resume_game(self):
        """Continua o jogo"""
        self.state = GameState.PLAYING

    def restart_level(self):
        """Reinicia o nível atual"""
        level = self.level_manager.get_current_level()
        if level:
            level.reset()
            self.current_puzzle_index = 0

        # Reseta tentativas
        self.wrong_attempts = 0
        self.current_actions = []

        self.state = GameState.PLAYING
        self.hud.show_message("Nivel reiniciado!", HIGHLIGHT_COLOR)

    def complete_level(self):
        """Completa o nível atual"""
        level = self.level_manager.get_current_level()
        if level:
            # Calcula bonus
            bonus = POINTS_PER_LEVEL

            # Adiciona pontos
            self.player.complete_level(level.id, bonus)

            # Mostra menu de vitória
            self.state = GameState.PAUSED
            self.menu.set_state(MenuState.VICTORY)

    def next_level(self):
        """Vai para o próximo nível"""
        if self.level_manager.next_level():
            self.current_puzzle_index = 0

            # Reseta tentativas
            self.wrong_attempts = 0
            self.current_actions = []

            self.state = GameState.PLAYING
            self.hud.show_message("Proximo nivel!", SUCCESS_COLOR)
        else:
            # Jogo completo!
            self.hud.show_message("Parabens! Voce completou o jogo!", SUCCESS_COLOR, 5.0)
            self.state = GameState.MENU

    # ==================== TRANSFORMAÇÕES ====================

    def apply_transformation(self, transform_type):
        """Aplica uma transformação ao objeto"""
        level = self.level_manager.get_current_level()
        if not level or len(level.shapes) == 0:
            return

        # Pega primeiro objeto (pode ser expandido)
        shape = level.shapes[0]

        if transform_type == 'translate':
            shape.translate(0.5, 0, 0)
        elif transform_type == 'rotate':
            shape.rotate_y(45)
        elif transform_type == 'scale_up':
            shape.scale_uniform(1.15)  # Aumenta 15%
        elif transform_type == 'scale_down':
            shape.scale_uniform(0.85)  # Diminui 15%
        elif transform_type == 'scale':  # Mantém compatibilidade
            shape.scale_uniform(1.15)
        elif transform_type == 'reflect':
            shape.reflect_x()
        elif transform_type == 'shear':
            shape.shear_xy(0.1, 0)

        # Registra a ação atual
        self.current_actions.append(transform_type)

        # Registra uso
        self.player.use_transformation(transform_type)

        # Verifica puzzle
        self.check_puzzle_completion()

    def change_shading_model(self, model_name):
        """Muda o modelo de iluminação"""
        if model_name in self.shading_models:
            self.current_shading = model_name
            self.player.use_shading_model(model_name)

            # Verifica puzzle de iluminação
            self.check_puzzle_completion()

    # ==================== PUZZLES ====================

    def get_current_puzzle(self):
        """Retorna o puzzle atual"""
        level = self.level_manager.get_current_level()
        if level and 0 <= self.current_puzzle_index < len(level.puzzles):
            return level.puzzles[self.current_puzzle_index]
        return None

    def check_puzzle_completion(self):
        """Verifica se o puzzle atual foi resolvido"""
        puzzle = self.get_current_puzzle()
        level = self.level_manager.get_current_level()

        if not puzzle or not level:
            return

        # Proteção: não processa se não tem mais vidas
        if self.player.lives <= 0:
            return

        # Verificação automática baseada em transformações/iluminação
        # Para puzzles de sequência - verifica se a sequência está correta
        if puzzle.type.value == 'sequence' and not puzzle.is_solved():
            required_actions = puzzle.data.get('required_actions', len(puzzle.solution.get('sequence', [])))

            # Verifica se completou o número de ações necessárias
            if len(self.current_actions) >= required_actions:
                # Verifica se a sequência está na ordem correta
                expected_sequence = [step['type'] for step in puzzle.solution.get('sequence', [])]
                actual_sequence = self.current_actions[-required_actions:]

                if actual_sequence == expected_sequence:
                    # Sequência correta!
                    is_correct, feedback = puzzle.check_solution({})

                    # Calcula pontos com base no número de tentativas
                    base_points = puzzle.get_reward_points()
                    total_attempts = len(self.current_actions)

                    # Se fez no mínimo de tentativas, ganha 100% dos pontos
                    # Cada tentativa extra acima do mínimo reduz 10% dos pontos
                    extra_attempts = total_attempts - required_actions
                    penalty_percentage = extra_attempts * 10  # 10% por tentativa extra
                    penalty_percentage = min(penalty_percentage, 90)  # Máximo de 90% de penalidade (sempre ganha pelo menos 10%)

                    final_points = int(base_points * (100 - penalty_percentage) / 100)
                    final_points = max(final_points, int(base_points * 0.1))  # Garante pelo menos 10% dos pontos

                    self.player.add_score(final_points)
                    self.hud.show_message(f"Perfeito! +{final_points} pontos!", SUCCESS_COLOR, 2.0)

                    # Marca objetivos como completos
                    for objective in level.objectives:
                        level.complete_objective(objective)

                    # Reseta tentativas e ações
                    self.wrong_attempts = 0
                    self.current_actions = []

                    # Avança para próximo puzzle
                    self.current_puzzle_index += 1
                else:
                    # Sequência errada!
                    self.handle_wrong_attempt()
                    # Não reseta current_actions aqui - deixa acumular até perder vida

        # Para puzzles de transformação - marca como completo automaticamente após aplicar
        elif puzzle.type.value == 'transformation' and not puzzle.is_solved():
            is_correct, feedback = puzzle.check_solution({})

            if is_correct:
                points = puzzle.get_reward_points()
                self.player.add_score(points)
                self.hud.show_message(f"{feedback} +{points} pontos!", SUCCESS_COLOR, 2.0)

                # Marca objetivos como completos
                for objective in level.objectives:
                    level.complete_objective(objective)

                # Reseta tentativas
                self.wrong_attempts = 0
                self.current_actions = []

                # Avança para próximo puzzle
                self.current_puzzle_index += 1

        # Para puzzles de iluminação
        elif puzzle.type.value == 'lighting':
            is_correct, feedback = puzzle.check_solution({'shading_model': self.current_shading})

            if is_correct:
                points = puzzle.get_reward_points()
                self.player.add_score(points)
                self.hud.show_message(f"{feedback} +{points} pontos!", SUCCESS_COLOR, 2.0)

                # Marca objetivos como completos
                for objective in level.objectives:
                    level.complete_objective(objective)

                # Reseta tentativas
                self.wrong_attempts = 0

                # Avança para próximo puzzle
                self.current_puzzle_index += 1

    def handle_wrong_attempt(self):
        """Trata tentativa errada"""
        self.wrong_attempts += 1
        remaining = self.max_wrong_attempts - self.wrong_attempts

        if self.wrong_attempts >= self.max_wrong_attempts:
            # Perde uma vida
            self.player.lose_life()

            # Verifica se ainda tem vidas
            if self.player.lives <= 0:
                # Game Over - sem mais vidas
                self.game_over()
            else:
                # Ainda tem vidas - mostra mensagem e reseta tentativas
                self.hud.show_message(f"Sequencia errada! Perdeu 1 vida! Vidas restantes: {self.player.lives}", ERROR_COLOR, 3.0)
                self.wrong_attempts = 0  # Reseta tentativas para nova chance
                # Não reseta current_actions - mantém a contagem acumulada
        # Removido: else que mostrava mensagem a cada tentativa errada

    def game_over(self):
        """Game Over - Mostra tela de Game Over com opções"""
        # Muda para o estado de Game Over
        self.state = GameState.GAME_OVER

        # Coloca o menu no estado de Game Over
        self.menu.set_state(MenuState.GAME_OVER)

    def show_hint(self):
        """Mostra dica do puzzle atual"""
        puzzle = self.get_current_puzzle()
        if puzzle:
            hint = puzzle.get_hint()
            self.hud.show_message(f"Dica: {hint}", HIGHLIGHT_COLOR, 5.0)
        else:
            self.hud.show_message("Nenhum puzzle ativo", TEXT_COLOR)

    def toggle_fullscreen(self):
        """Alterna entre modo tela cheia e janela"""
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            # Muda para tela cheia
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # Pega o tamanho real da tela
            self.window_width = self.screen.get_width()
            self.window_height = self.screen.get_height()
        else:
            # Volta para janela normal
            self.window_width = WINDOW_WIDTH
            self.window_height = WINDOW_HEIGHT
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        # Atualiza o renderer
        self.renderer = Renderer(self.window_width, self.window_height)
        self.renderer.set_surface(self.screen)

        # Atualiza a câmera
        self.camera.aspect = self.window_width / self.window_height

        # Atualiza menu e HUD
        self.menu = Menu(self.window_width, self.window_height)
        self.hud = HUD(self.window_width, self.window_height)

        # Mostra mensagem
        mode_text = "Tela cheia" if self.is_fullscreen else "Janela"
        self.hud.show_message(f"Modo: {mode_text}", HIGHLIGHT_COLOR, 2.0)

    # ==================== MODO TREINO ====================

    def start_training(self):
        """Inicia o modo treino"""
        self.state = GameState.TRAINING
        self.current_shape_index = 0

        # Importa as classes de formas
        try:
            from .objects.primitives import Cube, Pyramid, Sphere, Cylinder, Torus
        except ImportError:
            from objects.primitives import Cube, Pyramid, Sphere, Cylinder, Torus

        # Cria todas as formas disponíveis
        self.training_shapes = [
            Cube(size=2.0, color=(1.0, 0.5, 0.0)),
            Pyramid(base_size=2.0, height=2.5, color=(0.0, 0.8, 1.0)),
            Sphere(radius=1.2, subdivisions=2, color=(1.0, 0.0, 0.5)),
            Cylinder(radius=0.8, height=2.5, segments=16, color=(0.2, 1.0, 0.2)),
            Torus(major_radius=1.0, minor_radius=0.3, major_segments=16, minor_segments=8, color=(1.0, 1.0, 0.0))
        ]

        # Reseta câmera
        self.camera = Camera(
            position=[CAMERA_DISTANCE, CAMERA_HEIGHT, CAMERA_DISTANCE],
            target=[0, 0, 0],
            fov=FOV,
            aspect=self.window_width / self.window_height
        )

        # Modo treino iniciado (sem mensagem)

    def update_training(self):
        """Atualiza modo treino"""
        # Auto-rotação da forma atual
        if self.auto_rotate and len(self.training_shapes) > 0:
            current_shape = self.training_shapes[self.current_shape_index]
            current_shape.rotate_y(self.rotation_speed)

    def draw_training(self):
        """Desenha modo treino (com a mesma aparência do jogo normal)"""
        # Limpa a tela
        self.renderer.clear(BG_COLOR)

        # Renderiza forma atual
        if len(self.training_shapes) > 0:
            shape = self.training_shapes[self.current_shape_index]
            shading_model = self.shading_models[self.current_shading]

            vertices = shape.get_vertices()
            faces = shape.get_faces()
            normals = shape.get_normals()
            color = shape.get_color()

            self.renderer.draw_mesh(
                vertices,
                faces,
                normals,
                self.camera,
                shading_model,
                self.light,
                color
            )

        # Usa o HUD padrão do jogo, mas sem puzzle
        # Cria um "pseudo-level" para o HUD
        class TrainingLevel:
            def __init__(self, shape_name):
                self.id = 0
                self.name = "Modo Treino"
                self.title = "Modo Treino"
                self.description = f"Praticando com: {shape_name}"
                self.objectives = []
                self.difficulty = 1
                self.completed = False
                self.objectives_completed = []
                self.puzzles = []

            def get_progress(self):
                """Retorna progresso (sempre 0 no treino)"""
                return 0.0

            def is_completed(self):
                """Treino nunca completa"""
                return False

        shape_name = self.training_shapes[self.current_shape_index].name if len(self.training_shapes) > 0 else "..."
        training_level = TrainingLevel(shape_name)

        # Desenha HUD com informações do treino
        self.hud.draw(
            self.screen,
            self.player,
            training_level,
            None,  # Sem puzzle
            self.shading_models[self.current_shading],
            self.dt,
            0,  # Sem tentativas erradas no modo treino
            self.max_wrong_attempts
        )

    def next_shape(self):
        """Avança para a próxima forma"""
        if len(self.training_shapes) > 0:
            self.current_shape_index = (self.current_shape_index + 1) % len(self.training_shapes)

    def previous_shape(self):
        """Volta para a forma anterior"""
        if len(self.training_shapes) > 0:
            self.current_shape_index = (self.current_shape_index - 1) % len(self.training_shapes)

    def set_shape(self, index):
        """Define a forma atual pelo índice"""
        if 0 <= index < len(self.training_shapes):
            self.current_shape_index = index

    def apply_training_transformation(self, transform_type):
        """Aplica transformação no modo treino"""
        if len(self.training_shapes) == 0:
            return

        shape = self.training_shapes[self.current_shape_index]

        if transform_type == 'translate':
            shape.translate(0.5, 0, 0)
        elif transform_type == 'rotate':
            shape.rotate_y(45)
        elif transform_type == 'scale_up':
            shape.scale_uniform(1.15)
        elif transform_type == 'scale_down':
            shape.scale_uniform(0.85)
        elif transform_type == 'reflect':
            shape.reflect_x()
        elif transform_type == 'shear':
            shape.shear_xy(0.1, 0)


def main():
    """Função principal"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
