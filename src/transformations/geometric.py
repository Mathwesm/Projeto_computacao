"""
Classe para aplicar transformações geométricas em objetos 3D
Implementa: Translação, Rotação, Escala, Reflexão e Distorção
"""

from .matrix import Matrix4x4
import math
import numpy as np
from typing import Tuple, List, Union

try:
    from core.exceptions import TransformationException
    from core.logger import get_logger
except ImportError:
    from ..core.exceptions import TransformationException
    from ..core.logger import get_logger

logger = get_logger(__name__)


class GeometricTransformations:
    """Classe para gerenciar e aplicar transformações geométricas"""

    def __init__(self) -> None:
        """Inicializa com matriz identidade"""
        self.matrix: Matrix4x4 = Matrix4x4.identity()
        self.history: List[Tuple] = []  # Histórico de transformações aplicadas

    def reset(self) -> None:
        """Reseta para matriz identidade"""
        self.matrix = Matrix4x4.identity()
        self.history = []

    # ==================== TRANSLAÇÃO ====================
    def translate(self, tx: float, ty: float, tz: float) -> 'GeometricTransformations':
        """
        Aplica TRANSLAÇÃO (movimento)
        Move o objeto no espaço 3D
        Args:
            tx, ty, tz: Deslocamentos em cada eixo

        Raises:
            TransformationException: Se algum valor de translação for inválido
        """
        # Validação de inputs
        for name, value in [('tx', tx), ('ty', ty), ('tz', tz)]:
            if not np.isfinite(value):
                raise TransformationException(
                    f"Valor de translação {name} deve ser finito, recebido: {value}"
                )

        trans_matrix = Matrix4x4.translation(tx, ty, tz)
        self.matrix = self.matrix.multiply(trans_matrix)
        self.history.append(('translate', tx, ty, tz))
        logger.debug(f"Translação aplicada: tx={tx}, ty={ty}, tz={tz}")
        return self

    # ==================== ROTAÇÃO ====================
    def rotate_x(self, angle_degrees: float) -> 'GeometricTransformations':
        """
        Aplica ROTAÇÃO em torno do eixo X
        Args:
            angle_degrees: Ângulo em graus

        Raises:
            TransformationException: Se o ângulo for inválido
        """
        if not np.isfinite(angle_degrees):
            raise TransformationException(
                f"Ângulo de rotação deve ser finito, recebido: {angle_degrees}"
            )

        angle_rad = math.radians(angle_degrees)
        rot_matrix = Matrix4x4.rotation_x(angle_rad)
        self.matrix = self.matrix.multiply(rot_matrix)
        self.history.append(('rotate_x', angle_degrees))
        logger.debug(f"Rotação X aplicada: {angle_degrees}°")
        return self

    def rotate_y(self, angle_degrees):
        """
        Aplica ROTAÇÃO em torno do eixo Y
        Args:
            angle_degrees: Ângulo em graus
        """
        angle_rad = math.radians(angle_degrees)
        rot_matrix = Matrix4x4.rotation_y(angle_rad)
        self.matrix = self.matrix.multiply(rot_matrix)
        self.history.append(('rotate_y', angle_degrees))
        return self

    def rotate_z(self, angle_degrees):
        """
        Aplica ROTAÇÃO em torno do eixo Z
        Args:
            angle_degrees: Ângulo em graus
        """
        angle_rad = math.radians(angle_degrees)
        rot_matrix = Matrix4x4.rotation_z(angle_rad)
        self.matrix = self.matrix.multiply(rot_matrix)
        self.history.append(('rotate_z', angle_degrees))
        return self

    def rotate(self, rx_degrees, ry_degrees, rz_degrees):
        """
        Aplica ROTAÇÃO combinada (Euler angles)
        Args:
            rx_degrees, ry_degrees, rz_degrees: Ângulos em graus
        """
        rx_rad = math.radians(rx_degrees)
        ry_rad = math.radians(ry_degrees)
        rz_rad = math.radians(rz_degrees)
        rot_matrix = Matrix4x4.rotation(rx_rad, ry_rad, rz_rad)
        self.matrix = self.matrix.multiply(rot_matrix)
        self.history.append(('rotate', rx_degrees, ry_degrees, rz_degrees))
        return self

    # ==================== ESCALA ====================
    def scale(self, sx: float, sy: float, sz: float) -> 'GeometricTransformations':
        """
        Aplica ESCALA (redimensionamento)
        Aumenta ou diminui o tamanho do objeto
        Args:
            sx, sy, sz: Fatores de escala para cada eixo

        Raises:
            TransformationException: Se algum fator de escala for inválido
        """
        # Validação de inputs
        for i, (name, value) in enumerate([('sx', sx), ('sy', sy), ('sz', sz)]):
            if not np.isfinite(value):
                raise TransformationException(
                    f"Fator de escala {name} deve ser finito, recebido: {value}"
                )
            if abs(value) < 1e-10:
                logger.warning(f"Fator de escala {name} muito próximo de zero: {value}")
                raise TransformationException(
                    f"Fator de escala {name} não pode ser zero ou muito próximo de zero"
                )

        scale_matrix = Matrix4x4.scale(sx, sy, sz)
        self.matrix = self.matrix.multiply(scale_matrix)
        self.history.append(('scale', sx, sy, sz))
        logger.debug(f"Escala aplicada: sx={sx}, sy={sy}, sz={sz}")
        return self

    def scale_uniform(self, s):
        """
        Aplica ESCALA uniforme (mantém proporções)
        Args:
            s: Fator de escala igual para todos os eixos
        """
        return self.scale(s, s, s)

    # ==================== REFLEXÃO ====================
    def reflect_x(self):
        """
        Aplica REFLEXÃO em relação ao plano YZ
        Espelha o objeto no eixo X
        """
        reflect_matrix = Matrix4x4.reflection_x()
        self.matrix = self.matrix.multiply(reflect_matrix)
        self.history.append(('reflect_x',))
        return self

    def reflect_y(self):
        """
        Aplica REFLEXÃO em relação ao plano XZ
        Espelha o objeto no eixo Y
        """
        reflect_matrix = Matrix4x4.reflection_y()
        self.matrix = self.matrix.multiply(reflect_matrix)
        self.history.append(('reflect_y',))
        return self

    def reflect_z(self):
        """
        Aplica REFLEXÃO em relação ao plano XY
        Espelha o objeto no eixo Z
        """
        reflect_matrix = Matrix4x4.reflection_z()
        self.matrix = self.matrix.multiply(reflect_matrix)
        self.history.append(('reflect_z',))
        return self

    # ==================== DISTORÇÃO (SHEAR) ====================
    def shear_xy(self, shx, shy):
        """
        Aplica DISTORÇÃO no plano XY
        Distorce o objeto ao longo dos eixos X e Y
        Args:
            shx: Fator de distorção em X
            shy: Fator de distorção em Y
        """
        shear_matrix = Matrix4x4.shear_xy(shx, shy)
        self.matrix = self.matrix.multiply(shear_matrix)
        self.history.append(('shear_xy', shx, shy))
        return self

    def shear_xz(self, shx, shz):
        """
        Aplica DISTORÇÃO no plano XZ
        Args:
            shx: Fator de distorção em X
            shz: Fator de distorção em Z
        """
        shear_matrix = Matrix4x4.shear_xz(shx, shz)
        self.matrix = self.matrix.multiply(shear_matrix)
        self.history.append(('shear_xz', shx, shz))
        return self

    def shear_yz(self, shy, shz):
        """
        Aplica DISTORÇÃO no plano YZ
        Args:
            shy: Fator de distorção em Y
            shz: Fator de distorção em Z
        """
        shear_matrix = Matrix4x4.shear_yz(shy, shz)
        self.matrix = self.matrix.multiply(shear_matrix)
        self.history.append(('shear_yz', shy, shz))
        return self

    # ==================== APLICAÇÃO ====================
    def apply_to_point(self, point):
        """
        Aplica todas as transformações acumuladas a um ponto
        Args:
            point: Tupla (x, y, z)
        Returns:
            Ponto transformado (x, y, z)
        """
        return self.matrix.transform_point(point)

    def apply_to_vector(self, vector):
        """
        Aplica transformações a um vetor (sem translação)
        Args:
            vector: Tupla (x, y, z)
        Returns:
            Vetor transformado (x, y, z)
        """
        return self.matrix.transform_vector(vector)

    def apply_to_points(self, points):
        """
        Aplica transformações a uma lista de pontos
        Args:
            points: Lista de tuplas (x, y, z)
        Returns:
            Lista de pontos transformados
        """
        return [self.apply_to_point(p) for p in points]

    def get_matrix(self):
        """Retorna a matriz de transformação atual"""
        return self.matrix

    def set_matrix(self, matrix):
        """Define a matriz de transformação"""
        self.matrix = matrix
        return self

    def copy(self):
        """Cria uma cópia desta transformação"""
        new_transform = GeometricTransformations()
        new_transform.matrix = Matrix4x4(self.matrix.data.copy())
        new_transform.history = self.history.copy()
        return new_transform

    def get_history(self):
        """Retorna o histórico de transformações aplicadas"""
        return self.history.copy()

    def __str__(self):
        """Representação em string"""
        history_str = "\n".join([f"  - {h[0]}: {h[1:]}" for h in self.history])
        return f"GeometricTransformations:\n{history_str}"
