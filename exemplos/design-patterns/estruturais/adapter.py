"""
Padrão Adapter (Adaptador)

Converte a interface de uma classe em outra interface que os clientes esperam.
O Adapter permite que classes com interfaces incompatíveis trabalhem juntas.

Quando usar:
- Quando você quer usar uma classe existente mas sua interface não é compatível
- Quando você quer criar uma classe reutilizável que coopera com classes não relacionadas
- Quando você precisa usar várias subclasses mas é impraticável adaptar suas interfaces
"""

from abc import ABC, abstractmethod


# Target Interface - Interface esperada pelo cliente
class MediaPlayer(ABC):
    """Interface que o cliente espera usar."""
    
    @abstractmethod
    def play(self, audio_type: str, filename: str) -> str:
        pass


# Adaptee - Classe existente com interface incompatível
class AdvancedMediaPlayer(ABC):
    """Interface de um player avançado (incompatível com MediaPlayer)."""
    
    @abstractmethod
    def play_vlc(self, filename: str) -> str:
        pass
    
    @abstractmethod
    def play_mp4(self, filename: str) -> str:
        pass


class VlcPlayer(AdvancedMediaPlayer):
    """Implementação concreta para VLC."""
    
    def play_vlc(self, filename: str) -> str:
        return f"Reproduzindo arquivo VLC: {filename}"
    
    def play_mp4(self, filename: str) -> str:
        return "VlcPlayer não suporta MP4"


class Mp4Player(AdvancedMediaPlayer):
    """Implementação concreta para MP4."""
    
    def play_vlc(self, filename: str) -> str:
        return "Mp4Player não suporta VLC"
    
    def play_mp4(self, filename: str) -> str:
        return f"Reproduzindo arquivo MP4: {filename}"


# Adapter - Adapta AdvancedMediaPlayer para MediaPlayer
class MediaAdapter(MediaPlayer):
    """Adaptador que torna AdvancedMediaPlayer compatível com MediaPlayer."""
    
    def __init__(self, audio_type: str):
        self.audio_type = audio_type
        
        if audio_type == "vlc":
            self.advanced_player = VlcPlayer()
        elif audio_type == "mp4":
            self.advanced_player = Mp4Player()
        else:
            self.advanced_player = None
    
    def play(self, audio_type: str, filename: str) -> str:
        if audio_type == "vlc":
            return self.advanced_player.play_vlc(filename)
        elif audio_type == "mp4":
            return self.advanced_player.play_mp4(filename)
        return f"Formato não suportado: {audio_type}"


# Concrete Target - Implementação da interface alvo
class AudioPlayer(MediaPlayer):
    """Player de áudio que usa o adapter para formatos avançados."""
    
    def play(self, audio_type: str, filename: str) -> str:
        # Suporte nativo para MP3
        if audio_type == "mp3":
            return f"Reproduzindo arquivo MP3: {filename}"
        
        # Usa adapter para outros formatos
        elif audio_type in ["vlc", "mp4"]:
            adapter = MediaAdapter(audio_type)
            return adapter.play(audio_type, filename)
        
        else:
            return f"Formato inválido: {audio_type}"


# Exemplo 2: Adapter para APIs diferentes
class OldPaymentAPI:
    """API antiga de pagamento."""
    
    def process_payment(self, amount: float, card: str) -> dict:
        return {
            "success": True,
            "transaction_id": "OLD123",
            "amount_paid": amount,
            "card_used": card
        }


class NewPaymentAPI:
    """Nova API de pagamento com interface diferente."""
    
    def execute_transaction(self, payment_data: dict) -> dict:
        return {
            "status": "approved",
            "id": "NEW456",
            "total": payment_data["amount"],
            "method": payment_data["payment_method"]
        }


class PaymentProcessor(ABC):
    """Interface unificada para processamento de pagamentos."""
    
    @abstractmethod
    def pay(self, amount: float, payment_method: str) -> dict:
        pass


class OldPaymentAdapter(PaymentProcessor):
    """Adapta a API antiga para a interface unificada."""
    
    def __init__(self):
        self.old_api = OldPaymentAPI()
    
    def pay(self, amount: float, payment_method: str) -> dict:
        # Adapta a chamada
        result = self.old_api.process_payment(amount, payment_method)
        
        # Converte resposta para formato unificado
        return {
            "status": "success" if result["success"] else "failed",
            "transaction_id": result["transaction_id"],
            "amount": result["amount_paid"]
        }


class NewPaymentAdapter(PaymentProcessor):
    """Adapta a nova API para a interface unificada."""
    
    def __init__(self):
        self.new_api = NewPaymentAPI()
    
    def pay(self, amount: float, payment_method: str) -> dict:
        # Adapta a chamada
        payment_data = {
            "amount": amount,
            "payment_method": payment_method
        }
        result = self.new_api.execute_transaction(payment_data)
        
        # Converte resposta para formato unificado
        return {
            "status": result["status"],
            "transaction_id": result["id"],
            "amount": result["total"]
        }


class PaymentService:
    """Serviço que usa adaptadores para processar pagamentos."""
    
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor
    
    def checkout(self, amount: float, payment_method: str) -> str:
        result = self.processor.pay(amount, payment_method)
        
        if result["status"] in ["success", "approved"]:
            return (f"Pagamento aprovado!\n"
                   f"ID: {result['transaction_id']}\n"
                   f"Valor: R$ {result['amount']:.2f}")
        else:
            return "Pagamento recusado!"


# Demonstração de uso
def main():
    print("=== Adapter Pattern Examples ===\n")
    
    # Exemplo 1: Media Player
    print("1. Media Player Adapter:")
    player = AudioPlayer()
    
    print(player.play("mp3", "musica.mp3"))
    print(player.play("mp4", "video.mp4"))
    print(player.play("vlc", "filme.vlc"))
    print(player.play("avi", "video.avi"))
    print()
    
    # Exemplo 2: Payment API Adapter
    print("2. Payment API Adapters:")
    
    # Usando API antiga
    print("Usando API antiga:")
    old_service = PaymentService(OldPaymentAdapter())
    print(old_service.checkout(100.0, "Cartão 1234"))
    print()
    
    # Usando API nova
    print("Usando API nova:")
    new_service = PaymentService(NewPaymentAdapter())
    print(new_service.checkout(200.0, "Cartão 5678"))
    print()
    
    # Vantagem: código cliente não precisa mudar ao trocar APIs
    print("3. Fácil troca entre implementações:")
    services = [
        ("Old API", PaymentService(OldPaymentAdapter())),
        ("New API", PaymentService(NewPaymentAdapter()))
    ]
    
    for name, service in services:
        print(f"{name}: {service.checkout(50.0, 'PIX').split('!')[0]}!")


if __name__ == "__main__":
    main()
