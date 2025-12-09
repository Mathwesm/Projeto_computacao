"""
Sistema de menus do jogo
"""

import pygame
from enum import Enum
from .button import Button


class MenuState(Enum):
    """Estados possíveis do menu"""
    MAIN = "main"
    LEVEL_SELECT = "level_select"
    SETTINGS = "settings"
    HELP = "help"
    PAUSE = "pause"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class Menu:
    """Classe para gerenciar menus"""

    def __init__(self, width, height):
        """
        Inicializa o sistema de menus
        Args:
            width: Largura da tela
            height: Altura da tela
        """
        self.width = width
        self.height = height
        self.state = MenuState.MAIN
        self.previous_state = MenuState.MAIN  # Rastreia o estado anterior
        self.wait_for_mouse_release = False  # Espera usuário soltar mouse após mudança de estado

        # Sistema de desbloqueio de níveis
        self.unlocked_levels = [0]  # Nível 0 (primeiro nível) sempre desbloqueado

        # Fontes
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)

        # Botões
        self.buttons = {}
        self._create_buttons()

        # Cores
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 255, 100)
        self.text_color = (255, 255, 255)

    def _create_buttons(self):
        """Cria todos os botões dos menus"""
        center_x = self.width // 2
        center_y = self.height // 2

        # ==================== MENU PRINCIPAL ====================
        self.buttons['main_play'] = Button(
            center_x - 150, center_y - 140, 300, 60,
            "JOGAR", self.button_font
        )

        self.buttons['main_level_select'] = Button(
            center_x - 150, center_y - 60, 300, 60,
            "SELECIONAR NIVEL", self.button_font
        )

        self.buttons['main_training'] = Button(
            center_x - 150, center_y + 20, 300, 60,
            "MODO TREINO", self.button_font
        )

        self.buttons['main_help'] = Button(
            center_x - 150, center_y + 100, 300, 60,
            "COMO JOGAR", self.button_font
        )

        self.buttons['main_quit'] = Button(
            center_x - 150, center_y + 180, 300, 60,
            "SAIR", self.button_font
        )

        # ==================== MENU DE PAUSA ====================
        self.buttons['pause_resume'] = Button(
            center_x - 150, center_y - 60, 300, 60,
            "CONTINUAR", self.button_font
        )

        self.buttons['pause_restart'] = Button(
            center_x - 150, center_y + 20, 300, 60,
            "REINICIAR NIVEL", self.button_font
        )

        self.buttons['pause_menu'] = Button(
            center_x - 150, center_y + 100, 300, 60,
            "MENU PRINCIPAL", self.button_font
        )

        # ==================== MENU DE VITÓRIA ====================
        self.buttons['victory_next'] = Button(
            center_x - 150, center_y + 40, 300, 60,
            "PROXIMO NIVEL", self.button_font
        )

        self.buttons['victory_menu'] = Button(
            center_x - 150, center_y + 120, 300, 60,
            "MENU PRINCIPAL", self.button_font
        )

        # ==================== MENU DE GAME OVER ====================
        self.buttons['gameover_restart'] = Button(
            center_x - 150, center_y - 20, 300, 60,
            "REINICIAR FASE", self.button_font
        )

        self.buttons['gameover_menu'] = Button(
            center_x - 150, center_y + 60, 300, 60,
            "MENU PRINCIPAL", self.button_font
        )

        self.buttons['gameover_training'] = Button(
            center_x - 150, center_y + 140, 300, 60,
            "MODO TREINO", self.button_font
        )

        self.buttons['gameover_tutorial'] = Button(
            center_x - 150, center_y + 220, 300, 60,
            "COMO JOGAR", self.button_font
        )

        # ==================== MENU DE AJUDA ====================
        self.buttons['help_back'] = Button(
            center_x - 150, self.height - 100, 300, 60,
            "VOLTAR", self.button_font
        )

        # ==================== SELEÇÃO DE NÍVEIS ====================
        # Cria botões para cada nível (10 níveis)
        for i in range(10):
            col = i % 5
            row = i // 5

            x = 100 + col * 220
            y = 200 + row * 100

            self.buttons[f'level_{i+1}'] = Button(
                x, y, 200, 80,
                f"NIVEL {i+1}", self.button_font
            )

        self.buttons['levelselect_back'] = Button(
            center_x - 150, 600, 300, 60,
            "VOLTAR", self.button_font
        )

    def update(self, mouse_pos, mouse_pressed):
        """
        Atualiza o menu
        Args:
            mouse_pos: Posição do mouse
            mouse_pressed: Estado dos botões do mouse
        Returns:
            Ação do menu (string) ou None
        """
        # Se o estado mudou neste frame, não processa botões (evita duplo clique)
        if self.state != self.previous_state:
            self.previous_state = self.state
            self.wait_for_mouse_release = True  # Ativa flag para esperar soltar mouse
            return None

        # Se estamos esperando o usuário soltar o mouse
        if self.wait_for_mouse_release:
            if not mouse_pressed[0]:  # Mouse foi solto
                self.wait_for_mouse_release = False
            return None  # Não processa cliques até soltar

        if self.state == MenuState.MAIN:
            if self.buttons['main_play'].update(mouse_pos, mouse_pressed):
                return 'start_game'
            if self.buttons['main_level_select'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.LEVEL_SELECT
            if self.buttons['main_training'].update(mouse_pos, mouse_pressed):
                return 'start_training'
            if self.buttons['main_help'].update(mouse_pos, mouse_pressed):
                return 'show_tutorial'
            if self.buttons['main_quit'].update(mouse_pos, mouse_pressed):
                return 'quit'

        elif self.state == MenuState.PAUSE:
            if self.buttons['pause_resume'].update(mouse_pos, mouse_pressed):
                return 'resume'
            if self.buttons['pause_restart'].update(mouse_pos, mouse_pressed):
                return 'restart'
            if self.buttons['pause_menu'].update(mouse_pos, mouse_pressed):
                return 'main_menu'

        elif self.state == MenuState.VICTORY:
            if self.buttons['victory_next'].update(mouse_pos, mouse_pressed):
                return 'next_level'
            if self.buttons['victory_menu'].update(mouse_pos, mouse_pressed):
                return 'main_menu'

        elif self.state == MenuState.GAME_OVER:
            if self.buttons['gameover_restart'].update(mouse_pos, mouse_pressed):
                return 'restart_level'
            if self.buttons['gameover_menu'].update(mouse_pos, mouse_pressed):
                return 'main_menu'
            if self.buttons['gameover_training'].update(mouse_pos, mouse_pressed):
                return 'start_training'
            if self.buttons['gameover_tutorial'].update(mouse_pos, mouse_pressed):
                return 'show_tutorial'

        elif self.state == MenuState.HELP:
            if self.buttons['help_back'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.MAIN

        elif self.state == MenuState.LEVEL_SELECT:
            # Verifica clique em níveis
            for i in range(10):
                if self.buttons[f'level_{i+1}'].update(mouse_pos, mouse_pressed):
                    return f'select_level_{i+1}'

            if self.buttons['levelselect_back'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.MAIN

        return None

    def draw(self, surface):
        """Desenha o menu"""
        surface.fill(self.bg_color)

        if self.state == MenuState.MAIN:
            self._draw_main_menu(surface)
        elif self.state == MenuState.PAUSE:
            self._draw_pause_menu(surface)
        elif self.state == MenuState.VICTORY:
            self._draw_victory_menu(surface)

        elif self.state == MenuState.GAME_OVER:
            self._draw_gameover_menu(surface)
        elif self.state == MenuState.HELP:
            self._draw_help_menu(surface)
        elif self.state == MenuState.LEVEL_SELECT:
            self._draw_levelselect_menu(surface)

    def _draw_main_menu(self, surface):
        """Desenha menu principal"""
        # Título
        title = self.title_font.render("MATHSHAPE QUEST", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 280))
        surface.blit(title, title_rect)

        # Subtítulo
        subtitle = self.text_font.render("Aventura das Formas Geometricas", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 2 - 220))
        surface.blit(subtitle, subtitle_rect)

        # Botões
        self.buttons['main_play'].draw(surface)
        self.buttons['main_level_select'].draw(surface)
        self.buttons['main_training'].draw(surface)
        self.buttons['main_help'].draw(surface)
        self.buttons['main_quit'].draw(surface)

    def _draw_pause_menu(self, surface):
        """Desenha menu de pausa"""
        title = self.title_font.render("PAUSADO", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 200))
        surface.blit(title, title_rect)

        self.buttons['pause_resume'].draw(surface)
        self.buttons['pause_restart'].draw(surface)
        self.buttons['pause_menu'].draw(surface)

    def _draw_victory_menu(self, surface):
        """Desenha menu de vitória"""
        title = self.title_font.render("NIVEL COMPLETO!", True, (100, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 140))
        surface.blit(title, title_rect)

        subtitle = self.text_font.render("Parabens! Voce dominou as transformacoes!", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 2 - 60))
        surface.blit(subtitle, subtitle_rect)

        self.buttons['victory_next'].draw(surface)
        self.buttons['victory_menu'].draw(surface)

    def _draw_gameover_menu(self, surface):
        """Desenha menu de game over"""
        title = self.title_font.render("GAME OVER", True, (255, 100, 100))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 200))
        surface.blit(title, title_rect)

        subtitle = self.text_font.render("Nao desista! Tente novamente!", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 2 - 120))
        surface.blit(subtitle, subtitle_rect)

        help_text = self.text_font.render("Precisa de ajuda? Experimente o Modo Treino ou revise o tutorial!", True, (200, 200, 255))
        help_rect = help_text.get_rect(center=(self.width // 2, self.height // 2 - 70))
        surface.blit(help_text, help_rect)

        self.buttons['gameover_restart'].draw(surface)
        self.buttons['gameover_menu'].draw(surface)
        self.buttons['gameover_training'].draw(surface)
        self.buttons['gameover_tutorial'].draw(surface)

    def _draw_help_menu(self, surface):
        """Desenha menu de ajuda"""
        title = self.title_font.render("COMO JOGAR", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        surface.blit(title, title_rect)

        # Instruções
        instructions = [
            "CONTROLES:",
            "",
            "Mouse: Controlar camera (arrastar)",
            "Scroll: Zoom in/out",
            "Teclas 1-5: Aplicar transformacoes",
            "  1 - Translacao    2 - Rotacao    3 - Escala",
            "  4 - Reflexao      5 - Distorcao",
            "",
            "Teclas Q/W/E: Mudar iluminacao",
            "  Q - Lambertiano   W - Phong   E - Gouraud",
            "",
            "ESC: Pausar jogo",
            "H: Mostrar dica",
            "",
            "OBJETIVO:",
            "Resolva puzzles usando transformacoes geometricas",
            "e modelos de iluminacao para restaurar Geometria!"
        ]

        y = 140
        for line in instructions:
            text = self.text_font.render(line, True, self.text_color)
            surface.blit(text, (100, y))
            y += 30

        self.buttons['help_back'].draw(surface)

    def _draw_levelselect_menu(self, surface):
        """Desenha menu de seleção de níveis"""
        title = self.title_font.render("SELECIONAR NIVEL", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        surface.blit(title, title_rect)

        # Desenha botões dos níveis
        for i in range(10):
            self.buttons[f'level_{i+1}'].draw(surface)

            # Se o nível está bloqueado, desenha um cadeado em cima
            if i not in self.unlocked_levels:
                button = self.buttons[f'level_{i+1}']
                # Desenha um símbolo de cadeado
                lock_font = pygame.font.Font(None, 48)
                lock_text = lock_font.render("🔒", True, (200, 200, 200))
                lock_rect = lock_text.get_rect(center=button.rect.center)
                surface.blit(lock_text, lock_rect)

        self.buttons['levelselect_back'].draw(surface)

    def set_state(self, state):
        """Define o estado do menu"""
        self.previous_state = self.state  # Atualiza estado anterior
        self.state = state
        self.wait_for_mouse_release = True  # Espera soltar mouse após mudança externa
        # Reseta o estado de todos os botões para evitar cliques fantasmas
        for button in self.buttons.values():
            button.is_pressed = False
            button.is_hovered = False

    def update_unlocked_levels(self, player):
        """
        Atualiza quais níveis estão desbloqueados baseado no progresso do jogador
        Args:
            player: Objeto Player com os níveis completos
        """
        # Converte IDs dos níveis (1, 2, 3...) para índices (0, 1, 2...)
        # levels_completed contém IDs dos níveis (que começam em 1)
        completed_indices = [level_id - 1 for level_id in player.levels_completed]

        # Sempre desbloqueado: nível 0 (primeiro)
        self.unlocked_levels = [0]

        # Desbloqueia todos os níveis que o jogador completou
        for index in completed_indices:
            if index not in self.unlocked_levels and 0 <= index < 10:
                self.unlocked_levels.append(index)

        # Desbloqueia APENAS o próximo nível após o último completado
        if completed_indices:
            max_completed_index = max(completed_indices)
            next_index = max_completed_index + 1
            if next_index < 10 and next_index not in self.unlocked_levels:
                self.unlocked_levels.append(next_index)

        # Atualiza o estado dos botões (habilita/desabilita)
        for i in range(10):
            if f'level_{i+1}' in self.buttons:
                self.buttons[f'level_{i+1}'].set_enabled(i in self.unlocked_levels)
