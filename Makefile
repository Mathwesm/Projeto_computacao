.PHONY: help install install-dev run test clean lint format docs

help:
	@echo "MathShape Quest - Comandos disponíveis:"
	@echo ""
	@echo "  make install      - Instala o projeto"
	@echo "  make install-dev  - Instala com dependências de desenvolvimento"
	@echo "  make run          - Executa o jogo"
	@echo "  make test         - Executa os testes"
	@echo "  make test-cov     - Executa testes com cobertura"
	@echo "  make lint         - Verifica código com flake8"
	@echo "  make format       - Formata código com black"
	@echo "  make clean        - Remove arquivos temporários"
	@echo "  make docs         - Gera documentação"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy

run:
	python src/main.py

test:
	python test_modules.py

test-pytest:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/ --max-line-length=100

format:
	black src/ tests/ --line-length=100

type-check:
	mypy src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache .coverage htmlcov/ dist/ build/ *.egg-info

docs:
	@echo "Documentação em docs/"

# Atalhos úteis
t: test
r: run
c: clean
f: format
l: lint
