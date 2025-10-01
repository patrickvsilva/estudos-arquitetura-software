# Padrões de Projeto (Design Patterns)

## Introdução

Design Patterns são soluções reutilizáveis para problemas comuns em design de software. Eles representam as melhores práticas e foram formalizados pelo "Gang of Four" (GoF).

## Classificação dos Padrões

### 1. Padrões Criacionais (Creational Patterns)
Lidam com mecanismos de criação de objetos, tornando o sistema independente de como seus objetos são criados, compostos e representados.

- [Singleton](criacionais/singleton.md) - Garante uma única instância de uma classe
- [Factory Method](criacionais/factory-method.md) - Define uma interface para criar objetos
- [Abstract Factory](criacionais/abstract-factory.md) - Cria famílias de objetos relacionados
- [Builder](criacionais/builder.md) - Constrói objetos complexos passo a passo
- [Prototype](criacionais/prototype.md) - Cria objetos clonando um protótipo

### 2. Padrões Estruturais (Structural Patterns)
Lidam com a composição de classes e objetos para formar estruturas maiores.

- [Adapter](estruturais/adapter.md) - Adapta uma interface para outra
- [Bridge](estruturais/bridge.md) - Separa abstração de implementação
- [Composite](estruturais/composite.md) - Compõe objetos em estruturas de árvore
- [Decorator](estruturais/decorator.md) - Adiciona responsabilidades dinamicamente
- [Facade](estruturais/facade.md) - Fornece uma interface simplificada
- [Flyweight](estruturais/flyweight.md) - Compartilha objetos para economizar memória
- [Proxy](estruturais/proxy.md) - Fornece um substituto ou placeholder

### 3. Padrões Comportamentais (Behavioral Patterns)
Lidam com algoritmos e atribuição de responsabilidades entre objetos.

- [Strategy](comportamentais/strategy.md) - Define família de algoritmos intercambiáveis
- [Observer](comportamentais/observer.md) - Define dependência um-para-muitos
- [Command](comportamentais/command.md) - Encapsula requisições como objetos
- [Template Method](comportamentais/template-method.md) - Define esqueleto de algoritmo
- [Iterator](comportamentais/iterator.md) - Acessa elementos sequencialmente
- [State](comportamentais/state.md) - Altera comportamento quando estado muda
- [Chain of Responsibility](comportamentais/chain-of-responsibility.md) - Passa requisição por cadeia
- [Mediator](comportamentais/mediator.md) - Define objeto que encapsula interações
- [Memento](comportamentais/memento.md) - Captura e restaura estado interno
- [Visitor](comportamentais/visitor.md) - Separa algoritmo de estrutura

## Como Usar Este Guia

Cada padrão inclui:
1. **Intenção**: Qual problema o padrão resolve
2. **Motivação**: Cenário que demonstra o problema
3. **Estrutura**: Diagrama UML do padrão
4. **Participantes**: Classes e objetos envolvidos
5. **Implementação**: Código Python de exemplo
6. **Quando Usar**: Situações apropriadas
7. **Consequências**: Vantagens e desvantagens

## Exemplo Rápido: Strategy Pattern

```python
from abc import ABC, abstractmethod

# Strategy Interface
class EstrategiaDesconto(ABC):
    @abstractmethod
    def calcular_desconto(self, valor: float) -> float:
        pass

# Concrete Strategies
class DescontoNatal(EstrategiaDesconto):
    def calcular_desconto(self, valor: float) -> float:
        return valor * 0.20  # 20% de desconto

class DescontoBlackFriday(EstrategiaDesconto):
    def calcular_desconto(self, valor: float) -> float:
        return valor * 0.50  # 50% de desconto

class SemDesconto(EstrategiaDesconto):
    def calcular_desconto(self, valor: float) -> float:
        return 0.0

# Context
class Carrinho:
    def __init__(self, estrategia: EstrategiaDesconto):
        self._estrategia = estrategia
        self._valor_total = 0
    
    def adicionar_item(self, valor: float):
        self._valor_total += valor
    
    def calcular_total(self) -> float:
        desconto = self._estrategia.calcular_desconto(self._valor_total)
        return self._valor_total - desconto

# Uso
carrinho_natal = Carrinho(DescontoNatal())
carrinho_natal.adicionar_item(100)
print(f"Total com desconto de Natal: R$ {carrinho_natal.calcular_total()}")

carrinho_bf = Carrinho(DescontoBlackFriday())
carrinho_bf.adicionar_item(100)
print(f"Total com desconto Black Friday: R$ {carrinho_bf.calcular_total()}")
```

## Quando Usar Design Patterns

✅ **Use quando:**
- O problema se encaixa claramente no padrão
- Você precisa de flexibilidade e extensibilidade
- O código será mantido por outros desenvolvedores
- Você quer comunicar intenção claramente

❌ **Não use quando:**
- O problema é simples demais
- Adiciona complexidade desnecessária
- A equipe não conhece o padrão (ou eduque primeiro)

## Princípios por Trás dos Patterns

1. **Programe para interfaces, não implementações**
2. **Favoreça composição sobre herança**
3. **Encapsule o que varia**
4. **Princípios SOLID**

## Recursos Adicionais

- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [Python Design Patterns](https://python-patterns.guide/)
- Livro: "Design Patterns: Elements of Reusable Object-Oriented Software" (Gang of Four)
- Livro: "Head First Design Patterns" (mais didático)

## Próximos Passos

1. Estude cada categoria de padrões
2. Implemente exemplos práticos
3. Identifique padrões em código existente
4. Pratique refatoração usando patterns
