"""
Motor principal do jogo Crash
"""
import random


class BetItem:
    """Representa uma aposta individual"""
    def __init__(self, amount, auto_cashout=None):
        self.amount = amount
        self.auto_cashout = auto_cashout
        self.cashed_out = False
        self.cashout_multiplier = 0


class GameState:
    """Estados possíveis do jogo"""
    WAITING = "waiting"
    BETTING = "betting"
    FLYING = "flying"
    CRASHED = "crashed"


class GameEngine:
    """Gerencia a lógica principal do jogo"""
    def __init__(self):
        self.state = GameState.WAITING
        self.current_multiplier = 1.0
        self.crash_multiplier = 0.0
        self.active_bets = []
        self.last_results = []
        
        self.betting_time = 7
        self.round_interval = 5
        self.countdown_timer = 0
        
        self.on_state_change = None
        self.on_multiplier_update = None
        self.on_crash = None
        self.on_auto_cashout = None
        
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
    
    def _generate_crash_multiplier(self):
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
    
    def update_betting_countdown(self):
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
    
    def update_multiplier(self):
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
    
    def add_bet(self, amount, auto_cashout=None):
        """Adiciona uma nova aposta"""
        if self.state != GameState.BETTING:
            return False
            
        if len(self.active_bets) >= 5:
            return False
            
        new_bet = BetItem(amount, auto_cashout)
        self.active_bets.append(new_bet)
        return True
    
    def cashout_all(self):
        """Retira todas as apostas ativas"""
        if self.state != GameState.FLYING:
            return 0.0
            
        total_winnings = 0.0
        for bet in self.active_bets:
            if not bet.cashed_out:
                winnings = bet.amount * self.current_multiplier
                bet.cashed_out = True
                bet.cashout_multiplier = self.current_multiplier
                total_winnings += winnings
                
        return total_winnings
    
    def clear_bets(self):
        """Limpa todas as apostas"""
        if self.state != GameState.BETTING:
            return 0.0
            
        total_returned = sum(bet.amount for bet in self.active_bets)
        self.active_bets.clear()
        return total_returned
    
    def get_active_bets_total(self):
        """Retorna o total das apostas ativas"""
        return sum(bet.amount for bet in self.active_bets)