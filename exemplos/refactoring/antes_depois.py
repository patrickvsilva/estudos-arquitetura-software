"""
Exemplo de Refatoração: Antes e Depois

Este módulo demonstra como refatorar código aplicando princípios SOLID,
design patterns e boas práticas.

Cenário: Sistema de processamento de pedidos de e-commerce
"""

# ============================================================================
# ANTES: Código com problemas (code smells)
# ============================================================================

"""
Problemas identificados:
1. Classe muito grande (God Object)
2. Violação do SRP (muitas responsabilidades)
3. Código duplicado
4. Acoplamento alto
5. Falta de abstrações
6. Difícil de testar
7. Sem tratamento de erros
"""

class OrderProcessorBefore:
    """Classe que faz tudo - RUIM!"""
    
    def process_order(self, order_data):
        # Validação
        if not order_data.get('customer_email'):
            return False
        if not order_data.get('items'):
            return False
        
        # Calcular total
        total = 0
        for item in order_data['items']:
            total += item['price'] * item['quantity']
        
        # Aplicar desconto
        if total > 100:
            total = total * 0.9
        elif total > 500:
            total = total * 0.8
        
        # Calcular frete
        if total > 200:
            shipping = 0
        else:
            shipping = 10
        
        final_total = total + shipping
        
        # Salvar no banco (código hardcoded)
        import sqlite3
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_email, total) 
            VALUES (?, ?)
        """, (order_data['customer_email'], final_total))
        conn.commit()
        conn.close()
        
        # Enviar email (código hardcoded)
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('user@example.com', 'password')
        message = f"Seu pedido foi processado. Total: R$ {final_total}"
        server.sendmail('user@example.com', order_data['customer_email'], message)
        server.quit()
        
        return True


# ============================================================================
# DEPOIS: Código refatorado (aplicando boas práticas)
# ============================================================================

"""
Melhorias aplicadas:
1. Separação de responsabilidades (SRP)
2. Dependency Injection (DIP)
3. Strategy Pattern para descontos
4. Repository Pattern para acesso a dados
5. Type hints
6. Tratamento de erros
7. Fácil de testar
8. Código reutilizável
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Protocol
from decimal import Decimal


# Domain Models
@dataclass
class OrderItem:
    """Item de um pedido."""
    product_id: str
    name: str
    price: Decimal
    quantity: int
    
    def get_subtotal(self) -> Decimal:
        """Calcula subtotal do item."""
        return self.price * self.quantity


@dataclass
class Order:
    """Pedido do cliente."""
    customer_email: str
    items: List[OrderItem]
    
    def get_subtotal(self) -> Decimal:
        """Calcula subtotal de todos os itens."""
        return sum(item.get_subtotal() for item in self.items)
    
    def validate(self) -> None:
        """Valida o pedido."""
        if not self.customer_email:
            raise ValueError("Email do cliente é obrigatório")
        if not self.items:
            raise ValueError("Pedido deve ter pelo menos um item")
        if not all(item.quantity > 0 for item in self.items):
            raise ValueError("Quantidade deve ser maior que zero")


# Strategy Pattern para Descontos
class DiscountStrategy(ABC):
    """Interface para estratégias de desconto."""
    
    @abstractmethod
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        """Calcula desconto baseado no subtotal."""
        pass


class NoDiscount(DiscountStrategy):
    """Sem desconto."""
    
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        return Decimal('0')


class PercentageDiscount(DiscountStrategy):
    """Desconto percentual."""
    
    def __init__(self, min_value: Decimal, percentage: Decimal):
        self.min_value = min_value
        self.percentage = percentage
    
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        if subtotal >= self.min_value:
            return subtotal * self.percentage
        return Decimal('0')


class TieredDiscount(DiscountStrategy):
    """Desconto por faixas de valor."""
    
    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        if subtotal >= Decimal('500'):
            return subtotal * Decimal('0.20')  # 20% desconto
        elif subtotal >= Decimal('100'):
            return subtotal * Decimal('0.10')  # 10% desconto
        return Decimal('0')


# Strategy Pattern para Frete
class ShippingStrategy(ABC):
    """Interface para estratégias de frete."""
    
    @abstractmethod
    def calculate_shipping(self, subtotal: Decimal) -> Decimal:
        """Calcula custo de frete."""
        pass


class StandardShipping(ShippingStrategy):
    """Frete padrão."""
    
    def __init__(self, free_shipping_threshold: Decimal, base_cost: Decimal):
        self.threshold = free_shipping_threshold
        self.base_cost = base_cost
    
    def calculate_shipping(self, subtotal: Decimal) -> Decimal:
        if subtotal >= self.threshold:
            return Decimal('0')
        return self.base_cost


# Repository Pattern para Acesso a Dados
class OrderRepository(Protocol):
    """Interface para repositório de pedidos."""
    
    def save(self, order: Order, total: Decimal) -> int:
        """Salva pedido e retorna ID."""
        ...


class InMemoryOrderRepository:
    """Repositório em memória (para testes)."""
    
    def __init__(self):
        self.orders = []
    
    def save(self, order: Order, total: Decimal) -> int:
        order_id = len(self.orders) + 1
        self.orders.append({
            'id': order_id,
            'customer_email': order.customer_email,
            'total': total
        })
        return order_id


# Service para Notificações
class NotificationService(Protocol):
    """Interface para serviço de notificações."""
    
    def send_order_confirmation(self, email: str, order_id: int, total: Decimal) -> None:
        """Envia confirmação de pedido."""
        ...


class EmailNotificationService:
    """Serviço de notificação por email."""
    
    def send_order_confirmation(self, email: str, order_id: int, total: Decimal) -> None:
        # Simulação de envio de email
        print(f"[EMAIL] Enviado para {email}")
        print(f"        Pedido #{order_id} - Total: R$ {total:.2f}")


class ConsoleNotificationService:
    """Serviço de notificação por console (para desenvolvimento)."""
    
    def send_order_confirmation(self, email: str, order_id: int, total: Decimal) -> None:
        print(f"[CONSOLE] Pedido #{order_id} confirmado para {email} - R$ {total:.2f}")


# Service Principal - Orquestra as operações
class OrderProcessor:
    """Processa pedidos aplicando regras de negócio."""
    
    def __init__(
        self,
        repository: OrderRepository,
        notification_service: NotificationService,
        discount_strategy: DiscountStrategy,
        shipping_strategy: ShippingStrategy
    ):
        self.repository = repository
        self.notification_service = notification_service
        self.discount_strategy = discount_strategy
        self.shipping_strategy = shipping_strategy
    
    def process_order(self, order: Order) -> dict:
        """
        Processa um pedido completo.
        
        Returns:
            Dict com resultado do processamento
        """
        try:
            # Validar pedido
            order.validate()
            
            # Calcular valores
            subtotal = order.get_subtotal()
            discount = self.discount_strategy.calculate_discount(subtotal)
            shipping = self.shipping_strategy.calculate_shipping(subtotal)
            total = subtotal - discount + shipping
            
            # Salvar pedido
            order_id = self.repository.save(order, total)
            
            # Enviar notificação
            self.notification_service.send_order_confirmation(
                order.customer_email,
                order_id,
                total
            )
            
            return {
                'success': True,
                'order_id': order_id,
                'subtotal': float(subtotal),
                'discount': float(discount),
                'shipping': float(shipping),
                'total': float(total)
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Erro inesperado: {str(e)}"
            }


# Demonstração de uso
def main():
    print("=== Exemplo de Refatoração: Antes e Depois ===\n")
    
    # Criar pedido
    items = [
        OrderItem("P1", "Produto A", Decimal('50.00'), 2),
        OrderItem("P2", "Produto B", Decimal('30.00'), 1),
    ]
    order = Order(customer_email="cliente@example.com", items=items)
    
    # Configurar dependências
    repository = InMemoryOrderRepository()
    notification = ConsoleNotificationService()
    discount = TieredDiscount()
    shipping = StandardShipping(
        free_shipping_threshold=Decimal('200'),
        base_cost=Decimal('10')
    )
    
    # Processar pedido
    processor = OrderProcessor(repository, notification, discount, shipping)
    result = processor.process_order(order)
    
    # Exibir resultado
    if result['success']:
        print("\n✓ Pedido processado com sucesso!")
        print(f"  Pedido ID: {result['order_id']}")
        print(f"  Subtotal:  R$ {result['subtotal']:.2f}")
        print(f"  Desconto:  R$ {result['discount']:.2f}")
        print(f"  Frete:     R$ {result['shipping']:.2f}")
        print(f"  Total:     R$ {result['total']:.2f}")
    else:
        print(f"\n✗ Erro: {result['error']}")
    
    # Demonstrar flexibilidade
    print("\n\n=== Alterando Estratégias ===\n")
    
    # Pedido maior com desconto diferente
    items2 = [
        OrderItem("P3", "Produto C", Decimal('200.00'), 3),
    ]
    order2 = Order(customer_email="cliente2@example.com", items=items2)
    
    # Usar desconto percentual
    processor2 = OrderProcessor(
        repository,
        EmailNotificationService(),
        PercentageDiscount(Decimal('500'), Decimal('0.15')),  # 15% acima de 500
        shipping
    )
    
    result2 = processor2.process_order(order2)
    if result2['success']:
        print(f"\n✓ Pedido #{result2['order_id']} - Total: R$ {result2['total']:.2f}")


if __name__ == "__main__":
    main()
