"""
HUD (Head-Up Display) do jogo
Mostra informações durante o gameplay
"""

import pygame


class HUD:
    """Classe para gerenciar o HUD do jogo"""

    def __init__(self, width, height):
        """
        Inicializa o HUD
        Args:
            width: Largura da tela
            height: Altura da tela
        """
        self.width = width
        self.height = height

        # Fontes
        self.title_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

        # Cores
        self.bg_color = (40, 40, 80, 200)  # Com transparência
        self.border_color = (100, 100, 200)
        self.text_color = (255, 255, 255)
        self.highlight_color = (255, 255, 100)
        self.success_color = (100, 255, 100)
        self.error_color = (255, 100, 100)

        # Imagens
        self.heart_image = pygame.image.load("assets/img/imgcoração.png")
        # Redimensionar o coração para um tamanho adequado (30x30 pixels)
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        # Coração vazio
        self.heart_empty_image = pygame.image.load("assets/img/imgcoraçãovazio.png")
        self.heart_empty_image = pygame.transform.scale(self.heart_empty_image, (30, 30))

        # Estado
        self.show_controls = True
        self.show_puzzle_info = True
        self.show_stats = True

        # Mensagens temporárias
        self.temp_message = None
        self.temp_message_time = 0
        self.temp_message_duration = 3.0  # segundos

    def draw(self, surface, player, level, current_puzzle, shading_model, dt, wrong_attempts=0, max_wrong_attempts=5):
        """
        Desenha o HUD
        Args:
            surface: Superfície para desenhar
            player: Objeto Player
            level: Level atual
            current_puzzle: Puzzle atual (ou None)
            shading_model: Modelo de iluminação atual
            dt: Delta time
            wrong_attempts: Número de tentativas erradas
            max_wrong_attempts: Número máximo de tentativas erradas
        """
        # Atualiza mensagem temporária
        if self.temp_message:
            self.temp_message_time -= dt
            if self.temp_message_time <= 0:
                self.temp_message = None

        # Painel superior (stats)
        if self.show_stats:
            self._draw_top_panel(surface, player, level)

        # Painel lateral (informações do puzzle)
        if self.show_puzzle_info and current_puzzle:
            self._draw_puzzle_panel(surface, current_puzzle, wrong_attempts, max_wrong_attempts)

        # Painel de controles
        if self.show_controls:
            self._draw_controls_panel(surface)

        # Indicador de iluminação
        self._draw_shading_indicator(surface, shading_model)

        # Mensagem temporária
        if self.temp_message:
            self._draw_temp_message(surface)

    def _draw_top_panel(self, surface, player, level):
        """Desenha painel superior com estatísticas"""
        panel_height = 60
        panel = pygame.Surface((self.width, panel_height))
        panel.set_alpha(200)
        panel.fill(self.bg_color[:3])

        # Borda
        pygame.draw.rect(panel, self.border_color, (0, 0, self.width, panel_height), 2)

        # Score
        score_text = self.title_font.render(f"Score: {player.score}", True, self.highlight_color)
        panel.blit(score_text, (20, 15))

        # Vidas (usando imagens de coração)
        lives_label = self.title_font.render("Vidas: ", True, self.text_color)
        panel.blit(lives_label, (250, 15))

        # Desenhar corações (cheios e vazios)
        max_lives = 3  # Número máximo de vidas
        heart_x = 250 + lives_label.get_width() + 5
        heart_y = 12  # Ajustar para alinhar com o texto

        for i in range(max_lives):
            if i < player.lives:
                # Coração cheio (vida atual)
                panel.blit(self.heart_image, (heart_x + i * 28, heart_y))
            else:
                # Coração vazio (vida perdida)
                panel.blit(self.heart_empty_image, (heart_x + i * 28, heart_y))


        # Nível
        level_text = self.title_font.render(f"Nivel: {level.name}", True, self.text_color)
        level_rect = level_text.get_rect(center=(self.width // 2, panel_height // 2))
        panel.blit(level_text, level_rect)

        # Progresso do nível
        progress = level.get_progress()
        progress_text = self.text_font.render(f"Progresso: {int(progress * 100)}%", True, self.success_color)
        progress_rect = progress_text.get_rect(right=self.width - 20, centery=panel_height // 2)
        panel.blit(progress_text, progress_rect)

        surface.blit(panel, (0, 0))

    def _draw_puzzle_panel(self, surface, puzzle, wrong_attempts, max_wrong_attempts):
        """Desenha painel lateral com informações do puzzle"""
        panel_width = 350
        panel_height = 250
        panel_x = self.width - panel_width - 10
        panel_y = 80

        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(220)
        panel.fill(self.bg_color[:3])

        # Borda
        pygame.draw.rect(panel, self.border_color, (0, 0, panel_width, panel_height), 3)

        # Título
        title = self.title_font.render("PUZZLE ATUAL", True, self.highlight_color)
        panel.blit(title, (10, 10))

        # Tipo de puzzle
        type_text = self.text_font.render(f"Tipo: {puzzle.type.value}", True, self.text_color)
        panel.blit(type_text, (10, 50))

        # Dificuldade
        diff_text = self.text_font.render(f"Dificuldade: {'★' * puzzle.difficulty}", True, self.highlight_color)
        panel.blit(diff_text, (10, 80))

        # Descrição (com quebra de linha)
        description = puzzle.get_description()
        self._draw_wrapped_text(panel, description, (10, 110), panel_width - 20, self.small_font, self.text_color)

        # Tentativas (usa wrong_attempts ao invés de puzzle.attempts)
        attempts_text = self.small_font.render(
            f"Tentativas: {wrong_attempts}/{max_wrong_attempts}",
            True, self.text_color
        )
        panel.blit(attempts_text, (10, 200))

        # Dica disponível
        hint_text = self.small_font.render("Pressione H para dica", True, self.success_color)
        panel.blit(hint_text, (10, 225))

        surface.blit(panel, (panel_x, panel_y))

    def _draw_controls_panel(self, surface):
        """Desenha painel de controles"""
        panel_width = 300
        panel_height = 300  # Aumentado para caber mais controles
        panel_x = 10
        panel_y = 80

        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(220)
        panel.fill(self.bg_color[:3])

        # Borda
        pygame.draw.rect(panel, self.border_color, (0, 0, panel_width, panel_height), 3)

        # Título
        title = self.title_font.render("CONTROLES", True, self.highlight_color)
        panel.blit(title, (10, 10))

        # Lista de controles
        controls = [
            ("Mouse", "Rotacionar camera"),
            ("Scroll", "Zoom"),
            ("1", "Translacao"),
            ("2", "Rotacao"),
            ("3 ou +", "Aumentar escala"),
            ("- (menos)", "Diminuir escala"),
            ("4", "Reflexao"),
            ("5", "Distorcao"),
            ("Q/W/E", "Iluminacao"),
            ("H", "Dica"),
            ("ESC", "Pausar"),
        ]

        y = 50
        for key, action in controls:
            key_text = self.small_font.render(f"{key}:", True, self.highlight_color)
            action_text = self.small_font.render(action, True, self.text_color)

            panel.blit(key_text, (10, y))
            panel.blit(action_text, (80, y))
            y += 22

        surface.blit(panel, (panel_x, panel_y))

    def _draw_shading_indicator(self, surface, shading_model):
        """Desenha indicador do modelo de iluminação atual"""
        panel_width = 250
        panel_height = 80
        panel_x = self.width - panel_width - 10
        panel_y = self.height - panel_height - 10

        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(220)
        panel.fill(self.bg_color[:3])

        # Borda
        pygame.draw.rect(panel, self.border_color, (0, 0, panel_width, panel_height), 3)

        # Título
        title = self.text_font.render("ILUMINACAO", True, self.highlight_color)
        panel.blit(title, (10, 10))

        # Modelo atual
        model_name = shading_model.__class__.__name__
        model_text = self.title_font.render(model_name, True, self.success_color)
        panel.blit(model_text, (10, 40))

        surface.blit(panel, (panel_x, panel_y))

    def _draw_temp_message(self, surface):
        """Desenha mensagem temporária no centro da tela"""
        if not self.temp_message:
            return

        message, color = self.temp_message

        # Fundo semi-transparente
        panel_width = 600
        panel_height = 100
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height) // 2

        panel = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(230)
        panel.fill((30, 30, 30))

        # Borda
        pygame.draw.rect(panel, color, (0, 0, panel_width, panel_height), 4)

        # Mensagem
        text = self.title_font.render(message, True, color)
        text_rect = text.get_rect(center=(panel_width // 2, panel_height // 2))
        panel.blit(text, text_rect)

        surface.blit(panel, (panel_x, panel_y))

    def _draw_wrapped_text(self, surface, text, pos, max_width, font, color):
        """Desenha texto com quebra de linha"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        y = pos[1]
        for line in lines:
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (pos[0], y))
            y += font.get_height() + 2

    def show_message(self, message, color=None, duration=3.0):
        """
        Mostra uma mensagem temporária
        Args:
            message: Texto da mensagem
            color: Cor da mensagem (padrão: branco)
            duration: Duração em segundos
        """
        if color is None:
            color = self.text_color

        self.temp_message = (message, color)
        self.temp_message_time = duration

    def toggle_controls(self):
        """Alterna exibição do painel de controles"""
        self.show_controls = not self.show_controls

    def toggle_puzzle_info(self):
        """Alterna exibição do painel de puzzle"""
        self.show_puzzle_info = not self.show_puzzle_info
