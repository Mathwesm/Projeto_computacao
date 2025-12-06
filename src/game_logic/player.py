"""
Gerenciamento do estado do jogador
"""

import json
import os


class Player:
    """Classe para gerenciar o estado do jogador"""

    def __init__(self):
        """Inicializa o jogador"""
        self.score = 0
        self.lives = 3
        self.current_level = 0
        self.levels_completed = []
        self.total_time_played = 0
        self.transformations_used = {
            'translate': 0,
            'rotate': 0,
            'scale': 0,
            'reflect': 0,
            'shear': 0
        }
        self.shading_models_used = {
            'phong': 0,
            'lambertian': 0,
            'gouraud': 0
        }

    def add_score(self, points):
        """Adiciona pontos ao score"""
        self.score += points

    def lose_life(self):
        """Perde uma vida"""
        self.lives -= 1
        return self.lives > 0

    def gain_life(self):
        """Ganha uma vida"""
        self.lives = min(self.lives + 1, 5)

    def complete_level(self, level_id, bonus_points=0):
        """Marca um nível como completo"""
        if level_id not in self.levels_completed:
            self.levels_completed.append(level_id)
        self.add_score(bonus_points)

    def use_transformation(self, transform_type):
        """Registra uso de uma transformação"""
        if transform_type in self.transformations_used:
            self.transformations_used[transform_type] += 1

    def use_shading_model(self, model_type):
        """Registra uso de um modelo de iluminação"""
        if model_type in self.shading_models_used:
            self.shading_models_used[model_type] += 1

    def get_stats(self):
        """Retorna estatísticas do jogador"""
        return {
            'score': self.score,
            'lives': self.lives,
            'level': self.current_level,
            'levels_completed': len(self.levels_completed),
            'time_played': self.total_time_played,
            'transformations': self.transformations_used,
            'shading_models': self.shading_models_used
        }

    def reset(self):
        """Reseta o progresso do jogador"""
        self.__init__()

    def save_progress(self, filename='save.json'):
        """Salva o progresso em arquivo"""
        data = {
            'score': self.score,
            'lives': self.lives,
            'current_level': self.current_level,
            'levels_completed': self.levels_completed,
            'total_time_played': self.total_time_played,
            'transformations_used': self.transformations_used,
            'shading_models_used': self.shading_models_used
        }

        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False

    def load_progress(self, filename='save.json'):
        """Carrega o progresso de arquivo"""
        if not os.path.exists(filename):
            return False

        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.score = data.get('score', 0)
            self.lives = data.get('lives', 3)
            self.current_level = data.get('current_level', 0)
            self.levels_completed = data.get('levels_completed', [])
            self.total_time_played = data.get('total_time_played', 0)
            self.transformations_used = data.get('transformations_used', {})
            self.shading_models_used = data.get('shading_models_used', {})

            return True
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            return False
