# MathShape Quest
## Aventura das Formas Geométricas

**Projeto Final - Computação Gráfica**

Equipe: [Nomes dos integrantes]

---

## 📋 Agenda

1. Introdução
2. História do Jogo
3. Problema do Mundo Real
4. Transformações Geométricas Implementadas
5. Modelos de Iluminação
6. Arquitetura do Sistema
7. Demonstração
8. Conclusões

---

## 🎮 Introdução

**MathShape Quest** é um jogo educativo que ensina:

- Transformações Geométricas 3D
- Modelos de Iluminação
- Renderização 3D
- Conceitos de Matemática e Geometria

**Objetivo:** Tornar o aprendizado de computação gráfica divertido e interativo!

---

## 📖 História do Jogo

**Cenário:**
- Mundo matemático chamado "Geometria"
- Formas geométricas perderam suas propriedades
- Vírus digital corrompeu as transformações

**Missão do Jogador:**
- Restaurar as formas usando transformações geométricas
- Ajustar iluminação para revelar padrões ocultos
- Resolver problemas matemáticos
- Salvar o mundo de Geometria!

---

## 🎯 Problema do Mundo Real

### Por que este jogo é importante?

**Desafios da Educação Matemática:**
- Conceitos abstratos são difíceis de visualizar
- Falta de engajamento dos estudantes
- Dificuldade em compreender geometria espacial

**Nossa Solução:**
- Aprendizado visual e interativo
- Feedback imediato
- Progressão gradual de dificuldade
- Gamificação do aprendizado

**Público-Alvo:**
- Estudantes de ensino fundamental e médio
- Estudantes de computação gráfica
- Qualquer pessoa interessada em geometria!

---

## ✨ Transformações Geométricas

### 5 Transformações Implementadas

#### 1. **TRANSLAÇÃO**
- Move objetos no espaço 3D
- Matriz: Deslocamento em X, Y, Z

```
[1  0  0  tx]
[0  1  0  ty]
[0  0  1  tz]
[0  0  0  1 ]
```

#### 2. **ROTAÇÃO**
- Gira objetos em torno dos eixos X, Y, Z
- Usa ângulos de Euler
- Matriz de rotação 3D

```
Rotação Y:
[cos(θ)   0  sin(θ)  0]
[0        1  0       0]
[-sin(θ)  0  cos(θ)  0]
[0        0  0       1]
```

---

## ✨ Transformações Geométricas (cont.)

#### 3. **ESCALA**
- Redimensiona objetos
- Escala uniforme ou não-uniforme

```
[sx  0   0   0]
[0   sy  0   0]
[0   0   sz  0]
[0   0   0   1]
```

#### 4. **REFLEXÃO**
- Espelha objetos em relação aos planos
- Cria simetria

```
Reflexão em X:
[-1  0  0  0]
[0   1  0  0]
[0   0  1  0]
[0   0  0  1]
```

#### 5. **DISTORÇÃO (Shear)**
- Deforma objetos de forma controlada
- Aplicada em diferentes planos

---

## 💡 Modelos de Iluminação

### 3 Modelos Implementados

#### 1. **Lambertiano (Diffuse)**
```
I = Ia + Id * (N · L)
```
- Modelo mais simples
- Apenas luz ambiente e difusa
- Eficiente computacionalmente

**Características:**
- Superfícies mate
- Sem brilho especular
- Ideal para objetos não-reflexivos

---

## 💡 Modelos de Iluminação (cont.)

#### 2. **Phong**
```
I = Ia + Id * (N · L) + Is * (R · V)^n
```
- Modelo completo
- Componentes: ambiente, difusa e especular
- Cálculo por pixel

**Características:**
- Superfícies brilhantes e realistas
- Destaque especular (brilho)
- Mais custoso computacionalmente

**Onde:**
- Ia: Luz ambiente
- Id: Luz difusa
- Is: Luz especular
- N: Normal da superfície
- L: Direção da luz
- R: Direção de reflexão
- V: Direção de visão
- n: Coeficiente de brilho

---

## 💡 Modelos de Iluminação (cont.)

#### 3. **Gouraud**
- Similar ao Phong
- Cálculo nos vértices
- Interpolação de cores

**Características:**
- Mais eficiente que Phong
- Menor qualidade visual
- Boa para superfícies suaves

**Diferenças:**
- **Phong**: Calcula iluminação por pixel
- **Gouraud**: Calcula nos vértices, interpola cores
- **Lambertiano**: Apenas difusa

---

## 🏗️ Arquitetura do Sistema

### Estrutura Modular

```
src/
├── transformations/    # Matrizes e transformações
├── rendering/          # Iluminação e renderização
├── objects/            # Objetos 3D (primitivas)
├── game_logic/         # Lógica do jogo
└── ui/                 # Interface gráfica
```

### Tecnologias Utilizadas
- **Python 3.8+**
- **Pygame 2.5.2**: Engine de jogo
- **NumPy 1.24.3**: Computação matemática

---

## 🏗️ Componentes Principais

### 1. Sistema de Transformações
- Classe `Matrix4x4`: Operações com matrizes 4x4
- Classe `GeometricTransformations`: API de alto nível
- Matrizes homogêneas para transformações

### 2. Sistema de Renderização
- Classe `Renderer`: Engine 3D para Pygame
- Classe `Camera`: Sistema de câmera orbital
- Projeção perspectiva
- Back-face culling

### 3. Modelos de Iluminação
- Classes separadas: `PhongShading`, `LambertianShading`, `GouraudShading`
- Cálculo de vetores normais
- Produto escalar para iluminação

---

## 🏗️ Componentes Principais (cont.)

### 4. Objetos 3D
- Classe base `Shape3D`
- Primitivas: `Cube`, `Sphere`, `Pyramid`, `Cylinder`, `Torus`
- Geração procedural de malhas
- Cálculo automático de normais

### 5. Sistema de Jogo
- **10 níveis progressivos**
- Sistema de puzzles variados
- Pontuação e vidas
- Sistema de dicas

### 6. Interface Gráfica
- Menus completos (principal, pausa, vitória, etc.)
- HUD informativo
- Painel de controles
- Mensagens de feedback

---

## 🎯 Níveis do Jogo

### Progressão Educativa

1. **Tutorial - Translação** 🟢
2. **Rotação** 🟢
3. **Escala** 🟢
4. **Reflexão** 🟡
5. **Distorção** 🟡
6. **Iluminação Lambertiana** 🟡
7. **Iluminação Phong** 🟠
8. **Iluminação Gouraud** 🟠
9. **Combinação de Transformações** 🔴
10. **Desafio Final** 🔴

**Cada nível ensina um conceito específico!**

---

## 🎮 Controles do Jogo

### Câmera
- **Mouse (arrastar)**: Rotacionar câmera
- **Scroll**: Zoom in/out

### Transformações
- **Tecla 1**: Translação
- **Tecla 2**: Rotação
- **Tecla 3**: Escala
- **Tecla 4**: Reflexão
- **Tecla 5**: Distorção

### Iluminação
- **Q**: Lambertiano
- **W**: Phong
- **E**: Gouraud

### Outros
- **H**: Dica
- **ESC**: Pausar

---

## 🎥 Demonstração

### [MOMENTO DA DEMONSTRAÇÃO]

**O que mostrar:**
1. Menu principal
2. Tutorial (Nível 1)
3. Aplicar cada transformação
4. Mudar modelos de iluminação
5. Resolver um puzzle
6. Sistema de pontuação

**Aspectos técnicos a destacar:**
- Rotação suave da câmera
- Mudança visual entre modelos de iluminação
- Efeito das transformações em tempo real

---

## 📊 Resultados Alcançados

### ✅ Requisitos Atendidos

**Transformações Geométricas:**
- ✅ Translação
- ✅ Rotação
- ✅ Escala
- ✅ Reflexão
- ✅ Distorção (Shear)

**Modelos de Iluminação:**
- ✅ Phong
- ✅ Lambertiano
- ✅ Gouraud

**Objetivo Educativo:**
- ✅ Resolve problema do mundo real
- ✅ Interface intuitiva
- ✅ Progressão de aprendizado

---

## 💡 Conceitos Aprendidos

### Durante o Desenvolvimento

**Matemática:**
- Álgebra linear (matrizes)
- Geometria 3D
- Vetores e produtos escalares/vetoriais

**Computação Gráfica:**
- Pipeline de renderização 3D
- Transformações homogêneas
- Modelos de iluminação
- Projeção perspectiva
- Coordenadas homogêneas

**Engenharia de Software:**
- Arquitetura modular
- Design patterns
- Game loop
- Sistema de eventos

---

## 🚀 Possíveis Melhorias Futuras

### Funcionalidades Extras

1. **Mais Níveis**
   - Níveis customizáveis
   - Editor de níveis

2. **Multiplayer**
   - Competição entre jogadores
   - Ranking online

3. **Mais Objetos 3D**
   - Formas complexas
   - Importação de modelos 3D

4. **Efeitos Visuais**
   - Partículas
   - Sombras
   - Texturas

5. **Som e Música**
   - Efeitos sonoros
   - Trilha sonora

---

## 📚 Referências

### Bibliografia

1. **Computer Graphics: Principles and Practice** (Foley et al.)
2. **OpenGL Programming Guide** (Red Book)
3. **Real-Time Rendering** (Akenine-Möller et al.)
4. **Pygame Documentation** - https://www.pygame.org/docs/
5. **NumPy Documentation** - https://numpy.org/doc/

### Recursos Online
- Khan Academy - Transformações Lineares
- Scratchapixel - Computação Gráfica
- Learn OpenGL - Iluminação

---

## 🎓 Conclusões

### O que conquistamos:

✅ **Implementação Completa**
- Todas as transformações geométricas
- Todos os modelos de iluminação
- Renderização 3D funcional

✅ **Objetivo Educativo**
- Jogo divertido e educativo
- Interface intuitiva
- Progressão gradual

✅ **Qualidade Técnica**
- Código bem estruturado
- Documentação completa
- Arquitetura modular

### Aprendizado:
- Conceitos fundamentais de computação gráfica
- Desenvolvimento de jogos educativos
- Trabalho em equipe

---

## ❓ Perguntas?

### Obrigado pela atenção!

**Equipe de Desenvolvimento:**
[Nomes dos integrantes]

**Código-fonte:**
[Link do repositório]

**Contato:**
[Email da equipe]

---

## 🙏 Agradecimentos

- Professor(a) da disciplina
- Colegas de turma
- Comunidade Pygame
- Comunidade Python

**Desenvolvido com ❤️ para a disciplina de Computação Gráfica**

---

# DEMONSTRAÇÃO AO VIVO

**Vamos jogar!** 🎮
