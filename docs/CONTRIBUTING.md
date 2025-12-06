# Guia de Contribuição

Obrigado por considerar contribuir com o MathShape Quest!

## Como Contribuir

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Projeto_computacao_grafica.git
cd Projeto_computacao_grafica

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instale as dependências de desenvolvimento
make install-dev
# ou
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 2. Estrutura do Projeto

```
Projeto_computacao_grafica/
├── src/                    # Código fonte principal
│   ├── core/              # Componentes centrais (config, constantes, exceções)
│   ├── transformations/   # Sistema de transformações geométricas
│   ├── rendering/         # Sistema de renderização 3D
│   ├── objects/           # Objetos 3D (primitivas)
│   ├── game_logic/        # Lógica do jogo (player, puzzles, níveis)
│   ├── ui/                # Interface do usuário
│   └── utils/             # Utilitários e helpers
├── tests/                 # Testes
│   ├── unit/             # Testes unitários
│   └── integration/      # Testes de integração
├── assets/               # Recursos do jogo
├── docs/                 # Documentação
└── scripts/              # Scripts auxiliares
```

### 3. Padrões de Código

#### Formatação
- Use **Black** para formatação automática: `make format`
- Limite de linha: **100 caracteres**
- Use aspas simples para strings

#### Estilo
- Siga a **PEP 8**
- Use type hints quando apropriado
- Docstrings em formato Google style

```python
def funcao_exemplo(param1: int, param2: str) -> bool:
    """
    Breve descrição da função

    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2

    Returns:
        Descrição do retorno

    Raises:
        ValueError: Quando ocorre erro X
    """
    pass
```

### 4. Testes

- Escreva testes para novas funcionalidades
- Mantenha cobertura de testes acima de 80%
- Execute testes antes de fazer commit:

```bash
make test           # Executa test_modules.py
make test-pytest    # Executa pytest
make test-cov       # Executa com cobertura
```

### 5. Commits

- Use mensagens claras e descritivas
- Formato: `tipo: descrição`

Tipos:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas gerais

Exemplo:
```bash
git commit -m "feat: adiciona suporte para cilindros texturizados"
git commit -m "fix: corrige cálculo de iluminação Phong"
```

### 6. Pull Requests

1. Crie uma branch para sua feature:
   ```bash
   git checkout -b feat/minha-feature
   ```

2. Faça suas alterações e commits

3. Execute os checks de qualidade:
   ```bash
   python scripts/check_code_quality.py
   ```

4. Push e crie um Pull Request:
   ```bash
   git push origin feat/minha-feature
   ```

5. Descreva claramente suas mudanças no PR

### 7. Checklist do PR

- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Todos os testes passam
- [ ] Documentação foi atualizada
- [ ] Não há conflitos com a branch main

## Estrutura de Módulos

### Core (`src/core/`)
- **config.py**: Configurações do jogo
- **constants.py**: Constantes do projeto
- **exceptions.py**: Exceções personalizadas

### Transformations (`src/transformations/`)
- **matrix.py**: Operações com matrizes 4x4
- **geometric.py**: Transformações geométricas

### Rendering (`src/rendering/`)
- **lighting.py**: Modelos de iluminação
- **camera.py**: Sistema de câmera
- **renderer.py**: Engine de renderização

### Utils (`src/utils/`)
- **math_utils.py**: Utilitários matemáticos
- **color_utils.py**: Manipulação de cores
- **time_utils.py**: Controle de tempo
- **validators.py**: Validações

## Reportando Bugs

Use as [Issues do GitHub](https://github.com/seu-usuario/Projeto_computacao_grafica/issues)

Inclua:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)
- Informações do sistema (OS, Python version)

## Dúvidas?

Entre em contato através das Issues ou abra uma Discussion no GitHub.

---

**Obrigado por contribuir!** 🎮✨
