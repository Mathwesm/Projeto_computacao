"""
Tela de Tutorial do jogo
Explica como cada transformação funciona
"""

import pygame
import webbrowser


class Tutorial:
    """Classe para gerenciar a tela de tutorial"""

    def __init__(self, width, height):
        """
        Inicializa o tutorial
        Args:
            width: Largura da tela
            height: Altura da tela
        """
        self.width = width
        self.height = height

        # Fontes
        self.title_font = pygame.font.Font(None, 48)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

        # Cores
        self.bg_color = (20, 20, 40)
        self.panel_color = (40, 40, 80, 230)
        self.border_color = (100, 100, 200)
        self.title_color = (255, 255, 100)
        self.text_color = (255, 255, 255)
        self.highlight_color = (100, 200, 255)

        # Página atual do tutorial
        self.current_page = 0
        self.total_pages = 9  # Introdução + 5 transformações + 3 modelos de iluminação

        # Botão voltar
        self.back_button_rect = pygame.Rect(50, height - 80, 150, 50)
        self.next_button_rect = pygame.Rect(width - 200, height - 80, 150, 50)
        self.prev_button_rect = pygame.Rect(width // 2 - 100, height - 80, 80, 50)
        self.next_page_rect = pygame.Rect(width // 2 + 20, height - 80, 80, 50)

        # Retângulo do link do vídeo (será definido durante o draw)
        self.video_link_rect = None

        # Conteúdo do tutorial
        self.tutorial_content = {
            0: {
                'title': 'BEM-VINDO AO TUTORIAL',
                'subtitle': 'Aprenda sobre Transformações Geométricas',
                'description': [
                    'Neste jogo, você vai aprender sobre transformações geométricas',
                    'aplicadas em objetos 3D. Cada transformação altera o objeto de',
                    'uma maneira específica.',
                    '',
                    'Use as teclas 1-5 para aplicar transformações:',
                    '  1 - Translação',
                    '  2 - Rotação',
                    '  3/+ - Aumentar Escala',
                    '  - - Diminuir Escala',
                    '  4 - Reflexão',
                    '  5 - Distorção (Shear)',
                ],
                'image_path': None,
                'video_url': None
            },
            1: {
                'title': 'TRANSLAÇÃO',
                'subtitle': 'Mover objetos no espaço',
                'description': [
                    'A translação move um objeto de uma posição para outra',
                    'sem alterar sua forma, tamanho ou orientação.',
                    '',
                    'Tecla: 1',
                    '',
                    'Exemplo: Mover um cubo 2 unidades para a direita',
                    'mantém todas as suas propriedades, apenas muda a posição.',
                ],
                'image_path': 'assets/img/Translação.png',
                'video_url': 'https://www.youtube.com/watch?v=w88uizH38GA'
            },
            2: {
                'title': 'ROTAÇÃO',
                'subtitle': 'Girar objetos em torno de um eixo',
                'description': [
                    'A rotação gira um objeto em torno de um eixo (X, Y ou Z)',
                    'sem alterar sua forma ou tamanho.',
                    '',
                    'Tecla: 2',
                    '',
                    'Exemplo: Rotacionar 45° no eixo Y faz o objeto girar',
                    'como se estivesse em um prato giratório.',
                ],
                'image_path': 'assets/img/Rotação.jpg',
                'video_url': 'https://www.youtube.com/watch?v=e_OmNusD5xE'
            },
            3: {
                'title': 'ESCALA',
                'subtitle': 'Aumentar ou diminuir o tamanho',
                'description': [
                    'A escala aumenta ou diminui o tamanho de um objeto',
                    'mantendo suas proporções.',
                    '',
                    'Teclas: 3/+ (aumentar) ou - (diminuir)',
                    '',
                    'Exemplo: Escala de 2x dobra o tamanho do objeto,',
                    'escala de 0.5x reduz pela metade.',
                ],
                'image_path': 'assets/img/Escala.png',
                'video_url': 'https://www.youtube.com/watch?v=WowHp-7j800'
            },
            4: {
                'title': 'REFLEXÃO',
                'subtitle': 'Espelhar objetos',
                'description': [
                    'A reflexão cria uma imagem espelhada do objeto',
                    'em relação a um plano (XY, XZ ou YZ).',
                    '',
                    'Tecla: 4',
                    '',
                    'Exemplo: Reflexão no plano YZ inverte o objeto',
                    'da esquerda para direita.',
                ],
                'image_path': 'assets/img/Reflexão.png',
                'video_url': 'https://www.youtube.com/watch?v=VUBNWVD-ils'
            },
            5: {
                'title': 'DISTORÇÃO (SHEAR)',
                'subtitle': 'Inclinar objetos',
                'description': [
                    'A distorção (shear) inclina um objeto ao longo de um eixo,',
                    'criando uma forma "inclinada".',
                    '',
                    'Tecla: 5',
                    '',
                    'Exemplo: Shear no plano XY faz um cubo parecer',
                    'que está sendo empurrado para o lado.',
                ],
                'image_path': 'assets/img/Distorção.png',
                'video_url': 'https://www.youtube.com/watch?v=jUftXOykePk'
            },
            6: {
                'title': 'ILUMINAÇÃO LAMBERTIANA',
                'subtitle': 'Sombreamento difuso simples',
                'description': [
                    'O modelo Lambertiano (ou Difuso) simula superfícies foscas',
                    'que espalham a luz uniformemente em todas as direções.',
                    '',
                    'Tecla: Q',
                    '',
                    'Características:',
                    '• Não produz brilho ou reflexos especulares',
                    '• A intensidade depende do ângulo entre luz e superfície',
                    '• Ideal para materiais foscos (gesso, papel, madeira)',
                    '',
                    'Fórmula: I = I_luz × k_d × (N · L)',
                    'Onde N é a normal da superfície e L é a direção da luz.',
                ],
                'image_path': 'assets/img/Iluminação Lambertiana.png',
                'video_url': 'https://www.youtube.com/watch?v=A8wquHMK4wE'
            },
            7: {
                'title': 'ILUMINAÇÃO PHONG',
                'subtitle': 'Sombreamento realista com brilho',
                'description': [
                    'O modelo Phong adiciona reflexos especulares (brilho)',
                    'criando um efeito mais realista para superfícies brilhantes.',
                    '',
                    'Tecla: W',
                    '',
                    'Características:',
                    '• Combina iluminação difusa + especular + ambiente',
                    '• Produz pontos de brilho realistas',
                    '• Ideal para metais, plásticos, superfícies polidas',
                    '',
                    'O brilho aparece quando o ângulo de reflexão da luz',
                    'está alinhado com a direção de visão da câmera.',
                ],
                'image_path': 'assets/img/Iluminação Phong.jpg',
                'video_url': 'https://www.youtube.com/watch?v=A8wquHMK4wE'
            },
            8: {
                'title': 'ILUMINAÇÃO GOURAUD',
                'subtitle': 'Sombreamento interpolado nos vértices',
                'description': [
                    'O modelo Gouraud calcula a iluminação nos vértices',
                    'e interpola as cores entre eles para suavizar a superfície.',
                    '',
                    'Tecla: E',
                    '',
                    'Características:',
                    '• Computacionalmente mais eficiente que Phong',
                    '• Cria gradientes suaves de cor',
                    '• Pode perder detalhes de brilho especular',
                    '',
                    'Diferença do Phong: Gouraud calcula luz por vértice,',
                    'Phong calcula luz por pixel (mais preciso mas mais lento).',
                ],
                'image_path': 'assets/img/Iluminação Gouraud.jpeg',
                'video_url': 'https://www.youtube.com/watch?v=A8wquHMK4wE'
            }
        }

    def handle_click(self, pos):
        """
        Processa clique do mouse
        Args:
            pos: Posição do mouse (x, y)
        Returns:
            Ação a ser executada ('back', 'next', 'prev', None)
        """
        if self.back_button_rect.collidepoint(pos):
            return 'back'
        elif self.next_page_rect.collidepoint(pos) and self.current_page < self.total_pages - 1:
            self.current_page += 1
            return None
        elif self.prev_button_rect.collidepoint(pos) and self.current_page > 0:
            self.current_page -= 1
            return None
        # Verifica se clicou no link do vídeo
        elif self.video_link_rect and self.video_link_rect.collidepoint(pos):
            content = self.tutorial_content[self.current_page]
            if content['video_url']:
                webbrowser.open(content['video_url'])
            return None
        return None

    def draw(self, surface):
        """
        Desenha a tela de tutorial
        Args:
            surface: Superfície para desenhar
        """
        # Background
        surface.fill(self.bg_color)

        # Painel principal
        panel_width = self.width - 100
        panel_height = self.height - 150
        panel_x = 50
        panel_y = 30

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill(self.panel_color)
        pygame.draw.rect(panel, self.border_color, (0, 0, panel_width, panel_height), 3)

        # Conteúdo da página atual
        content = self.tutorial_content[self.current_page]

        # Título
        title = self.title_font.render(content['title'], True, self.title_color)
        title_rect = title.get_rect(center=(panel_width // 2, 40))
        panel.blit(title, title_rect)

        # Subtítulo
        subtitle = self.subtitle_font.render(content['subtitle'], True, self.highlight_color)
        subtitle_rect = subtitle.get_rect(center=(panel_width // 2, 90))
        panel.blit(subtitle, subtitle_rect)

        # Descrição
        y_offset = 140
        for line in content['description']:
            text = self.text_font.render(line, True, self.text_color)
            panel.blit(text, (50, y_offset))
            y_offset += 30

        # Lado direito: Imagem e vídeo
        right_x = panel_width - 380
        right_y = 150

        # Placeholder para imagem (se existir)
        if content['image_path']:
            try:
                # Tenta carregar a imagem
                image = pygame.image.load(content['image_path'])
                image = pygame.transform.scale(image, (350, 220))
                panel.blit(image, (right_x, right_y))
            except:
                # Se não encontrar a imagem, mostra placeholder
                placeholder_rect = pygame.Rect(right_x, right_y, 350, 220)
                pygame.draw.rect(panel, (60, 60, 100), placeholder_rect)
                pygame.draw.rect(panel, self.border_color, placeholder_rect, 2)
                placeholder_text = self.small_font.render('[Imagem aqui]', True, self.text_color)
                placeholder_text_rect = placeholder_text.get_rect(center=placeholder_rect.center)
                panel.blit(placeholder_text, placeholder_text_rect)

        # Link do vídeo (logo abaixo da imagem) - CLICÁVEL
        if content['video_url']:
            video_y = right_y + 240
            video_label = self.text_font.render("Vídeo Tutorial:", True, self.title_color)
            panel.blit(video_label, (right_x, video_y))

            # Cria área clicável para o link
            mouse_pos = pygame.mouse.get_pos()
            # Ajusta a posição do mouse relativa ao painel
            relative_mouse_x = mouse_pos[0] - panel_x
            relative_mouse_y = mouse_pos[1] - panel_y

            video_text_surface = self.small_font.render(content['video_url'], True, self.highlight_color)
            video_text_rect = video_text_surface.get_rect(topleft=(right_x, video_y + 30))

            # Verifica se o mouse está sobre o link
            is_hover = video_text_rect.collidepoint(relative_mouse_x, relative_mouse_y)

            # Muda a cor se hover e adiciona sublinhado
            link_color = (150, 220, 255) if is_hover else self.highlight_color
            video_text = self.small_font.render(content['video_url'], True, link_color)
            panel.blit(video_text, (right_x, video_y + 30))

            # Sublinha o link se hover
            if is_hover:
                pygame.draw.line(panel, link_color,
                               (right_x, video_y + 30 + video_text_surface.get_height()),
                               (right_x + video_text_surface.get_width(), video_y + 30 + video_text_surface.get_height()),
                               1)

            # Salva o retângulo do link (ajustado para coordenadas da tela)
            self.video_link_rect = pygame.Rect(
                panel_x + right_x,
                panel_y + video_y + 30,
                video_text_surface.get_width(),
                video_text_surface.get_height()
            )

            help_text = self.small_font.render("(Clique para abrir no navegador)", True, self.text_color)
            panel.blit(help_text, (right_x, video_y + 55))

        # Indicador de página
        page_text = self.text_font.render(f"Página {self.current_page + 1} de {self.total_pages}", True, self.text_color)
        page_rect = page_text.get_rect(center=(panel_width // 2, panel_height - 40))
        panel.blit(page_text, page_rect)

        surface.blit(panel, (panel_x, panel_y))

        # Botões
        self._draw_button(surface, self.back_button_rect, "VOLTAR", self.title_color)

        if self.current_page > 0:
            self._draw_button(surface, self.prev_button_rect, "< Ant", self.text_color)

        if self.current_page < self.total_pages - 1:
            self._draw_button(surface, self.next_page_rect, "Prox >", self.text_color)

    def _draw_button(self, surface, rect, text, color):
        """Desenha um botão"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        # Fundo do botão
        button_color = (80, 80, 150) if is_hover else (50, 50, 100)
        pygame.draw.rect(surface, button_color, rect)
        pygame.draw.rect(surface, self.border_color, rect, 2)

        # Texto do botão
        text_surface = self.text_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
