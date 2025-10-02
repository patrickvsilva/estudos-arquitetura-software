# Princípios SOLID

Os princípios SOLID são cinco princípios de design orientado a objetos que tornam o software mais compreensível, flexível e sustentável.

## S - Single Responsibility Principle (SRP)
### Princípio da Responsabilidade Única

**Definição**: Uma classe deve ter apenas uma razão para mudar.

**Explicação**: Cada classe deve ter apenas uma responsabilidade ou funcionalidade bem definida.

### Exemplo Ruim (Viola SRP):

```python
class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
    
    def salvar_no_banco(self):
        # Lógica de persistência
        pass
    
    def enviar_email(self):
        # Lógica de envio de email
        pass
    
    def gerar_relatorio(self):
        # Lógica de relatório
        pass
```

### Exemplo Bom (Segue SRP):

```python
class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

class UsuarioRepository:
    def salvar(self, usuario):
        # Lógica de persistência
        pass

class EmailService:
    def enviar(self, usuario, mensagem):
        # Lógica de envio de email
        pass

class RelatorioService:
    def gerar_relatorio_usuario(self, usuario):
        # Lógica de relatório
        pass
```

## O - Open/Closed Principle (OCP)
### Princípio Aberto/Fechado

**Definição**: Classes devem estar abertas para extensão, mas fechadas para modificação.

**Explicação**: Você deve poder adicionar novas funcionalidades sem modificar o código existente.

### Exemplo Ruim:

```python
class Pagamento:
    def processar(self, tipo):
        if tipo == "credito":
            # Processar cartão de crédito
            pass
        elif tipo == "debito":
            # Processar cartão de débito
            pass
        # Para adicionar PIX, precisa modificar esta classe
```

### Exemplo Bom:

```python
from abc import ABC, abstractmethod

class ProcessadorPagamento(ABC):
    @abstractmethod
    def processar(self):
        pass

class PagamentoCredito(ProcessadorPagamento):
    def processar(self):
        # Lógica específica para crédito
        pass

class PagamentoDebito(ProcessadorPagamento):
    def processar(self):
        # Lógica específica para débito
        pass

class PagamentoPix(ProcessadorPagamento):
    def processar(self):
        # Nova forma de pagamento sem modificar código existente
        pass
```

## L - Liskov Substitution Principle (LSP)
### Princípio da Substituição de Liskov

**Definição**: Objetos de uma superclasse devem poder ser substituídos por objetos de suas subclasses sem quebrar a aplicação.

**Explicação**: Subclasses devem ser substituíveis por suas classes base.

### Exemplo:

```python
class Ave(ABC):
    @abstractmethod
    def mover(self):
        pass

class Pardal(Ave):
    def mover(self):
        return "Voando"

class Pinguim(Ave):
    def mover(self):
        return "Nadando"  # Não quebra o contrato

# Melhor design: separar comportamentos
class Ave(ABC):
    @abstractmethod
    def mover(self):
        pass

class AveVoadora(Ave):
    def mover(self):
        return self.voar()
    
    @abstractmethod
    def voar(self):
        pass

class AveNadadora(Ave):
    def mover(self):
        return self.nadar()
    
    @abstractmethod
    def nadar(self):
        pass
```

## I - Interface Segregation Principle (ISP)
### Princípio da Segregação de Interface

**Definição**: Uma classe não deve ser forçada a implementar interfaces que ela não usa.

**Explicação**: É melhor ter várias interfaces específicas do que uma interface geral.

### Exemplo Ruim:

```python
class Trabalhador(ABC):
    @abstractmethod
    def trabalhar(self):
        pass
    
    @abstractmethod
    def comer(self):
        pass
    
    @abstractmethod
    def dormir(self):
        pass

class Robo(Trabalhador):
    def trabalhar(self):
        pass
    
    def comer(self):
        # Robô não come, mas é forçado a implementar
        raise NotImplementedError
    
    def dormir(self):
        # Robô não dorme, mas é forçado a implementar
        raise NotImplementedError
```

### Exemplo Bom:

```python
class Trabalhavel(ABC):
    @abstractmethod
    def trabalhar(self):
        pass

class Alimentavel(ABC):
    @abstractmethod
    def comer(self):
        pass

class Descansavel(ABC):
    @abstractmethod
    def dormir(self):
        pass

class Humano(Trabalhavel, Alimentavel, Descansavel):
    def trabalhar(self):
        pass
    
    def comer(self):
        pass
    
    def dormir(self):
        pass

class Robo(Trabalhavel):
    def trabalhar(self):
        pass
```

## D - Dependency Inversion Principle (DIP)
### Princípio da Inversão de Dependência

**Definição**: Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações.

**Explicação**: Dependa de abstrações (interfaces), não de implementações concretas.

### Exemplo Ruim:

```python
class MySQLDatabase:
    def save(self, data):
        # Salva no MySQL
        pass

class Usuario:
    def __init__(self):
        self.db = MySQLDatabase()  # Dependência direta
    
    def salvar(self, dados):
        self.db.save(dados)
```

### Exemplo Bom:

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        # Salva no MySQL
        pass

class PostgreSQLDatabase(Database):
    def save(self, data):
        # Salva no PostgreSQL
        pass

class Usuario:
    def __init__(self, database: Database):
        self.db = database  # Depende da abstração
    
    def salvar(self, dados):
        self.db.save(dados)

# Uso
mysql_db = MySQLDatabase()
usuario = Usuario(mysql_db)

# Fácil trocar para outro banco
postgres_db = PostgreSQLDatabase()
usuario2 = Usuario(postgres_db)
```

## Benefícios dos Princípios SOLID

1. **Código mais limpo e organizado**
2. **Facilita manutenção e extensão**
3. **Reduz acoplamento**
4. **Aumenta coesão**
5. **Facilita testes unitários**
6. **Melhora reusabilidade**

## Resumo

- **S**: Uma classe, uma responsabilidade
- **O**: Aberto para extensão, fechado para modificação
- **L**: Subclasses devem ser substituíveis
- **I**: Interfaces específicas, não genéricas
- **D**: Dependa de abstrações, não de implementações

## Referências

- [SOLID Principles - Wikipedia](https://en.wikipedia.org/wiki/SOLID)
- [Uncle Bob - SOLID Principles](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html)
