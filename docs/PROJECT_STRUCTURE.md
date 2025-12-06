# Estrutura do Projeto - Guia Detalhado

Este documento fornece uma visão detalhada da organização do projeto MathShape Quest.

## 📁 Estrutura de Diretórios

### `/` (Raiz)
Arquivos de configuração e documentação principal.

```
├── README.md              # Documentação principal
├── CHANGELOG.md           # Histórico de versões
├── requirements.txt       # Dependências Python
├── setup.py              # Script de instalação
├── pyproject.toml        # Configuração moderna do projeto
├── Makefile              # Comandos úteis (Linux/Mac)
├── .gitignore            # Arquivos ignorados pelo Git
├── run.bat               # Script de execução (Windows)
└── run.sh                # Script de execução (Linux/Mac)
```

### `/src` - Código Fonte
Todo o código do jogo organizado por módulos.

#### `/src/core` - Núcleo do Sistema
**Propósito**: Configurações e componentes fundamentais

```
core/
├── __init__.py         # Exporta símbolos principais
├── config.py           # Configurações do jogo
├── constants.py        # Constantes matemáticas e valores fixos
└── exceptions.py       # Exceções personalizadas
```

**Quando usar**:
- Para configurar parâmetros do jogo
- Para definir constantes globais
- Para lançar exceções específicas

**Exemplo**:
```python
from core import WINDOW_WIDTH, WINDOW_HEIGHT, VERSION
from core.exceptions import RenderException
```

#### `/src/utils` - Utilitários
**Propósito**: Funções auxiliares reutilizáveis

```
utils/
├── __init__.py         # Exporta utilitários
├── math_utils.py       # Funções matemáticas (clamp, lerp, etc)
├── color_utils.py      # Manipulação de cores
├── time_utils.py       # Timer, FPS counter
└── validators.py       # Validação de dados
```

**Quando usar**:
- Para operações matemáticas comuns
- Para conversão/manipulação de cores
- Para controle de tempo
- Para validar entrada de dados

**Exemplo**:
```python
from utils import clamp, normalize_vector, Timer
from utils.color_utils import interpolate_color
```

#### `/src/transformations` - Transformações Geométricas
**Propósito**: Sistema de transformações 3D

```
transformations/
├── __init__.py         # Exporta classes principais
├── matrix.py           # Classe Matrix4x4
└── geometric.py        # Classe GeometricTransformations
```

**Responsabilidades**:
- Operações com matrizes 4x4
- Translação, rotação, escala
- Reflexão, distorção
- Composição de transformações

**Exemplo**:
```python
from transformations import Matrix4x4, GeometricTransformations

transform = GeometricTransformations()
transform.translate(1, 0, 0)
transform.rotate_y(45)
```

#### `/src/objects` - Objetos 3D
**Propósito**: Definição de objetos e primitivas 3D

```
objects/
├── __init__.py         # Exporta primitivas
├── shape3d.py          # Classe base Shape3D
└── primitives.py       # Cubo, Esfera, Pirâmide, etc
```

**Primitivas disponíveis**:
- `Cube`: Cubo
- `Sphere`: Esfera
- `Pyramid`: Pirâmide
- `Cylinder`: Cilindro
- `Torus`: Torus

**Exemplo**:
```python
from objects import Cube, Sphere

cube = Cube(size=2)
cube.translate(0, 1, 0)
cube.rotate_y(45)
```

#### `/src/rendering` - Renderização 3D
**Propósito**: Sistema de renderização e iluminação

```
rendering/
├── __init__.py         # Exporta componentes de renderização
├── renderer.py         # Engine de renderização
├── camera.py           # Sistema de câmera
└── lighting.py         # Modelos de iluminação
```

**Componentes**:
- **Renderer**: Renderiza objetos 3D na tela
- **Camera**: Controla visão e projeção
- **Light**: Fonte de luz
- **PhongShading**, **LambertianShading**, **GouraudShading**: Modelos de iluminação

**Exemplo**:
```python
from rendering import Renderer, Camera, PhongShading

renderer = Renderer(800, 600)
camera = Camera([5, 2, 5], [0, 0, 0])
shading = PhongShading()
```

#### `/src/game_logic` - Lógica do Jogo
**Propósito**: Regras e mecânicas do jogo

```
game_logic/
├── __init__.py         # Exporta componentes de jogo
├── player.py           # Sistema de jogador
├── puzzle.py           # Sistema de puzzles
└── level.py            # Sistema de níveis
```

**Componentes**:
- **Player**: Gerencia vidas, pontuação, progresso
- **Puzzle**: Define puzzles e verificações
- **Level**: Representa um nível
- **LevelManager**: Gerencia progressão de níveis

**Exemplo**:
```python
from game_logic import Player, LevelManager

player = Player()
level_manager = LevelManager()
current_level = level_manager.get_current_level()
```

#### `/src/ui` - Interface do Usuário
**Propósito**: Menus e HUD

```
ui/
├── __init__.py         # Exporta componentes UI
├── menu.py             # Sistema de menus
├── hud.py              # HUD do jogo
└── button.py           # Botões interativos
```

**Componentes**:
- **Menu**: Menu principal e de pausa
- **HUD**: Interface durante o jogo
- **Button**: Botões clicáveis

**Exemplo**:
```python
from ui import Menu, HUD, Button

menu = Menu(800, 600)
hud = HUD(800, 600)
```

### `/tests` - Testes
Testes automatizados do código.

```
tests/
├── __init__.py
├── conftest.py              # Configuração do pytest
├── unit/                    # Testes unitários
│   ├── test_math_utils.py
│   └── test_color_utils.py
└── integration/             # Testes de integração
    └── test_transformations.py
```

**Como executar**:
```bash
# Testes básicos
python test_modules.py

# Testes com pytest
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=src --cov-report=html
```

### `/docs` - Documentação
Documentação detalhada do projeto.

```
docs/
├── ARCHITECTURE.md       # Arquitetura do sistema
├── CONTRIBUTING.md       # Guia de contribuição
├── PROJECT_STRUCTURE.md  # Este arquivo
└── api/                  # Documentação da API
```

### `/assets` - Recursos
Recursos do jogo (fontes, sons, texturas).

```
assets/
├── README.md
├── fonts/               # Fontes TTF/OTF
├── sounds/              # Arquivos de áudio
└── textures/            # Imagens e texturas
```

### `/scripts` - Scripts Auxiliares
Scripts úteis para desenvolvimento.

```
scripts/
├── run_tests.py            # Executor de testes
└── check_code_quality.py   # Verificador de qualidade
```

## 🔄 Fluxo de Execução

### 1. Inicialização
```
main.py
  → importa Game
  → Game.__init__()
    → pygame.init()
    → cria Renderer, Camera, Player, etc
  → Game.run()
```

### 2. Loop Principal
```
Game.run()
  ├── handle_events()      # Processa input
  ├── update(dt)           # Atualiza estado
  ├── render()             # Renderiza frame
  └── clock.tick(FPS)      # Controla FPS
```

### 3. Renderização
```
Renderer.render(shape, camera, light, shading)
  ├── Aplica transformações do objeto
  ├── Aplica transformação de câmera
  ├── Projeta para 2D
  ├── Calcula iluminação
  └── Desenha na tela
```

## 📦 Dependências Entre Módulos

### Hierarquia (do mais baixo para o mais alto)
```
1. core (base)
2. utils (usa core)
3. transformations (usa utils, core)
4. objects (usa transformations, utils, core)
5. rendering (usa objects, transformations, utils, core)
6. game_logic (usa rendering, objects, utils, core)
7. ui (usa game_logic, utils, core)
8. game (usa tudo)
```

### Regras
- ✅ Módulos superiores podem usar inferiores
- ❌ Módulos inferiores NÃO devem usar superiores
- ✅ `core` e `utils` não dependem de outros módulos internos

## 🛠️ Comandos Úteis

### Linux/Mac (com Makefile)
```bash
make help          # Lista comandos disponíveis
make install       # Instala dependências
make run           # Executa o jogo
make test          # Executa testes
make test-cov      # Testes com cobertura
make lint          # Verifica código
make format        # Formata código
make clean         # Limpa arquivos temporários
```

### Windows (sem make)
```bash
# Instalar
pip install -r requirements.txt

# Executar
python src/main.py
# ou
run.bat

# Testar
python test_modules.py
pytest tests/

# Limpar
python scripts/clean.py
```

## 📝 Convenções de Código

### Nomenclatura
- **Arquivos**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções/variáveis**: `snake_case`
- **Constantes**: `UPPER_SNAKE_CASE`

### Imports
```python
# Ordem:
1. Bibliotecas padrão
2. Bibliotecas externas
3. Módulos locais

# Exemplo:
import sys
import os

import pygame
import numpy as np

from .core import config
from .utils import math_utils
```

### Docstrings
```python
def funcao(param1: int, param2: str) -> bool:
    """
    Breve descrição

    Args:
        param1: Descrição
        param2: Descrição

    Returns:
        Descrição do retorno

    Raises:
        ValueError: Quando...
    """
    pass
```

## 🔍 Encontrando o que Precisa

### Preciso de...

**Configurações do jogo**
→ `src/core/config.py`

**Constantes matemáticas**
→ `src/core/constants.py`

**Funções matemáticas**
→ `src/utils/math_utils.py`

**Manipular cores**
→ `src/utils/color_utils.py`

**Timer ou FPS counter**
→ `src/utils/time_utils.py`

**Transformar objetos 3D**
→ `src/transformations/`

**Criar objetos 3D**
→ `src/objects/primitives.py`

**Renderizar cenas**
→ `src/rendering/renderer.py`

**Controlar câmera**
→ `src/rendering/camera.py`

**Iluminação**
→ `src/rendering/lighting.py`

**Lógica de níveis**
→ `src/game_logic/level.py`

**Sistema de pontuação**
→ `src/game_logic/player.py`

**Interface gráfica**
→ `src/ui/`

## 📚 Recursos Adicionais

- **Arquitetura**: Veja `docs/ARCHITECTURE.md`
- **Contribuir**: Veja `docs/CONTRIBUTING.md`
- **Changelog**: Veja `CHANGELOG.md`
- **README**: Veja `README.md`

---

**Última atualização**: 2025-12-03
