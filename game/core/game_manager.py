"""
Gerenciador global do estado da aplicação
Singleton que gerencia saldo, jogos disponíveis e jogo atual
"""
from typing import Dict, Optional, Type
from game.core.base_game import BaseGame


class GameManager:
    """Gerencia o estado global da aplicação (Singleton)"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.balance: float = 1000.0
        self.available_games: Dict[str, Type[BaseGame]] = {}
        self.current_game: Optional[BaseGame] = None
        self._initialized = True
    
    def register_game(self, game_name: str, game_class: Type[BaseGame]):
        """Registra um novo jogo disponível"""
        self.available_games[game_name] = game_class
    
    def set_current_game(self, game_name: str) -> BaseGame:
        """
        Define o jogo atual
        Args:
            game_name: Nome do jogo a ser ativado
        Returns:
            Instância do jogo
        """
        if self.current_game:
            self.current_game.cleanup()
        
        game_class = self.available_games.get(game_name)
        if not game_class:
            raise ValueError(f"Jogo '{game_name}' não encontrado")
        
        self.current_game = game_class()
        return self.current_game
    
    def get_current_game(self) -> Optional[BaseGame]:
        """Retorna o jogo atual"""
        return self.current_game
    
    def add_balance(self, amount: float):
        """Adiciona ao saldo"""
        self.balance += amount
    
    def subtract_balance(self, amount: float) -> bool:
        """
        Subtrai do saldo
        Returns:
            True se tinha saldo suficiente
        """
        if amount > self.balance:
            return False
        self.balance -= amount
        return True
    
    def get_balance(self) -> float:
        """Retorna o saldo atual"""
        return self.balance
    
    def reset_balance(self, initial_balance: float = 1000.0):
        """Reseta o saldo para valor inicial"""
        self.balance = initial_balance
