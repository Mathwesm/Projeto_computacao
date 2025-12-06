"""
Validadores
Funções para validação de dados de entrada
"""

from typing import Tuple, List, Union, Any
import numpy as np

try:
    from ..core.exceptions import InvalidMatrixException, InvalidVertexDataException
except ImportError:
    from core.exceptions import InvalidMatrixException, InvalidVertexDataException


def validate_color(color: Any) -> bool:
    """
    Valida se uma cor está no formato correto

    Args:
        color: Valor a ser validado

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(color, (tuple, list)):
        return False

    if len(color) not in [3, 4]:  # RGB ou RGBA
        return False

    return all(isinstance(c, (int, float)) and 0 <= c <= 255 for c in color)


def validate_vector3(vector: Any) -> bool:
    """
    Valida se um vetor 3D está no formato correto

    Args:
        vector: Valor a ser validado

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(vector, (list, tuple, np.ndarray)):
        return False

    if len(vector) != 3:
        return False

    return all(isinstance(v, (int, float)) for v in vector)


def validate_matrix(matrix: Any, expected_shape: Tuple[int, int] = (4, 4)) -> bool:
    """
    Valida se uma matriz está no formato correto

    Args:
        matrix: Valor a ser validado
        expected_shape: Forma esperada da matriz

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(matrix, np.ndarray):
        try:
            matrix = np.array(matrix)
        except (ValueError, TypeError):
            return False

    if matrix.shape != expected_shape:
        return False

    # Verifica se todos os valores são numéricos
    return np.issubdtype(matrix.dtype, np.number)


def validate_vertices(vertices: Any) -> bool:
    """
    Valida lista de vértices

    Args:
        vertices: Lista de vértices a validar

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(vertices, (list, np.ndarray)):
        return False

    if len(vertices) == 0:
        return False

    # Verifica se cada vértice é um vetor 3D válido
    return all(validate_vector3(v) for v in vertices)


def validate_faces(faces: Any, num_vertices: int) -> bool:
    """
    Valida lista de faces

    Args:
        faces: Lista de faces a validar
        num_vertices: Número de vértices disponíveis

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(faces, (list, tuple)):
        return False

    if len(faces) == 0:
        return False

    for face in faces:
        if not isinstance(face, (list, tuple)):
            return False

        # Face deve ter pelo menos 3 vértices
        if len(face) < 3:
            return False

        # Todos os índices devem ser válidos
        if not all(isinstance(idx, int) and 0 <= idx < num_vertices for idx in face):
            return False

    return True


def validate_normal(normal: Any) -> bool:
    """
    Valida se uma normal está no formato correto

    Args:
        normal: Vetor normal a validar

    Returns:
        True se válido, False caso contrário
    """
    if not validate_vector3(normal):
        return False

    # Verifica se a normal não é zero
    magnitude = np.linalg.norm(normal)
    return magnitude > 1e-6


def validate_range(value: Union[int, float],
                  min_val: Union[int, float],
                  max_val: Union[int, float]) -> bool:
    """
    Valida se um valor está dentro de um intervalo

    Args:
        value: Valor a validar
        min_val: Valor mínimo
        max_val: Valor máximo

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(value, (int, float)):
        return False

    return min_val <= value <= max_val


def validate_positive(value: Union[int, float]) -> bool:
    """
    Valida se um valor é positivo

    Args:
        value: Valor a validar

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(value, (int, float)):
        return False

    return value > 0


def validate_non_negative(value: Union[int, float]) -> bool:
    """
    Valida se um valor não é negativo

    Args:
        value: Valor a validar

    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(value, (int, float)):
        return False

    return value >= 0


def require_valid_matrix(matrix: Any, name: str = "Matrix") -> np.ndarray:
    """
    Valida matriz e levanta exceção se inválida

    Args:
        matrix: Matriz a validar
        name: Nome da matriz para mensagem de erro

    Returns:
        Matriz validada como numpy array

    Raises:
        InvalidMatrixException: Se a matriz for inválida
    """
    if not validate_matrix(matrix):
        raise InvalidMatrixException(f"{name} inválida")

    return np.array(matrix)


def require_valid_vertices(vertices: Any) -> List:
    """
    Valida vértices e levanta exceção se inválidos

    Args:
        vertices: Vértices a validar

    Returns:
        Lista de vértices validados

    Raises:
        InvalidVertexDataException: Se os vértices forem inválidos
    """
    if not validate_vertices(vertices):
        raise InvalidVertexDataException("Lista de vértices inválida")

    return list(vertices)
