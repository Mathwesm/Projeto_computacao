# Controles de Escala Aprimorados

## ✨ Nova Funcionalidade

Agora você tem controle total sobre a escala dos objetos 3D!

### Antes
- **Tecla 3**: Aplicava escala (só aumentava)

### Agora
- **Tecla 3 ou +**: **Aumenta** a escala (+15%)
- **Tecla -**: **Diminui** a escala (-15%)

## 🎮 Como Usar

### Aumentar Tamanho

Pressione qualquer uma dessas teclas:
- **3** (teclado numérico ou normal)
- **+** (shift + =)
- **=** (funciona como +)

**Resultado:** Objeto aumenta 15% do tamanho atual

### Diminuir Tamanho

Pressione:
- **-** (tecla de menos)

**Resultado:** Objeto diminui para 85% do tamanho atual

## 📊 Efeito da Escala

### Matemática

**Aumentar (15%):**
```
Tamanho Novo = Tamanho Atual × 1.15
```

**Diminuir (15%):**
```
Tamanho Novo = Tamanho Atual × 0.85
```

### Exemplo Prático

Começando com cubo de tamanho 1.0:

| Ação | Fator | Tamanho |
|------|-------|---------|
| Inicial | 1.0 | 1.00 |
| Aumentar (+) | ×1.15 | 1.15 |
| Aumentar (+) | ×1.15 | 1.32 |
| Diminuir (-) | ×0.85 | 1.12 |
| Diminuir (-) | ×0.85 | 0.95 |

### Sequência de Transformações

Você pode aplicar múltiplas vezes:

```
Tamanho inicial: 1.0
Pressiona + : 1.0 × 1.15 = 1.15
Pressiona + : 1.15 × 1.15 = 1.32
Pressiona + : 1.32 × 1.15 = 1.52
Pressiona - : 1.52 × 0.85 = 1.29
```

## 🔍 Detalhes Técnicos

### Implementação

**Arquivo:** `src/game.py`

**Aumentar:**
```python
elif key == pygame.K_3 or key == pygame.K_PLUS or key == pygame.K_EQUALS:
    self.apply_transformation('scale_up')

# ...

elif transform_type == 'scale_up':
    shape.scale_uniform(1.15)  # Aumenta 15%
```

**Diminuir:**
```python
elif key == pygame.K_MINUS:
    self.apply_transformation('scale_down')

# ...

elif transform_type == 'scale_down':
    shape.scale_uniform(0.85)  # Diminui 15%
```

### Método `scale_uniform`

**Arquivo:** `src/objects/shape3d.py`

```python
def scale_uniform(self, factor):
    """
    Aplica escala uniforme em todos os eixos

    Args:
        factor: Fator de escala
                > 1.0 = aumenta
                < 1.0 = diminui
                = 1.0 = sem mudança
    """
    self.transform.scale_uniform(factor)
    self.update_transformed_vertices()
```

### Matriz de Escala

A transformação usa matriz 4×4:

```
[sx  0   0   0]
[0   sy  0   0]
[0   0   sz  0]
[0   0   0   1]
```

Para escala uniforme: `sx = sy = sz = factor`

**Aumentar (1.15):**
```
[1.15  0     0     0]
[0     1.15  0     0]
[0     0     1.15  0]
[0     0     0     1]
```

**Diminuir (0.85):**
```
[0.85  0     0     0]
[0     0.85  0     0]
[0     0     0.85  0]
[0     0     0     1]
```

## 🎯 Dicas de Uso

### Controle Fino

Para ajustes precisos:
1. Use **+** para aumentar gradualmente
2. Use **-** para diminuir gradualmente
3. Combine com rotação para ver todos os ângulos

### Efeitos Visuais

**Objetos Pequenos:**
- Mais detalhes visíveis
- Difícil de ver de longe
- Bom para examinar faces

**Objetos Grandes:**
- Visão panorâmica
- Pode sair da tela
- Bom para ver estrutura geral

### Combinações

**Escala + Rotação:**
```
1. Pressione + várias vezes (aumenta)
2. Pressione 2 (rotaciona)
3. Veja o objeto maior de outro ângulo
```

**Escala + Zoom:**
```
1. Pressione - (diminui objeto)
2. Scroll para cima (aproxima câmera)
3. Objeto parece do mesmo tamanho, mas com perspectiva diferente
```

## ⚙️ Configuração

### Alterar Fatores de Escala

Edite `src/game.py` (linhas ~435-437):

```python
elif transform_type == 'scale_up':
    shape.scale_uniform(1.15)  # Mude este valor

elif transform_type == 'scale_down':
    shape.scale_uniform(0.85)  # Mude este valor
```

**Valores Recomendados:**

| Efeito | Aumentar | Diminuir | Descrição |
|--------|----------|----------|-----------|
| Sutil | 1.05 | 0.95 | Mudança de 5% |
| Moderado | 1.15 | 0.85 | Mudança de 15% (padrão) |
| Dramático | 1.25 | 0.75 | Mudança de 25% |
| Extremo | 1.50 | 0.50 | Mudança de 50% |

### Limites

O código não impõe limites de escala, mas você pode adicionar:

```python
# Exemplo de limites
MIN_SCALE = 0.1  # Mínimo 10% do original
MAX_SCALE = 5.0  # Máximo 5x o original

# Antes de aplicar escala
current_scale = shape.get_current_scale()
if transform_type == 'scale_up' and current_scale < MAX_SCALE:
    shape.scale_uniform(1.15)
elif transform_type == 'scale_down' and current_scale > MIN_SCALE:
    shape.scale_uniform(0.85)
```

## 📱 HUD Atualizado

O painel de controles (pressione **C**) agora mostra:

```
CONTROLES
────────────────
Mouse:      Rotacionar camera
Scroll:     Zoom
1:          Translacao
2:          Rotacao
3 ou +:     Aumentar escala    ← NOVO
- (menos):  Diminuir escala    ← NOVO
4:          Reflexao
5:          Distorcao
Q/W/E:      Iluminacao
H:          Dica
ESC:        Pausar
```

## 🎓 Conceito Educacional

### Escala Uniforme vs. Não-Uniforme

**Uniforme** (atual):
- Todos os eixos com mesmo fator
- Mantém proporções
- Cubo continua cubo

**Não-Uniforme** (pode adicionar):
- Eixos com fatores diferentes
- Distorce proporções
- Cubo pode virar paralelepípedo

### Transformações Compostas

Escala + outras transformações:

```
Ordem importa:
  Escala → Rotação ≠ Rotação → Escala
```

**Exemplo:**
1. Escala 2× → Rotação 90°
   - Objeto dobra de tamanho, depois gira
2. Rotação 90° → Escala 2×
   - Objeto gira, depois dobra de tamanho
   - Resultado visual diferente!

## 🧪 Experimentos

### Teste 1: Crescimento Exponencial
```
Pressione + 10 vezes seguidas
Fator final: 1.15^10 ≈ 4.05
Objeto fica ~4× maior!
```

### Teste 2: Diminuir até Mínimo
```
Pressione - 20 vezes
Fator final: 0.85^20 ≈ 0.04
Objeto fica ~4% do tamanho original (muito pequeno!)
```

### Teste 3: Cancelamento
```
Pressione + uma vez: ×1.15
Pressione - uma vez: ×0.85
Resultado: 1.15 × 0.85 ≈ 0.98
Quase volta ao original (pequena diferença)
```

## 📚 Recursos Adicionais

- **Código:** `src/game.py` (linhas 156-172, 430-443)
- **Transformações:** `src/transformations/geometric.py`
- **Objetos:** `src/objects/shape3d.py`
- **HUD:** `src/ui/hud.py` (linhas 174-186)

## 🎮 Execute e Teste!

```bash
python run_game.py
```

**Experimente:**
1. Pressione **+** várias vezes
2. Veja o objeto crescer
3. Pressione **-** várias vezes
4. Veja o objeto encolher
5. Combine com rotação (tecla 2)
6. Veja de todos os ângulos!

---

**Divirta-se explorando escalas!** 🎮✨
