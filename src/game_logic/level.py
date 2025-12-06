"""
Sistema de níveis do jogo
"""

from .puzzle import Puzzle, PuzzleType

try:
    from ..objects.primitives import Cube, Pyramid, Sphere, Cylinder, Torus
except ImportError:
    from objects.primitives import Cube, Pyramid, Sphere, Cylinder, Torus


class Level:
    """Classe para representar um nível do jogo"""

    def __init__(self, level_id, name, description, difficulty=1):
        """
        Inicializa um nível
        Args:
            level_id: ID único do nível
            name: Nome do nível
            description: Descrição/história do nível
            difficulty: Dificuldade (1-5)
        """
        self.id = level_id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.completed = False

        # Puzzles do nível
        self.puzzles = []

        # Objetos 3D do nível
        self.shapes = []

        # Configurações visuais
        self.background_color = (20, 20, 40)
        self.required_shading_model = None

        # Objetivos do nível
        self.objectives = []
        self.objectives_completed = []

    def add_puzzle(self, puzzle):
        """Adiciona um puzzle ao nível"""
        self.puzzles.append(puzzle)

    def add_shape(self, shape):
        """Adiciona um objeto 3D ao nível"""
        self.shapes.append(shape)

    def add_objective(self, objective):
        """Adiciona um objetivo ao nível"""
        self.objectives.append(objective)

    def complete_objective(self, objective):
        """Marca um objetivo como completo"""
        if objective in self.objectives and objective not in self.objectives_completed:
            self.objectives_completed.append(objective)

    def is_completed(self):
        """Verifica se o nível está completo"""
        # Todos os puzzles resolvidos
        puzzles_solved = all(p.is_solved() for p in self.puzzles)

        # Todos os objetivos completos
        objectives_done = len(self.objectives_completed) == len(self.objectives)

        return puzzles_solved and objectives_done

    def get_progress(self):
        """Retorna progresso do nível (0.0-1.0)"""
        if len(self.puzzles) == 0 and len(self.objectives) == 0:
            return 1.0

        total_tasks = len(self.puzzles) + len(self.objectives)
        completed_tasks = sum(1 for p in self.puzzles if p.is_solved()) + len(self.objectives_completed)

        return completed_tasks / total_tasks if total_tasks > 0 else 0.0

    def reset(self):
        """Reseta o progresso do nível"""
        self.completed = False
        self.objectives_completed = []
        for puzzle in self.puzzles:
            puzzle.solved = False
            puzzle.attempts = 0


class LevelManager:
    """Gerenciador de níveis do jogo"""

    def __init__(self):
        """Inicializa o gerenciador de níveis"""
        self.levels = []
        self.current_level_index = 0
        self._create_levels()

    def _create_levels(self):
        """Cria todos os níveis do jogo"""

        # ==================== NÍVEL 1: Tutorial - Translação ====================
        level1 = Level(
            1,
            "Capítulo 1: O Despertar das Formas",
            "As formas geométricas perderam suas posições. "
            "Use TRANSLAÇÃO e ROTAÇÃO para posicionar o cubo corretamente!",
            difficulty=2
        )

        # Adiciona um cubo
        cube = Cube(size=1.5, color=(0.2, 0.6, 1.0))
        level1.add_shape(cube)

        # Puzzle de translação + rotação (mais complexo)
        puzzle1 = Puzzle(PuzzleType.SEQUENCE, difficulty=2)
        puzzle1.solution['sequence'] = [
            {'step': 1, 'type': 'translate', 'hint': 'Passo 1: Mova o cubo'},
            {'step': 2, 'type': 'rotate', 'hint': 'Passo 2: Rotacione o cubo'},
            {'step': 3, 'type': 'translate', 'hint': 'Passo 3: Ajuste a posição'}
        ]
        puzzle1.data['description'] = "Sequência: Translação → Rotação → Translação"
        puzzle1.data['required_actions'] = 3  # Precisa fazer 3 ações
        level1.add_puzzle(puzzle1)

        # Objetivos
        level1.add_objective("Aplicar translação ao cubo")
        level1.add_objective("Aplicar rotação ao cubo")
        level1.add_objective("Entender combinação de transformações")

        # Modelo de iluminação recomendado
        level1.required_shading_model = 'lambertian'

        self.levels.append(level1)

        # ==================== NÍVEL 2: Rotação ====================
        level2 = Level(
            2,
            "Capítulo 2: A Dança das Rotações",
            "As formas precisam girar! Use ROTAÇÃO e ESCALA para ajustar a pirâmide.",
            difficulty=2
        )

        pyramid = Pyramid(base_size=1.5, height=2.0, color=(1.0, 0.5, 0.0))
        level2.add_shape(pyramid)

        puzzle2 = Puzzle(PuzzleType.SEQUENCE, difficulty=2)
        puzzle2.solution['sequence'] = [
            {'step': 1, 'type': 'rotate', 'hint': 'Passo 1: Rotacione a pirâmide'},
            {'step': 2, 'type': 'scale', 'hint': 'Passo 2: Ajuste o tamanho'}
        ]
        puzzle2.data['description'] = "Sequência: Rotação → Escala"
        puzzle2.data['required_actions'] = 2
        level2.add_puzzle(puzzle2)

        level2.add_objective("Aplicar rotação")
        level2.add_objective("Aplicar escala")
        level2.required_shading_model = 'phong'

        self.levels.append(level2)

        # ==================== NÍVEL 3: Escala ====================
        level3 = Level(
            3,
            "Capítulo 3: O Poder do Tamanho",
            "Use TRANSLAÇÃO, ROTAÇÃO e ESCALA para posicionar a esfera!",
            difficulty=3
        )

        sphere = Sphere(radius=0.8, subdivisions=2, color=(0.0, 1.0, 0.5))
        level3.add_shape(sphere)

        puzzle3 = Puzzle(PuzzleType.SEQUENCE, difficulty=3)
        puzzle3.solution['sequence'] = [
            {'step': 1, 'type': 'scale', 'hint': 'Passo 1: Ajuste o tamanho'},
            {'step': 2, 'type': 'rotate', 'hint': 'Passo 2: Rotacione'},
            {'step': 3, 'type': 'translate', 'hint': 'Passo 3: Posicione'}
        ]
        puzzle3.data['description'] = "Sequência: Escala → Rotação → Translação"
        puzzle3.data['required_actions'] = 3
        level3.add_puzzle(puzzle3)

        level3.add_objective("Aplicar escala uniforme")
        level3.add_objective("Combinar 3 transformações")
        level3.add_objective("Entender proporções")
        level3.required_shading_model = 'gouraud'

        self.levels.append(level3)

        # ==================== NÍVEL 4: Reflexão ====================
        level4 = Level(
            4,
            "Capítulo 4: O Espelho Mágico",
            "Use REFLEXÃO para espelhar as formas e criar simetria!",
            difficulty=3
        )

        cylinder = Cylinder(radius=0.6, height=2.0, color=(1.0, 0.0, 1.0))
        level4.add_shape(cylinder)

        puzzle4 = Puzzle(PuzzleType.TRANSFORMATION, difficulty=3)
        puzzle4.solution['transforms'] = [
            {'type': 'reflect', 'axis': 'x'}
        ]
        puzzle4.data['description'] = "Espelhe o cilindro no eixo X"
        level4.add_puzzle(puzzle4)

        level4.add_objective("Aplicar reflexão")
        level4.add_objective("Criar simetria")
        level4.required_shading_model = 'phong'

        self.levels.append(level4)

        # ==================== NÍVEL 5: Distorção ====================
        level5 = Level(
            5,
            "Capítulo 5: A Distorção Dimensional",
            "Domine a DISTORÇÃO (Shear) para deformar as formas!",
            difficulty=3
        )

        torus = Torus(major_radius=1.0, minor_radius=0.3, color=(1.0, 1.0, 0.0))
        level5.add_shape(torus)

        puzzle5 = Puzzle(PuzzleType.TRANSFORMATION, difficulty=3)
        puzzle5.solution['transforms'] = [
            {'type': 'shear', 'plane': 'xy', 'factor': 0.3}
        ]
        puzzle5.data['description'] = "Distorça o torus no plano XY"
        level5.add_puzzle(puzzle5)

        level5.add_objective("Aplicar distorção")
        level5.add_objective("Entender deformação")
        level5.required_shading_model = 'lambertian'

        self.levels.append(level5)

        # ==================== NÍVEL 6: Iluminação - Lambertiano ====================
        level6 = Level(
            6,
            "Capítulo 6: A Luz Difusa",
            "Explore o modelo de iluminação LAMBERTIANO para iluminar as formas!",
            difficulty=3
        )

        cube2 = Cube(size=1.5, color=(0.8, 0.2, 0.2))
        level6.add_shape(cube2)

        puzzle6 = Puzzle(PuzzleType.LIGHTING, difficulty=3)
        puzzle6.solution['shading_model'] = 'lambertian'
        puzzle6.data['description'] = "Use iluminação Lambertiana para revelar o padrão"
        level6.add_puzzle(puzzle6)

        level6.add_objective("Aplicar modelo Lambertiano")
        level6.required_shading_model = 'lambertian'

        self.levels.append(level6)

        # ==================== NÍVEL 7: Iluminação - Phong ====================
        level7 = Level(
            7,
            "Capítulo 7: O Brilho Especular",
            "Domine o modelo de iluminação PHONG com componente especular!",
            difficulty=4
        )

        sphere2 = Sphere(radius=1.0, subdivisions=2, color=(0.2, 0.8, 0.8))
        level7.add_shape(sphere2)

        puzzle7 = Puzzle(PuzzleType.LIGHTING, difficulty=4)
        puzzle7.solution['shading_model'] = 'phong'
        puzzle7.data['description'] = "Use iluminação Phong para criar brilho realista"
        level7.add_puzzle(puzzle7)

        level7.add_objective("Aplicar modelo Phong")
        level7.add_objective("Observar reflexo especular")
        level7.required_shading_model = 'phong'

        self.levels.append(level7)

        # ==================== NÍVEL 8: Iluminação - Gouraud ====================
        level8 = Level(
            8,
            "Capítulo 8: A Interpolação Suave",
            "Aprenda o modelo GOURAUD que interpola cores nos vértices!",
            difficulty=4
        )

        pyramid2 = Pyramid(base_size=1.8, height=2.5, color=(0.5, 1.0, 0.2))
        level8.add_shape(pyramid2)

        puzzle8 = Puzzle(PuzzleType.LIGHTING, difficulty=4)
        puzzle8.solution['shading_model'] = 'gouraud'
        puzzle8.data['description'] = "Use iluminação Gouraud para suavizar as faces"
        level8.add_puzzle(puzzle8)

        level8.add_objective("Aplicar modelo Gouraud")
        level8.add_objective("Comparar com Phong")
        level8.required_shading_model = 'gouraud'

        self.levels.append(level8)

        # ==================== NÍVEL 9: Combinação de Transformações ====================
        level9 = Level(
            9,
            "Capítulo 9: A Harmonia das Transformações",
            "Combine TODAS as transformações para resolver puzzles complexos!",
            difficulty=5
        )

        # Múltiplas formas
        level9.add_shape(Cube(size=1.0, color=(1.0, 0.3, 0.3)))
        level9.add_shape(Sphere(radius=0.7, subdivisions=2, color=(0.3, 1.0, 0.3)))
        level9.add_shape(Pyramid(base_size=1.2, height=1.8, color=(0.3, 0.3, 1.0)))

        puzzle9 = Puzzle(PuzzleType.SEQUENCE, difficulty=5)
        puzzle9.data['description'] = "Aplique sequência: Rotação → Escala → Translação"
        level9.add_puzzle(puzzle9)

        # Puzzle matemático
        math_puzzle = Puzzle(PuzzleType.MATH, difficulty=4)
        level9.add_puzzle(math_puzzle)

        level9.add_objective("Combinar 3+ transformações")
        level9.add_objective("Resolver puzzle matemático")
        level9.add_objective("Usar todos os modelos de iluminação")
        level9.required_shading_model = 'phong'

        self.levels.append(level9)

        # ==================== NÍVEL 10: Desafio Final ====================
        level10 = Level(
            10,
            "Capítulo Final: O Restaurador Mestre",
            "Teste final! Use tudo que aprendeu para restaurar Geometria!",
            difficulty=5
        )

        # Todas as formas
        level10.add_shape(Cube(size=0.8, color=(1.0, 0.0, 0.0)))
        level10.add_shape(Sphere(radius=0.6, subdivisions=2, color=(0.0, 1.0, 0.0)))
        level10.add_shape(Pyramid(base_size=0.9, height=1.5, color=(0.0, 0.0, 1.0)))
        level10.add_shape(Cylinder(radius=0.5, height=1.5, color=(1.0, 1.0, 0.0)))
        level10.add_shape(Torus(major_radius=0.8, minor_radius=0.2, color=(1.0, 0.0, 1.0)))

        # Múltiplos puzzles
        for i in range(3):
            level10.add_puzzle(Puzzle(PuzzleType.TRANSFORMATION, difficulty=5))

        level10.add_puzzle(Puzzle(PuzzleType.MATH, difficulty=5))
        level10.add_puzzle(Puzzle(PuzzleType.LIGHTING, difficulty=5))

        level10.add_objective("Resolver todos os puzzles")
        level10.add_objective("Dominar todas as transformações")
        level10.add_objective("Dominar todos os modelos de iluminação")
        level10.required_shading_model = 'phong'

        self.levels.append(level10)

    def get_current_level(self):
        """Retorna o nível atual"""
        if 0 <= self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        return None

    def next_level(self):
        """Avança para o próximo nível"""
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
            return True
        return False

    def previous_level(self):
        """Volta para o nível anterior"""
        if self.current_level_index > 0:
            self.current_level_index -= 1
            return True
        return False

    def goto_level(self, level_index):
        """Vai para um nível específico"""
        if 0 <= level_index < len(self.levels):
            self.current_level_index = level_index
            return True
        return False

    def get_total_levels(self):
        """Retorna o número total de níveis"""
        return len(self.levels)

    def get_progress(self):
        """Retorna progresso geral (0.0-1.0)"""
        if len(self.levels) == 0:
            return 0.0

        completed = sum(1 for level in self.levels if level.is_completed())
        return completed / len(self.levels)
