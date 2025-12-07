# 🎮 MathShape Quest - Aventura das Formas Geométricas

**Jogo Educativo de Computação Gráfica**

Um jogo interativo que ensina conceitos de transformações geométricas e iluminação 3D de forma divertida e educativa.

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de Computação Gráfica e implementa um jogo educativo completo que demonstra:

### ✨ Transformações Geométricas Implementadas
- **Translação**: Movimento de objetos no espaço 3D
- **Rotação**: Rotação em torno dos eixos X, Y e Z
- **Escala**: Redimensionamento uniforme e não-uniforme
- **Reflexão**: Espelhamento em relação aos planos XY, XZ e YZ
- **Distorção (Shear)**: Deformação controlada dos objetos

### 💡 Modelos de Iluminação Implementados
- **Lambertiano**: Modelo de iluminação difusa simples
- **Phong**: Modelo completo com componentes ambiente, difusa e especular
- **Gouraud**: Modelo com interpolação de cores nos vértices

### 🎯 Problema do Mundo Real que Resolve
O jogo ajuda estudantes a:
- Aprender conceitos de geometria de forma visual e interativa
- Entender transformações geométricas 3D
- Compreender modelos de iluminação e renderização
- Desenvolver raciocínio espacial e lógico
- Tornar o aprendizado de matemática mais engajante

---

## 🎮 História do Jogo

Em um mundo matemático chamado "Geometria", as formas geométricas perderam suas propriedades após um vírus digital. O jogador é um jovem matemático que precisa restaurar as formas usando transformações geométricas e ajustar a iluminação para revelar padrões ocultos que solucionam problemas matemáticos.

---

## 🚀 Como Executar

### Requisitos
- Python 3.8 ou superior
- Pygame 2.5.2
- NumPy 1.24.3

### Instalação Rápida

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Projeto_computacao_grafica.git
cd Projeto_computacao_grafica
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o jogo:
```bash
# Método mais simples (recomendado):
python run_game.py

# Outros métodos:
python src/main.py
python -m src.main

# Scripts prontos:
./run.sh        # Linux/Mac
run.bat         # Windows
```

**📖 Guia completo de execução:** Veja [QUICK_START.md](QUICK_START.md)

---

## 🎮 Controles

### Câmera
- **Mouse (arrastar)**: Rotacionar câmera ao redor do objeto
- **Scroll do Mouse**: Zoom in/out

### Transformações Geométricas
- **1**: Aplicar Translação
- **2**: Aplicar Rotação
- **3 ou +**: Aumentar Escala (15%)
- **-** (menos): Diminuir Escala (15%)
- **4**: Aplicar Reflexão
- **5**: Aplicar Distorção (Shear)

### Modelos de Iluminação
- **Q**: Modelo Lambertiano
- **W**: Modelo Phong
- **E**: Modelo Gouraud

### Modo Treino (Troca de Formas)
- **Tab / Seta Direita**: Próxima forma
- **Seta Esquerda**: Forma anterior
- **6**: Cubo
- **7**: Pirâmide
- **8**: Esfera
- **9**: Cilindro
- **0**: Torus

### Outras Ações
- **H**: Mostrar dica do puzzle atual (modo jogo)
- **C**: Alternar painel de controles
- **R**: Ativar/desativar rotação automática
- **F11**: Alternar tela cheia
- **ESC**: Pausar jogo / Voltar ao menu

---

## 🎯 Modo Treino

O **Modo Treino** é um ambiente livre para experimentar todas as transformações geométricas e modelos de iluminação sem pressão ou puzzles.

**Diferença do modo normal**: Você pode trocar entre 5 formas geométricas diferentes:
- **Cubo** (Tecla 6)
- **Pirâmide** (Tecla 7)
- **Esfera** (Tecla 8)
- **Cilindro** (Tecla 9)
- **Torus** (Tecla 0)

Use **Tab/Setas** para navegar entre as formas ou pressione as teclas **6-0** para seleção direta. Todas as outras funcionalidades são idênticas ao modo de jogo normal.

---

## 📚 Estrutura do Projeto

```
Projeto_computacao_grafica/
├── src/                        # Código fonte
│   ├── main.py                 # Ponto de entrada
│   ├── game.py                 # Loop principal
│   │
│   ├── core/                   # Módulo central
│   │   ├── config.py           # Configurações
│   │   ├── constants.py        # Constantes
│   │   └── exceptions.py       # Exceções personalizadas
│   │
│   ├── transformations/        # Transformações geométricas
│   │   ├── matrix.py           # Matrizes 4x4
│   │   └── geometric.py        # Transformações 3D
│   │
│   ├── rendering/              # Sistema de renderização
│   │   ├── lighting.py         # Modelos de iluminação
│   │   ├── camera.py           # Câmera 3D
│   │   └── renderer.py         # Engine de renderização
│   │
│   ├── objects/                # Objetos 3D
│   │   ├── shape3d.py          # Classe base
│   │   └── primitives.py       # Primitivas geométricas
│   │
│   ├── game_logic/             # Lógica do jogo
│   │   ├── player.py           # Sistema de jogador
│   │   ├── puzzle.py           # Puzzles
│   │   └── level.py            # Níveis
│   │
│   ├── ui/                     # Interface do usuário
│   │   ├── button.py           # Botões
│   │   ├── menu.py             # Menus
│   │   └── hud.py              # HUD
│   │
│   └── utils/                  # Utilitários
│       ├── math_utils.py       # Funções matemáticas
│       ├── color_utils.py      # Manipulação de cores
│       ├── time_utils.py       # Controle de tempo
│       └── validators.py       # Validações
│
├── tests/                      # Testes
│   ├── unit/                   # Testes unitários
│   └── integration/            # Testes de integração
│
├── docs/                       # Documentação
│   ├── ARCHITECTURE.md         # Arquitetura
│   ├── CONTRIBUTING.md         # Guia de contribuição
│   └── api/                    # Documentação da API
│
├── assets/                     # Recursos do jogo
│   ├── fonts/                  # Fontes
│   ├── sounds/                 # Sons
│   └── textures/               # Texturas
│
├── scripts/                    # Scripts úteis
│   ├── run_tests.py           # Executor de testes
│   └── check_code_quality.py # Verificador de qualidade
│
├── .gitignore                  # Arquivos ignorados pelo Git
├── setup.py                    # Instalação do projeto
├── pyproject.toml             # Configuração do projeto
├── Makefile                    # Comandos úteis
├── requirements.txt           # Dependências
├── CHANGELOG.md               # Histórico de mudanças
└── README.md                  # Este arquivo
```

---

## 🎓 Conceitos Implementados

### 1. Transformações Geométricas

Todas as transformações são implementadas usando **matrizes homogêneas 4x4**:

#### Translação
```
[1  0  0  tx]
[0  1  0  ty]
[0  0  1  tz]
[0  0  0  1 ]
```

#### Rotação (exemplo: eixo Y)
```
[cos(θ)   0  sin(θ)  0]
[0        1  0       0]
[-sin(θ)  0  cos(θ)  0]
[0        0  0       1]
```

#### Escala
```
[sx  0   0   0]
[0   sy  0   0]
[0   0   sz  0]
[0   0   0   1]
```

### 2. Modelos de Iluminação

#### Lambertiano (Diffuse)
```
I = Ia + Id * (N · L)
```
Onde:
- Ia: Luz ambiente
- Id: Intensidade difusa
- N: Vetor normal
- L: Vetor direção da luz

#### Phong
```
I = Ia + Id * (N · L) + Is * (R · V)^n
```
Onde:
- Is: Intensidade especular
- R: Vetor de reflexão
- V: Vetor de visão
- n: Coeficiente de brilho

#### Gouraud
Calcula iluminação nos vértices e interpola cores entre eles.

---

## 🎯 Níveis do Jogo

O jogo possui **10 níveis progressivos**:

1. **Capítulo 1**: O Despertar das Formas (Translação)
2. **Capítulo 2**: A Dança das Rotações (Rotação)
3. **Capítulo 3**: O Poder do Tamanho (Escala)
4. **Capítulo 4**: O Espelho Mágico (Reflexão)
5. **Capítulo 5**: A Distorção Dimensional (Distorção)
6. **Capítulo 6**: A Luz Difusa (Modelo Lambertiano)
7. **Capítulo 7**: O Brilho Especular (Modelo Phong)
8. **Capítulo 8**: A Interpolação Suave (Modelo Gouraud)
9. **Capítulo 9**: A Harmonia das Transformações (Combinação)
10. **Capítulo Final**: O Restaurador Mestre (Desafio Final)

---

## 🏆 Sistema de Pontuação

- **Puzzle resolvido**: 100 pontos × dificuldade
- **Nível completo**: 500 pontos bônus
- **Penalidade por tentativa**: -20 pontos

---

## 👥 Equipe de Desenvolvimento

[Adicione os nomes dos integrantes do grupo aqui]

---

## 📖 Referências

- **Computação Gráfica**: Conceitos fundamentais de transformações e iluminação
- **OpenGL Programming Guide**: Referência para modelos de iluminação
- **Pygame Documentation**: Framework de desenvolvimento de jogos em Python

---

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Computação Gráfica.

---

## 🎥 Demonstração

[Adicione screenshots ou vídeo de demonstração aqui]

---

## 📧 Contato

Para dúvidas ou sugestões sobre o projeto, entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido com ❤️ para a disciplina de Computação Gráfica**
