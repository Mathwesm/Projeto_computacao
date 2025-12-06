"""
Primitivas geométricas 3D
Define formas básicas como Cubo, Esfera, Pirâmide, etc.
"""

import numpy as np
import math
from .shape3d import Shape3D


class Cube(Shape3D):
    """Cubo 3D"""

    def __init__(self, size=1.0, color=(1.0, 0.5, 0.0)):
        """
        Cria um cubo
        Args:
            size: Tamanho do lado do cubo
            color: Cor RGB (0.0-1.0)
        """
        s = size / 2

        # 8 vértices do cubo
        vertices = [
            (-s, -s, -s),  # 0
            ( s, -s, -s),  # 1
            ( s,  s, -s),  # 2
            (-s,  s, -s),  # 3
            (-s, -s,  s),  # 4
            ( s, -s,  s),  # 5
            ( s,  s,  s),  # 6
            (-s,  s,  s),  # 7
        ]

        # 6 faces (cada face é um quadrilátero)
        faces = [
            [0, 1, 2, 3],  # Frente
            [4, 5, 6, 7],  # Trás
            [0, 1, 5, 4],  # Baixo
            [2, 3, 7, 6],  # Cima
            [0, 3, 7, 4],  # Esquerda
            [1, 2, 6, 5],  # Direita
        ]

        super().__init__(vertices, faces, color)
        self.name = "Cube"


class Pyramid(Shape3D):
    """Pirâmide 3D (base quadrada)"""

    def __init__(self, base_size=1.0, height=1.5, color=(0.0, 0.8, 1.0)):
        """
        Cria uma pirâmide
        Args:
            base_size: Tamanho da base
            height: Altura da pirâmide
            color: Cor RGB (0.0-1.0)
        """
        s = base_size / 2
        h = height / 2

        # 5 vértices
        vertices = [
            (-s, -h, -s),  # 0 - Base inferior esquerda
            ( s, -h, -s),  # 1 - Base inferior direita
            ( s, -h,  s),  # 2 - Base superior direita
            (-s, -h,  s),  # 3 - Base superior esquerda
            ( 0,  h,  0),  # 4 - Topo
        ]

        # 5 faces
        faces = [
            [0, 1, 2, 3],  # Base
            [0, 1, 4],     # Lado 1
            [1, 2, 4],     # Lado 2
            [2, 3, 4],     # Lado 3
            [3, 0, 4],     # Lado 4
        ]

        super().__init__(vertices, faces, color)
        self.name = "Pyramid"


class Sphere(Shape3D):
    """Esfera 3D (aproximada por subdivisão)"""

    def __init__(self, radius=1.0, subdivisions=2, color=(1.0, 0.0, 0.5)):
        """
        Cria uma esfera
        Args:
            radius: Raio da esfera
            subdivisions: Nível de subdivisão (qualidade)
            color: Cor RGB (0.0-1.0)
        """
        # Cria um icosaedro e subdivide
        vertices, faces = self._create_icosphere(radius, subdivisions)

        super().__init__(vertices, faces, color)
        self.name = "Sphere"

    def _create_icosphere(self, radius, subdivisions):
        """Cria uma esfera usando subdivisão de icosaedro"""
        # Constantes do icosaedro
        t = (1.0 + math.sqrt(5.0)) / 2.0

        # 12 vértices do icosaedro
        vertices = [
            (-1,  t,  0),
            ( 1,  t,  0),
            (-1, -t,  0),
            ( 1, -t,  0),
            ( 0, -1,  t),
            ( 0,  1,  t),
            ( 0, -1, -t),
            ( 0,  1, -t),
            ( t,  0, -1),
            ( t,  0,  1),
            (-t,  0, -1),
            (-t,  0,  1),
        ]

        # Normaliza e aplica raio
        vertices = [
            tuple(np.array(v) / np.linalg.norm(v) * radius)
            for v in vertices
        ]

        # 20 faces do icosaedro
        faces = [
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
        ]

        # Subdivisão
        for _ in range(subdivisions):
            vertices, faces = self._subdivide(vertices, faces, radius)

        return vertices, faces

    def _subdivide(self, vertices, faces, radius):
        """Subdivide as faces da esfera"""
        new_faces = []
        edge_cache = {}

        def get_middle_point(v1_idx, v2_idx):
            """Obtém ponto médio entre dois vértices"""
            key = tuple(sorted([v1_idx, v2_idx]))
            if key in edge_cache:
                return edge_cache[key]

            v1 = np.array(vertices[v1_idx])
            v2 = np.array(vertices[v2_idx])
            middle = (v1 + v2) / 2.0

            # Normaliza e aplica raio
            middle = middle / np.linalg.norm(middle) * radius

            vertices.append(tuple(middle))
            edge_cache[key] = len(vertices) - 1
            return edge_cache[key]

        # Subdivide cada face em 4
        for face in faces:
            v1, v2, v3 = face[:3]

            a = get_middle_point(v1, v2)
            b = get_middle_point(v2, v3)
            c = get_middle_point(v3, v1)

            new_faces.append([v1, a, c])
            new_faces.append([v2, b, a])
            new_faces.append([v3, c, b])
            new_faces.append([a, b, c])

        return vertices, new_faces


class Cylinder(Shape3D):
    """Cilindro 3D"""

    def __init__(self, radius=0.5, height=2.0, segments=16, color=(0.2, 1.0, 0.2)):
        """
        Cria um cilindro
        Args:
            radius: Raio do cilindro
            height: Altura do cilindro
            segments: Número de segmentos (qualidade)
            color: Cor RGB (0.0-1.0)
        """
        vertices = []
        faces = []

        h = height / 2

        # Cria vértices do círculo superior e inferior
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)

            vertices.append((x, -h, z))  # Círculo inferior
            vertices.append((x,  h, z))  # Círculo superior

        # Adiciona centros das tampas
        center_bottom = len(vertices)
        vertices.append((0, -h, 0))

        center_top = len(vertices)
        vertices.append((0,  h, 0))

        # Cria faces laterais
        for i in range(segments):
            next_i = (i + 1) % segments

            v1 = i * 2
            v2 = i * 2 + 1
            v3 = next_i * 2 + 1
            v4 = next_i * 2

            faces.append([v1, v4, v3, v2])

        # Cria tampa inferior
        for i in range(segments):
            next_i = (i + 1) % segments
            faces.append([center_bottom, next_i * 2, i * 2])

        # Cria tampa superior
        for i in range(segments):
            next_i = (i + 1) % segments
            faces.append([center_top, i * 2 + 1, next_i * 2 + 1])

        super().__init__(vertices, faces, color)
        self.name = "Cylinder"


class Torus(Shape3D):
    """Torus 3D (Rosquinha)"""

    def __init__(self, major_radius=1.0, minor_radius=0.3, major_segments=16, minor_segments=8, color=(1.0, 1.0, 0.0)):
        """
        Cria um torus
        Args:
            major_radius: Raio maior (do centro ao tubo)
            minor_radius: Raio menor (do tubo)
            major_segments: Segmentos ao redor do eixo principal
            minor_segments: Segmentos ao redor do tubo
            color: Cor RGB (0.0-1.0)
        """
        vertices = []
        faces = []

        # Gera vértices
        for i in range(major_segments):
            theta = 2 * math.pi * i / major_segments

            for j in range(minor_segments):
                phi = 2 * math.pi * j / minor_segments

                x = (major_radius + minor_radius * math.cos(phi)) * math.cos(theta)
                y = minor_radius * math.sin(phi)
                z = (major_radius + minor_radius * math.cos(phi)) * math.sin(theta)

                vertices.append((x, y, z))

        # Gera faces
        for i in range(major_segments):
            next_i = (i + 1) % major_segments

            for j in range(minor_segments):
                next_j = (j + 1) % minor_segments

                v1 = i * minor_segments + j
                v2 = next_i * minor_segments + j
                v3 = next_i * minor_segments + next_j
                v4 = i * minor_segments + next_j

                faces.append([v1, v2, v3, v4])

        super().__init__(vertices, faces, color)
        self.name = "Torus"
