"""
Classe para operações com matrizes 4x4
Implementa álgebra linear para transformações homogêneas 3D
"""

import numpy as np
import math

try:
    from core.exceptions import SingularMatrixException
    from core.logger import get_logger
except ImportError:
    from ..core.exceptions import SingularMatrixException
    from ..core.logger import get_logger

logger = get_logger(__name__)


class Matrix4x4:
    """Classe para representar e manipular matrizes 4x4"""

    def __init__(self, data=None):
        """
        Inicializa uma matriz 4x4
        Args:
            data: Matriz numpy 4x4 ou None para matriz identidade
        """
        if data is None:
            self.data = np.eye(4, dtype=np.float32)
        else:
            self.data = np.array(data, dtype=np.float32)

    @staticmethod
    def identity():
        """Retorna matriz identidade"""
        return Matrix4x4()

    @staticmethod
    def translation(tx, ty, tz):
        """
        Cria matriz de TRANSLAÇÃO
        Move um ponto no espaço 3D
        """
        matrix = np.eye(4, dtype=np.float32)
        matrix[0, 3] = tx
        matrix[1, 3] = ty
        matrix[2, 3] = tz
        return Matrix4x4(matrix)

    @staticmethod
    def rotation_x(angle):
        """
        Cria matriz de ROTAÇÃO em torno do eixo X
        Args:
            angle: Ângulo em radianos
        """
        c = math.cos(angle)
        s = math.sin(angle)
        matrix = np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def rotation_y(angle):
        """
        Cria matriz de ROTAÇÃO em torno do eixo Y
        Args:
            angle: Ângulo em radianos
        """
        c = math.cos(angle)
        s = math.sin(angle)
        matrix = np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def rotation_z(angle):
        """
        Cria matriz de ROTAÇÃO em torno do eixo Z
        Args:
            angle: Ângulo em radianos
        """
        c = math.cos(angle)
        s = math.sin(angle)
        matrix = np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def rotation(rx, ry, rz):
        """
        Cria matriz de ROTAÇÃO combinada (Euler angles)
        Aplica rotações em ordem: Z -> Y -> X
        """
        mat_x = Matrix4x4.rotation_x(rx)
        mat_y = Matrix4x4.rotation_y(ry)
        mat_z = Matrix4x4.rotation_z(rz)
        return mat_z.multiply(mat_y).multiply(mat_x)

    @staticmethod
    def scale(sx, sy, sz):
        """
        Cria matriz de ESCALA
        Aumenta ou diminui o tamanho do objeto
        """
        matrix = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def reflection_x():
        """
        Cria matriz de REFLEXÃO em relação ao plano YZ
        Espelha o objeto no eixo X
        """
        matrix = np.array([
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def reflection_y():
        """
        Cria matriz de REFLEXÃO em relação ao plano XZ
        Espelha o objeto no eixo Y
        """
        matrix = np.array([
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def reflection_z():
        """
        Cria matriz de REFLEXÃO em relação ao plano XY
        Espelha o objeto no eixo Z
        """
        matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def shear_xy(shx, shy):
        """
        Cria matriz de DISTORÇÃO (Shear) no plano XY
        Distorce o objeto ao longo dos eixos X e Y
        """
        matrix = np.array([
            [1, shx, 0, 0],
            [shy, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def shear_xz(shx, shz):
        """
        Cria matriz de DISTORÇÃO (Shear) no plano XZ
        """
        matrix = np.array([
            [1, 0, shx, 0],
            [0, 1, 0, 0],
            [shz, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def shear_yz(shy, shz):
        """
        Cria matriz de DISTORÇÃO (Shear) no plano YZ
        """
        matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, shy, 0],
            [0, shz, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def perspective(fov, aspect, near, far):
        """
        Cria matriz de projeção perspectiva
        Args:
            fov: Campo de visão em graus
            aspect: Razão de aspecto (largura/altura)
            near: Plano próximo
            far: Plano distante
        """
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        matrix = np.array([
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)
        return Matrix4x4(matrix)

    @staticmethod
    def look_at(eye, target, up):
        """
        Cria matriz de visualização (câmera)
        Args:
            eye: Posição da câmera
            target: Ponto alvo
            up: Vetor "para cima"
        """
        eye = np.array(eye, dtype=np.float32)
        target = np.array(target, dtype=np.float32)
        up = np.array(up, dtype=np.float32)

        # Calcula eixos da câmera
        z_axis = eye - target
        z_axis = z_axis / np.linalg.norm(z_axis)

        x_axis = np.cross(up, z_axis)
        x_axis = x_axis / np.linalg.norm(x_axis)

        y_axis = np.cross(z_axis, x_axis)

        # Cria matriz de visualização
        matrix = np.array([
            [x_axis[0], x_axis[1], x_axis[2], -np.dot(x_axis, eye)],
            [y_axis[0], y_axis[1], y_axis[2], -np.dot(y_axis, eye)],
            [z_axis[0], z_axis[1], z_axis[2], -np.dot(z_axis, eye)],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        return Matrix4x4(matrix)

    def multiply(self, other):
        """Multiplica esta matriz por outra"""
        result_data = np.dot(self.data, other.data)
        return Matrix4x4(result_data)

    def transform_point(self, point):
        """
        Transforma um ponto 3D usando esta matriz
        Args:
            point: Tupla ou lista (x, y, z)
        Returns:
            Ponto transformado (x, y, z)
        """
        # Converte para coordenadas homogêneas
        p = np.array([point[0], point[1], point[2], 1.0], dtype=np.float32)

        # Aplica transformação
        transformed = np.dot(self.data, p)

        # Normaliza coordenadas homogêneas
        if transformed[3] != 0:
            transformed = transformed / transformed[3]

        return tuple(transformed[:3])

    def transform_vector(self, vector):
        """
        Transforma um vetor 3D (sem translação)
        Args:
            vector: Tupla ou lista (x, y, z)
        Returns:
            Vetor transformado (x, y, z)
        """
        # Usa w=0 para vetores (não afetados por translação)
        v = np.array([vector[0], vector[1], vector[2], 0.0], dtype=np.float32)

        # Aplica transformação
        transformed = np.dot(self.data, v)

        return tuple(transformed[:3])

    def inverse(self):
        """
        Retorna a matriz inversa

        Raises:
            SingularMatrixException: Se a matriz for singular (determinante ~= 0)
        """
        det = np.linalg.det(self.data)
        if abs(det) < 1e-10:
            logger.error(f"Tentativa de inverter matriz singular (det={det})")
            raise SingularMatrixException(
                f"Não é possível inverter matriz com determinante próximo de zero: {det}"
            )

        try:
            inv_data = np.linalg.inv(self.data)
            return Matrix4x4(inv_data)
        except np.linalg.LinAlgError as e:
            logger.error(f"Erro ao inverter matriz: {e}")
            raise SingularMatrixException(f"Erro ao calcular inversa da matriz: {e}") from e

    def transpose(self):
        """Retorna a matriz transposta"""
        trans_data = self.data.T
        return Matrix4x4(trans_data)

    def __str__(self):
        """Representação em string da matriz"""
        return str(self.data)
