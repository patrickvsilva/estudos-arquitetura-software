# Makefile para facilitar tarefas comuns do projeto

.PHONY: help install clean test lint format run-examples docs

# Variáveis
PYTHON := python3
PIP := pip
VENV := venv
SRC_DIR := exemplos
TEST_DIR := tests

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala as dependências do projeto
	$(PIP) install -r requirements.txt

install-dev: ## Instala as dependências de desenvolvimento
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

venv: ## Cria um ambiente virtual
	$(PYTHON) -m venv $(VENV)
	@echo "Ambiente virtual criado. Ative com: source $(VENV)/bin/activate"

clean: ## Remove arquivos temporários e cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	@echo "Arquivos temporários removidos!"

test: ## Executa todos os testes
	pytest $(TEST_DIR) -v

test-cov: ## Executa testes com cobertura
	pytest $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html

test-watch: ## Executa testes em modo watch
	pytest-watch $(TEST_DIR) -v

lint: ## Executa verificações de qualidade de código
	@echo "Executando pylint..."
	pylint $(SRC_DIR) || true
	@echo "\nExecutando flake8..."
	flake8 $(SRC_DIR) --max-line-length=100 || true
	@echo "\nExecutando mypy..."
	mypy $(SRC_DIR) || true

format: ## Formata o código com black e isort
	@echo "Formatando código com black..."
	black $(SRC_DIR) $(TEST_DIR)
	@echo "Organizando imports com isort..."
	isort $(SRC_DIR) $(TEST_DIR)
	@echo "Código formatado!"

format-check: ## Verifica se o código está formatado corretamente
	black --check $(SRC_DIR) $(TEST_DIR)
	isort --check-only $(SRC_DIR) $(TEST_DIR)

run-singleton: ## Executa exemplo de Singleton
	$(PYTHON) exemplos/design-patterns/criacionais/singleton.py

run-strategy: ## Executa exemplo de Strategy
	$(PYTHON) exemplos/design-patterns/comportamentais/strategy.py

run-adapter: ## Executa exemplo de Adapter
	$(PYTHON) exemplos/design-patterns/estruturais/adapter.py

run-refactoring: ## Executa exemplo de refatoração
	$(PYTHON) exemplos/refactoring/antes_depois.py

run-examples: ## Executa todos os exemplos
	@echo "=== Singleton Pattern ==="
	$(PYTHON) exemplos/design-patterns/criacionais/singleton.py
	@echo "\n=== Strategy Pattern ==="
	$(PYTHON) exemplos/design-patterns/comportamentais/strategy.py
	@echo "\n=== Adapter Pattern ==="
	$(PYTHON) exemplos/design-patterns/estruturais/adapter.py
	@echo "\n=== Refactoring Example ==="
	$(PYTHON) exemplos/refactoring/antes_depois.py

docs: ## Gera documentação (se configurado)
	@echo "Documentação disponível no README.md e na pasta docs/"
	@echo "Para visualizar no navegador, considere usar mkdocs:"
	@echo "  mkdocs serve"

check: format-check lint test ## Executa todas as verificações

all: clean install test lint ## Instala, testa e verifica qualidade

.DEFAULT_GOAL := help
