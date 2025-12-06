#!/bin/bash

echo "============================================================"
echo "MATHSHAPE QUEST - Aventura das Formas Geometricas"
echo "============================================================"
echo ""
echo "Verificando ambiente..."
echo ""

# Verifica se Python esta instalado
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null
then
    echo "ERRO: Python nao encontrado!"
    echo "Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Determina comando Python
if command -v python3 &> /dev/null
then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "Python encontrado!"
echo ""

# Verifica se as dependencias estao instaladas
echo "Verificando dependencias..."
$PYTHON_CMD -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Pygame nao encontrado. Instalando dependencias..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERRO ao instalar dependencias!"
        exit 1
    fi
fi

echo "Dependencias OK!"
echo ""
echo "Iniciando jogo..."
echo ""

# Executa o jogo
cd src
$PYTHON_CMD main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERRO ao executar o jogo!"
fi

cd ..
