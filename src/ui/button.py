"""
Sistema de botões para UI
"""

import pygame


class Button:
    """Classe para botões clicáveis"""

    def __init__(self, x, y, width, height, text, font,
                 color=(100, 100, 200), hover_color=(150, 150, 255),
                 text_color=(255, 255, 255), border_color=(200, 200, 255)):
        """
        Inicializa um botão
        Args:
            x, y: Posição
            width, height: Dimensões
            text: Texto do botão
            font: Fonte pygame
            color: Cor normal
            hover_color: Cor quando mouse está sobre
            text_color: Cor do texto
            border_color: Cor da borda
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color

        self.is_hovered = False
        self.is_pressed = False
        self.enabled = True

    def update(self, mouse_pos, mouse_pressed):
        """
        Atualiza estado do botão
        Args:
            mouse_pos: Posição do mouse (x, y)
            mouse_pressed: Estado dos botões do mouse
        Returns:
            True se foi clicado, False caso contrário
        """
        if not self.enabled:
            self.is_hovered = False
            return False

        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Detecta clique
        if self.is_hovered and mouse_pressed[0]:
            if not self.is_pressed:
                self.is_pressed = True
                return True
        else:
            self.is_pressed = False

        return False

    def draw(self, surface):
        """Desenha o botão"""
        # Escolhe cor
        current_color = self.hover_color if self.is_hovered else self.color

        if not self.enabled:
            current_color = (80, 80, 80)

        # Desenha fundo
        pygame.draw.rect(surface, current_color, self.rect)

        # Desenha borda
        pygame.draw.rect(surface, self.border_color, self.rect, 3)

        # Desenha texto centralizado
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def set_text(self, text):
        """Altera o texto do botão"""
        self.text = text

    def set_enabled(self, enabled):
        """Habilita/desabilita o botão"""
        self.enabled = enabled
