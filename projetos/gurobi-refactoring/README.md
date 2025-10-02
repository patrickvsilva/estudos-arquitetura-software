# Projeto: Refatoração de Notebook Gurobi

## Objetivo

Refatorar um notebook Jupyter que utiliza o Gurobi Optimizer, aplicando princípios de engenharia de software, SOLID e boas práticas Python.

## Estrutura do Projeto

```
gurobi-refactoring/
├── README.md                 # Este arquivo
├── notebooks/                # Notebooks originais e refatorados
│   ├── original/            # Notebook original (antes da refatoração)
│   └── refatorado/          # Notebook refatorado (após aplicar melhorias)
├── src/                     # Código Python modularizado
│   ├── __init__.py
│   ├── models/              # Modelos de domínio
│   │   ├── __init__.py
│   │   └── optimization_model.py
│   ├── services/            # Lógica de negócio
│   │   ├── __init__.py
│   │   └── optimizer_service.py
│   └── utils/               # Utilitários
│       ├── __init__.py
│       └── data_loader.py
├── tests/                   # Testes automatizados
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── data/                    # Dados de exemplo
│   └── sample_data.json
├── requirements.txt         # Dependências Python
└── pyproject.toml          # Configuração do projeto
```

## Objetivos de Refatoração

### 1. Separação de Responsabilidades
- [ ] Separar lógica de otimização da apresentação
- [ ] Criar classes para modelos de domínio
- [ ] Extrair serviços de otimização
- [ ] Isolar carregamento de dados

### 2. Aplicar Princípios SOLID

#### Single Responsibility
- Cada classe/função tem uma única responsabilidade
- Modelos focam em dados
- Serviços focam em lógica de negócio

#### Open/Closed
- Extensível para novos tipos de otimização
- Fechado para modificações no core

#### Liskov Substitution
- Interfaces bem definidas
- Implementações substituíveis

#### Interface Segregation
- Interfaces específicas e coesas

#### Dependency Inversion
- Dependência de abstrações, não implementações
- Injeção de dependências

### 3. Melhorias de Código

- [ ] Adicionar type hints
- [ ] Escrever docstrings completas
- [ ] Implementar tratamento de erros
- [ ] Criar testes unitários (>80% coverage)
- [ ] Configurar linting (black, pylint, mypy)
- [ ] Adicionar logging estruturado

### 4. Boas Práticas Gurobi

- [ ] Gerenciar corretamente recursos (context managers)
- [ ] Validar entradas antes de criar modelo
- [ ] Separar construção do modelo de resolução
- [ ] Extrair e formatar resultados de forma limpa

## Exemplo: Antes e Depois

### Antes (Código de Notebook)

```python
import gurobipy as gp
from gurobipy import GRB

# Dados hardcoded
custos = [10, 20, 30, 40]
capacidades = [100, 200, 150, 180]
demanda = 400

# Criar modelo
m = gp.Model()

# Variáveis
x = []
for i in range(len(custos)):
    x.append(m.addVar(ub=capacidades[i], name=f"x{i}"))

# Objetivo
obj = sum(custos[i] * x[i] for i in range(len(custos)))
m.setObjective(obj, GRB.MINIMIZE)

# Restrição
m.addConstr(sum(x) >= demanda)

# Resolver
m.optimize()

# Resultados
for i in range(len(x)):
    print(f"x{i} = {x[i].X}")
print(f"Custo total: {m.ObjVal}")
```

### Depois (Código Refatorado)

```python
# models/optimization_model.py
from dataclasses import dataclass
from typing import List

@dataclass
class FacilityData:
    """Dados de uma instalação."""
    id: int
    custo_unitario: float
    capacidade: float

@dataclass
class ProblemData:
    """Dados do problema de otimização."""
    instalacoes: List[FacilityData]
    demanda_total: float
    
    def validar(self) -> None:
        """Valida os dados de entrada."""
        if self.demanda_total <= 0:
            raise ValueError("Demanda deve ser positiva")
        if not self.instalacoes:
            raise ValueError("Deve haver pelo menos uma instalação")


# services/optimizer_service.py
from abc import ABC, abstractmethod
import gurobipy as gp
from gurobipy import GRB
from models.optimization_model import ProblemData

class OptimizerResult:
    """Resultado da otimização."""
    def __init__(self, alocacoes: dict, custo_total: float, status: str):
        self.alocacoes = alocacoes
        self.custo_total = custo_total
        self.status = status

class Optimizer(ABC):
    """Interface para otimizadores."""
    @abstractmethod
    def otimizar(self, dados: ProblemData) -> OptimizerResult:
        pass

class GurobiOptimizer(Optimizer):
    """Implementação usando Gurobi."""
    
    def otimizar(self, dados: ProblemData) -> OptimizerResult:
        """
        Otimiza alocação de recursos.
        
        Args:
            dados: Dados do problema validados
            
        Returns:
            Resultado da otimização
        """
        dados.validar()
        
        with gp.Env() as env, gp.Model(env=env) as modelo:
            # Criar variáveis
            variaveis = self._criar_variaveis(modelo, dados)
            
            # Definir objetivo
            self._definir_objetivo(modelo, variaveis, dados)
            
            # Adicionar restrições
            self._adicionar_restricoes(modelo, variaveis, dados)
            
            # Resolver
            modelo.optimize()
            
            return self._extrair_resultado(modelo, variaveis)
    
    def _criar_variaveis(self, modelo, dados):
        """Cria variáveis de decisão."""
        return {
            inst.id: modelo.addVar(
                ub=inst.capacidade,
                name=f"x_{inst.id}"
            )
            for inst in dados.instalacoes
        }
    
    def _definir_objetivo(self, modelo, variaveis, dados):
        """Define função objetivo."""
        obj = sum(
            inst.custo_unitario * variaveis[inst.id]
            for inst in dados.instalacoes
        )
        modelo.setObjective(obj, GRB.MINIMIZE)
    
    def _adicionar_restricoes(self, modelo, variaveis, dados):
        """Adiciona restrições ao modelo."""
        modelo.addConstr(
            sum(variaveis.values()) >= dados.demanda_total,
            name="demanda"
        )
    
    def _extrair_resultado(self, modelo, variaveis):
        """Extrai resultado da otimização."""
        if modelo.status != GRB.OPTIMAL:
            return OptimizerResult({}, 0.0, "INVIÁVEL")
        
        alocacoes = {
            var_id: var.X
            for var_id, var in variaveis.items()
        }
        
        return OptimizerResult(
            alocacoes=alocacoes,
            custo_total=modelo.ObjVal,
            status="ÓTIMO"
        )


# Uso
from models.optimization_model import FacilityData, ProblemData
from services.optimizer_service import GurobiOptimizer

# Preparar dados
instalacoes = [
    FacilityData(id=1, custo_unitario=10, capacidade=100),
    FacilityData(id=2, custo_unitario=20, capacidade=200),
    FacilityData(id=3, custo_unitario=30, capacidade=150),
    FacilityData(id=4, custo_unitario=40, capacidade=180),
]

dados = ProblemData(instalacoes=instalacoes, demanda_total=400)

# Otimizar
optimizer = GurobiOptimizer()
resultado = optimizer.otimizar(dados)

# Exibir resultados
print(f"Status: {resultado.status}")
print(f"Custo Total: R$ {resultado.custo_total:.2f}")
for inst_id, alocacao in resultado.alocacoes.items():
    print(f"Instalação {inst_id}: {alocacao:.2f} unidades")
```

## Como Começar

1. **Adicionar notebook original**
   ```bash
   # Coloque seu notebook original em notebooks/original/
   ```

2. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar análise do código original**
   - Identificar responsabilidades
   - Mapear dependências
   - Detectar code smells

4. **Aplicar refatorações incrementais**
   - Extrair funções
   - Criar classes
   - Adicionar testes
   - Modularizar código

5. **Validar melhorias**
   ```bash
   # Executar testes
   pytest tests/ -v --cov=src
   
   # Executar linting
   black src/ tests/
   pylint src/
   mypy src/
   ```

## Métricas de Qualidade

| Métrica | Antes | Depois | Objetivo |
|---------|-------|--------|----------|
| Linhas por função | >50 | <20 | <20 |
| Cobertura de testes | 0% | >80% | >80% |
| Complexidade ciclomática | >10 | <5 | <5 |
| Duplicação de código | Alta | Baixa | <5% |
| Type hints | 0% | 100% | 100% |

## Referências

- [Gurobi Documentation](https://www.gurobi.com/documentation/)
- [Refactoring: Improving the Design of Existing Code](https://martinfowler.com/books/refactoring.html)
- [Clean Code in Python](https://www.packtpub.com/product/clean-code-in-python/9781788835831)
