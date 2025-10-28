"""
Implementação do jogo Crash usando a arquitetura modular
"""
import random
from typing import Optional
from game.core.base_game import BaseGame, BetItem


class GameState:
    """Estados possíveis do jogo Crash"""
    WAITING = "waiting"
    BETTING = "betting"
    FLYING = "flying"
    CRASHED = "crashed"


class CrashBetItem(BetItem):
    """Aposta específica do Crash com auto-cashout"""
    def __init__(self, amount: float, auto_cashout: Optional[float] = None):
        super().__init__(amount)
        self.auto_cashout = auto_cashout


class CrashGame(BaseGame):
    """Implementação do jogo Crash"""
    
    def __init__(self):
        super().__init__()
        self.state = GameState.WAITING
        self.current_multiplier = 1.0
        self.crash_multiplier = 0.0
        
        self.betting_time = 7
        self.round_interval = 5
        self.countdown_timer = 0
        
        # Callbacks específicos do Crash
        self.on_multiplier_update: Optional[callable] = None
        self.on_crash: Optional[callable] = None
        self.on_auto_cashout: Optional[callable] = None
    
    def start_new_round(self):
        """Inicia uma nova rodada"""
        self.state = GameState.BETTING
        self.current_multiplier = 1.0
        self.crashed = False
        self.crash_multiplier = self._generate_crash_multiplier()
        self.active_bets.clear()
        self.countdown_timer = self.betting_time
        
        if self.on_state_change:
            self.on_state_change(self.state, self.countdown_timer)
    
    def can_bet(self) -> bool:
        """Retorna se é possível fazer apostas"""
        return self.state == GameState.BETTING
    
    def add_bet(self, amount: float, **kwargs) -> bool:
        """Adiciona uma nova aposta"""
        if not self.can_bet():
            return False
            
        if len(self.active_bets) >= 5:
            return False
        
        auto_cashout = kwargs.get('auto_cashout')
        new_bet = CrashBetItem(amount, auto_cashout)
        self.active_bets.append(new_bet)
        return True
    
    def can_cashout(self) -> bool:
        """Retorna se é possível fazer cashout"""
        return self.state == GameState.FLYING
    
    def cashout_all(self) -> float:
        """Retira todas as apostas ativas"""
        if not self.can_cashout():
            return 0.0
            
        total_winnings = 0.0
        for bet in self.active_bets:
            if not bet.cashed_out:
                winnings = bet.amount * self.current_multiplier
                bet.cashed_out = True
                bet.cashout_multiplier = self.current_multiplier
                total_winnings += winnings
                
        return total_winnings
    
    def clear_bets(self) -> float:
        """Limpa todas as apostas"""
        if self.state != GameState.BETTING:
            return 0.0
            
        total_returned = sum(bet.amount for bet in self.active_bets)
        self.active_bets.clear()
        return total_returned
    
    def get_game_state(self) -> str:
        """Retorna o estado atual do jogo"""
        return self.state
    
    def cleanup(self):
        """Limpa recursos"""
        self.active_bets.clear()
        self.on_state_change = None
        self.on_multiplier_update = None
        self.on_crash = None
        self.on_auto_cashout = None
    
    def _generate_crash_multiplier(self) -> float:
        """Gera um multiplicador de crash com distribuição específica"""
        r = random.random()
        
        if r < 0.60:
            multiplier = random.uniform(1.01, 2.0)
        elif r < 0.90:
            multiplier = random.uniform(3.0, 9.0)
        elif r < 0.99:
            multiplier = random.uniform(10.0, 20.0)
        else:
            multiplier = random.uniform(20.0, 100.0)
            
        return round(multiplier, 2)
    
    def update_betting_countdown(self) -> bool:
        """Atualiza o countdown de apostas"""
        if self.state != GameState.BETTING:
            return False
            
        self.countdown_timer -= 1
        
        if self.countdown_timer <= 0:
            self.start_flying()
            return False
            
        if self.on_state_change:
            self.on_state_change(self.state, self.countdown_timer)
        return True
    
    def start_flying(self):
        """Inicia a fase de voo"""
        self.state = GameState.FLYING
        if self.on_state_change:
            self.on_state_change(self.state, 0)
    
    def update_multiplier(self) -> bool:
        """Atualiza o multiplicador durante o voo"""
        if self.state != GameState.FLYING:
            return False
        
        base_increment = 0.008
        
        if self.current_multiplier < 2.0:
            increment = base_increment + (self.current_multiplier * 0.002)
        elif self.current_multiplier < 5.0:
            factor = (self.current_multiplier - 2.0) / 3.0
            increment = base_increment + (self.current_multiplier * 0.003) + (factor * 0.01)
        elif self.current_multiplier < 10.0:
            factor = (self.current_multiplier - 5.0) / 5.0
            increment = base_increment + (self.current_multiplier * 0.004) + (factor * 0.02)
        else:
            factor = (self.current_multiplier - 10.0) / 20.0
            increment = base_increment + (self.current_multiplier * 0.005) + (factor * 0.03)
        
        new_multiplier = self.current_multiplier + increment
        
        if new_multiplier >= self.crash_multiplier:
            self.current_multiplier = self.crash_multiplier
        else:
            self.current_multiplier = new_multiplier
        
        self._check_auto_cashouts()
        
        if self.current_multiplier >= self.crash_multiplier:
            self.crash()
            return False
            
        if self.on_multiplier_update:
            self.on_multiplier_update(self.current_multiplier)
        return True
    
    def _check_auto_cashouts(self):
        """Verifica e executa auto-cashouts"""
        for bet in self.active_bets:
            if isinstance(bet, CrashBetItem):
                if (not bet.cashed_out and 
                    bet.auto_cashout and 
                    self.current_multiplier >= bet.auto_cashout):
                    
                    bet.cashed_out = True
                    bet.cashout_multiplier = self.current_multiplier
                    winnings = bet.amount * bet.cashout_multiplier
                    
                    if self.on_auto_cashout:
                        self.on_auto_cashout(bet, bet.cashout_multiplier, winnings)
    
    def crash(self):
        """Processa o crash"""
        self.state = GameState.CRASHED
        self.last_results.insert(0, self.crash_multiplier)
        if len(self.last_results) > 10:
            self.last_results.pop()
            
        if self.on_state_change:
            self.on_state_change(self.state, 0)
            
        if self.on_crash:
            self.on_crash(self.crash_multiplier)
