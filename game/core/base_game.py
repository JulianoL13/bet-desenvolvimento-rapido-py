"""
Classe base abstrata para todos os jogos
Define a interface comum que todos os jogos devem implementar
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Callable


class BetItem:
    """Representa uma aposta individual (compartilhada entre todos os jogos)"""
    def __init__(self, amount: float, **kwargs):
        self.amount = amount
        self.cashed_out = False
        self.cashout_multiplier = 0.0
        self.extra_data = kwargs  # Dados extras específicos do jogo


class BaseGame(ABC):
    """
    Classe base abstrata para todos os jogos
    Define a interface que todos os jogos devem seguir
    """
    
    def __init__(self):
        self.active_bets: List[BetItem] = []
        self.last_results: List[float] = []
        
        # Callbacks que a UI pode assinar
        self.on_state_change: Optional[Callable] = None
        self.on_result: Optional[Callable] = None
        self.on_bet_outcome: Optional[Callable] = None
    
    @abstractmethod
    def start_new_round(self):
        """Inicia uma nova rodada do jogo"""
        pass
    
    @abstractmethod
    def can_bet(self) -> bool:
        """Retorna se é possível fazer apostas no momento"""
        pass
    
    @abstractmethod
    def add_bet(self, amount: float, **kwargs) -> bool:
        """
        Adiciona uma nova aposta
        Args:
            amount: Valor da aposta
            **kwargs: Parâmetros específicos do jogo (ex: auto_cashout para Crash)
        Returns:
            True se a aposta foi adicionada com sucesso
        """
        pass
    
    @abstractmethod
    def can_cashout(self) -> bool:
        """Retorna se é possível fazer cashout no momento"""
        pass
    
    @abstractmethod
    def cashout_all(self) -> float:
        """
        Retira todas as apostas ativas
        Returns:
            Total de ganhos
        """
        pass
    
    @abstractmethod
    def clear_bets(self) -> float:
        """
        Cancela todas as apostas ativas (se possível)
        Returns:
            Total devolvido
        """
        pass
    
    @abstractmethod
    def get_game_state(self) -> str:
        """Retorna o estado atual do jogo"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """Limpa recursos quando o jogo é fechado"""
        pass
    
    def get_active_bets_total(self) -> float:
        """Retorna o total das apostas ativas"""
        return sum(bet.amount for bet in self.active_bets)
    
    def get_game_name(self) -> str:
        """Retorna o nome do jogo"""
        return self.__class__.__name__.replace('Game', '')
