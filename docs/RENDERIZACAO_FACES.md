# Renderização de Faces - Backface Culling

## Problema Resolvido

**Antes:** Quando você olhava os objetos por baixo, eles apareciam vazios/sem base.

**Agora:** Todos os lados dos objetos são visíveis, incluindo as bases!

## O que foi mudado?

### 1. Backface Culling Desabilitado

O sistema de renderização tinha um recurso chamado "backface culling" que não desenhava faces que estavam "de costas" para a câmera. Isso é uma otimização comum em 3D, mas fazia com que você não visse as bases dos objetos.

**Arquivo:** `src/rendering/renderer.py` (linha 184-200)

**Antes:**
```python
# Back-face culling
centroid = np.mean(face_vertices, axis=0)
view_dir = centroid - np.array(camera.position)
if np.dot(normal, view_dir) > 0:
    continue  # ❌ Não renderiza faces de trás
```

**Depois:**
```python
# Back-face culling (opcional via config)
centroid = np.mean(face_vertices, axis=0)
view_dir = centroid - np.array(camera.position)
is_backface = np.dot(normal, view_dir) > 0

# Se backface culling estiver ativo, pula faces de trás
if ENABLE_BACKFACE_CULLING and is_backface:
    continue

# Se a face está de costas, inverte a normal para iluminação correta
if is_backface:
    normal = -normal  # ✅ Renderiza mas corrige iluminação
```

### 2. Nova Configuração Adicionada

**Arquivo:** `src/core/config.py` (linha 38)

```python
# Configurações de renderização 3D
NEAR_PLANE = 0.1
FAR_PLANE = 1000.0
FOV = 90  # Field of view em graus
ENABLE_BACKFACE_CULLING = False  # ✅ Se False, mostra bases dos objetos
```

## Como Funciona Agora?

### Modo Atual (ENABLE_BACKFACE_CULLING = False)

✅ **Vantagens:**
- Você vê todos os lados dos objetos
- Bases, topos e todos os lados são visíveis
- Melhor para visualização educacional
- Você pode girar a câmera e ver o objeto completo

⚠️ **Desvantagens:**
- Renderiza mais faces (pode ser um pouco mais lento)
- Alguns pixels são desenhados duas vezes

### Modo Otimizado (ENABLE_BACKFACE_CULLING = True)

✅ **Vantagens:**
- Mais rápido (renderiza menos faces)
- Melhor performance

❌ **Desvantagens:**
- Não mostra faces de trás
- Objetos parecem vazios por baixo

## Como Alterar o Comportamento

Para mudar entre os modos, edite `src/core/config.py`:

```python
# Para ver todas as faces (atual):
ENABLE_BACKFACE_CULLING = False

# Para otimizar performance:
ENABLE_BACKFACE_CULLING = True
```

## Detalhes Técnicos

### O que é Backface Culling?

Backface culling é uma técnica de otimização em computação gráfica 3D que:

1. **Calcula a normal da face** (vetor perpendicular à superfície)
2. **Calcula a direção da câmera** (da face para a câmera)
3. **Faz o produto escalar** entre normal e direção
4. **Se positivo:** face está de costas → não renderiza
5. **Se negativo:** face está de frente → renderiza

### Código Explicado

```python
# 1. Calcula centro da face
centroid = np.mean(face_vertices, axis=0)

# 2. Vetor da face para a câmera
view_dir = centroid - np.array(camera.position)

# 3. Produto escalar (dot product)
is_backface = np.dot(normal, view_dir) > 0

# 4. Decisão
if ENABLE_BACKFACE_CULLING and is_backface:
    continue  # Pula esta face

# 5. Correção de iluminação para faces de trás
if is_backface:
    normal = -normal  # Inverte normal
```

### Por que Inverter a Normal?

Quando uma face está de costas mas ainda assim é renderizada, sua normal aponta na direção oposta à câmera. Isso faria a iluminação ficar incorreta (muito escura).

Ao inverter a normal (`normal = -normal`), garantimos que a iluminação seja calculada corretamente, como se a face estivesse de frente.

## Objetos que Agora Têm Bases Visíveis

Todos os objetos 3D já tinham bases definidas no código, mas não eram visíveis:

### ✅ Cubo
- 6 faces completas (frente, trás, topo, base, esquerda, direita)
- Agora você vê todas as 6 faces

### ✅ Pirâmide
- Base quadrada + 4 lados triangulares
- Agora você vê a base quando olha por baixo

### ✅ Cilindro
- Tampa superior + tampa inferior + lateral
- Agora você vê ambas as tampas

### ✅ Esfera
- Todas as faces estão visíveis de qualquer ângulo

### ✅ Torus
- Superfície completa visível

## Testes

Execute os testes para confirmar:

```bash
python test_modules.py
```

Todos os testes devem passar:
```
✓ Transformações: PASSOU
✓ Renderização: PASSOU
✓ Objetos 3D: PASSOU
✓ Lógica do jogo: PASSOU
✓ Interface: PASSOU
✓ Configurações: PASSOU
```

## Executar o Jogo

```bash
python run_game.py
```

Agora quando você girar a câmera (arrastando o mouse), verá todas as faces dos objetos, incluindo as bases!

## Controles de Câmera

- **Mouse (arrastar)**: Rotaciona câmera ao redor do objeto
- **Scroll**: Zoom in/out
- **Experimente:** Gire a câmera para baixo e veja as bases!

## Performance

Com `ENABLE_BACKFACE_CULLING = False`:
- FPS pode ser ligeiramente menor
- Mais faces sendo renderizadas
- Mas a diferença é mínima para este projeto educacional

Se você tiver problemas de performance:
1. Mude `ENABLE_BACKFACE_CULLING = True` no config
2. Ou reduza o número de subdivisões nas esferas

## Recursos Adicionais

- **Documentação de Renderização:** `docs/ARCHITECTURE.md`
- **Código do Renderer:** `src/rendering/renderer.py`
- **Primitivas 3D:** `src/objects/primitives.py`
- **Configurações:** `src/core/config.py`

---

**Problema resolvido!** Agora você pode ver seus objetos 3D completamente de qualquer ângulo! 🎮✨
