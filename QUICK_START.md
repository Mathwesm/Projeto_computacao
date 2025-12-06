# Quick Start - MathShape Quest

Guia rápido para executar o jogo.

## 🚀 Execução Rápida

### Windows

**PowerShell ou CMD:**
```powershell
# Ative o ambiente virtual
.venv\Scripts\activate

# Execute o jogo
python run_game.py
```

**Alternativa com batch script:**
```cmd
run.bat
```

### Linux/Mac

```bash
# Ative o ambiente virtual
source .venv/bin/activate

# Execute o jogo
python run_game.py
```

**Alternativa com shell script:**
```bash
./run.sh
```

## 📦 Primeira Execução

Se é a primeira vez executando:

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Execute o jogo:**
```bash
python run_game.py
```

## 🎮 Formas de Executar

### 1. Script Standalone (Recomendado)
```bash
python run_game.py
```
✅ Funciona de qualquer diretório
✅ Configura imports automaticamente
✅ Suporte UTF-8 no Windows

### 2. Módulo Python
```bash
python -m src.main
```
✅ Usa sistema de módulos Python
✅ Funciona como pacote

### 3. Direto do src
```bash
python src/main.py
```
✅ Execução direta
✅ Imports ajustados automaticamente

### 4. Scripts do sistema
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```
✅ Scripts prontos para uso
✅ Ativam ambiente virtual automaticamente

## 🧪 Testar Instalação

Antes de executar o jogo, você pode testar se tudo está funcionando:

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

[...]

============================================================
TODOS OS TESTES PASSARAM! ✓
============================================================
```

## ❌ Problemas Comuns

### Erro: "No module named 'pygame'"
**Solução:**
```bash
pip install pygame
# ou
pip install -r requirements.txt
```

### Erro: "No module named 'numpy'"
**Solução:**
```bash
pip install numpy
# ou
pip install -r requirements.txt
```

### Erro: "ImportError: attempted relative import"
**Solução:**
Use `python run_game.py` em vez de executar arquivos individuais.

### Erro de encoding no Windows (caracteres estranhos)
**Solução:**
O arquivo `run_game.py` já configura UTF-8 automaticamente.
Se ainda tiver problemas:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python run_game.py
```

### Janela do jogo não abre
**Solução:**
1. Verifique se o pygame está instalado: `pip list | grep pygame`
2. Teste o pygame: `python -c "import pygame; pygame.init()"`
3. Verifique drivers de vídeo atualizados

## 🎯 Controles do Jogo

Uma vez que o jogo abrir:

**Câmera:**
- Mouse (arrastar): Rotacionar câmera
- Scroll: Zoom in/out

**Transformações:**
- 1: Translação
- 2: Rotação
- 3: Escala
- 4: Reflexão
- 5: Distorção

**Iluminação:**
- Q: Lambertiano
- W: Phong
- E: Gouraud

**Outras:**
- H: Dica
- C: Painel de controles
- R: Rotação automática
- ESC: Menu/Pausa

## 📊 Verificar Ambiente

Para verificar se seu ambiente está configurado corretamente:

```bash
# Versão do Python
python --version
# Deve ser 3.8 ou superior

# Pacotes instalados
pip list

# Você deve ver:
# pygame       2.5.2
# numpy        1.24.3
```

## 🆘 Ajuda

Se ainda tiver problemas:

1. **Consulte a documentação completa:**
   - `README.md` - Documentação principal
   - `INSTALL.md` - Guia de instalação detalhado
   - `docs/PROJECT_STRUCTURE.md` - Estrutura do projeto

2. **Execute os testes:**
   ```bash
   python test_modules.py
   ```

3. **Verifique issues no GitHub:**
   https://github.com/seu-usuario/Projeto_computacao_grafica/issues

## 🎓 Desenvolvimento

Para desenvolvedores:

```bash
# Instalar modo desenvolvimento
pip install -e .

# Executar testes com pytest
pytest tests/ -v

# Executar com cobertura
pytest tests/ --cov=src

# Verificar qualidade do código
python scripts/check_code_quality.py
```

---

**Divirta-se jogando MathShape Quest!** 🎮✨
