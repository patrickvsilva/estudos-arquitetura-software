# Estudos de Arquitetura de Software

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 Descrição

Plano de estudos prático sobre arquitetura de software, padrões de projeto, engenharia de software e boas práticas em Python, com refatoração de notebook Gurobi e criação de API FastAPI.

Este repositório serve como um guia de estudos estruturado para desenvolvedores que desejam aprofundar seus conhecimentos em arquitetura de software, design patterns e melhores práticas de desenvolvimento.

## 🎯 Objetivos

- Compreender os principais conceitos de arquitetura de software
- Dominar padrões de projeto (Design Patterns)
- Aplicar boas práticas de engenharia de software
- Refatorar código existente (notebook Gurobi) aplicando princípios SOLID
- Desenvolver uma API REST moderna com FastAPI

## 📚 Conteúdo

### 1. Fundamentos de Arquitetura de Software
- Estilos arquiteturais (Monolítico, Microserviços, Event-Driven, etc.)
- Princípios SOLID
- Clean Architecture
- Domain-Driven Design (DDD)
- Arquitetura Hexagonal (Ports and Adapters)

### 2. Padrões de Projeto (Design Patterns)
- **Padrões Criacionais**: Singleton, Factory, Abstract Factory, Builder, Prototype
- **Padrões Estruturais**: Adapter, Bridge, Composite, Decorator, Facade, Proxy
- **Padrões Comportamentais**: Strategy, Observer, Command, Template Method, Iterator

### 3. Boas Práticas em Python
- Type hints e type checking com mypy
- Documentação de código (docstrings, Sphinx)
- Testes (pytest, unittest, coverage)
- Linting e formatação (pylint, black, flake8, isort)
- Estrutura de projetos Python
- Gerenciamento de dependências (pip, poetry, pipenv)

### 4. Projeto Prático: Refatoração Gurobi
- Análise do código original (notebook)
- Identificação de code smells
- Aplicação de refatorações
- Separação de responsabilidades
- Implementação de testes

### 5. Projeto Prático: API FastAPI
- Configuração do projeto
- Estrutura de pastas
- Endpoints REST
- Validação de dados com Pydantic
- Documentação automática (Swagger/OpenAPI)
- Testes de API
- Deploy

## 🚀 Como Usar Este Repositório

### Pré-requisitos
```bash
# Python 3.8 ou superior
python --version

# Recomendado: uso de ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### Instalação
```bash
# Clone o repositório
git clone https://github.com/patrickvsilva/estudos-arquitetura-software.git
cd estudos-arquitetura-software

# Instale as dependências (quando disponíveis)
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
estudos-arquitetura-software/
├── docs/                          # Documentação teórica
│   ├── arquitetura/              # Conceitos de arquitetura
│   ├── design-patterns/          # Padrões de projeto
│   └── boas-praticas/            # Boas práticas Python
├── exemplos/                     # Exemplos práticos
│   ├── design-patterns/          # Implementações de patterns
│   └── refactoring/              # Exemplos de refatoração
├── projetos/                     # Projetos práticos
│   ├── gurobi-refactoring/       # Refatoração notebook Gurobi
│   └── fastapi-project/          # API com FastAPI
├── tests/                        # Testes
├── .gitignore                    # Arquivos ignorados pelo Git
├── LICENSE                       # Licença MIT
├── README.md                     # Este arquivo
└── requirements.txt              # Dependências Python
```

## 🔧 Ferramentas e Tecnologias

- **Python 3.8+**: Linguagem principal
- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados
- **pytest**: Framework de testes
- **mypy**: Type checking
- **black**: Code formatter
- **Gurobi**: Otimização matemática (para projeto de refatoração)

## 📖 Recursos de Estudo

### Livros Recomendados
- "Clean Architecture" - Robert C. Martin
- "Design Patterns: Elements of Reusable Object-Oriented Software" - Gang of Four
- "Refactoring: Improving the Design of Existing Code" - Martin Fowler
- "Python Clean Code" - Mariano Anaya
- "Architecture Patterns with Python" - Harry Percival & Bob Gregory

### Links Úteis
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)
- [Real Python Tutorials](https://realpython.com/)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Patrick V. Silva**

---

⭐️ Se este repositório foi útil para você, considere dar uma estrela!
