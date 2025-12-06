"""
MathShape Quest - Aventura das Formas Geométricas
Jogo Educativo de Computação Gráfica

Projeto desenvolvido para a disciplina de Computação Gráfica
Demonstra:
- Transformações Geométricas (Translação, Rotação, Escala, Reflexão, Distorção)
- Modelos de Iluminação (Phong, Lambertiano, Gouraud)
- Renderização 3D
- Conceitos educativos de matemática e geometria
"""

import sys
import os

# Adiciona o diretório pai ao path para imports funcionarem
if __name__ == "__main__":
    # Quando executado diretamente
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from game import main
except ImportError:
    from src.game import main

if __name__ == "__main__":
    print("=" * 60)
    print("MATHSHAPE QUEST - Aventura das Formas Geométricas")
    print("=" * 60)
    print("Projeto de Computação Gráfica")
    print()
    print("Carregando jogo...")
    print()

    try:
        main()
    except Exception as e:
        print(f"\nErro ao executar o jogo: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")
