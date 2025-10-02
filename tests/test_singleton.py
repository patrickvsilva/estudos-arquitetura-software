"""
Testes para o padrão Singleton.

Demonstra como testar design patterns e boas práticas de testes.
"""

import sys
from pathlib import Path
import importlib.util

# Adiciona o diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Import do módulo com hífen no nome
spec = importlib.util.spec_from_file_location(
    "singleton",
    root_dir / "exemplos" / "design-patterns" / "criacionais" / "singleton.py"
)
singleton_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(singleton_module)

Database = singleton_module.Database
Logger = singleton_module.Logger
Configuration = singleton_module.Configuration


class TestSingletonDatabase:
    """Testes para Database Singleton (usando metaclass)."""
    
    def test_singleton_instance(self):
        """Verifica que sempre retorna a mesma instância."""
        db1 = Database()
        db2 = Database()
        assert db1 is db2
    
    def test_shared_state(self):
        """Verifica que o estado é compartilhado entre instâncias."""
        db1 = Database()
        original_connection = db1.connection
        
        db2 = Database()
        assert db2.connection == original_connection


class TestSingletonLogger:
    """Testes para Logger Singleton (usando decorador)."""
    
    def test_singleton_instance(self):
        """Verifica que sempre retorna a mesma instância."""
        logger1 = Logger()
        logger2 = Logger()
        assert logger1 is logger2
    
    def test_shared_logs(self):
        """Verifica que os logs são compartilhados."""
        logger1 = Logger()
        initial_count = len(logger1.logs)
        
        logger1.log("Test message 1")
        
        logger2 = Logger()
        logger2.log("Test message 2")
        
        # Ambos devem ter acesso aos mesmos logs
        assert len(logger1.logs) == len(logger2.logs)
        assert len(logger1.logs) == initial_count + 2


class TestSingletonConfiguration:
    """Testes para Configuration Singleton (usando __new__)."""
    
    def test_singleton_instance(self):
        """Verifica que sempre retorna a mesma instância."""
        config1 = Configuration()
        config2 = Configuration()
        assert config1 is config2
    
    def test_shared_settings(self):
        """Verifica que as configurações são compartilhadas."""
        config1 = Configuration()
        config1.set("test_key", "test_value")
        
        config2 = Configuration()
        assert config2.get("test_key") == "test_value"
    
    def test_initialization_once(self):
        """Verifica que __init__ só executa uma vez."""
        config1 = Configuration()
        original_settings = config1.settings.copy()
        
        config2 = Configuration()
        # settings deve ser o mesmo objeto
        assert config2.settings is config1.settings
