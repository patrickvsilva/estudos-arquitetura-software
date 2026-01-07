# Resumo do livro Arquitetura Limpa

## Detalhes do Livro

- Título: Clean Archtecture

- Autor: Robert C. Martin (Uncle Bob)

- 464 Páginas

## Visão geral do SOLID

- S — Single Responsibility Principle (Responsabilidade Única).
- O — Open-Closed Principle (Aberto/Fechado).
- L — Liskov Substitution Principle (Substituição de Liskov).
- I — Interface Segregation Principle (Segregação de Interfaces).
- D — Dependency Inversion Principle (Inversão de Dependência).

Esses princípios foram popularizados por Robert C. Martin (“Uncle Bob”) e visam tornar o código mais entendível, flexível e reutilizável.

## SRP – Responsabilidade Única

Ideia: uma classe deve ter apenas um motivo para mudar, ou seja, uma única responsabilidade bem definida.

### Antes (várias responsabilidades)

```python
class OrderService:
    def __init__(self, items):
        self.items = items

    def total(self):
        return sum(item["price"] for item in self.items)

    def save_to_db(self):
        print("Saving order to database...")

    def send_email_confirmation(self):
        print("Sending email confirmation...")
```

Aqui a mesma classe calcula total, persiste e envia e-mail, acumulando responsabilidades diferentes.

### Depois (responsabilidades separadas)

```python
class Order:
    def __init__(self, items):
        self.items = items

    def total(self):
        return sum(item["price"] for item in self.items)


class OrderRepository:
    def save(self, order: Order):
        print("Saving order to database...")


class EmailService:
    def send_order_confirmation(self, order: Order):
        print("Sending email confirmation...")
```

Cada classe tem uma responsabilidade clara: domínio do pedido, persistência e envio de e-mail separados, o que facilita mudança e testes.

## OCP – Aberto/Fechado

Ideia: módulos devem estar abertos para extensão, mas fechados para modificação; adiciona‑se comportamento novo sem editar código já testado.

### Antes (if/else para cada tipo novo)

```python
class DiscountCalculator:
    def calculate(self, customer_type, amount):
        if customer_type == "regular":
            return amount
        elif customer_type == "vip":
            return amount * 0.9
        elif customer_type == "employee":
            return amount * 0.8
        # sempre que surge um tipo novo, mexe neste método
```

Qualquer novo tipo de cliente exige mudar o método, aumentando risco de regressão.

### Depois (extensível por classes)

```python
from abc import ABC, abstractmethod

class DiscountPolicy(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        ...


class RegularDiscount(DiscountPolicy):
    def apply(self, amount: float) -> float:
        return amount


class VipDiscount(DiscountPolicy):
    def apply(self, amount: float) -> float:
        return amount * 0.9


class EmployeeDiscount(DiscountPolicy):
    def apply(self, amount: float) -> float:
        return amount * 0.8


class DiscountCalculator:
    def __init__(self, policy: DiscountPolicy):
        self.policy = policy

    def calculate(self, amount: float) -> float:
        return self.policy.apply(amount)
```

Para um novo tipo de desconto, cria‑se outra implementação de `DiscountPolicy` sem alterar `DiscountCalculator`, apenas injetando a nova política.

------

## LSP – Substituição de Liskov

Ideia: objetos de uma subclasse devem poder substituir objetos da superclasse sem quebrar o comportamento esperado do cliente.

### Antes (herança que quebra expectativas)

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value
```

Se um código espera que alterar `width` não altere `height`, isso será violado com `Square`, quebrando o contrato de `Rectangle`.

### Depois (composição em vez de herança errada)

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square:
    def __init__(self, size):
        self.size = size

    def area(self):
        return self.size * self.size
```

Agora `Square` não é mais um subtipo de `Rectangle`, evitando violações de LSP; cada tipo tem contrato coerente para quem o usa.

------

## ISP – Segregação de Interfaces

Ideia: clientes não devem ser forçados a depender de métodos que não usam; é melhor ter várias interfaces pequenas do que uma interface gorda.

### Antes (interface com métodos demais)

```python
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):
        ...

    @abstractmethod
    def eat(self):
        ...


class Robot(Worker):
    def work(self):
        print("Robot working")

    def eat(self):
        # método sem sentido para robô
        raise NotImplementedError("Robots don't eat")
```

`Robot` é obrigado a implementar um método que não faz sentido para ele, o que indica interface mal dividida.

### Depois (interfaces específicas)

```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self):
        ...


class Eatable(ABC):
    @abstractmethod
    def eat(self):
        ...


class Human(Workable, Eatable):
    def work(self):
        print("Human working")

    def eat(self):
        print("Human eating")


class Robot(Workable):
    def work(self):
        print("Robot working")
```

Cada classe implementa apenas as capacidades que fazem sentido, mantendo dependências mais enxutas e claras.

------

## DIP – Inversão de Dependência

Ideia: módulos de alto nível não devem depender de módulos de baixo nível; ambos devem depender de abstrações, facilitando troca de implementações.

### Antes (dependência direta em implementação concreta)

```python
class MySQLDatabase:
    def connect(self):
        print("Connecting to MySQL...")

    def save(self, data):
        print(f"Saving {data} to MySQL")


class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # acoplado

    def create_user(self, user_data):
        self.db.connect()
        self.db.save(user_data)
```

`UserService` fica preso a `MySQLDatabase`, dificultando testes e troca por outro banco.

### Depois (dependência em abstração + injeção)

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def save(self, data):
        ...


class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL...")

    def save(self, data):
        print(f"Saving {data} to MySQL")


class InMemoryDatabase(Database):
    def connect(self):
        print("Using in-memory DB")

    def save(self, data):
        print(f"Storing {data} in memory")


class UserService:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, user_data):
        self.db.connect()
        self.db.save(user_data)
```

Agora `UserService` depende apenas da abstração `Database`, e é possível trocar a implementação (por exemplo, `InMemoryDatabase` em testes) sem alterar a lógica de alto nível.