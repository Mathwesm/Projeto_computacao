# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-12-03

### Adicionado
- ✨ Estrutura completa do projeto organizada por módulos
- 🎮 Sistema de jogo completo com 10 níveis progressivos
- 🔄 Transformações geométricas (translação, rotação, escala, reflexão, distorção)
- 💡 Modelos de iluminação (Phong, Lambertiano, Gouraud)
- 📦 Primitivas 3D (cubo, esfera, pirâmide, cilindro, torus)
- 🎯 Sistema de puzzles educativos
- 🎨 Interface gráfica completa (menus, HUD)
- 📐 Sistema de câmera 3D com controles interativos
- 🧮 Utilitários matemáticos e de cores
- ⏱️ Sistema de tempo e pontuação
- 🧪 Suite de testes (unitários e integração)
- 📚 Documentação completa

### Estrutura
- `src/core/` - Módulo central (config, constantes, exceções)
- `src/utils/` - Utilitários reutilizáveis
- `src/transformations/` - Sistema de transformações
- `src/objects/` - Objetos e primitivas 3D
- `src/rendering/` - Sistema de renderização
- `src/game_logic/` - Lógica do jogo
- `src/ui/` - Interface do usuário
- `tests/` - Testes unitários e de integração
- `docs/` - Documentação do projeto
- `scripts/` - Scripts auxiliares

### Técnico
- Matrizes homogêneas 4x4 para transformações
- Pipeline de renderização 3D completo
- Sistema modular e extensível
- Type hints em todo o código
- Testes automatizados
- Configuração via pyproject.toml e setup.py

### Recursos Educacionais
- História envolvente sobre geometria
- Progressão gradual de dificuldade
- Dicas contextualizadas
- Feedback visual imediato
- Sistema de pontuação motivador

## [Não Lançado]

### Planejado
- 🎵 Sistema de áudio e efeitos sonoros
- 🖼️ Sistema de texturas para objetos 3D
- 🌟 Efeitos visuais (partículas, brilhos)
- 💾 Sistema de save/load
- 🏆 Sistema de conquistas
- 📊 Estatísticas detalhadas
- 🌐 Suporte a múltiplos idiomas
- 🎮 Suporte a joystick/gamepad

### Possíveis Melhorias
- Otimização de renderização
- Mais primitivas 3D
- Editor de níveis
- Modo multiplayer local
- Tutorial interativo
- Modo sandbox

## Formato

### Tipos de Mudanças
- **Adicionado** - para novas funcionalidades
- **Modificado** - para mudanças em funcionalidades existentes
- **Descontinuado** - para funcionalidades que serão removidas
- **Removido** - para funcionalidades removidas
- **Corrigido** - para correção de bugs
- **Segurança** - para vulnerabilidades

---

**Legenda de Emojis:**
- ✨ Nova funcionalidade
- 🐛 Correção de bug
- 📚 Documentação
- 🎨 Estilo/UI
- ⚡ Performance
- 🔒 Segurança
- 🧪 Testes
- 🔧 Configuração
- ♻️ Refatoração
