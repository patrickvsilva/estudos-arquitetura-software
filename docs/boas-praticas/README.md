# Boas Práticas em Python

## Introdução

Este guia apresenta boas práticas essenciais para desenvolvimento em Python, focando em código limpo, manutenível e profissional.

## Conteúdo

1. [Type Hints e Type Checking](type-hints.md)
2. [Documentação de Código](documentacao.md)
3. [Testes Automatizados](testes.md)
4. [Linting e Formatação](linting.md)
5. [Estrutura de Projetos](estrutura-projetos.md)
6. [Gerenciamento de Dependências](dependencias.md)

## Princípios Fundamentais

### 1. The Zen of Python (PEP 20)

```python
import this
```

Princípios principais:
- **Bonito é melhor que feio**
- **Explícito é melhor que implícito**
- **Simples é melhor que complexo**
- **Legibilidade conta**
- **Casos especiais não são especiais o bastante para quebrar as regras**

### 2. PEP 8 - Style Guide

```python
# Bom: nomes descritivos, snake_case
def calcular_preco_total(itens: list, taxa_imposto: float) -> float:
    subtotal = sum(item.preco for item in itens)
    return subtotal * (1 + taxa_imposto)

# Ruim: nomes curtos, camelCase em funções
def calcPreco(i: list, t: float) -> float:
    s = sum(x.preco for x in i)
    return s * (1 + t)
```

### 3. Code Smells e Refatoração

#### Code Smell: Função Muito Longa
```python
# Ruim
def processar_pedido(pedido):
    # 100 linhas de código
    pass

# Bom
def processar_pedido(pedido):
    validar_pedido(pedido)
    calcular_total(pedido)
    aplicar_desconto(pedido)
    processar_pagamento(pedido)
    enviar_confirmacao(pedido)
```

#### Code Smell: Duplicação de Código
```python
# Ruim
def calcular_area_retangulo(largura, altura):
    return largura * altura

def calcular_area_quadrado(lado):
    return lado * lado  # Duplicação conceitual

# Bom
def calcular_area_retangulo(largura, altura):
    return largura * altura

def calcular_area_quadrado(lado):
    return calcular_area_retangulo(lado, lado)
```

## Type Hints

```python
from typing import List, Dict, Optional, Union

def processar_usuarios(
    usuarios: List[Dict[str, str]],
    filtro: Optional[str] = None
) -> List[str]:
    """
    Processa lista de usuários e retorna nomes filtrados.
    
    Args:
        usuarios: Lista de dicionários com dados dos usuários
        filtro: String opcional para filtrar usuários
        
    Returns:
        Lista de nomes de usuários processados
    """
    if filtro:
        usuarios = [u for u in usuarios if filtro in u.get('nome', '')]
    return [u['nome'] for u in usuarios]
```

## Documentação (Docstrings)

```python
def calcular_media(numeros: List[float]) -> float:
    """
    Calcula a média aritmética de uma lista de números.
    
    Esta função aceita uma lista de números de ponto flutuante
    e retorna sua média aritmética. Se a lista estiver vazia,
    retorna 0.0.
    
    Args:
        numeros (List[float]): Lista de números para calcular a média.
        
    Returns:
        float: A média aritmética dos números.
        
    Raises:
        TypeError: Se algum elemento não for um número.
        
    Examples:
        >>> calcular_media([1.0, 2.0, 3.0])
        2.0
        >>> calcular_media([])
        0.0
    """
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)
```

## Testes Automatizados

```python
import pytest

def soma(a: int, b: int) -> int:
    """Soma dois números inteiros."""
    return a + b

# Testes
def test_soma_positivos():
    assert soma(2, 3) == 5

def test_soma_negativos():
    assert soma(-2, -3) == -5

def test_soma_zero():
    assert soma(0, 5) == 5

@pytest.mark.parametrize("a,b,esperado", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_soma_parametrizada(a, b, esperado):
    assert soma(a, b) == esperado
```

## Context Managers

```python
# Usando with para gerenciar recursos
with open('arquivo.txt', 'r') as f:
    conteudo = f.read()

# Criando seu próprio context manager
from contextlib import contextmanager

@contextmanager
def temporizador():
    import time
    inicio = time.time()
    try:
        yield
    finally:
        fim = time.time()
        print(f"Tempo decorrido: {fim - inicio:.2f}s")

# Uso
with temporizador():
    # código a ser medido
    sum(range(1000000))
```

## List Comprehensions e Generators

```python
# List comprehension
quadrados = [x**2 for x in range(10)]

# Generator expression (mais eficiente com memória)
quadrados_gen = (x**2 for x in range(10))

# Dict comprehension
quadrados_dict = {x: x**2 for x in range(10)}

# Set comprehension
numeros_unicos = {x % 10 for x in range(100)}
```

## Decoradores

```python
from functools import wraps
import time

def medir_tempo(func):
    """Decorador que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        print(f"{func.__name__} levou {fim - inicio:.4f}s")
        return resultado
    return wrapper

@medir_tempo
def funcao_lenta():
    time.sleep(1)
    return "Concluído"
```

## Tratamento de Exceções

```python
# Bom: específico e informativo
def dividir(a: float, b: float) -> float:
    """Divide dois números."""
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError(f"Não é possível dividir {a} por zero")
    except TypeError as e:
        raise TypeError(f"Argumentos devem ser números: {e}")

# Ruim: captura genérica
def dividir_ruim(a, b):
    try:
        return a / b
    except:  # Nunca faça isso!
        return None
```

## Logging

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def processar_dados(dados):
    logger.info("Iniciando processamento de dados")
    try:
        # processar dados
        resultado = len(dados)
        logger.debug(f"Processados {resultado} itens")
        return resultado
    except Exception as e:
        logger.error(f"Erro no processamento: {e}", exc_info=True)
        raise
```

## Dataclasses (Python 3.7+)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    """Representa um usuário do sistema."""
    id: int
    nome: str
    email: str
    ativo: bool = True
    idade: Optional[int] = None
    
    def __post_init__(self):
        """Validações após inicialização."""
        if not self.email or '@' not in self.email:
            raise ValueError(f"Email inválido: {self.email}")

# Uso
usuario = Usuario(id=1, nome="João", email="joao@example.com")
print(usuario)  # Usuario(id=1, nome='João', email='joao@example.com', ativo=True, idade=None)
```

## Checklist de Boas Práticas

- [ ] Seguir PEP 8 para estilo de código
- [ ] Usar type hints em funções e métodos
- [ ] Escrever docstrings para módulos, classes e funções
- [ ] Criar testes automatizados (coverage > 80%)
- [ ] Usar linters (pylint, flake8) e formatadores (black)
- [ ] Gerenciar dependências com requirements.txt ou poetry
- [ ] Usar logging em vez de prints
- [ ] Tratar exceções específicas
- [ ] Evitar código duplicado (DRY - Don't Repeat Yourself)
- [ ] Manter funções pequenas e focadas (SRP)
- [ ] Usar control de versão (Git)
- [ ] Revisar código (code review)

## Ferramentas Recomendadas

### Linting e Formatação
- **black**: Formatador automático
- **isort**: Organiza imports
- **pylint**: Análise estática
- **flake8**: Verificação de estilo
- **mypy**: Type checking

### Testes
- **pytest**: Framework de testes
- **pytest-cov**: Cobertura de testes
- **hypothesis**: Testes baseados em propriedades
- **tox**: Testes em múltiplos ambientes

### Qualidade
- **bandit**: Segurança
- **radon**: Complexidade ciclomática
- **pre-commit**: Git hooks

## Recursos Adicionais

- [PEP 8 - Style Guide](https://pep8.org/)
- [Real Python](https://realpython.com/)
- [Python Testing with pytest](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)
- [Effective Python](https://effectivepython.com/)
