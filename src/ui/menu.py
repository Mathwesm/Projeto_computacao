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

        # ==================== MENU PRINCIPAL ====================
        self.buttons['main_play'] = Button(
            center_x - 150, 250, 300, 60,
            "JOGAR", self.button_font
        )

        self.buttons['main_level_select'] = Button(
            center_x - 150, 330, 300, 60,
            "SELECIONAR NIVEL", self.button_font
        )

        self.buttons['main_help'] = Button(
            center_x - 150, 410, 300, 60,
            "COMO JOGAR", self.button_font
        )

        self.buttons['main_quit'] = Button(
            center_x - 150, 490, 300, 60,
            "SAIR", self.button_font
        )

        # ==================== MENU DE PAUSA ====================
        self.buttons['pause_resume'] = Button(
            center_x - 150, 250, 300, 60,
            "CONTINUAR", self.button_font
        )

        self.buttons['pause_restart'] = Button(
            center_x - 150, 330, 300, 60,
            "REINICIAR NIVEL", self.button_font
        )

        self.buttons['pause_menu'] = Button(
            center_x - 150, 410, 300, 60,
            "MENU PRINCIPAL", self.button_font
        )

        # ==================== MENU DE VITÓRIA ====================
        self.buttons['victory_next'] = Button(
            center_x - 150, 350, 300, 60,
            "PROXIMO NIVEL", self.button_font
        )

        self.buttons['victory_menu'] = Button(
            center_x - 150, 430, 300, 60,
            "MENU PRINCIPAL", self.button_font
        )

        # ==================== MENU DE GAME OVER ====================
        self.buttons['gameover_restart'] = Button(
            center_x - 150, 350, 300, 60,
            "REINICIAR FASE", self.button_font
        )

        self.buttons['gameover_menu'] = Button(
            center_x - 150, 430, 300, 60,
            "MENU PRINCIPAL", self.button_font
        )

        # ==================== MENU DE AJUDA ====================
        self.buttons['help_back'] = Button(
            center_x - 150, 600, 300, 60,
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
        if self.state == MenuState.MAIN:
            if self.buttons['main_play'].update(mouse_pos, mouse_pressed):
                return 'start_game'
            if self.buttons['main_level_select'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.LEVEL_SELECT
            if self.buttons['main_help'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.HELP
            if self.buttons['main_quit'].update(mouse_pos, mouse_pressed):
                return 'quit'

        elif self.state == MenuState.PAUSE:
            if self.buttons['pause_resume'].update(mouse_pos, mouse_pressed):
                return 'resume'
            if self.buttons['pause_restart'].update(mouse_pos, mouse_pressed):
                return 'restart'
            if self.buttons['pause_menu'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.MAIN
                return 'main_menu'

        elif self.state == MenuState.VICTORY:
            if self.buttons['victory_next'].update(mouse_pos, mouse_pressed):
                return 'next_level'
            if self.buttons['victory_menu'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.MAIN
                return 'main_menu'

        elif self.state == MenuState.GAME_OVER:
            if self.buttons['gameover_restart'].update(mouse_pos, mouse_pressed):
                return 'restart_level'
            if self.buttons['gameover_menu'].update(mouse_pos, mouse_pressed):
                self.state = MenuState.MAIN
                return 'main_menu'

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
        title_rect = title.get_rect(center=(self.width // 2, 120))
        surface.blit(title, title_rect)

        # Subtítulo
        subtitle = self.text_font.render("Aventura das Formas Geometricas", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 180))
        surface.blit(subtitle, subtitle_rect)

        # Botões
        self.buttons['main_play'].draw(surface)
        self.buttons['main_level_select'].draw(surface)
        self.buttons['main_help'].draw(surface)
        self.buttons['main_quit'].draw(surface)

    def _draw_pause_menu(self, surface):
        """Desenha menu de pausa"""
        title = self.title_font.render("PAUSADO", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, 120))
        surface.blit(title, title_rect)

        self.buttons['pause_resume'].draw(surface)
        self.buttons['pause_restart'].draw(surface)
        self.buttons['pause_menu'].draw(surface)

    def _draw_victory_menu(self, surface):
        """Desenha menu de vitória"""
        title = self.title_font.render("NIVEL COMPLETO!", True, (100, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, 150))
        surface.blit(title, title_rect)

        subtitle = self.text_font.render("Parabens! Voce dominou as transformacoes!", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 250))
        surface.blit(subtitle, subtitle_rect)

        self.buttons['victory_next'].draw(surface)
        self.buttons['victory_menu'].draw(surface)

    def _draw_gameover_menu(self, surface):
        """Desenha menu de game over"""
        title = self.title_font.render("GAME OVER", True, (255, 100, 100))
        title_rect = title.get_rect(center=(self.width // 2, 150))
        surface.blit(title, title_rect)

        subtitle = self.text_font.render("Nao desista! Tente novamente!", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 250))
        surface.blit(subtitle, subtitle_rect)

        self.buttons['gameover_restart'].draw(surface)
        self.buttons['gameover_menu'].draw(surface)

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

        self.buttons['levelselect_back'].draw(surface)

    def set_state(self, state):
        """Define o estado do menu"""
        self.state = state
