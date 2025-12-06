# Arquitetura do Projeto

Este documento descreve a arquitetura e organização do MathShape Quest.

## Visão Geral

O projeto segue uma arquitetura modular, separando responsabilidades em diferentes camadas:

```
┌─────────────────────────────────────────┐
│           Interface (UI)                 │
│  (Menu, HUD, Buttons)                   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Game Logic Layer                  │
│  (Player, Levels, Puzzles)              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Rendering & Graphics Layer          │
│  (Renderer, Camera, Lighting)           │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│    Transformations & Objects Layer       │
│  (Matrices, Geometric Transforms, 3D)   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Core & Utils Layer               │
│  (Config, Constants, Utilities)         │
└─────────────────────────────────────────┘
```

## Camadas do Sistema

### 1. Core Layer (`src/core/`)

Camada fundamental que contém configurações e componentes centrais.

**Responsabilidades:**
- Configurações globais do jogo
- Constantes do projeto
- Exceções personalizadas
- Tipos e enumerações básicas

**Módulos:**
- `config.py`: Configurações (resolução, FPS, cores, etc)
- `constants.py`: Constantes matemáticas e valores fixos
- `exceptions.py`: Hierarquia de exceções customizadas

**Princípios:**
- Sem dependências de outros módulos do projeto
- Apenas configuração e definições
- Valores imutáveis sempre que possível

### 2. Utils Layer (`src/utils/`)

Utilitários reutilizáveis em todo o projeto.

**Responsabilidades:**
- Funções matemáticas auxiliares
- Manipulação de cores
- Controle de tempo
- Validações de dados

**Módulos:**
- `math_utils.py`: Funções matemáticas (clamp, lerp, normalize, etc)
- `color_utils.py`: Conversão e manipulação de cores
- `time_utils.py`: Timer, FPS counter, formatação de tempo
- `validators.py`: Validação de dados de entrada

**Princípios:**
- Funções puras quando possível
- Sem estado global
- Dependência apenas de bibliotecas padrão e numpy

### 3. Transformations Layer (`src/transformations/`)

Sistema de transformações geométricas 3D.

**Responsabilidades:**
- Operações com matrizes 4x4
- Transformações geométricas (translação, rotação, escala, etc)
- Composição de transformações

**Módulos:**
- `matrix.py`: Classe Matrix4x4 e operações matriciais
- `geometric.py`: Classe GeometricTransformations

**Implementações:**
- Matrizes homogêneas 4x4
- Translação, rotação (X, Y, Z), escala
- Reflexão, distorção (shear)
- Composição de transformações

**Princípios:**
- Usa numpy para eficiência
- Imutabilidade de matrizes (retorna novas matrizes)
- Validação de dados de entrada

### 4. Objects Layer (`src/objects/`)

Objetos 3D e primitivas geométricas.

**Responsabilidades:**
- Definição de objetos 3D
- Primitivas geométricas (cubo, esfera, etc)
- Gerenciamento de vértices, faces e normais

**Módulos:**
- `shape3d.py`: Classe base Shape3D
- `primitives.py`: Primitivas (Cube, Sphere, Pyramid, Cylinder, Torus)

**Hierarquia:**
```
Shape3D (base)
├── Cube
├── Sphere
├── Pyramid
├── Cylinder
└── Torus
```

**Princípios:**
- Cada objeto tem vértices, faces e normais
- Suporta transformações geométricas
- Calcula normais automaticamente

### 5. Rendering Layer (`src/rendering/`)

Sistema de renderização 3D e iluminação.

**Responsabilidades:**
- Renderização de objetos 3D
- Sistema de câmera
- Modelos de iluminação

**Módulos:**
- `renderer.py`: Classe Renderer (engine de renderização)
- `camera.py`: Classe Camera (controle de câmera)
- `lighting.py`: Modelos de iluminação (Phong, Lambertian, Gouraud)

**Modelos de Iluminação:**
- **Lambertian**: Iluminação difusa simples
- **Phong**: Modelo completo (ambiente + difusa + especular)
- **Gouraud**: Interpolação de cores nos vértices

**Pipeline de Renderização:**
1. Transformação de modelo (Model Transform)
2. Transformação de visão (View Transform)
3. Projeção (Projection)
4. Clipping
5. Conversão para coordenadas de tela
6. Rasterização
7. Aplicação de iluminação

**Princípios:**
- Separação entre geometria e aparência
- Suporte a múltiplos modelos de iluminação
- Pipeline configurável

### 6. Game Logic Layer (`src/game_logic/`)

Lógica central do jogo.

**Responsabilidades:**
- Sistema de jogador e pontuação
- Gerenciamento de níveis
- Sistema de puzzles

**Módulos:**
- `player.py`: Classe Player (vidas, pontuação, progresso)
- `level.py`: Classes Level e LevelManager
- `puzzle.py`: Classes Puzzle e PuzzleType

**Fluxo do Jogo:**
```
Menu → Level 1 → Puzzle → Level 2 → ... → Level 10 → Fim
         ↓         ↓
      Objetivo   Verificação
```

**Princípios:**
- Estado do jogo centralizado
- Progressão linear de níveis
- Sistema de pontuação consistente

### 7. UI Layer (`src/ui/`)

Interface do usuário.

**Responsabilidades:**
- Sistema de menus
- HUD (Head-Up Display)
- Componentes interativos

**Módulos:**
- `menu.py`: Classe Menu e MenuState
- `hud.py`: Classe HUD (interface durante o jogo)
- `button.py`: Classe Button (botões interativos)

**Componentes:**
- Menu principal
- Menu de pausa
- HUD de jogo (pontuação, vidas, tempo, controles)
- Botões e controles

**Princípios:**
- Separação entre lógica e apresentação
- Responsivo a diferentes resoluções
- Feedback visual para interações

## Fluxo de Dados

### Inicialização
```
main.py → Game.__init__() → Inicializa componentes
```

### Loop Principal
```
Game.run()
  → handle_events()
  → update(dt)
  → render()
  → clock.tick(FPS)
```

### Renderização de Objeto 3D
```
Shape3D → Renderer
  → Aplica transformações
  → Projeta para 2D
  → Aplica iluminação
  → Desenha na tela
```

## Padrões de Design Utilizados

### 1. **Singleton Pattern**
- Usado em: `LevelManager`, `Renderer`
- Garante única instância de componentes críticos

### 2. **State Pattern**
- Usado em: `GameState`, `MenuState`
- Gerencia diferentes estados do jogo

### 3. **Strategy Pattern**
- Usado em: Modelos de iluminação
- Permite trocar algoritmos de iluminação em runtime

### 4. **Factory Pattern**
- Usado em: Criação de primitivas 3D
- Facilita criação de objetos complexos

### 5. **Observer Pattern**
- Usado em: Sistema de eventos do jogo
- Desacopla componentes que reagem a eventos

## Dependências Entre Módulos

```
ui → game_logic → rendering → objects → transformations → utils
                                               ↓
                                             core
```

**Regras:**
- Módulos de camadas superiores podem usar camadas inferiores
- Camadas inferiores NÃO devem conhecer camadas superiores
- `core` e `utils` não dependem de nenhum outro módulo interno

## Extensibilidade

### Adicionar Nova Primitiva 3D
1. Criar classe em `objects/primitives.py`
2. Herdar de `Shape3D`
3. Definir vértices e faces no `__init__`

### Adicionar Novo Modelo de Iluminação
1. Criar classe em `rendering/lighting.py`
2. Herdar de classe base de iluminação
3. Implementar método `calculate_color()`

### Adicionar Novo Tipo de Puzzle
1. Adicionar enum em `PuzzleType`
2. Implementar lógica em `Puzzle.check_solution()`
3. Adicionar ao `LevelManager`

## Performance

### Otimizações Implementadas
- Uso de numpy para cálculos vetoriais
- Cache de matrizes de transformação
- Culling de faces não visíveis
- Limit de FPS configur

### Benchmarks Alvo
- FPS: 60 (configurável)
- Tempo de renderização por frame: < 16ms
- Memória: < 200MB

## Segurança

- Validação de entrada do usuário
- Tratamento de exceções em pontos críticos
- Sem execução de código dinâmico
- Sem acesso a arquivos sensíveis

## Testes

### Estrutura de Testes
```
tests/
├── unit/              # Testes de unidades individuais
│   ├── test_math_utils.py
│   └── test_color_utils.py
└── integration/       # Testes de integração
    └── test_transformations.py
```

### Cobertura
- Alvo: > 80% de cobertura
- Foco em lógica crítica (transformações, renderização)
- Testes de UI menos prioritários

## Documentação

- Docstrings em todos os módulos públicos
- Type hints para melhor IDE support
- Exemplos de uso em docstrings
- Documentação externa em `docs/`

---

**Última atualização:** 2025-12-03
