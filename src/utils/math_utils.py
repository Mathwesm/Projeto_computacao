"""
Utilitários matemáticos
Funções auxiliares para cálculos matemáticos comuns
"""

import math
from typing import List, Tuple, Union
import numpy as np


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Limita um valor entre um mínimo e máximo

    Args:
        value: Valor a ser limitado
        min_val: Valor mínimo
        max_val: Valor máximo

    Returns:
        Valor limitado entre min_val e max_val
    """
    return max(min_val, min(max_val, value))


def lerp(start: float, end: float, t: float) -> float:
    """
    Interpolação linear entre dois valores

    Args:
        start: Valor inicial
        end: Valor final
        t: Fator de interpolação (0.0 a 1.0)

    Returns:
        Valor interpolado
    """
    return start + (end - start) * t


def map_range(value: float, from_min: float, from_max: float,
              to_min: float, to_max: float) -> float:
    """
    Mapeia um valor de um intervalo para outro

    Args:
        value: Valor a ser mapeado
        from_min: Mínimo do intervalo de origem
        from_max: Máximo do intervalo de origem
        to_min: Mínimo do intervalo de destino
        to_max: Máximo do intervalo de destino

    Returns:
        Valor mapeado
    """
    return to_min + (value - from_min) * (to_max - to_min) / (from_max - from_min)


def normalize_vector(vector: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    Normaliza um vetor (torna seu comprimento igual a 1)

    Args:
        vector: Vetor a ser normalizado

    Returns:
        Vetor normalizado
    """
    v = np.array(vector, dtype=float)
    magnitude = np.linalg.norm(v)

    if magnitude < 1e-10:
        return v

    return v / magnitude


def distance_3d(p1: Union[List[float], np.ndarray],
                p2: Union[List[float], np.ndarray]) -> float:
    """
    Calcula a distância euclidiana entre dois pontos 3D

    Args:
        p1: Primeiro ponto [x, y, z]
        p2: Segundo ponto [x, y, z]

    Returns:
        Distância entre os pontos
    """
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    return np.linalg.norm(p2 - p1)


def angle_between_vectors(v1: Union[List[float], np.ndarray],
                          v2: Union[List[float], np.ndarray]) -> float:
    """
    Calcula o ângulo entre dois vetores (em radianos)

    Args:
        v1: Primeiro vetor
        v2: Segundo vetor

    Returns:
        Ângulo em radianos
    """
    v1_norm = normalize_vector(v1)
    v2_norm = normalize_vector(v2)

    dot_product = np.dot(v1_norm, v2_norm)
    dot_product = clamp(dot_product, -1.0, 1.0)

    return math.acos(dot_product)


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    """
    Interpolação suave entre dois valores (função smoothstep)

    Args:
        edge0: Limite inferior
        edge1: Limite superior
        x: Valor a interpolar

    Returns:
        Valor interpolado suavemente
    """
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def ease_in_out(t: float) -> float:
    """
    Função de easing in-out para animações suaves

    Args:
        t: Valor entre 0 e 1

    Returns:
        Valor com easing aplicado
    """
    t = clamp(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def cross_product(v1: Union[List[float], np.ndarray],
                  v2: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    Calcula o produto vetorial entre dois vetores

    Args:
        v1: Primeiro vetor
        v2: Segundo vetor

    Returns:
        Produto vetorial
    """
    return np.cross(v1, v2)


def dot_product(v1: Union[List[float], np.ndarray],
                v2: Union[List[float], np.ndarray]) -> float:
    """
    Calcula o produto escalar entre dois vetores

    Args:
        v1: Primeiro vetor
        v2: Segundo vetor

    Returns:
        Produto escalar
    """
    return np.dot(v1, v2)


def reflect_vector(incident: Union[List[float], np.ndarray],
                   normal: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    Calcula o vetor refletido dado um vetor incidente e uma normal

    Args:
        incident: Vetor incidente
        normal: Vetor normal

    Returns:
        Vetor refletido
    """
    incident = np.array(incident, dtype=float)
    normal = normalize_vector(normal)

    return incident - 2 * np.dot(incident, normal) * normal
