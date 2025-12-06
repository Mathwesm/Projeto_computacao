# Assets

Pasta para recursos do jogo.

## Estrutura

```
assets/
├── fonts/          # Fontes personalizadas
├── sounds/         # Efeitos sonoros e música
└── textures/       # Texturas para objetos 3D
```

## Fontes

Coloque arquivos de fonte (.ttf, .otf) na pasta `fonts/`.

Exemplo:
```
fonts/
├── main.ttf
├── title.ttf
└── mono.ttf
```

## Sons

Coloque arquivos de áudio (.wav, .ogg, .mp3) na pasta `sounds/`.

Exemplo:
```
sounds/
├── click.wav
├── success.wav
├── error.wav
└── background.ogg
```

## Texturas

Coloque imagens (.png, .jpg) na pasta `textures/`.

Exemplo:
```
textures/
├── cube_texture.png
├── sphere_texture.png
└── background.jpg
```

## Formato Recomendado

- **Fontes**: TTF ou OTF
- **Sons**: OGG (música), WAV (efeitos)
- **Imagens**: PNG com transparência, JPG para fotos

## Licenciamento

Certifique-se de que todos os assets têm licenças apropriadas para uso em projetos educacionais.

## Assets Padrão

O jogo funciona sem assets externos, usando:
- Fonte padrão do Pygame
- Cores sólidas para objetos
- Sem sons (silencioso)

Assets personalizados melhoram a experiência mas são opcionais.
