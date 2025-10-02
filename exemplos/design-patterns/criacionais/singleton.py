"""
Padrão Singleton

Garante que uma classe tenha apenas uma instância e fornece um ponto global de acesso a ela.

Quando usar:
- Quando precisa de exatamente uma instância de uma classe
- Quando a instância deve ser acessível de vários pontos
- Para gerenciar recursos compartilhados (conexão DB, logger, config)
"""

from typing import Optional


# Implementação 1: Usando metaclass
class SingletonMeta(type):
    """Metaclass que implementa o padrão Singleton."""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """Exemplo de classe Singleton usando metaclass."""
    
    def __init__(self):
        self.connection = "Database Connection"
    
    def query(self, sql: str) -> str:
        return f"Executing: {sql}"


# Implementação 2: Usando decorador
def singleton(cls):
    """Decorador que implementa o padrão Singleton."""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Logger:
    """Exemplo de classe Singleton usando decorador."""
    
    def __init__(self):
        self.logs = []
    
    def log(self, message: str) -> None:
        self.logs.append(message)
        print(f"[LOG] {message}")


# Implementação 3: Usando __new__ (mais Pythonic)
class Configuration:
    """Exemplo de classe Singleton usando __new__."""
    
    _instance: Optional['Configuration'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.settings = {}
    
    def set(self, key: str, value: str) -> None:
        self.settings[key] = value
    
    def get(self, key: str) -> Optional[str]:
        return self.settings.get(key)


# Demonstração de uso
def main():
    print("=== Singleton Pattern Examples ===\n")
    
    # Exemplo 1: Database (Metaclass)
    print("1. Database Singleton (Metaclass):")
    db1 = Database()
    db2 = Database()
    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"db1.query('SELECT *'): {db1.query('SELECT *')}")
    print()
    
    # Exemplo 2: Logger (Decorator)
    print("2. Logger Singleton (Decorator):")
    logger1 = Logger()
    logger2 = Logger()
    print(f"logger1 is logger2: {logger1 is logger2}")  # True
    logger1.log("First message")
    logger2.log("Second message")
    print(f"Total logs: {len(logger1.logs)}")  # 2
    print()
    
    # Exemplo 3: Configuration (__new__)
    print("3. Configuration Singleton (__new__):")
    config1 = Configuration()
    config1.set("app_name", "MyApp")
    config2 = Configuration()
    print(f"config1 is config2: {config1 is config2}")  # True
    print(f"config2.get('app_name'): {config2.get('app_name')}")  # MyApp
    print()


if __name__ == "__main__":
    main()
