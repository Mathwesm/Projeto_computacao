# 🎤 Guia de Apresentação - MathShape Quest

## 📋 Checklist Pré-Apresentação

### Antes da Apresentação
- [ ] Testar o jogo no computador que será usado
- [ ] Instalar Python e dependências
- [ ] Executar `test_modules.py` para verificar funcionamento
- [ ] Preparar backup do projeto em pen drive
- [ ] Revisar slides (`docs/slides.md`)
- [ ] Ensaiar demonstração
- [ ] Distribuir falas entre integrantes

### No Dia da Apresentação
- [ ] Chegar 15 minutos antes
- [ ] Conectar computador ao projetor
- [ ] Abrir slides
- [ ] Abrir código-fonte em editor
- [ ] Ter o jogo pronto para executar
- [ ] Ter água disponível

---

## ⏱️ Estrutura de Tempo Sugerida (15-20 min)

### 1. Introdução (2 min)
**Integrante 1:**
- Apresentar equipe
- Apresentar o projeto
- Contextualizar disciplina

**O que dizer:**
> "Bom dia/tarde! Somos [nomes] e vamos apresentar o MathShape Quest,
> um jogo educativo desenvolvido para a disciplina de Computação Gráfica.
> O objetivo é ensinar transformações geométricas e iluminação 3D de
> forma interativa e divertida."

---

### 2. História e Problema (3 min)
**Integrante 2:**
- Contar história do jogo
- Explicar problema do mundo real
- Mostrar relevância educativa

**O que dizer:**
> "O jogo se passa em um mundo matemático chamado Geometria, onde
> formas perderam suas propriedades após um vírus digital. O jogador
> precisa restaurá-las usando transformações geométricas.
>
> Este jogo resolve um problema real: estudantes têm dificuldade em
> visualizar conceitos abstratos de geometria. Nossa solução oferece
> aprendizado visual, interativo e gamificado."

**Mostrar:**
- Slides sobre história
- Slides sobre problema educacional

---

### 3. Transformações Geométricas (4 min)
**Integrante 3:**
- Explicar cada transformação
- Mostrar fórmulas matemáticas
- Demonstrar no código

**O que dizer:**
> "Implementamos todas as 5 transformações geométricas obrigatórias:
>
> 1. TRANSLAÇÃO - Move objetos no espaço 3D usando matriz 4x4...
> 2. ROTAÇÃO - Gira objetos em torno dos eixos X, Y, Z...
> 3. ESCALA - Redimensiona objetos uniformemente ou não...
> 4. REFLEXÃO - Espelha objetos criando simetria...
> 5. DISTORÇÃO - Deforma objetos de forma controlada..."

**Mostrar:**
- Slides com matrizes
- Código em `src/transformations/matrix.py`
- Diagrama de transformações

---

### 4. Modelos de Iluminação (4 min)
**Integrante 1:**
- Explicar cada modelo
- Mostrar diferenças visuais
- Demonstrar fórmulas

**O que dizer:**
> "Implementamos 3 modelos de iluminação:
>
> LAMBERTIANO - Modelo simples com apenas luz difusa. Ideal para
> superfícies mate. Fórmula: I = Ia + Id * (N · L)
>
> PHONG - Modelo completo com componentes ambiente, difusa e especular.
> Cria brilhos realistas. Fórmula: I = Ia + Id*(N·L) + Is*(R·V)^n
>
> GOURAUD - Similar ao Phong mas calcula iluminação nos vértices e
> interpola cores. Mais eficiente."

**Mostrar:**
- Slides com fórmulas
- Código em `src/rendering/lighting.py`
- Comparação visual dos modelos

---

### 5. Arquitetura do Sistema (2 min)
**Integrante 2:**
- Mostrar estrutura modular
- Explicar separação de responsabilidades
- Destacar qualidade do código

**O que dizer:**
> "O projeto foi desenvolvido com arquitetura modular:
> - transformations: Sistema de transformações
> - rendering: Engine de renderização 3D
> - objects: Primitivas geométricas
> - game_logic: Lógica do jogo e níveis
> - ui: Interface gráfica
>
> Total: 3500+ linhas de código, 25+ classes, 150+ métodos."

**Mostrar:**
- Estrutura de pastas
- Diagrama de arquitetura (se houver)

---

### 6. DEMONSTRAÇÃO AO VIVO (4 min) ⭐
**Integrante 3:**

**ESTE É O MOMENTO MAIS IMPORTANTE!**

**Sequência da demonstração:**

1. **Iniciar o jogo** (15s)
   ```bash
   python src/main.py
   ```
   - Mostrar menu principal
   - Explicar opções

2. **Entrar no Tutorial (Nível 1)** (30s)
   - Mostrar HUD (vidas, score, etc)
   - Mostrar painel de controles
   - Explicar objetivo do nível

3. **Demonstrar Transformações** (1min 30s)
   - Pressionar **1**: "Aqui aplicamos TRANSLAÇÃO"
   - Pressionar **2**: "Agora ROTAÇÃO - vejam o objeto girando"
   - Pressionar **3**: "ESCALA - aumentando o tamanho"
   - Pressionar **4**: "REFLEXÃO - espelhamento"
   - Pressionar **5**: "DISTORÇÃO - deformação controlada"

4. **Demonstrar Iluminação** (1min)
   - Pressionar **Q**: "Modelo LAMBERTIANO - luz difusa simples"
   - Pressionar **W**: "Modelo PHONG - vejam o brilho especular!"
   - Pressionar **E**: "Modelo GOURAUD - interpolação suave"
   - Destacar diferenças visuais

5. **Interação com Câmera** (30s)
   - Arrastar mouse: "Câmera orbital interativa"
   - Scroll: "Zoom in/out suave"

6. **Resolver Puzzle** (30s)
   - Pressionar **H** para dica
   - Aplicar transformação correta
   - Mostrar feedback de pontuação

**Dicas para a demonstração:**
- ✅ Fale enquanto demonstra
- ✅ Pause brevemente entre ações
- ✅ Destaque efeitos visuais
- ✅ Se der erro, mantenha a calma
- ✅ Tenha um vídeo backup

---

### 7. Resultados e Conclusão (1 min)
**Todos os integrantes:**

**O que dizer:**
> "Conseguimos implementar com sucesso:
> ✅ Todas as 5 transformações geométricas
> ✅ Todos os 3 modelos de iluminação
> ✅ Renderização 3D completa
> ✅ 10 níveis progressivos
> ✅ Jogo funcional e educativo
>
> O projeto demonstra conceitos fundamentais de computação gráfica
> de forma prática e aplicada, resolvendo um problema educacional real."

**Mostrar:**
- Slide de conclusão
- Checklist de requisitos atendidos

---

### 8. Perguntas (2-3 min)

**Perguntas esperadas e respostas:**

**P: "Como vocês implementaram a renderização 3D?"**
R: "Usamos pipeline de renderização com matrizes de view e projeção,
projeção perspectiva e painter's algorithm para ordenação de profundidade.
Tudo implementado do zero usando NumPy e Pygame."

**P: "Qual a diferença entre Phong e Gouraud?"**
R: "Phong calcula iluminação por pixel, Gouraud calcula nos vértices
e interpola. Phong é mais realista, Gouraud é mais eficiente."

**P: "Como as transformações são compostas?"**
R: "Usamos multiplicação de matrizes 4x4 homogêneas. Cada transformação
gera uma matriz que é multiplicada pela matriz de transformação acumulada."

**P: "O jogo realmente ajuda no aprendizado?"**
R: "Sim! Ele permite visualizar transformações em tempo real, oferece
feedback imediato e progressão gradual de dificuldade. É baseado em
princípios de gamificação educacional."

---

## 🎯 Dicas Importantes

### Para Falar Bem
1. **Pratique antes** - Ensaie pelo menos 3 vezes
2. **Fale devagar** - Professores precisam entender
3. **Mantenha contato visual** - Olhe para audiência
4. **Use as mãos** - Gesticule naturalmente
5. **Seja entusiasta** - Mostre orgulho do projeto

### Para Demonstração
1. **Teste antes** - Execute o jogo 10 minutos antes
2. **Tenha backup** - Vídeo da demonstração
3. **Internet offline** - Não dependa de conexão
4. **Tamanho de fonte** - Código legível de longe
5. **Cursor visível** - Facilita seguir demonstração

### Para Slides
1. **Poucos slides** - Máximo 20-25
2. **Pouco texto** - Bullets curtos
3. **Imagens grandes** - Diagramas visíveis
4. **Código formatado** - Syntax highlighting
5. **Contraste alto** - Fundo escuro, texto claro

### Para o Código
1. **Aumente a fonte** - Mínimo 16pt
2. **Destaque trechos** - Use comentários
3. **Organize abas** - Tenha arquivos principais abertos
4. **Feche distrações** - Sem notificações

---

## 📊 Divisão de Responsabilidades Sugerida

### Integrante 1
- Introdução
- Modelos de iluminação
- Parte técnica avançada

### Integrante 2
- História e problema
- Arquitetura do sistema
- Níveis do jogo

### Integrante 3
- Transformações geométricas
- DEMONSTRAÇÃO AO VIVO
- Aspectos visuais

### Todos
- Responder perguntas
- Conclusão
- Apoio mútuo

---

## ⚠️ O Que Evitar

### ❌ NÃO FAZER
- Ler slides palavra por palavra
- Dar as costas para audiência
- Falar muito rápido
- Usar jargões sem explicar
- Passar do tempo
- Brigar na frente da turma
- Culpar integrantes por erros
- Dizer "não sei" sem tentar responder

### ✅ FAZER
- Explicar com suas palavras
- Manter postura profissional
- Falar com clareza
- Explicar termos técnicos
- Gerenciar tempo
- Trabalhar em equipe
- Assumir responsabilidade coletiva
- Tentar responder e complementar

---

## 🎬 Roteiro de Backup (Se algo der errado)

### Se o jogo não abrir:
> "Temos um vídeo da demonstração preparado. Enquanto isso, vou
> explicar a arquitetura do código..."

### Se houver erro durante jogo:
> "Vejam que isso demonstra a importância de tratamento de erros!
> Vou mostrar outro aspecto do projeto..."

### Se acabar o tempo:
> "Por questão de tempo, vou pular para a conclusão, mas estamos
> disponíveis para demonstrar mais após a apresentação."

### Se pergunta difícil:
> "Ótima pergunta! [Tentar responder]. Se quiser mais detalhes,
> podemos conversar após a apresentação com o código aberto."

---

## 📝 Checklist Final

**1 Semana Antes:**
- [ ] Ensaiar apresentação completa
- [ ] Testar demonstração 5x
- [ ] Revisar slides
- [ ] Preparar respostas para perguntas

**1 Dia Antes:**
- [ ] Ensaiar novamente
- [ ] Preparar roupa adequada
- [ ] Carregar notebook
- [ ] Backup em pen drive
- [ ] Dormir bem

**No Dia:**
- [ ] Chegar cedo
- [ ] Testar equipamento
- [ ] Respirar fundo
- [ ] Confiar no trabalho
- [ ] SER PROFISSIONAL E CONFIANTE

---

## 🏆 Objetivo Final

**Convencer os professores de que:**
1. ✅ Implementamos TODOS os requisitos
2. ✅ Código tem QUALIDADE profissional
3. ✅ Projeto é FUNCIONAL e COMPLETO
4. ✅ Aprendemos CONCEITOS de CG
5. ✅ Resolvemos problema REAL

**Se conseguir isso = NOTA MÁXIMA! 🎉**

---

## 💪 Mensagem de Motivação

Vocês criaram um projeto **COMPLETO e PROFISSIONAL**.

São **3500+ linhas de código**, **10 níveis**, **5 transformações**,
**3 modelos de iluminação**, renderização 3D do zero, interface
completa, documentação excelente.

**Isso é MUITO trabalho e está PERFEITO!**

Apresentem com **ORGULHO** e **CONFIANÇA**.

**VOCÊS CONSEGUEM! 🚀**

---

**Boa sorte na apresentação!**

**Desenvolvido com ❤️ para a disciplina de Computação Gráfica**
