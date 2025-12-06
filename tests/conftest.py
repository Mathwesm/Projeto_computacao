"""
Configuração do pytest
Fixtures e configurações compartilhadas entre testes
"""

import pytest
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def sample_vertices():
    """Fixture com vértices de exemplo para testes"""
    return [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]


@pytest.fixture
def sample_faces():
    """Fixture com faces de exemplo para testes"""
    return [
        [0, 1, 2],
        [0, 2, 3]
    ]


@pytest.fixture
def sample_colors():
    """Fixture com cores de exemplo para testes"""
    return {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0)
    }
