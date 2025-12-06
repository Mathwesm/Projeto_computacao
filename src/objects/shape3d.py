"""
Classe base para objetos 3D
"""

import numpy as np
from core.logger import get_logger
from core.exceptions import SingularMatrixException

try:
    from ..transformations.geometric import GeometricTransformations
except ImportError:
    from transformations.geometric import GeometricTransformations

logger = get_logger(__name__)


class Shape3D:
    """Classe base para representar objetos 3D"""

    def __init__(self, vertices, faces, color=(1.0, 0.5, 0.0)):
        """
        Inicializa um objeto 3D
        Args:
            vertices: Lista de vértices [(x, y, z), ...]
            faces: Lista de faces (cada face é lista de índices de vértices)
            color: Cor do material RGB (0.0-1.0)
        """
        self.original_vertices = np.array(vertices, dtype=np.float32)
        self.vertices = self.original_vertices.copy()
        self.faces = faces
        self.color = color

        # Transformações acumuladas
        self.transform = GeometricTransformations()

        # Calcula normais
        self.normals = self._calculate_normals()
        # Guarda normais originais para otimização
        self.original_normals = np.array(self.normals, dtype=np.float32)

        # Propriedades do objeto
        self.name = "Shape3D"
        self.visible = True

    def _calculate_normals(self):
        """Calcula vetores normais para cada face"""
        normals = []

        for face in self.faces:
            if len(face) < 3:
                normals.append((0, 1, 0))
                continue

            # Pega três vértices da face
            v0 = self.vertices[face[0]]
            v1 = self.vertices[face[1]]
            v2 = self.vertices[face[2]]

            # Calcula vetores das arestas
            edge1 = v1 - v0
            edge2 = v2 - v0

            # Produto vetorial para obter normal
            normal = np.cross(edge1, edge2)
            norm_magnitude = np.linalg.norm(normal)

            if norm_magnitude > 0:
                normal = normal / norm_magnitude

            normals.append(tuple(normal))

        return normals

    def apply_transformations(self):
        """
        Aplica as transformações acumuladas aos vértices e normais
        Otimizado: transforma normais diretamente ao invés de recalcular
        """
        # Transforma vértices usando multiplicação matricial (mais rápido)
        transform_matrix = self.transform.matrix.data

        # Adiciona coordenada homogênea (w=1) aos vértices
        ones = np.ones((len(self.original_vertices), 1), dtype=np.float32)
        vertices_homogeneous = np.hstack([self.original_vertices, ones])

        # Aplica transformação (multiplicação matricial vetorizada)
        transformed = (transform_matrix @ vertices_homogeneous.T).T
        self.vertices = transformed[:, :3]  # Remove coordenada homogênea

        # Transforma normais usando matriz normal (inverse-transpose)
        # Para normais, usamos apenas a parte 3x3 da matriz
        try:
            # Matriz normal = inversa transposta da parte rotação/escala
            rotation_scale = transform_matrix[:3, :3]
            normal_matrix = np.linalg.inv(rotation_scale).T

            # Aplica transformação às normais (mais rápido que recalcular)
            transformed_normals = (normal_matrix @ self.original_normals.T).T

            # Normaliza os vetores
            norms = np.linalg.norm(transformed_normals, axis=1, keepdims=True)
            norms[norms == 0] = 1  # Evita divisão por zero
            self.normals = (transformed_normals / norms).tolist()

            logger.debug(f"Transformações aplicadas com otimização (vetorizado)")

        except np.linalg.LinAlgError:
            # Se a matriz for singular, recalcula normais do zero
            logger.warning("Matriz singular detectada, recalculando normais do zero")
            self.normals = self._calculate_normals()

    def reset_transformations(self):
        """Reseta todas as transformações"""
        self.transform.reset()
        self.vertices = self.original_vertices.copy()
        self.normals = self._calculate_normals()

    # ==================== MÉTODOS DE TRANSFORMAÇÃO ====================

    def translate(self, tx, ty, tz):
        """Aplica translação"""
        self.transform.translate(tx, ty, tz)
        self.apply_transformations()
        return self

    def rotate_x(self, angle):
        """Aplica rotação em X"""
        self.transform.rotate_x(angle)
        self.apply_transformations()
        return self

    def rotate_y(self, angle):
        """Aplica rotação em Y"""
        self.transform.rotate_y(angle)
        self.apply_transformations()
        return self

    def rotate_z(self, angle):
        """Aplica rotação em Z"""
        self.transform.rotate_z(angle)
        self.apply_transformations()
        return self

    def rotate(self, rx, ry, rz):
        """Aplica rotação combinada"""
        self.transform.rotate(rx, ry, rz)
        self.apply_transformations()
        return self

    def scale(self, sx, sy, sz):
        """Aplica escala"""
        self.transform.scale(sx, sy, sz)
        self.apply_transformations()
        return self

    def scale_uniform(self, s):
        """Aplica escala uniforme"""
        self.transform.scale_uniform(s)
        self.apply_transformations()
        return self

    def reflect_x(self):
        """Aplica reflexão em X"""
        self.transform.reflect_x()
        self.apply_transformations()
        return self

    def reflect_y(self):
        """Aplica reflexão em Y"""
        self.transform.reflect_y()
        self.apply_transformations()
        return self

    def reflect_z(self):
        """Aplica reflexão em Z"""
        self.transform.reflect_z()
        self.apply_transformations()
        return self

    def shear_xy(self, shx, shy):
        """Aplica distorção XY"""
        self.transform.shear_xy(shx, shy)
        self.apply_transformations()
        return self

    def shear_xz(self, shx, shz):
        """Aplica distorção XZ"""
        self.transform.shear_xz(shx, shz)
        self.apply_transformations()
        return self

    def shear_yz(self, shy, shz):
        """Aplica distorção YZ"""
        self.transform.shear_yz(shy, shz)
        self.apply_transformations()
        return self

    # ==================== MÉTODOS AUXILIARES ====================

    def get_vertices(self):
        """Retorna os vértices transformados"""
        return self.vertices.tolist()

    def get_faces(self):
        """Retorna as faces"""
        return self.faces

    def get_normals(self):
        """Retorna as normais"""
        return self.normals

    def get_color(self):
        """Retorna a cor do material"""
        return self.color

    def set_color(self, color):
        """Define a cor do material"""
        self.color = color

    def get_centroid(self):
        """Retorna o centroide do objeto"""
        return tuple(np.mean(self.vertices, axis=0))

    def get_bounding_box(self):
        """Retorna a bounding box (min, max)"""
        min_point = np.min(self.vertices, axis=0)
        max_point = np.max(self.vertices, axis=0)
        return (tuple(min_point), tuple(max_point))

    def copy(self):
        """Cria uma cópia do objeto"""
        new_shape = Shape3D(
            self.original_vertices.tolist(),
            self.faces.copy(),
            self.color
        )
        new_shape.transform = self.transform.copy()
        new_shape.apply_transformations()
        return new_shape
