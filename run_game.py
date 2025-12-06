"""
Script para executar o MathShape Quest
Pode ser executado de qualquer lugar
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configura encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == "__main__":
    print("=" * 60)
    print("MATHSHAPE QUEST - Aventura das Formas Geométricas")
    print("=" * 60)
    print("Projeto de Computação Gráfica")
    print()
    print("Carregando jogo...")
    print()

    try:
        from game import main
        main()
    except Exception as e:
        print(f"\nErro ao executar o jogo: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")
