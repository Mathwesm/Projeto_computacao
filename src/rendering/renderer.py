"""
Engine de renderização 3D para Pygame
"""

import pygame
import numpy as np
from .lighting import Light


class Renderer:
    """Renderizador 3D básico para Pygame"""

    def __init__(self, width, height):
        """
        Inicializa o renderizador
        Args:
            width: Largura da tela
            height: Altura da tela
        """
        self.width = width
        self.height = height
        self.surface = None

    def set_surface(self, surface):
        """Define a superfície de renderização"""
        self.surface = surface

    def project_point(self, point_3d, camera):
        """
        Projeta um ponto 3D para coordenadas 2D de tela
        Args:
            point_3d: Ponto 3D (x, y, z)
            camera: Objeto Camera
        Returns:
            Tupla (x_screen, y_screen, depth) ou None se fora da tela
        """
        # Aplica transformações de view e projeção
        vp_matrix = camera.get_view_projection_matrix()
        point_4d = vp_matrix.transform_point(point_3d)

        x, y, z = point_4d

        # Verifica se está dentro do frustum
        if z <= 0:
            return None

        # Normaliza para NDC (Normalized Device Coordinates)
        # Já está normalizado pela transformação homogênea

        # Converte para coordenadas de tela
        screen_x = int((x + 1) * 0.5 * self.width)
        screen_y = int((1 - (y + 1) * 0.5) * self.height)

        # Verifica se está dentro da tela
        if screen_x < 0 or screen_x >= self.width or screen_y < 0 or screen_y >= self.height:
            return None

        return (screen_x, screen_y, z)

    def draw_line_3d(self, point1, point2, camera, color, width=1):
        """
        Desenha uma linha 3D
        Args:
            point1, point2: Pontos 3D
            camera: Objeto Camera
            color: Cor RGB
            width: Espessura da linha
        """
        if self.surface is None:
            return

        # Projeta os pontos
        proj1 = self.project_point(point1, camera)
        proj2 = self.project_point(point2, camera)

        if proj1 is None or proj2 is None:
            return

        # Desenha a linha
        pygame.draw.line(
            self.surface,
            color,
            (proj1[0], proj1[1]),
            (proj2[0], proj2[1]),
            width
        )

    def draw_wireframe(self, vertices, edges, camera, color):
        """
        Desenha um objeto em wireframe
        Args:
            vertices: Lista de vértices 3D
            edges: Lista de pares de índices de vértices
            camera: Objeto Camera
            color: Cor RGB
        """
        for edge in edges:
            v1 = vertices[edge[0]]
            v2 = vertices[edge[1]]
            self.draw_line_3d(v1, v2, camera, color, 2)

    def draw_filled_triangle(self, v1, v2, v3, camera, color):
        """
        Desenha um triângulo 3D preenchido
        Args:
            v1, v2, v3: Vértices 3D do triângulo
            camera: Objeto Camera
            color: Cor RGB
        """
        if self.surface is None:
            return

        # Projeta os vértices
        proj1 = self.project_point(v1, camera)
        proj2 = self.project_point(v2, camera)
        proj3 = self.project_point(v3, camera)

        # Verifica se todos os vértices estão visíveis
        if proj1 is None or proj2 is None or proj3 is None:
            return

        # Desenha o triângulo preenchido
        points = [
            (proj1[0], proj1[1]),
            (proj2[0], proj2[1]),
            (proj3[0], proj3[1])
        ]

        pygame.draw.polygon(self.surface, color, points)

    def draw_mesh(self, vertices, faces, normals, camera, shading_model, light, material_color):
        """
        Desenha uma malha 3D com iluminação
        Args:
            vertices: Lista de vértices 3D
            faces: Lista de faces (cada face é uma lista de índices de vértices)
            normals: Lista de normais (uma por face ou por vértice)
            camera: Objeto Camera
            shading_model: Modelo de iluminação (PhongShading, etc.)
            light: Objeto Light
            material_color: Cor do material (0.0-1.0)
        """
        if self.surface is None:
            return

        # Ordena faces por profundidade (painter's algorithm básico)
        face_depths = []
        for face in faces:
            # Calcula centroide da face
            centroid = np.mean([vertices[i] for i in face], axis=0)

            # Calcula profundidade
            depth = np.linalg.norm(centroid - np.array(camera.position))
            face_depths.append((depth, face))

        # Ordena do mais distante para o mais próximo
        face_depths.sort(reverse=True, key=lambda x: x[0])

        # Renderiza cada face
        for depth, face in face_depths:
            if len(face) < 3:
                continue

            # Pega os vértices da face
            face_vertices = [vertices[i] for i in face]

            # Calcula normal da face (se não fornecida)
            if len(normals) == len(faces):
                # Normais por face
                face_idx = faces.index(face)
                normal = normals[face_idx]
            else:
                # Calcula normal da face
                v0 = np.array(face_vertices[0])
                v1 = np.array(face_vertices[1])
                v2 = np.array(face_vertices[2])
                edge1 = v1 - v0
                edge2 = v2 - v0
                normal = np.cross(edge1, edge2)
                norm_mag = np.linalg.norm(normal)
                if norm_mag > 0:
                    normal = normal / norm_mag

            # Back-face culling (opcional via config)
            # Garante que normal é um array numpy
            normal = np.array(normal)

            centroid = np.mean(face_vertices, axis=0)
            view_dir = centroid - np.array(camera.position)
            is_backface = np.dot(normal, view_dir) > 0

            # Se backface culling estiver ativo, pula faces de trás
            try:
                from core.config import ENABLE_BACKFACE_CULLING
            except ImportError:
                from ..core.config import ENABLE_BACKFACE_CULLING

            if ENABLE_BACKFACE_CULLING and is_backface:
                continue

            # Se a face está de costas, inverte a normal para iluminação correta
            if is_backface:
                normal = -normal

            # Calcula cor com iluminação
            color = shading_model.calculate_color(
                centroid,
                normal,
                light,
                material_color,
                camera.position
            )

            # Triangula a face se tiver mais de 3 vértices
            for i in range(1, len(face_vertices) - 1):
                self.draw_filled_triangle(
                    face_vertices[0],
                    face_vertices[i],
                    face_vertices[i + 1],
                    camera,
                    color
                )

    def clear(self, color):
        """Limpa a tela com uma cor"""
        if self.surface:
            self.surface.fill(color)

    def draw_text(self, text, position, font, color):
        """
        Desenha texto na tela
        Args:
            text: Texto a desenhar
            position: Posição (x, y)
            font: Objeto pygame.font.Font
            color: Cor RGB
        """
        if self.surface is None:
            return

        text_surface = font.render(text, True, color)
        self.surface.blit(text_surface, position)
