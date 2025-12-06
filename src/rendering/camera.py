"""
Sistema de câmera 3D
"""

import numpy as np
import math

try:
    from ..transformations.matrix import Matrix4x4
except ImportError:
    from transformations.matrix import Matrix4x4


class Camera:
    """Classe para representar uma câmera 3D"""

    def __init__(self, position, target, up=(0, 1, 0), fov=90, aspect=16/9, near=0.1, far=1000):
        """
        Inicializa a câmera
        Args:
            position: Posição da câmera (x, y, z)
            target: Ponto alvo (x, y, z)
            up: Vetor "para cima" (x, y, z)
            fov: Campo de visão em graus
            aspect: Razão de aspecto (largura/altura)
            near: Plano de corte próximo
            far: Plano de corte distante
        """
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

        # Ângulos de rotação orbital
        self.orbit_angle_h = 0  # Horizontal (ao redor do eixo Y)
        self.orbit_angle_v = 0  # Vertical
        self.orbit_distance = np.linalg.norm(self.position - self.target)

        self.update_matrices()

    def update_matrices(self):
        """Atualiza as matrizes de view e projeção"""
        self.view_matrix = Matrix4x4.look_at(self.position, self.target, self.up)
        self.projection_matrix = Matrix4x4.perspective(self.fov, self.aspect, self.near, self.far)

    def move(self, dx, dy, dz):
        """Move a câmera no espaço"""
        self.position += np.array([dx, dy, dz], dtype=np.float32)
        self.update_matrices()

    def set_position(self, x, y, z):
        """Define a posição da câmera"""
        self.position = np.array([x, y, z], dtype=np.float32)
        self.update_matrices()

    def set_target(self, x, y, z):
        """Define o ponto alvo da câmera"""
        self.target = np.array([x, y, z], dtype=np.float32)
        self.update_matrices()

    def look_at(self, target):
        """Faz a câmera olhar para um ponto"""
        self.target = np.array(target, dtype=np.float32)
        self.update_matrices()

    def orbit(self, delta_h, delta_v):
        """
        Orbita a câmera ao redor do ponto alvo
        Args:
            delta_h: Delta do ângulo horizontal (em radianos)
            delta_v: Delta do ângulo vertical (em radianos)
        """
        self.orbit_angle_h += delta_h
        self.orbit_angle_v += delta_v

        # Limita ângulo vertical para evitar gimbal lock
        self.orbit_angle_v = np.clip(self.orbit_angle_v, -math.pi/2 + 0.1, math.pi/2 - 0.1)

        # Calcula nova posição
        x = self.target[0] + self.orbit_distance * math.cos(self.orbit_angle_v) * math.sin(self.orbit_angle_h)
        y = self.target[1] + self.orbit_distance * math.sin(self.orbit_angle_v)
        z = self.target[2] + self.orbit_distance * math.cos(self.orbit_angle_v) * math.cos(self.orbit_angle_h)

        self.position = np.array([x, y, z], dtype=np.float32)
        self.update_matrices()

    def zoom(self, delta):
        """
        Ajusta o zoom (distância da câmera ao alvo)
        Args:
            delta: Delta da distância
        """
        self.orbit_distance = max(1.0, self.orbit_distance + delta)

        # Recalcula posição mantendo os ângulos
        x = self.target[0] + self.orbit_distance * math.cos(self.orbit_angle_v) * math.sin(self.orbit_angle_h)
        y = self.target[1] + self.orbit_distance * math.sin(self.orbit_angle_v)
        z = self.target[2] + self.orbit_distance * math.cos(self.orbit_angle_v) * math.cos(self.orbit_angle_h)

        self.position = np.array([x, y, z], dtype=np.float32)
        self.update_matrices()

    def get_view_projection_matrix(self):
        """Retorna a matriz combinada view * projection"""
        return self.projection_matrix.multiply(self.view_matrix)

    def get_position(self):
        """Retorna a posição da câmera"""
        return tuple(self.position)

    def get_forward_vector(self):
        """Retorna o vetor de direção da câmera"""
        forward = self.target - self.position
        norm = np.linalg.norm(forward)
        if norm > 0:
            forward = forward / norm
        return tuple(forward)
