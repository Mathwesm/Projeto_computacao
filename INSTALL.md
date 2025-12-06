# 🚀 Guia de Instalação - MathShape Quest

## Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes do Python)

## Verificar Instalação do Python

Abra o terminal/prompt de comando e execute:

```bash
python --version
```

ou

```bash
python3 --version
```

Você deve ver algo como: `Python 3.8.x` ou superior.

## Passos de Instalação

### 1. Baixar/Clonar o Projeto

Se estiver usando Git:
```bash
git clone https://github.com/seu-usuario/Projeto_computacao_grafica.git
cd Projeto_computacao_grafica
```

Ou simplesmente extraia o arquivo ZIP do projeto.

### 2. Criar Ambiente Virtual (Recomendado)

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

ou

```bash
python -m pip install -r requirements.txt
```

### 4. Executar o Jogo

```bash
python src/main.py
```

ou

```bash
cd src
python main.py
```

## Verificação da Instalação

Se tudo estiver correto, você deverá ver:

```
============================================================
MATHSHAPE QUEST - Aventura das Formas Geométricas
============================================================
Projeto de Computação Gráfica

Carregando jogo...
```

E uma janela do jogo deverá abrir.

## Problemas Comuns

### Erro: "No module named pygame"

**Solução:**
```bash
pip install pygame
```

### Erro: "No module named numpy"

**Solução:**
```bash
pip install numpy
```

### Erro: "Python não reconhecido como comando"

**Solução:**
- Certifique-se de que Python está instalado
- Adicione Python ao PATH do sistema
- Tente usar `python3` ao invés de `python`

### Janela do jogo não abre

**Solução:**
- Verifique se todas as dependências estão instaladas
- Certifique-se de que seu sistema suporta Pygame
- Execute o jogo a partir do diretório correto

## Instalação Manual das Dependências

Se `requirements.txt` não funcionar:

```bash
pip install pygame==2.5.2
pip install numpy==1.24.3
```

## Testando Componentes Individuais

Para testar apenas as transformações geométricas:

```python
cd src
python -c "from transformations import Matrix4x4; print('Transformacoes OK!')"
```

Para testar a renderização:

```python
python -c "from rendering import PhongShading; print('Renderizacao OK!')"
```

## Suporte

Se encontrar problemas:
1. Verifique a versão do Python
2. Certifique-se de que todas as dependências estão instaladas
3. Consulte a documentação do Pygame: https://www.pygame.org/docs/
4. Entre em contato com a equipe de desenvolvimento

## Desinstalação

Para remover o ambiente virtual:

```bash
# Desative o ambiente primeiro
deactivate

# Depois remova a pasta
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

---

**Desenvolvido com ❤️ para a disciplina de Computação Gráfica**
