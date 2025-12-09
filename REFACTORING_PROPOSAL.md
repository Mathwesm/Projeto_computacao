# 🔧 Proposta de Refatoração - MathShape Quest
## Análise de Programador Sênior

---

## 📊 Estado Atual do Projeto

### Estatísticas
- **Total de linhas**: ~6.000 linhas
- **Arquivo game.py**: 916 linhas (MUITO GRANDE)
- **Estrutura**: Modular mas com problemas de organização

---

## 🔴 Problemas Identificados

### 1. **God Class - Classe Game (~916 linhas)**
**Problema**: A classe `Game` viola o princípio Single Responsibility (SRP)
- Gerencia estado do jogo
- Gerencia renderização
- Gerencia input
- Gerencia lógica de puzzles
- Gerencia transições de estado
- Gerencia modo treino
- Gerencia tutorial

**Impacto**:
- Difícil de testar
- Difícil de manter
- Alto acoplamento
- Baixa coesão

### 2. **Duplicação de Código**
- Lógica de reset de vidas repetida em vários lugares
- Normalização de ações repetida
- Validação de puzzles espalhada

### 3. **Falta de Abstração**
- Estados do jogo misturados com lógica de negócio
- Sem padrão State para gerenciar estados
- Input handling acoplado à classe principal

### 4. **Violação de Princípios SOLID**

#### Single Responsibility (SRP) ❌
- `Game` faz muitas coisas
- `Menu` gerencia estado E renderização E input

#### Open/Closed (OCP) ❌
- Adicionar novo tipo de puzzle requer modificar várias classes
- Adicionar nova transformação requer mudanças em múltiplos lugares

#### Liskov Substitution (LSP) ✅
- Shapes são substituíveis (BOM)

#### Interface Segregation (ISP) ⚠️
- Poderia ter interfaces menores

#### Dependency Inversion (DIP) ❌
- Depende de implementações concretas, não abstrações

### 5. **Problemas de Arquitetura**
- Sem camada de serviços
- Sem separação clara entre apresentação e lógica
- Sem gerenciamento de eventos
- Sem sistema de estados robusto

### 6. **Gerenciamento de Estado Frágil**
- Estados gerenciados manualmente
- Fácil de ter bugs de transição (como vimos)
- Sem validação de transições

### 7. **Falta de Testes**
- Código difícil de testar (alto acoplamento)
- Sem testes unitários
- Sem testes de integração

---

## ✅ Proposta de Refatoração

### 🎯 Objetivo
Manter 100% da funcionalidade atual, mas com:
- Código mais limpo e organizado
- Fácil de testar
- Fácil de estender
- Seguindo princípios SOLID
- Usando padrões de design apropriados

---

## 🏗️ Nova Arquitetura Proposta

### 1. **Pattern: State Pattern para Game States**

```python
# src/game_states/base_state.py
from abc import ABC, abstractmethod

class GameState(ABC):
    """Estado base do jogo"""

    def __init__(self, game_context):
        self.context = game_context

    @abstractmethod
    def enter(self):
        """Chamado quando entra no estado"""
        pass

    @abstractmethod
    def exit(self):
        """Chamado quando sai do estado"""
        pass

    @abstractmethod
    def update(self, dt):
        """Atualiza lógica do estado"""
        pass

    @abstractmethod
    def render(self, surface):
        """Renderiza o estado"""
        pass

    @abstractmethod
    def handle_input(self, events):
        """Processa input"""
        pass


# src/game_states/menu_state.py
class MenuState(GameState):
    """Estado do menu"""

    def __init__(self, game_context):
        super().__init__(game_context)
        self.menu = Menu(game_context.width, game_context.height)

    def enter(self):
        """Inicializa menu"""
        self.menu.reset()

    def exit(self):
        """Cleanup do menu"""
        pass

    def update(self, dt):
        """Atualiza menu"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        action = self.menu.update(mouse_pos, mouse_pressed)

        if action == 'start_game':
            self.context.change_state('playing')
        elif action == 'start_training':
            self.context.change_state('training')
        # etc...

    def render(self, surface):
        """Desenha menu"""
        self.menu.draw(surface)

    def handle_input(self, events):
        """Processa input do menu"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.context.quit()


# src/game_states/playing_state.py
class PlayingState(GameState):
    """Estado jogando"""

    def __init__(self, game_context):
        super().__init__(game_context)
        self.level_controller = LevelController(game_context)
        self.puzzle_validator = PuzzleValidator()
        self.input_handler = GameInputHandler()

    def enter(self):
        """Inicializa gameplay"""
        self.level_controller.load_current_level()
        self.context.player.reset_attempt_state()

    def update(self, dt):
        """Atualiza gameplay"""
        self.level_controller.update(dt)

        # Verifica vitória
        if self.level_controller.is_level_complete():
            self.context.change_state('victory')

        # Verifica game over
        if self.context.player.lives <= 0:
            self.context.change_state('game_over')

    def render(self, surface):
        """Renderiza gameplay"""
        self.level_controller.render(surface)

    def handle_input(self, events):
        """Processa input do jogo"""
        actions = self.input_handler.process(events)
        self.level_controller.apply_actions(actions)


# src/game_states/training_state.py
class TrainingState(GameState):
    """Estado modo treino"""

    def __init__(self, game_context):
        super().__init__(game_context)
        self.training_controller = TrainingController(game_context)

    def enter(self):
        """Entra no modo treino - sem vidas/score"""
        self.training_controller.setup()

    # ... implementação similar
```

### 2. **Pattern: Command Pattern para Ações**

```python
# src/commands/base_command.py
from abc import ABC, abstractmethod

class Command(ABC):
    """Comando base"""

    @abstractmethod
    def execute(self, shape):
        """Executa comando"""
        pass

    @abstractmethod
    def undo(self, shape):
        """Desfaz comando"""
        pass


# src/commands/transform_commands.py
class TranslateCommand(Command):
    """Comando de translação"""

    def __init__(self, dx, dy, dz):
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.previous_transform = None

    def execute(self, shape):
        self.previous_transform = shape.get_transform_matrix()
        shape.translate(self.dx, self.dy, self.dz)
        return 'translate'  # Retorna tipo de ação

    def undo(self, shape):
        shape.set_transform_matrix(self.previous_transform)


class RotateCommand(Command):
    """Comando de rotação"""
    # Similar...


class ScaleCommand(Command):
    """Comando de escala"""
    # Similar...


# src/commands/command_invoker.py
class CommandInvoker:
    """Gerencia execução de comandos"""

    def __init__(self):
        self.history = []
        self.current_index = -1

    def execute(self, command, target):
        """Executa comando e armazena histórico"""
        action_type = command.execute(target)

        # Remove comandos após o índice atual (se voltamos e executamos novo)
        self.history = self.history[:self.current_index + 1]

        # Adiciona ao histórico
        self.history.append((command, target, action_type))
        self.current_index += 1

        return action_type

    def undo(self):
        """Desfaz último comando"""
        if self.current_index >= 0:
            command, target, _ = self.history[self.current_index]
            command.undo(target)
            self.current_index -= 1

    def redo(self):
        """Refaz comando"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            command, target, _ = self.history[self.current_index]
            command.execute(target)

    def get_action_history(self):
        """Retorna histórico de ações"""
        return [action_type for _, _, action_type in self.history[:self.current_index + 1]]

    def clear(self):
        """Limpa histórico"""
        self.history = []
        self.current_index = -1
```

### 3. **Pattern: Service Layer**

```python
# src/services/puzzle_service.py
class PuzzleService:
    """Serviço de gerenciamento de puzzles"""

    def __init__(self):
        self.validator = PuzzleValidator()
        self.hint_system = HintSystem()

    def validate_solution(self, puzzle, actions):
        """Valida solução do puzzle"""
        return self.validator.validate(puzzle, actions)

    def get_hint(self, puzzle, current_actions):
        """Retorna dica para o puzzle"""
        return self.hint_system.generate_hint(puzzle, current_actions)

    def calculate_score(self, puzzle, attempts):
        """Calcula pontuação"""
        base_score = 100 * puzzle.difficulty
        penalty = attempts * 20
        return max(0, base_score - penalty)


# src/services/player_service.py
class PlayerService:
    """Serviço de gerenciamento do jogador"""

    def __init__(self, player):
        self.player = player

    def lose_life(self):
        """Jogador perde uma vida"""
        self.player.lives -= 1
        return self.player.lives <= 0  # Retorna se é game over

    def reset_lives(self):
        """Reseta vidas"""
        self.player.lives = 3

    def add_score(self, points):
        """Adiciona pontos"""
        self.player.score += points

    def complete_level(self, level_id):
        """Marca nível como completo"""
        if level_id not in self.player.levels_completed:
            self.player.levels_completed.append(level_id)

    def can_access_level(self, level_id):
        """Verifica se pode acessar nível"""
        if level_id == 1:
            return True  # Primeiro nível sempre disponível

        # Pode acessar se completou o anterior
        return (level_id - 1) in self.player.levels_completed


# src/services/level_service.py
class LevelService:
    """Serviço de gerenciamento de níveis"""

    def __init__(self, level_manager):
        self.level_manager = level_manager

    def load_level(self, level_index):
        """Carrega um nível"""
        self.level_manager.goto_level(level_index)
        level = self.level_manager.get_current_level()
        level.reset()  # Sempre reseta ao carregar
        return level

    def next_level(self):
        """Avança para próximo nível"""
        if self.level_manager.next_level():
            return self.load_level(self.level_manager.current_level_index)
        return None

    def restart_level(self):
        """Reinicia nível atual"""
        return self.load_level(self.level_manager.current_level_index)
```

### 4. **Pattern: Event System**

```python
# src/events/event_system.py
from typing import Callable, Dict, List

class EventType:
    """Tipos de eventos do jogo"""
    PUZZLE_SOLVED = "puzzle_solved"
    PUZZLE_FAILED = "puzzle_failed"
    LEVEL_COMPLETE = "level_complete"
    LIFE_LOST = "life_lost"
    GAME_OVER = "game_over"
    SCORE_CHANGED = "score_changed"
    STATE_CHANGED = "state_changed"


class EventSystem:
    """Sistema centralizado de eventos"""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """Inscreve um listener para um evento"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        """Remove um listener"""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)

    def emit(self, event_type: str, data=None):
        """Dispara um evento"""
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)


# Uso:
# event_system.subscribe(EventType.PUZZLE_SOLVED, lambda data: print(f"Puzzle {data['puzzle_id']} solved!"))
# event_system.emit(EventType.PUZZLE_SOLVED, {'puzzle_id': 1, 'score': 100})
```

### 5. **Pattern: Strategy Pattern para Validação de Puzzles**

```python
# src/validators/base_validator.py
from abc import ABC, abstractmethod

class PuzzleValidationStrategy(ABC):
    """Estratégia base de validação"""

    @abstractmethod
    def validate(self, puzzle, actions):
        """Valida puzzle"""
        pass


# src/validators/sequence_validator.py
class SequenceValidator(PuzzleValidationStrategy):
    """Valida puzzles de sequência"""

    def validate(self, puzzle, actions):
        # Normaliza ações (scale_up/down -> scale)
        normalized_actions = [self._normalize_action(a) for a in actions]

        expected = [step['type'] for step in puzzle.solution.get('sequence', [])]

        return normalized_actions == expected

    def _normalize_action(self, action):
        """Normaliza nomes de ações"""
        if action in ['scale_up', 'scale_down']:
            return 'scale'
        return action


# src/validators/transformation_validator.py
class TransformationValidator(PuzzleValidationStrategy):
    """Valida puzzles de transformação"""

    def validate(self, puzzle, actions):
        # Lógica específica para transformação
        pass


# src/validators/lighting_validator.py
class LightingValidator(PuzzleValidationStrategy):
    """Valida puzzles de iluminação"""

    def validate(self, puzzle, shading_model):
        expected = puzzle.solution.get('shading_model')
        return shading_model == expected


# src/validators/puzzle_validator.py
class PuzzleValidator:
    """Valida puzzles usando estratégias"""

    def __init__(self):
        self.strategies = {
            'sequence': SequenceValidator(),
            'transformation': TransformationValidator(),
            'lighting': LightingValidator(),
        }

    def validate(self, puzzle, data):
        """Valida puzzle usando estratégia apropriada"""
        strategy = self.strategies.get(puzzle.type.value)
        if strategy:
            return strategy.validate(puzzle, data)
        return False
```

### 6. **Pattern: Factory para Níveis e Puzzles**

```python
# src/factories/level_factory.py
class LevelFactory:
    """Fábrica de níveis"""

    @staticmethod
    def create_level_1():
        """Cria nível 1"""
        level = Level(
            1,
            "Capítulo 1: O Despertar das Formas",
            "As formas geométricas perderam suas posições...",
            difficulty=2
        )

        # Adiciona componentes
        level.add_shape(ShapeFactory.create_cube())
        level.add_puzzle(PuzzleFactory.create_sequence_puzzle(
            steps=['translate', 'rotate', 'translate'],
            difficulty=2
        ))
        level.add_objective("Aplicar translação ao cubo")
        level.add_objective("Aplicar rotação ao cubo")

        return level

    @staticmethod
    def create_all_levels():
        """Cria todos os níveis"""
        return [
            LevelFactory.create_level_1(),
            LevelFactory.create_level_2(),
            # ...
        ]


# src/factories/puzzle_factory.py
class PuzzleFactory:
    """Fábrica de puzzles"""

    @staticmethod
    def create_sequence_puzzle(steps, difficulty):
        """Cria puzzle de sequência"""
        puzzle = Puzzle(PuzzleType.SEQUENCE, difficulty)
        puzzle.solution['sequence'] = [
            {'step': i+1, 'type': step, 'hint': f'Passo {i+1}: {step}'}
            for i, step in enumerate(steps)
        ]
        return puzzle

    @staticmethod
    def create_lighting_puzzle(required_shading, difficulty):
        """Cria puzzle de iluminação"""
        puzzle = Puzzle(PuzzleType.LIGHTING, difficulty)
        puzzle.solution['shading_model'] = required_shading
        return puzzle
```

---

## 📁 Nova Estrutura de Diretórios

```
src/
├── main.py                     # Entry point
│
├── core/                       # Núcleo do jogo
│   ├── game.py                # Classe Game refatorada (~150 linhas)
│   ├── game_context.py        # Contexto compartilhado
│   ├── config.py              # Configurações
│   └── constants.py           # Constantes
│
├── states/                     # Estados do jogo (State Pattern)
│   ├── base_state.py          # Estado base abstrato
│   ├── menu_state.py          # Estado de menu
│   ├── playing_state.py       # Estado jogando
│   ├── paused_state.py        # Estado pausado
│   ├── victory_state.py       # Estado de vitória
│   ├── game_over_state.py     # Estado game over
│   ├── training_state.py      # Estado modo treino
│   └── tutorial_state.py      # Estado tutorial
│
├── commands/                   # Comandos (Command Pattern)
│   ├── base_command.py        # Comando base
│   ├── transform_commands.py  # Comandos de transformação
│   └── command_invoker.py     # Gerenciador de comandos
│
├── services/                   # Camada de serviços
│   ├── puzzle_service.py      # Serviço de puzzles
│   ├── player_service.py      # Serviço de jogador
│   ├── level_service.py       # Serviço de níveis
│   └── save_service.py        # Serviço de salvamento
│
├── validators/                 # Validadores (Strategy Pattern)
│   ├── base_validator.py      # Validador base
│   ├── sequence_validator.py  # Valida sequências
│   ├── transform_validator.py # Valida transformações
│   ├── lighting_validator.py  # Valida iluminação
│   └── puzzle_validator.py    # Coordenador de validação
│
├── factories/                  # Fábricas (Factory Pattern)
│   ├── level_factory.py       # Cria níveis
│   ├── puzzle_factory.py      # Cria puzzles
│   └── shape_factory.py       # Cria formas
│
├── controllers/                # Controladores
│   ├── level_controller.py    # Controla nível atual
│   ├── training_controller.py # Controla modo treino
│   └── input_controller.py    # Processa input
│
├── events/                     # Sistema de eventos
│   ├── event_system.py        # Sistema centralizado
│   └── event_types.py         # Tipos de eventos
│
├── ui/                         # Interface
│   ├── components/            # Componentes UI reutilizáveis
│   │   ├── button.py
│   │   ├── panel.py
│   │   └── text_box.py
│   ├── views/                 # Views específicas
│   │   ├── menu_view.py
│   │   ├── hud_view.py
│   │   └── tutorial_view.py
│   └── styles/                # Estilos e temas
│       └── theme.py
│
├── game_logic/                 # Lógica do jogo
│   ├── entities/
│   │   ├── player.py
│   │   ├── level.py
│   │   └── puzzle.py
│   └── managers/
│       └── level_manager.py
│
├── rendering/                  # Renderização 3D
│   ├── camera.py
│   ├── renderer.py
│   ├── lighting/
│   │   ├── base_shading.py
│   │   ├── phong.py
│   │   ├── lambertian.py
│   │   └── gouraud.py
│   └── post_processing/
│
├── objects/                    # Objetos 3D
│   ├── base/
│   │   └── shape3d.py
│   └── primitives/
│       ├── cube.py
│       ├── sphere.py
│       ├── pyramid.py
│       ├── cylinder.py
│       └── torus.py
│
├── transformations/            # Transformações geométricas
│   ├── matrix.py
│   └── geometric.py
│
└── utils/                      # Utilitários
    ├── math_utils.py
    ├── color_utils.py
    └── validators.py
```

---

## 🎯 Classe Game Refatorada

```python
# src/core/game.py
class Game:
    """Classe principal do jogo - REFATORADA (~150 linhas)"""

    def __init__(self):
        """Inicializa o jogo"""
        pygame.init()

        # Contexto compartilhado
        self.context = GameContext()
        self.setup_window()
        self.setup_components()
        self.setup_states()

        # Sistema de eventos
        self.event_system = EventSystem()
        self.setup_event_listeners()

        # Estado inicial
        self.current_state = self.states['menu']
        self.current_state.enter()

    def setup_window(self):
        """Configura janela"""
        self.context.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption(TITLE)
        self.context.clock = pygame.time.Clock()

    def setup_components(self):
        """Configura componentes do jogo"""
        self.context.player = Player()
        self.context.level_manager = LevelManager()
        self.context.renderer = Renderer(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.context.camera = Camera()
        self.context.light = Light()

        # Serviços
        self.context.player_service = PlayerService(self.context.player)
        self.context.level_service = LevelService(self.context.level_manager)
        self.context.puzzle_service = PuzzleService()

    def setup_states(self):
        """Configura estados do jogo"""
        self.states = {
            'menu': MenuState(self.context),
            'playing': PlayingState(self.context),
            'paused': PausedState(self.context),
            'victory': VictoryState(self.context),
            'game_over': GameOverState(self.context),
            'training': TrainingState(self.context),
            'tutorial': TutorialState(self.context),
        }

    def setup_event_listeners(self):
        """Configura listeners de eventos"""
        self.event_system.subscribe(
            EventType.LEVEL_COMPLETE,
            lambda data: self.change_state('victory')
        )
        self.event_system.subscribe(
            EventType.GAME_OVER,
            lambda data: self.change_state('game_over')
        )

    def change_state(self, new_state_name):
        """Muda estado do jogo"""
        if new_state_name in self.states:
            self.current_state.exit()
            self.current_state = self.states[new_state_name]
            self.current_state.enter()

            self.event_system.emit(
                EventType.STATE_CHANGED,
                {'state': new_state_name}
            )

    def run(self):
        """Loop principal do jogo"""
        running = True

        while running:
            # Delta time
            dt = self.context.clock.tick(FPS) / 1000.0

            # Processa eventos
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Atualiza estado atual
            self.current_state.handle_input(events)
            self.current_state.update(dt)

            # Renderiza
            self.context.screen.fill((0, 0, 0))
            self.current_state.render(self.context.screen)
            pygame.display.flip()

        pygame.quit()
```

---

## 🧪 Testabilidade

Com essa refatoração, testes ficam muito mais fáceis:

```python
# tests/unit/test_puzzle_validator.py
import pytest
from src.validators.sequence_validator import SequenceValidator

class TestSequenceValidator:

    def test_validate_correct_sequence(self):
        """Testa sequência correta"""
        validator = SequenceValidator()
        puzzle = create_test_puzzle(['translate', 'rotate', 'scale'])
        actions = ['translate', 'rotate', 'scale']

        assert validator.validate(puzzle, actions) == True

    def test_validate_incorrect_sequence(self):
        """Testa sequência incorreta"""
        validator = SequenceValidator()
        puzzle = create_test_puzzle(['translate', 'rotate'])
        actions = ['rotate', 'translate']

        assert validator.validate(puzzle, actions) == False

    def test_normalize_scale_actions(self):
        """Testa normalização de scale_up/down"""
        validator = SequenceValidator()
        puzzle = create_test_puzzle(['scale'])
        actions = ['scale_up']

        assert validator.validate(puzzle, actions) == True


# tests/unit/test_player_service.py
class TestPlayerService:

    def test_lose_life(self):
        """Testa perder vida"""
        player = Player()
        service = PlayerService(player)

        is_game_over = service.lose_life()

        assert player.lives == 2
        assert is_game_over == False

    def test_game_over_on_last_life(self):
        """Testa game over ao perder última vida"""
        player = Player()
        player.lives = 1
        service = PlayerService(player)

        is_game_over = service.lose_life()

        assert player.lives == 0
        assert is_game_over == True


# tests/integration/test_level_completion.py
class TestLevelCompletion:

    def test_complete_level_unlocks_next(self):
        """Testa que completar nível desbloqueia próximo"""
        player = Player()
        player_service = PlayerService(player)

        # Completa nível 1
        player_service.complete_level(1)

        # Deve poder acessar nível 2
        assert player_service.can_access_level(2) == True

        # NÃO deve poder acessar nível 3
        assert player_service.can_access_level(3) == False
```

---

## 📈 Benefícios da Refatoração

### 1. **Manutenibilidade** 📝
- Arquivos menores (~150-300 linhas cada)
- Responsabilidades claras
- Fácil encontrar código

### 2. **Testabilidade** 🧪
- Componentes isolados
- Fácil criar mocks
- Testes unitários simples

### 3. **Extensibilidade** 🔧
- Adicionar novo tipo de puzzle? Crie novo validator
- Adicionar novo estado? Crie nova State class
- Adicionar novo comando? Crie novo Command

### 4. **Reusabilidade** ♻️
- Serviços podem ser usados em qualquer lugar
- Comandos são independentes
- Validadores são plugáveis

### 5. **Legibilidade** 👓
- Código auto-documentado
- Padrões conhecidos
- Estrutura clara

### 6. **Performance** ⚡
- Event system evita polling
- Command pattern permite otimização
- Melhor gerenciamento de memória

### 7. **Colaboração** 👥
- Múltiplos devs podem trabalhar simultaneamente
- Menos conflitos de merge
- Código review mais fácil

---

## 🚀 Plano de Implementação

### Fase 1: Fundação (Semana 1)
1. Criar estrutura de diretórios
2. Implementar Event System
3. Implementar Command Pattern
4. Criar Service Layer base

### Fase 2: Estados (Semana 2)
1. Implementar State Pattern
2. Migrar MenuState
3. Migrar PlayingState
4. Migrar outros estados

### Fase 3: Validação (Semana 3)
1. Implementar Strategy Pattern para validação
2. Criar validadores específicos
3. Integrar com PuzzleService

### Fase 4: Testes (Semana 4)
1. Criar testes unitários
2. Criar testes de integração
3. Garantir cobertura >80%

### Fase 5: Refinamento (Semana 5)
1. Documentação
2. Code review
3. Otimizações

---

## 📊 Comparação: Antes vs Depois

### Antes
```python
# game.py - 916 linhas
class Game:
    def update_playing(self):
        # 200+ linhas de lógica misturada
        if puzzle solved:
            # código aqui
        if game over:
            # código aqui
        if lives lost:
            # código aqui
        # etc...
```

### Depois
```python
# game.py - ~150 linhas
class Game:
    def run(self):
        while running:
            self.current_state.update(dt)

# playing_state.py - ~200 linhas
class PlayingState(GameState):
    def update(self, dt):
        self.level_controller.update(dt)

        if self.level_controller.is_complete():
            self.context.change_state('victory')

# level_controller.py - ~150 linhas
class LevelController:
    def update(self, dt):
        # Lógica específica de nível
```

---

## 🎓 Conclusão

Esta refatoração transforma o código de:
- ❌ Procedural e monolítico
- ❌ Difícil de testar
- ❌ Difícil de estender

Para:
- ✅ Orientado a objetos com padrões de design
- ✅ Altamente testável
- ✅ Facilmente extensível
- ✅ Manutenível a longo prazo
- ✅ Profissional e escalável

**O jogo permanece 100% funcional, mas o código fica de nível sênior.**

---

## 💡 Dica Final

**Não refatore tudo de uma vez!**
- Comece por uma área pequena
- Adicione testes
- Refatore incrementalmente
- Mantenha o jogo funcionando

**"Make it work, make it right, make it fast"** - Kent Beck

---

*Documento criado por programador sênior para guiar refatoração profissional do MathShape Quest.*
