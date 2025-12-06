"""
Gerenciamento do estado do jogador
"""

import json
import os
from dataclasses import dataclass, field
from typing import List, Dict
from pathlib import Path
from core.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Player:
    """Classe para gerenciar o estado do jogador usando dataclass"""

    score: int = 0
    lives: int = 3
    current_level: int = 0
    levels_completed: List[int] = field(default_factory=list)
    total_time_played: float = 0.0
    transformations_used: Dict[str, int] = field(default_factory=lambda: {
        'translate': 0,
        'rotate': 0,
        'scale': 0,
        'reflect': 0,
        'shear': 0
    })
    shading_models_used: Dict[str, int] = field(default_factory=lambda: {
        'phong': 0,
        'lambertian': 0,
        'gouraud': 0
    })

    def __post_init__(self) -> None:
        """Validação após inicialização"""
        if self.lives < 0:
            raise ValueError("Lives cannot be negative")
        if self.score < 0:
            raise ValueError("Score cannot be negative")
        if self.current_level < 0:
            raise ValueError("Current level cannot be negative")

    def add_score(self, points: int) -> None:
        """Adiciona pontos ao score"""
        self.score += points

    def lose_life(self) -> bool:
        """Perde uma vida e retorna True se ainda tem vidas"""
        self.lives -= 1
        return self.lives > 0

    def gain_life(self) -> None:
        """Ganha uma vida (máximo 5)"""
        self.lives = min(self.lives + 1, 5)

    def complete_level(self, level_id: int, bonus_points: int = 0) -> None:
        """Marca um nível como completo"""
        if level_id not in self.levels_completed:
            self.levels_completed.append(level_id)
        self.add_score(bonus_points)

    def use_transformation(self, transform_type: str) -> None:
        """Registra uso de uma transformação"""
        if transform_type in self.transformations_used:
            self.transformations_used[transform_type] += 1

    def use_shading_model(self, model_type: str) -> None:
        """Registra uso de um modelo de iluminação"""
        if model_type in self.shading_models_used:
            self.shading_models_used[model_type] += 1

    def get_stats(self) -> Dict[str, any]:
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

    def reset(self) -> None:
        """Reseta o progresso do jogador"""
        self.score = 0
        self.lives = 3
        self.current_level = 0
        self.levels_completed = []
        self.total_time_played = 0.0
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

    def save_progress(self, filepath: Path = Path('saves/save.json')) -> bool:
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
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with filepath.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Progresso salvo com sucesso em {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar progresso: {e}", exc_info=True)
            return False

    def load_progress(self, filepath: Path = Path('saves/save.json')) -> bool:
        """Carrega o progresso de arquivo"""
        if not filepath.exists():
            logger.warning(f"Arquivo de save não encontrado: {filepath}")
            return False

        try:
            with filepath.open('r', encoding='utf-8') as f:
                data = json.load(f)

            self.score = data.get('score', 0)
            self.lives = data.get('lives', 3)
            self.current_level = data.get('current_level', 0)
            self.levels_completed = data.get('levels_completed', [])
            self.total_time_played = data.get('total_time_played', 0.0)
            self.transformations_used = data.get('transformations_used', {
                'translate': 0, 'rotate': 0, 'scale': 0, 'reflect': 0, 'shear': 0
            })
            self.shading_models_used = data.get('shading_models_used', {
                'phong': 0, 'lambertian': 0, 'gouraud': 0
            })

            logger.info(f"Progresso carregado com sucesso de {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar progresso: {e}", exc_info=True)
            return False
