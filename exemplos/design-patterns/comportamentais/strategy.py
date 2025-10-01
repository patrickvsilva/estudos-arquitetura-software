"""
Padrão Strategy

Define uma família de algoritmos, encapsula cada um deles e os torna intercambiáveis.
Strategy permite que o algoritmo varie independentemente dos clientes que o utilizam.

Quando usar:
- Quando você tem várias formas de fazer a mesma coisa
- Quando quer evitar múltiplos if/else ou switch/case
- Quando algoritmos devem ser intercambiáveis em tempo de execução
"""

from abc import ABC, abstractmethod
from typing import List


# Strategy Interface
class PaymentStrategy(ABC):
    """Interface para estratégias de pagamento."""
    
    @abstractmethod
    def pay(self, amount: float) -> str:
        """Processa pagamento usando a estratégia específica."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Valida se o método de pagamento é válido."""
        pass


# Concrete Strategies
class CreditCardPayment(PaymentStrategy):
    """Pagamento com cartão de crédito."""
    
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def validate(self) -> bool:
        """Valida cartão de crédito."""
        return len(self.card_number) == 16 and len(self.cvv) == 3
    
    def pay(self, amount: float) -> str:
        """Processa pagamento com cartão."""
        if not self.validate():
            return "Erro: Cartão inválido"
        return f"Pagamento de R$ {amount:.2f} processado com Cartão de Crédito ****{self.card_number[-4:]}"


class PixPayment(PaymentStrategy):
    """Pagamento via PIX."""
    
    def __init__(self, pix_key: str):
        self.pix_key = pix_key
    
    def validate(self) -> bool:
        """Valida chave PIX."""
        return len(self.pix_key) > 0
    
    def pay(self, amount: float) -> str:
        """Processa pagamento via PIX."""
        if not self.validate():
            return "Erro: Chave PIX inválida"
        return f"Pagamento de R$ {amount:.2f} processado via PIX para {self.pix_key}"


class BoletoPayment(PaymentStrategy):
    """Pagamento via boleto bancário."""
    
    def __init__(self, cpf: str):
        self.cpf = cpf
    
    def validate(self) -> bool:
        """Valida CPF."""
        return len(self.cpf) == 11
    
    def pay(self, amount: float) -> str:
        """Gera boleto."""
        if not self.validate():
            return "Erro: CPF inválido"
        barcode = "34191.79001 01043.510047 91020.150008 1 84560000000000"
        return f"Boleto gerado no valor de R$ {amount:.2f}\nCódigo de barras: {barcode}"


# Context
class ShoppingCart:
    """Carrinho de compras que usa Strategy para pagamento."""
    
    def __init__(self):
        self._items: List[float] = []
        self._payment_strategy: PaymentStrategy = None
    
    def add_item(self, price: float) -> None:
        """Adiciona item ao carrinho."""
        self._items.append(price)
    
    def get_total(self) -> float:
        """Calcula total do carrinho."""
        return sum(self._items)
    
    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Define estratégia de pagamento."""
        self._payment_strategy = strategy
    
    def checkout(self) -> str:
        """Finaliza compra usando a estratégia definida."""
        if not self._payment_strategy:
            return "Erro: Nenhum método de pagamento selecionado"
        
        total = self.get_total()
        if total == 0:
            return "Erro: Carrinho vazio"
        
        return self._payment_strategy.pay(total)


# Exemplo adicional: Strategy para cálculo de frete
class ShippingStrategy(ABC):
    """Interface para estratégias de envio."""
    
    @abstractmethod
    def calculate_cost(self, weight: float, distance: float) -> float:
        """Calcula custo de envio."""
        pass


class StandardShipping(ShippingStrategy):
    """Envio padrão (mais barato, mais lento)."""
    
    def calculate_cost(self, weight: float, distance: float) -> float:
        return weight * 0.5 + distance * 0.1


class ExpressShipping(ShippingStrategy):
    """Envio expresso (mais caro, mais rápido)."""
    
    def calculate_cost(self, weight: float, distance: float) -> float:
        return weight * 1.0 + distance * 0.3


class SameDayShipping(ShippingStrategy):
    """Envio no mesmo dia (muito caro, imediato)."""
    
    def calculate_cost(self, weight: float, distance: float) -> float:
        return weight * 2.0 + distance * 0.5 + 15.0  # Taxa adicional fixa


class Order:
    """Pedido que usa Strategy para calcular frete."""
    
    def __init__(self, weight: float, distance: float):
        self.weight = weight
        self.distance = distance
        self._shipping_strategy: ShippingStrategy = StandardShipping()
    
    def set_shipping_strategy(self, strategy: ShippingStrategy) -> None:
        """Define estratégia de envio."""
        self._shipping_strategy = strategy
    
    def get_shipping_cost(self) -> float:
        """Calcula custo de envio usando estratégia."""
        return self._shipping_strategy.calculate_cost(self.weight, self.distance)


# Demonstração de uso
def main():
    print("=== Strategy Pattern Examples ===\n")
    
    # Exemplo 1: Pagamento
    print("1. Payment Strategies:")
    cart = ShoppingCart()
    cart.add_item(100.0)
    cart.add_item(50.0)
    cart.add_item(75.0)
    print(f"Total do carrinho: R$ {cart.get_total():.2f}\n")
    
    # Pagamento com cartão
    print("Tentando pagar com Cartão de Crédito:")
    cart.set_payment_strategy(CreditCardPayment("1234567812345678", "123"))
    print(cart.checkout())
    print()
    
    # Pagamento com PIX
    print("Tentando pagar com PIX:")
    cart.set_payment_strategy(PixPayment("meuemail@example.com"))
    print(cart.checkout())
    print()
    
    # Pagamento com Boleto
    print("Tentando pagar com Boleto:")
    cart.set_payment_strategy(BoletoPayment("12345678901"))
    print(cart.checkout())
    print()
    
    # Exemplo 2: Frete
    print("2. Shipping Strategies:")
    order = Order(weight=5.0, distance=100.0)
    
    print(f"Envio Padrão: R$ {order.get_shipping_cost():.2f}")
    
    order.set_shipping_strategy(ExpressShipping())
    print(f"Envio Expresso: R$ {order.get_shipping_cost():.2f}")
    
    order.set_shipping_strategy(SameDayShipping())
    print(f"Envio no Mesmo Dia: R$ {order.get_shipping_cost():.2f}")


if __name__ == "__main__":
    main()
