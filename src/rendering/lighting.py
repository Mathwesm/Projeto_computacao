"""
Modelos de iluminação 3D
Implementa: Phong, Lambertiano (Diffuse) e Gouraud
"""

import numpy as np
import math


class Light:
    """Classe para representar uma fonte de luz"""

    def __init__(self, position, color=(1.0, 1.0, 1.0), intensity=1.0):
        """
        Inicializa uma fonte de luz
        Args:
            position: Posição da luz (x, y, z)
            color: Cor da luz RGB (0.0-1.0)
            intensity: Intensidade da luz
        """
        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.intensity = intensity

    def get_direction_to(self, point):
        """
        Calcula vetor direção da luz para um ponto
        Args:
            point: Ponto 3D (x, y, z)
        Returns:
            Vetor normalizado da luz para o ponto
        """
        point = np.array(point, dtype=np.float32)
        direction = self.position - point
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction = direction / norm
        return direction

    def get_distance_to(self, point):
        """Calcula distância da luz até um ponto"""
        point = np.array(point, dtype=np.float32)
        return np.linalg.norm(self.position - point)


class LambertianShading:
    """
    Modelo de iluminação LAMBERTIANO (Diffuse)

    Modelo mais simples, considera apenas iluminação difusa.
    Intensidade = Ia + Id * (N · L)

    Onde:
    - Ia: Luz ambiente
    - Id: Intensidade da luz difusa
    - N: Vetor normal da superfície
    - L: Vetor direção da luz
    """

    def __init__(self, ambient=0.2, diffuse=0.8):
        """
        Inicializa o modelo Lambertiano
        Args:
            ambient: Intensidade da luz ambiente (0.0-1.0)
            diffuse: Intensidade da componente difusa (0.0-1.0)
        """
        self.ambient = ambient
        self.diffuse = diffuse

    def calculate_color(self, point, normal, light, material_color, camera_pos=None):
        """
        Calcula a cor de um ponto usando iluminação Lambertiana
        Args:
            point: Posição do ponto 3D
            normal: Vetor normal da superfície
            light: Objeto Light
            material_color: Cor do material RGB (0.0-1.0)
            camera_pos: Posição da câmera (não usado no Lambertiano)
        Returns:
            Cor RGB final (0-255)
        """
        # Normaliza o vetor normal
        normal = np.array(normal, dtype=np.float32)
        norm_magnitude = np.linalg.norm(normal)
        if norm_magnitude > 0:
            normal = normal / norm_magnitude

        # Direção da luz
        light_dir = light.get_direction_to(point)

        # Componente ambiente
        ambient_component = self.ambient * np.array(material_color, dtype=np.float32)

        # Componente difusa (Lambertiana)
        # I_diffuse = I_light * k_d * (N · L)
        n_dot_l = max(0.0, np.dot(normal, light_dir))
        diffuse_component = (
            self.diffuse *
            light.intensity *
            n_dot_l *
            np.array(material_color, dtype=np.float32) *
            light.color
        )

        # Cor final
        final_color = ambient_component + diffuse_component

        # Clamping (0.0-1.0) e conversão para RGB (0-255)
        final_color = np.clip(final_color, 0.0, 1.0)
        return tuple((final_color * 255).astype(int))


class PhongShading:
    """
    Modelo de iluminação PHONG

    Modelo completo com componentes ambiente, difusa e especular.
    Calcula iluminação por pixel.

    Intensidade = Ia + Id * (N · L) + Is * (R · V)^n

    Onde:
    - Ia: Luz ambiente
    - Id: Intensidade difusa
    - Is: Intensidade especular
    - N: Vetor normal
    - L: Vetor direção da luz
    - R: Vetor de reflexão
    - V: Vetor de visão
    - n: Coeficiente de brilho
    """

    def __init__(self, ambient=0.2, diffuse=0.6, specular=0.5, shininess=32):
        """
        Inicializa o modelo Phong
        Args:
            ambient: Intensidade da luz ambiente
            diffuse: Intensidade da componente difusa
            specular: Intensidade da componente especular
            shininess: Coeficiente de brilho (quanto maior, mais concentrado o brilho)
        """
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def calculate_color(self, point, normal, light, material_color, camera_pos):
        """
        Calcula a cor de um ponto usando iluminação Phong
        Args:
            point: Posição do ponto 3D
            normal: Vetor normal da superfície
            light: Objeto Light
            material_color: Cor do material RGB (0.0-1.0)
            camera_pos: Posição da câmera
        Returns:
            Cor RGB final (0-255)
        """
        # Normaliza o vetor normal
        normal = np.array(normal, dtype=np.float32)
        norm_magnitude = np.linalg.norm(normal)
        if norm_magnitude > 0:
            normal = normal / norm_magnitude

        # Direção da luz
        light_dir = light.get_direction_to(point)

        # Vetor de visão (da superfície para a câmera)
        point = np.array(point, dtype=np.float32)
        camera_pos = np.array(camera_pos, dtype=np.float32)
        view_dir = camera_pos - point
        view_norm = np.linalg.norm(view_dir)
        if view_norm > 0:
            view_dir = view_dir / view_norm

        # Componente ambiente
        ambient_component = self.ambient * np.array(material_color, dtype=np.float32)

        # Componente difusa
        n_dot_l = max(0.0, np.dot(normal, light_dir))
        diffuse_component = (
            self.diffuse *
            light.intensity *
            n_dot_l *
            np.array(material_color, dtype=np.float32) *
            light.color
        )

        # Componente especular
        # Vetor de reflexão: R = 2(N · L)N - L
        reflect_dir = 2.0 * n_dot_l * normal - light_dir
        reflect_norm = np.linalg.norm(reflect_dir)
        if reflect_norm > 0:
            reflect_dir = reflect_dir / reflect_norm

        r_dot_v = max(0.0, np.dot(reflect_dir, view_dir))
        specular_component = (
            self.specular *
            light.intensity *
            (r_dot_v ** self.shininess) *
            light.color
        )

        # Cor final
        final_color = ambient_component + diffuse_component + specular_component

        # Clamping e conversão para RGB
        final_color = np.clip(final_color, 0.0, 1.0)
        return tuple((final_color * 255).astype(int))


class GouraudShading:
    """
    Modelo de iluminação GOURAUD

    Similar ao Phong, mas calcula iluminação nos vértices e interpola
    as cores entre eles (mais eficiente que Phong).

    Usa o mesmo modelo de iluminação que Phong, mas aplicado nos vértices.
    Intensidade = Ia + Id * (N · L) + Is * (R · V)^n
    """

    def __init__(self, ambient=0.2, diffuse=0.6, specular=0.4, shininess=16):
        """
        Inicializa o modelo Gouraud
        Args:
            ambient: Intensidade da luz ambiente
            diffuse: Intensidade da componente difusa
            specular: Intensidade da componente especular
            shininess: Coeficiente de brilho
        """
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def calculate_vertex_color(self, vertex, normal, light, material_color, camera_pos):
        """
        Calcula a cor de um vértice usando iluminação Gouraud
        (mesmo cálculo que Phong, mas nos vértices)
        Args:
            vertex: Posição do vértice 3D
            normal: Vetor normal no vértice
            light: Objeto Light
            material_color: Cor do material RGB (0.0-1.0)
            camera_pos: Posição da câmera
        Returns:
            Cor RGB final (0.0-1.0) para interpolação
        """
        # Normaliza o vetor normal
        normal = np.array(normal, dtype=np.float32)
        norm_magnitude = np.linalg.norm(normal)
        if norm_magnitude > 0:
            normal = normal / norm_magnitude

        # Direção da luz
        light_dir = light.get_direction_to(vertex)

        # Vetor de visão
        vertex = np.array(vertex, dtype=np.float32)
        camera_pos = np.array(camera_pos, dtype=np.float32)
        view_dir = camera_pos - vertex
        view_norm = np.linalg.norm(view_dir)
        if view_norm > 0:
            view_dir = view_dir / view_norm

        # Componente ambiente
        ambient_component = self.ambient * np.array(material_color, dtype=np.float32)

        # Componente difusa
        n_dot_l = max(0.0, np.dot(normal, light_dir))
        diffuse_component = (
            self.diffuse *
            light.intensity *
            n_dot_l *
            np.array(material_color, dtype=np.float32) *
            light.color
        )

        # Componente especular
        reflect_dir = 2.0 * n_dot_l * normal - light_dir
        reflect_norm = np.linalg.norm(reflect_dir)
        if reflect_norm > 0:
            reflect_dir = reflect_dir / reflect_norm

        r_dot_v = max(0.0, np.dot(reflect_dir, view_dir))
        specular_component = (
            self.specular *
            light.intensity *
            (r_dot_v ** self.shininess) *
            light.color
        )

        # Cor final (mantém em 0.0-1.0 para interpolação posterior)
        final_color = ambient_component + diffuse_component + specular_component
        final_color = np.clip(final_color, 0.0, 1.0)

        return final_color

    def calculate_color(self, point, normal, light, material_color, camera_pos):
        """
        Calcula cor (mesmo que nos vértices, para compatibilidade)
        Args:
            point: Posição do ponto 3D
            normal: Vetor normal da superfície
            light: Objeto Light
            material_color: Cor do material RGB (0.0-1.0)
            camera_pos: Posição da câmera
        Returns:
            Cor RGB final (0-255)
        """
        color = self.calculate_vertex_color(point, normal, light, material_color, camera_pos)
        return tuple((color * 255).astype(int))

    @staticmethod
    def interpolate_colors(color1, color2, color3, w1, w2, w3):
        """
        Interpola cores dos vértices usando coordenadas baricêntricas
        Args:
            color1, color2, color3: Cores RGB dos vértices (0.0-1.0)
            w1, w2, w3: Pesos baricêntricos
        Returns:
            Cor interpolada RGB (0-255)
        """
        color1 = np.array(color1, dtype=np.float32)
        color2 = np.array(color2, dtype=np.float32)
        color3 = np.array(color3, dtype=np.float32)

        interpolated = w1 * color1 + w2 * color2 + w3 * color3
        interpolated = np.clip(interpolated, 0.0, 1.0)

        return tuple((interpolated * 255).astype(int))


def create_shading_model(model_type, **kwargs):
    """
    Factory function para criar modelos de iluminação
    Args:
        model_type: 'phong', 'lambertian' ou 'gouraud'
        **kwargs: Parâmetros específicos do modelo
    Returns:
        Instância do modelo de iluminação
    """
    model_type = model_type.lower()

    if model_type == 'phong':
        return PhongShading(**kwargs)
    elif model_type == 'lambertian':
        return LambertianShading(**kwargs)
    elif model_type == 'gouraud':
        return GouraudShading(**kwargs)
    else:
        raise ValueError(f"Modelo de iluminação '{model_type}' não reconhecido")
