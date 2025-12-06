"""
Exceções personalizadas do projeto
Define exceções específicas para diferentes módulos do jogo
"""


class GameException(Exception):
    """Exceção base para o jogo"""
    pass


class RenderException(GameException):
    """Exceção relacionada à renderização"""
    pass


class TransformationException(GameException):
    """Exceção relacionada a transformações geométricas"""
    pass


class ShaderException(RenderException):
    """Exceção relacionada a shaders/iluminação"""
    pass


class CameraException(RenderException):
    """Exceção relacionada à câmera"""
    pass


class ObjectException(GameException):
    """Exceção relacionada a objetos 3D"""
    pass


class InvalidVertexDataException(ObjectException):
    """Exceção quando dados de vértices são inválidos"""
    pass


class InvalidMatrixException(TransformationException):
    """Exceção quando uma matriz é inválida"""
    pass


class PuzzleException(GameException):
    """Exceção relacionada a puzzles"""
    pass


class LevelException(GameException):
    """Exceção relacionada a níveis"""
    pass


class UIException(GameException):
    """Exceção relacionada à interface do usuário"""
    pass


class InputException(GameException):
    """Exceção relacionada a entrada do usuário"""
    pass


class ResourceNotFoundException(GameException):
    """Exceção quando um recurso não é encontrado"""
    def __init__(self, resource_type: str, resource_name: str):
        self.resource_type = resource_type
        self.resource_name = resource_name
        super().__init__(f"{resource_type} não encontrado: {resource_name}")


class ConfigurationException(GameException):
    """Exceção relacionada a configurações"""
    pass
