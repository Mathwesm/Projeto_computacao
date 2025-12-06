"""
Utilitários de cores
Funções para manipulação e conversão de cores
"""

from typing import Tuple, Union, List


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Converte cor RGB para hexadecimal

    Args:
        rgb: Tupla (R, G, B) com valores 0-255

    Returns:
        String hexadecimal no formato '#RRGGBB'
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Converte cor hexadecimal para RGB

    Args:
        hex_color: String hexadecimal '#RRGGBB' ou 'RRGGBB'

    Returns:
        Tupla (R, G, B) com valores 0-255
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def interpolate_color(color1: Tuple[int, int, int],
                      color2: Tuple[int, int, int],
                      t: float) -> Tuple[int, int, int]:
    """
    Interpola entre duas cores

    Args:
        color1: Cor inicial (R, G, B)
        color2: Cor final (R, G, B)
        t: Fator de interpolação (0.0 a 1.0)

    Returns:
        Cor interpolada
    """
    t = max(0.0, min(1.0, t))
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)


def darken_color(color: Tuple[int, int, int], factor: float = 0.7) -> Tuple[int, int, int]:
    """
    Escurece uma cor

    Args:
        color: Cor RGB
        factor: Fator de escurecimento (0.0 a 1.0, menor = mais escuro)

    Returns:
        Cor escurecida
    """
    factor = max(0.0, min(1.0, factor))
    return tuple(int(c * factor) for c in color)


def lighten_color(color: Tuple[int, int, int], factor: float = 1.3) -> Tuple[int, int, int]:
    """
    Clareia uma cor

    Args:
        color: Cor RGB
        factor: Fator de clareamento (maior que 1.0)

    Returns:
        Cor clareada
    """
    return tuple(min(255, int(c * factor)) for c in color)


def normalize_color(color: Union[Tuple[int, int, int], Tuple[float, float, float]],
                   to_range: str = 'float') -> Union[Tuple[float, float, float], Tuple[int, int, int]]:
    """
    Normaliza valores de cor entre diferentes intervalos

    Args:
        color: Cor a ser normalizada
        to_range: 'float' (0-1) ou 'int' (0-255)

    Returns:
        Cor normalizada
    """
    if to_range == 'float':
        if all(0 <= c <= 1 for c in color):
            return color
        return tuple(c / 255.0 for c in color)
    else:  # to_range == 'int'
        if all(0 <= c <= 255 for c in color):
            return color
        return tuple(int(c * 255) for c in color)


def blend_colors(color1: Tuple[int, int, int],
                color2: Tuple[int, int, int],
                mode: str = 'average') -> Tuple[int, int, int]:
    """
    Combina duas cores usando diferentes modos de blend

    Args:
        color1: Primeira cor
        color2: Segunda cor
        mode: Modo de blend ('average', 'multiply', 'screen', 'add')

    Returns:
        Cor resultante
    """
    if mode == 'average':
        return tuple((c1 + c2) // 2 for c1, c2 in zip(color1, color2))
    elif mode == 'multiply':
        return tuple(int((c1 * c2) / 255) for c1, c2 in zip(color1, color2))
    elif mode == 'screen':
        return tuple(255 - int(((255 - c1) * (255 - c2)) / 255) for c1, c2 in zip(color1, color2))
    elif mode == 'add':
        return tuple(min(255, c1 + c2) for c1, c2 in zip(color1, color2))
    else:
        return color1


def get_complementary_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Retorna a cor complementar

    Args:
        color: Cor RGB

    Returns:
        Cor complementar
    """
    return tuple(255 - c for c in color)


def color_to_grayscale(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Converte cor para escala de cinza

    Args:
        color: Cor RGB

    Returns:
        Cor em escala de cinza
    """
    gray = int(0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])
    return (gray, gray, gray)
