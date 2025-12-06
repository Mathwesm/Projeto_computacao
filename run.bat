@echo off
echo ============================================================
echo MATHSHAPE QUEST - Aventura das Formas Geometricas
echo ============================================================
echo.
echo Verificando ambiente...
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Verifica se as dependencias estao instaladas
echo Verificando dependencias...
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Pygame nao encontrado. Instalando dependencias...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERRO ao instalar dependencias!
        pause
        exit /b 1
    )
)

echo Dependencias OK!
echo.
echo Iniciando jogo...
echo.

REM Executa o jogo
cd src
python main.py

if errorlevel 1 (
    echo.
    echo ERRO ao executar o jogo!
    pause
)

cd ..
