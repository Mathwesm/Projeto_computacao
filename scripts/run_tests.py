"""
Script para executar todos os testes do projeto
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

if __name__ == "__main__":
    import pytest

    # Argumentos para o pytest
    args = [
        'tests/',
        '-v',
        '--cov=src',
        '--cov-report=html',
        '--cov-report=term-missing'
    ]

    # Executa pytest
    exit_code = pytest.main(args)
    sys.exit(exit_code)
