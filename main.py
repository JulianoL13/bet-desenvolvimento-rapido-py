"""
Aplicação principal do jogo Crash
"""
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import Snackbar
from kivy.factory import Factory
from kivy.properties import BooleanProperty, NumericProperty
import random

from game.logic.engine import GameEngine, GameState
from game.ui.components import HistorySquare, WinnerItem
from game.ui.widgets import (
    ModernCard, GlowButton, AnimatedMultiplier, 
    GradientBackground, FloatingHistoryItem, ModernWinnerItem, PulseEffect
)
from game.ui.theme import theme


def show_snackbar(text):
    """Exibe mensagem de feedback ao usuário"""
    snackbar = Snackbar(text=text)
    snackbar.open()


class MainScreen(Screen):
    """Tela principal do jogo"""
    auto_cashout_enabled = BooleanProperty(False)
    bet_amount = NumericProperty(10.0)
    auto_cashout_value = NumericProperty(5.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(auto_cashout_enabled=self.update_checkbox_color)
        
        self.game_engine = GameEngine()
        self.game_engine.on_state_change = self.on_game_state_change
        self.game_engine.on_multiplier_update = self.on_multiplier_update
        self.game_engine.on_crash = self.on_crash
        self.game_engine.on_auto_cashout = self.on_auto_cashout
        
        self.balance = 1000.00
        self.names = [
            "An***ymous", "Pl***er", "Ga***r", "Lu***y", "Wi***r",
            "Cr***h", "Be***r", "Fa***t", "Bi***n", "Ac***e",
            "Ph***x", "Sh***w", "Vo***x", "Bl***e", "Ti***n",
            "Sp***e", "Ro***e", "Ze***h", "No***a", "St***r",
            "An***us", "Us***r", "Pl***r", "Ga***r", "Wi***r"
        ]
        
        Clock.schedule_once(self.start_new_round, 2)
        Clock.schedule_interval(self.update_winners_display, 3)
    
    def start_new_round(self, dt):
        """Inicia uma nova rodada"""
        self.game_engine.start_new_round()
        self.update_balance_display()
    
    def on_game_state_change(self, state, countdown):
        """Callback quando o estado do jogo muda"""
        if state == GameState.BETTING:
            self.ids.round_status.text = 'Apostas abertas!'
            self.ids.countdown.text = f'{countdown}s'
            self.ids.cashout_btn.disabled = True
            self.ids.bet_button.disabled = False
            self.update_bets_display()
            self.animate_countdown()
            Clock.unschedule(self.update_countdown)
            Clock.schedule_interval(self.update_countdown, 1)
            
        elif state == GameState.FLYING:
            self.ids.round_status.text = 'Decolando!'
            self.ids.countdown.text = ''
            self.ids.cashout_btn.disabled = False
            self.ids.bet_button.disabled = True
            self.animate_takeoff()
            Clock.unschedule(self.update_countdown)
            Clock.schedule_interval(self.update_multiplier, 0.1)
            
        elif state == GameState.CRASHED:
            self.ids.round_status.text = f'CRASH em {self.game_engine.crash_multiplier:.2f}x!'
            self.ids.cashout_btn.disabled = True
            Clock.unschedule(self.update_multiplier)
            self.animate_plane_crash()
            Clock.schedule_once(self.start_new_round, self.game_engine.round_interval)
    
    def update_countdown(self, dt):
        """Atualiza o countdown de apostas"""
        if not self.game_engine.update_betting_countdown():
            Clock.unschedule(self.update_countdown)
        else:
            self.ids.countdown.text = f'{self.game_engine.countdown_timer}s'
            self.animate_countdown_number()
    
    def update_multiplier(self, dt):
        """Atualiza o multiplicador"""
        if not self.game_engine.update_multiplier():
            Clock.unschedule(self.update_multiplier)
    
    def on_multiplier_update(self, multiplier):
        """Callback quando o multiplicador é atualizado"""
        self.ids.multiplier_display.text = f'{multiplier:.2f}x'
        
        all_cashed_out = all(bet.cashed_out for bet in self.game_engine.active_bets if self.game_engine.active_bets)
        if all_cashed_out and self.game_engine.active_bets:
            self.ids.multiplier_display.text_color = [1, 0.5, 0, 1]
        else:
            self.ids.multiplier_display.text_color = [0, 1, 0, 1]
    
    def on_crash(self, crash_multiplier):
        """Callback quando ocorre o crash"""
        self.update_history_display()
    
    def on_auto_cashout(self, bet, multiplier, winnings):
        """Callback quando auto cashout é executado"""
        self.balance += winnings
        show_snackbar(f'Auto cashout! Ganhou R$ {winnings:.2f} em {multiplier:.2f}x')
        self.update_bets_display()
        self.ids.balance_label.text = f'Saldo: R$ {self.balance:.2f}'
    
    def update_winners_display(self, dt):
        """Atualiza a exibição dos winners aleatórios"""
        self.ids.winners_bar.clear_widgets()
        
        for i in range(5):
            name = random.choice(self.names)
            
            rand = random.random()
            if rand < 0.70:
                amount = random.uniform(50, 2000)
                multiplier = random.uniform(1.5, 8.0)
            elif rand < 0.95:
                amount = random.uniform(2000, 15000)
                multiplier = random.uniform(3.0, 25.0)
            else:
                amount = random.uniform(15000, 100000)
                multiplier = random.uniform(10.0, 50.0)
            
            winner_widget = WinnerItem(name=name, amount=amount, multiplier=multiplier)
            winner_widget.size_hint_x = 0.2
            self.ids.winners_bar.add_widget(winner_widget)
    
    def decrease_bet_amount(self):
        """Diminui o valor da aposta"""
        if self.bet_amount > 1:
            self.bet_amount -= 1
            self.ids.bet_amount_input.text = str(int(self.bet_amount))
    
    def increase_bet_amount(self):
        """Aumenta o valor da aposta"""
        if self.bet_amount < self.balance:
            self.bet_amount += 1
            self.ids.bet_amount_input.text = str(int(self.bet_amount))
    
    def set_bet_amount(self, amount):
        """Define o valor da aposta"""
        if amount <= self.balance:
            self.bet_amount = amount
            self.ids.bet_amount_input.text = str(int(amount))
    
    def on_bet_amount_validate(self):
        """Callback quando o usuário pressiona Enter no campo de aposta"""
        try:
            value = float(self.ids.bet_amount_input.text)
            if value > 0 and value <= self.balance:
                self.bet_amount = value
                show_snackbar(f'Valor da aposta definido para R$ {value:.2f}')
            else:
                show_snackbar('Valor inválido! Use um valor entre R$ 0,01 e seu saldo.')
                self.ids.bet_amount_input.text = str(int(self.bet_amount))
        except ValueError:
            show_snackbar('Digite um valor numérico válido!')
            self.ids.bet_amount_input.text = str(int(self.bet_amount))
    
    def on_bet_amount_focus(self, instance, value):
        """Callback quando o campo de aposta ganha/perde foco"""
        if not value:
            self.on_bet_amount_validate()
    
    def decrease_auto_cashout(self):
        """Diminui o valor do auto cashout"""
        if self.auto_cashout_value > 1.1:
            self.auto_cashout_value -= 0.1
    
    def increase_auto_cashout(self):
        """Aumenta o valor do auto cashout"""
        if self.auto_cashout_value < 100:
            self.auto_cashout_value += 0.1
    
    def toggle_auto_cashout(self):
        """Ativa/desativa o auto cashout"""
        self.auto_cashout_enabled = not self.auto_cashout_enabled
    
    def update_checkbox_color(self, instance, value):
        """Atualiza a cor do checkbox baseado no estado"""
        if hasattr(self, 'ids') and 'auto_cashout_checkbox' in self.ids:
            if value:
                self.ids.auto_cashout_checkbox.md_bg_color = [0.2, 0.8, 0.2, 1]
            else:
                self.ids.auto_cashout_checkbox.md_bg_color = [0.4, 0.4, 0.4, 1]
    
    def add_bet(self):
        """Adiciona uma nova aposta"""
        if self.bet_amount <= 0:
            show_snackbar('Valor deve ser maior que zero!')
            return
            
        if self.bet_amount > self.balance:
            show_snackbar('Saldo insuficiente!')
            return
        
        auto_cashout_value = None
        if self.auto_cashout_enabled:
            auto_cashout_value = self.auto_cashout_value
            if auto_cashout_value <= 1.0:
                show_snackbar('Auto Cashout deve ser maior que 1.0x!')
                return
        
        if self.game_engine.add_bet(self.bet_amount, auto_cashout_value):
            self.balance -= self.bet_amount
            self.update_bets_display()
            self.update_balance_display()
            show_snackbar(f'Aposta de R$ {self.bet_amount:.2f} adicionada!')
        else:
            show_snackbar('Não foi possível adicionar a aposta!')
    
    def cashout_all(self):
        """Retira todas as apostas ativas"""
        total_winnings = self.game_engine.cashout_all()
        if total_winnings > 0:
            self.balance += total_winnings
            self.update_bets_display()
            self.update_balance_display()
            show_snackbar(f'Retirada total! Ganho: R$ {total_winnings:.2f}')
            self.animate_plane_exit()
        else:
            show_snackbar('Nenhuma aposta ativa para retirar.')
    
    def clear_bets(self):
        """Limpa todas as apostas ativas"""
        total_returned = self.game_engine.clear_bets()
        if total_returned > 0:
            self.balance += total_returned
            self.update_bets_display()
            self.update_balance_display()
            show_snackbar('Apostas canceladas!')
        else:
            show_snackbar('Não é possível limpar apostas fora da fase de apostas.')
    
    def update_bets_display(self):
        """Atualiza a exibição das apostas ativas"""
        self.ids.bets_list.clear_widgets()
        total_bets = self.game_engine.get_active_bets_total()
        self.ids.total_bets_label.text = f'Apostas: R$ {total_bets:.2f}'
        
        has_bets = len(self.game_engine.active_bets) > 0
        self.ids.clear_bets_btn.disabled = not has_bets
        
        for i, bet in enumerate(self.game_engine.active_bets):
            item = OneLineListItem()
            item.text = f'Aposta {i+1}: R$ {bet.amount:.2f}'
            if bet.auto_cashout:
                item.text += f' (Auto: {bet.auto_cashout:.2f}x)'
            if bet.cashed_out:
                item.text += f' (Retirado em {bet.cashout_multiplier:.2f}x)'
            item.theme_text_color = 'Primary'
            self.ids.bets_list.add_widget(item)
    
    def update_balance_display(self):
        """Atualiza a exibição do saldo"""
        self.ids.balance_label.text = f'Saldo: R$ {self.balance:.2f}'
    
    def update_history_display(self):
        """Atualiza a exibição do histórico de resultados"""
        self.ids.history_container.clear_widgets()
        
        if self.game_engine.last_results:
            recent = self.game_engine.last_results[-5:]
            
            colors = [
                [0.2, 0.8, 0.4, 0.8],
                [1.0, 0.6, 0.2, 0.8],
                [0.3, 0.3, 0.3, 0.8],
                [0.8, 0.2, 0.2, 0.8],
                [0.5, 0.5, 0.5, 0.8],
            ]
            
            for i, result in enumerate(recent):
                history_square = HistorySquare()
                history_square.text = f'{result:.2f}'
                history_square.md_bg_color = colors[i % len(colors)]
                self.ids.history_container.add_widget(history_square)
    
    def animate_plane_exit(self):
        """Anima o avião saindo (cashout)"""
        anim = Animation(text_color=[0, 1, 1, 1], duration=1)
        anim.start(self.ids.multiplier_display)
        Clock.schedule_once(lambda dt: setattr(self.ids.multiplier_display, 'text_color', [0, 1, 0, 1]), 1.1)
    
    def animate_plane_crash(self):
        """Anima o crash"""
        anim = Animation(text_color=[1, 0, 0, 1], duration=0.5)
        anim.start(self.ids.multiplier_display)
        Clock.schedule_once(lambda dt: self.restore_plane(), 2.0)
    
    def restore_plane(self):
        """Restaura o texto após animação"""
        self.ids.multiplier_display.text_color = [0, 1, 0, 1]
    
    def animate_countdown(self):
        """Anima o início da contagem regressiva"""
        anim_status = Animation(
            text_color=[1.0, 0.8, 0.2, 1],
            duration=0.3
        ) + Animation(
            text_color=[0.9, 0.9, 0.9, 1],
            duration=0.3
        )
        anim_status.start(self.ids.round_status)
        
        anim_countdown = Animation(
            text_color=[1.0, 0.6, 0.2, 1],
            duration=0.5
        )
        anim_countdown.start(self.ids.countdown)
    
    def animate_countdown_number(self):
        """Anima cada mudança de número no countdown"""
        anim = Animation(
            text_color=[1.0, 0.4, 0.1, 1],
            duration=0.2
        ) + Animation(
            text_color=[1.0, 0.6, 0.2, 1],
            duration=0.3
        )
        anim.start(self.ids.countdown)
    
    def animate_takeoff(self):
        """Anima a decolagem"""
        anim_status = Animation(
            text_color=[0.2, 0.8, 0.4, 1],
            duration=0.5
        )
        anim_status.start(self.ids.round_status)
        
        def pulse_takeoff():
            anim_pulse = Animation(
                text_color=[0.1, 0.9, 0.3, 1],
                duration=0.8
            ) + Animation(
                text_color=[0.2, 0.8, 0.4, 1],
                duration=0.8
            )
            anim_pulse.start(self.ids.round_status)
            Clock.schedule_once(lambda dt: pulse_takeoff(), 1.6)
        
        Clock.schedule_once(lambda dt: pulse_takeoff(), 0.5)


class PlaneCrashApp(MDApp):
    def build(self):
        Window.size = (1920, 1080)
        Builder.load_file('main.kv')
        
        Factory.register('HistorySquare', HistorySquare)
        Factory.register('WinnerItem', WinnerItem)
        Factory.register('ModernCard', ModernCard)
        Factory.register('GlowButton', GlowButton)
        Factory.register('AnimatedMultiplier', AnimatedMultiplier)
        Factory.register('GradientBackground', GradientBackground)
        Factory.register('FloatingHistoryItem', FloatingHistoryItem)
        Factory.register('ModernWinnerItem', ModernWinnerItem)
        Factory.register('PulseEffect', PulseEffect)
        
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        return sm


if __name__ == '__main__':
    PlaneCrashApp().run()
