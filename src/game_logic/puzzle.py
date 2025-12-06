"""
Sistema de puzzles do jogo
"""

from enum import Enum
import random
import math


class PuzzleType(Enum):
    """Tipos de puzzles disponíveis"""
    TRANSFORMATION = "transformation"  # Aplicar transformações corretas
    MATCHING = "matching"              # Encaixar formas
    LIGHTING = "lighting"              # Ajustar iluminação
    MATH = "math"                      # Resolver problemas matemáticos
    SEQUENCE = "sequence"              # Sequência de transformações


class Puzzle:
    """Classe base para puzzles"""

    def __init__(self, puzzle_type, difficulty=1):
        """
        Inicializa um puzzle
        Args:
            puzzle_type: Tipo do puzzle (PuzzleType)
            difficulty: Nível de dificuldade (1-5)
        """
        self.type = puzzle_type
        self.difficulty = difficulty
        self.solved = False
        self.attempts = 0
        self.max_attempts = 3 + difficulty

        # Dados específicos do puzzle
        self.data = {}
        self.solution = {}
        self.current_state = {}

        self._generate()

    def _generate(self):
        """Gera o puzzle (implementado nas subclasses)"""
        if self.type == PuzzleType.TRANSFORMATION:
            self._generate_transformation_puzzle()
        elif self.type == PuzzleType.MATCHING:
            self._generate_matching_puzzle()
        elif self.type == PuzzleType.LIGHTING:
            self._generate_lighting_puzzle()
        elif self.type == PuzzleType.MATH:
            self._generate_math_puzzle()
        elif self.type == PuzzleType.SEQUENCE:
            self._generate_sequence_puzzle()

    def _generate_transformation_puzzle(self):
        """Gera puzzle de transformação"""
        # Escolhe transformações aleatórias
        transformations = ['translate', 'rotate', 'scale', 'reflect', 'shear']
        num_transforms = min(1 + self.difficulty, 3)

        self.solution['transforms'] = []

        for _ in range(num_transforms):
            transform = random.choice(transformations)

            if transform == 'translate':
                self.solution['transforms'].append({
                    'type': 'translate',
                    'x': random.randint(-3, 3),
                    'y': random.randint(-2, 2),
                    'z': random.randint(-3, 3)
                })
            elif transform == 'rotate':
                axis = random.choice(['x', 'y', 'z'])
                angle = random.choice([45, 90, 135, 180])
                self.solution['transforms'].append({
                    'type': 'rotate',
                    'axis': axis,
                    'angle': angle
                })
            elif transform == 'scale':
                factor = random.choice([0.5, 0.75, 1.5, 2.0])
                self.solution['transforms'].append({
                    'type': 'scale',
                    'factor': factor
                })
            elif transform == 'reflect':
                axis = random.choice(['x', 'y', 'z'])
                self.solution['transforms'].append({
                    'type': 'reflect',
                    'axis': axis
                })
            elif transform == 'shear':
                plane = random.choice(['xy', 'xz', 'yz'])
                self.solution['transforms'].append({
                    'type': 'shear',
                    'plane': plane,
                    'factor': random.uniform(0.2, 0.5)
                })

        self.data['description'] = self._create_transformation_description()

    def _generate_matching_puzzle(self):
        """Gera puzzle de encaixe"""
        # Define forma alvo e transformações necessárias
        self.solution['target_shape'] = random.choice(['cube', 'pyramid', 'sphere'])
        self.solution['rotation'] = {
            'x': random.choice([0, 45, 90, 180]),
            'y': random.choice([0, 45, 90, 180]),
            'z': random.choice([0, 45, 90, 180])
        }
        self.data['description'] = "Encaixe a forma na posição correta"

    def _generate_lighting_puzzle(self):
        """Gera puzzle de iluminação"""
        # Escolhe modelo de iluminação correto
        self.solution['shading_model'] = random.choice(['phong', 'lambertian', 'gouraud'])
        self.solution['light_position'] = [
            random.randint(-5, 5),
            random.randint(5, 10),
            random.randint(-5, 5)
        ]
        self.data['description'] = "Ajuste a iluminação para revelar o padrão oculto"

    def _generate_math_puzzle(self):
        """Gera puzzle matemático"""
        # Operações matemáticas simples
        operations = ['+', '-', '*']
        difficulty_range = 10 * self.difficulty

        a = random.randint(1, difficulty_range)
        b = random.randint(1, difficulty_range)
        op = random.choice(operations)

        if op == '+':
            result = a + b
        elif op == '-':
            result = a - b
        else:  # '*'
            result = a * b

        self.solution['answer'] = result
        self.data['question'] = f"{a} {op} {b} = ?"
        self.data['description'] = f"Resolva: {self.data['question']}"

    def _generate_sequence_puzzle(self):
        """Gera puzzle de sequência"""
        # Sequência de transformações
        num_steps = 2 + self.difficulty
        self.solution['sequence'] = []

        transformations = ['translate', 'rotate', 'scale']

        for i in range(num_steps):
            transform = random.choice(transformations)
            self.solution['sequence'].append({
                'step': i + 1,
                'type': transform,
                'hint': f"Passo {i + 1}: Aplicar {transform}"
            })

        self.data['description'] = f"Complete a sequência de {num_steps} transformações"

    def _create_transformation_description(self):
        """Cria descrição legível das transformações"""
        descriptions = []
        for t in self.solution['transforms']:
            if t['type'] == 'translate':
                descriptions.append(f"Mover ({t['x']}, {t['y']}, {t['z']})")
            elif t['type'] == 'rotate':
                descriptions.append(f"Rotacionar {t['angle']}° em {t['axis'].upper()}")
            elif t['type'] == 'scale':
                descriptions.append(f"Escalar {t['factor']}x")
            elif t['type'] == 'reflect':
                descriptions.append(f"Espelhar em {t['axis'].upper()}")
            elif t['type'] == 'shear':
                descriptions.append(f"Distorcer em {t['plane'].upper()}")

        return "Aplique: " + ", ".join(descriptions)

    def check_solution(self, player_answer):
        """
        Verifica se a solução está correta
        Args:
            player_answer: Resposta do jogador
        Returns:
            (correto: bool, feedback: str)
        """
        self.attempts += 1

        if self.type == PuzzleType.MATH:
            if player_answer == self.solution['answer']:
                self.solved = True
                return (True, "Correto! Problema resolvido.")
            else:
                return (False, f"Incorreto. Tente novamente. ({self.max_attempts - self.attempts} tentativas restantes)")

        elif self.type == PuzzleType.LIGHTING:
            # Verifica se o modelo de iluminação está correto
            if player_answer.get('shading_model') == self.solution['shading_model']:
                self.solved = True
                return (True, f"Correto! Modelo {self.solution['shading_model']} aplicado.")
            else:
                return (False, "Modelo de iluminação incorreto.")

        # Para outros tipos, retorna sucesso (verificação visual)
        self.solved = True
        return (True, "Puzzle resolvido!")

    def get_hint(self):
        """Retorna uma dica para o puzzle"""
        if self.type == PuzzleType.TRANSFORMATION:
            if len(self.solution['transforms']) > 0:
                first = self.solution['transforms'][0]
                return f"Dica: Comece com {first['type']}"

        elif self.type == PuzzleType.MATH:
            answer = self.solution['answer']
            # Dá os primeiros dígitos
            hint_digits = str(answer)[:len(str(answer))//2]
            return f"Dica: A resposta começa com {hint_digits}..."

        elif self.type == PuzzleType.LIGHTING:
            return f"Dica: Use o modelo {self.solution['shading_model']}"

        return "Dica: Observe com atenção os padrões"

    def is_solved(self):
        """Verifica se o puzzle está resolvido"""
        return self.solved

    def get_description(self):
        """Retorna descrição do puzzle"""
        return self.data.get('description', 'Resolva o puzzle')

    def get_reward_points(self):
        """Calcula pontos de recompensa"""
        base_points = 100
        difficulty_multiplier = self.difficulty
        attempt_penalty = max(0, (self.attempts - 1) * 20)

        return max(50, base_points * difficulty_multiplier - attempt_penalty)
