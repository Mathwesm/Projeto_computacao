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
    from .ui import Menu, MenuState, HUD
except ImportError:
    from core.config import *
    from rendering import Camera, Renderer, Light, create_shading_model
    from game_logic import Player, LevelManager
    from ui import Menu, MenuState, HUD


class GameState(Enum):
    """Estados do jogo"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"  # Tela de Game Over com opções


class Game:
    """Classe principal do jogo"""

    def __init__(self):
        """Inicializa o jogo"""
        pygame.init()

        # Configuração da janela
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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

        # Renderização 3D
        self.renderer = Renderer(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.renderer.set_surface(self.screen)

        # Câmera
        self.camera = Camera(
            position=[CAMERA_DISTANCE, CAMERA_HEIGHT, CAMERA_DISTANCE],
            target=[0, 0, 0],
            fov=FOV,
            aspect=WINDOW_WIDTH / WINDOW_HEIGHT
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
                    self.mouse_dragging = True
                    self.last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
                    self.last_mouse_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_dragging and self.state == GameState.PLAYING:
                    self.handle_camera_drag(event.pos)

            # Scroll do mouse (zoom)
            elif event.type == pygame.MOUSEWHEEL:
                if self.state == GameState.PLAYING:
                    self.camera.zoom(-event.y * CAMERA_ZOOM_SPEED)

    def handle_keydown(self, key):
        """Processa teclas pressionadas"""
        if self.state == GameState.PLAYING:
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

    def update_menu(self):
        """Atualiza menu"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.menu.update(mouse_pos, mouse_pressed)

        if action == 'start_game':
            self.start_game()
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
        self.hud.draw(
            self.screen,
            self.player,
            level,
            current_puzzle,
            shading_model,
            self.dt
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
                    points = puzzle.get_reward_points()
                    self.player.add_score(points)
                    self.hud.show_message(f"Perfeito! +{points} pontos!", SUCCESS_COLOR, 2.0)

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
                    self.current_actions = []  # Reseta para tentar novamente

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
        else:
            self.hud.show_message(f"Sequencia errada! Tentativas restantes: {remaining}", WARNING_COLOR, 2.0)

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


def main():
    """Função principal"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
