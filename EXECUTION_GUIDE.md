# Guia de Execução - MathShape Quest

## ✅ Problema Resolvido

O erro `ImportError: attempted relative import with no known parent package` foi corrigido!

### O que foi feito?

1. **Corrigido `src/main.py`:**
   - Adicionado suporte para imports tanto relativos quanto absolutos
   - Configurado sys.path automaticamente

2. **Corrigido `src/game.py`:**
   - Imports funcionam tanto como módulo quanto como script direto

3. **Criado `run_game.py`:**
   - Script standalone na raiz do projeto
   - Funciona de qualquer diretório
   - Configura imports automaticamente
   - Suporte UTF-8 para Windows

## 🚀 Como Executar (Passo a Passo)

### Método 1: Script Standalone (RECOMENDADO)

```powershell
# No PowerShell/CMD, dentro da pasta do projeto:
python run_game.py
```

✅ **Vantagens:**
- Funciona sempre
- Não precisa se preocupar com imports
- Suporte UTF-8 automático
- Mensagens amigáveis

### Método 2: Módulo Python

```bash
python -m src.main
```

✅ **Vantagens:**
- Usa sistema de módulos Python
- Imports relativos funcionam corretamente

### Método 3: Direto do src

```bash
python src/main.py
```

✅ **Vantagens:**
- Execução direta
- Imports ajustados automaticamente

### Método 4: Scripts Prontos

**Windows:**
```cmd
run.bat
```

**Linux/Mac:**
```bash
./run.sh
```

## 📁 Estrutura de Imports

### Antes (Não funcionava diretamente)
```python
# src/main.py
from .game import main  # ❌ Erro ao executar diretamente
```

### Depois (Funciona sempre)
```python
# src/main.py
import sys
import os

# Configura path
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Tenta import relativo, depois absoluto
try:
    from game import main
except ImportError:
    from src.game import main
```

## 🧪 Testar Antes de Executar

Sempre rode os testes antes de executar o jogo:

```bash
python test_modules.py
```

Você deve ver:
```
============================================================
TESTE DE MODULOS - MathShape Quest
============================================================

1. Testando transformações geométricas...
   ✓ Matrix4x4 OK
   ✓ GeometricTransformations OK
   ✓ Transformações: PASSOU

2. Testando renderização e iluminação...
   ✓ Light OK
   ✓ Modelos de iluminação OK
   ✓ Camera OK
   ✓ Renderer OK
   ✓ Renderização: PASSOU

3. Testando objetos 3D...
   ✓ Cubo: 8 vértices
   ✓ Esfera: 162 vértices
   ✓ Pirâmide: 5 vértices
   ✓ Cilindro: 34 vértices
   ✓ Torus: 128 vértices
   ✓ Objetos 3D: PASSOU

4. Testando lógica do jogo...
   ✓ Player OK (Score: 100)
   ✓ Puzzle OK (Tipo: transformation)
   ✓ LevelManager OK (10 níveis)
   ✓ Nível atual: Capítulo 1: O Despertar das Formas
   ✓ Lógica do jogo: PASSOU

5. Testando interface...
   ✓ Button importado OK
   ✓ Menu importado OK
   ✓ HUD importado OK
   ✓ Interface: PASSOU

6. Testando configurações...
   ✓ Resolução: 1280x720
   ✓ FPS: 60
   ✓ Transformações: 5
   ✓ Modelos de iluminação: 3
   ✓ Versão: 1.0.0
   ✓ Configurações: PASSOU

============================================================
TODOS OS TESTES PASSARAM! ✓
============================================================
```

## ❌ Troubleshooting

### Problema: "No module named 'pygame'"

**Solução:**
```bash
pip install -r requirements.txt
```

### Problema: "ImportError: attempted relative import"

**Solução:**
Use `python run_game.py` em vez de executar arquivos individuais.

### Problema: Caracteres estranhos no Windows

**Solução:**
O `run_game.py` já configura UTF-8 automaticamente. Se ainda tiver problemas:
```powershell
chcp 65001
python run_game.py
```

### Problema: Janela não abre

**Checklist:**
1. ✅ Pygame está instalado? `pip show pygame`
2. ✅ Drivers de vídeo atualizados?
3. ✅ Teste pygame: `python -c "import pygame; pygame.init()"`

## 📝 Resumo de Comandos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Testar instalação
python test_modules.py

# 3. Executar o jogo (escolha um):
python run_game.py          # Recomendado
python -m src.main          # Como módulo
python src/main.py          # Direto
./run.sh                    # Linux/Mac
run.bat                     # Windows

# 4. Desenvolvimento:
pip install -e .            # Instalar modo dev
pytest tests/ -v            # Executar testes
python scripts/check_code_quality.py  # Verificar qualidade
```

## 🎯 Próximos Passos

Agora que o jogo está funcionando:

1. **Jogue!** 🎮
   - Explore os 10 níveis
   - Aprenda transformações geométricas
   - Experimente diferentes modelos de iluminação

2. **Customize:** 🎨
   - Adicione suas próprias formas em `src/objects/primitives.py`
   - Crie novos níveis em `src/game_logic/level.py`
   - Modifique cores em `src/core/config.py`

3. **Contribua:** 🤝
   - Leia `docs/CONTRIBUTING.md`
   - Adicione features
   - Reporte bugs no GitHub

## 📚 Documentação Adicional

- **README.md**: Documentação principal do projeto
- **QUICK_START.md**: Guia rápido de início
- **INSTALL.md**: Instruções detalhadas de instalação
- **docs/ARCHITECTURE.md**: Arquitetura do sistema
- **docs/PROJECT_STRUCTURE.md**: Estrutura de pastas
- **docs/CONTRIBUTING.md**: Como contribuir

## ✨ Status

✅ Todos os imports corrigidos
✅ Múltiplas formas de execução funcionando
✅ Testes passando (6/6)
✅ Compatibilidade Windows/Linux/Mac
✅ Suporte UTF-8
✅ Documentação completa

---

**O jogo está pronto para ser executado!** 🚀

Execute: `python run_game.py`
