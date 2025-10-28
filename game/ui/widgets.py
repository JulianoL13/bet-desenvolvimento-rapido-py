"""
Componentes modernos de UI com efeitos visuais
"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout


class ModernCard(MDBoxLayout):
    """Card moderno com gradiente e sombra"""
    bg_color = ListProperty([0.1, 0.1, 0.15, 1])
    shadow_color = ListProperty([0, 0, 0, 0.3])
    corner_radius = NumericProperty(15)
    elevation = NumericProperty(8)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.update_graphics()
    
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.shadow_color)
            RoundedRectangle(
                pos=(self.x - 2, self.y - 2),
                size=(self.width + 4, self.height + 4),
                radius=[self.corner_radius]
            )
            
            Color(*self.bg_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.corner_radius]
            )


class GlowButton(MDRaisedButton):
    """Botão com efeito de glow animado"""
    glow_color = ListProperty([0, 0.8, 1, 0.5])
    is_glowing = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(is_glowing=self.toggle_glow)
        self.bind(size=self.update_glow, pos=self.update_glow)
        self.update_glow()
    
    def update_glow(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.glow_color)
            RoundedRectangle(
                pos=(self.x - 2, self.y - 2),
                size=(self.width + 4, self.height + 4),
                radius=[8]
            )
    
    def toggle_glow(self, instance, value):
        if value:
            self.start_glow()
        else:
            self.stop_glow()
    
    def start_glow(self):
        anim = Animation(glow_color=[0, 0.8, 1, 0.8], duration=0.5) + \
               Animation(glow_color=[0, 0.8, 1, 0.3], duration=0.5)
        anim.repeat = True
        anim.start(self)
    
    def stop_glow(self):
        Animation.cancel_all(self)
        self.glow_color = [0, 0.8, 1, 0.5]


class AnimatedMultiplier(MDLabel):
    """Multiplicador com animações suaves"""
    target_value = NumericProperty(1.0)
    current_value = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(target_value=self.animate_to_target)
    
    def animate_to_target(self, instance, value):
        anim = Animation(current_value=value, duration=0.3, t='out_cubic')
        anim.start(self)
    
    def on_current_value(self, instance, value):
        self.text = f'{value:.2f}x'


class GradientBackground(Widget):
    """Fundo com gradiente animado"""
    color1 = ListProperty([0.05, 0.05, 0.1, 1])
    color2 = ListProperty([0.1, 0.05, 0.15, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.update_graphics()
        self.start_gradient_animation()
    
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color1)
            RoundedRectangle(pos=self.pos, size=self.size)
    
    def start_gradient_animation(self):
        def animate_gradient(dt):
            anim1 = Animation(color1=[0.05, 0.05, 0.1, 1], duration=3)
            anim2 = Animation(color2=[0.1, 0.05, 0.15, 1], duration=3)
            anim1.start(self)
            anim2.start(self)
        
        Clock.schedule_interval(animate_gradient, 6)



class FloatingHistoryItem(Widget):
    """Item do histórico com efeito flutuante"""
    text = StringProperty('1.00x')
    bg_color = ListProperty([0.2, 0.4, 0.8, 0.8])
    is_floating = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (60, 40)
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.update_graphics()
        
        self.label = MDLabel(
            text=self.text,
            theme_text_color='Custom',
            text_color=[1, 1, 1, 1],
            font_size='14sp',
            bold=True,
            halign='center',
            valign='center'
        )
        self.add_widget(self.label)
        
        if self.is_floating:
            self.start_floating_animation()
    
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[8])
    
    def start_floating_animation(self):
        anim = Animation(y=self.y + 5, duration=2, t='in_out_sine') + \
               Animation(y=self.y - 5, duration=2, t='in_out_sine')
        anim.repeat = True
        anim.start(self)


class ModernWinnerItem(MDBoxLayout):
    """Item de winner com design moderno"""
    name = StringProperty('Player')
    amount = NumericProperty(0)
    multiplier = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 0.2
        self.spacing = '5dp'
        self.padding = '10dp'
        
        self.avatar = Widget(size_hint_y=0.4)
        self.avatar.canvas.add(Color(0.2, 0.6, 1, 1))
        self.avatar.canvas.add(Ellipse(pos=self.avatar.pos, size=self.avatar.size))
        
        self.name_label = MDLabel(
            text=self.name,
            theme_text_color='Custom',
            text_color=[0.9, 0.9, 1, 1],
            font_size='12sp',
            halign='center',
            size_hint_y=0.3
        )
        
        self.amount_label = MDLabel(
            text=f'R$ {self.amount:.0f}',
            theme_text_color='Custom',
            text_color=[0.2, 0.8, 0.2, 1],
            font_size='14sp',
            bold=True,
            halign='center',
            size_hint_y=0.3
        )
        
        self.add_widget(self.avatar)
        self.add_widget(self.name_label)
        self.add_widget(self.amount_label)
        
        self.bind(name=self.update_name)
        self.bind(amount=self.update_amount)
    
    def update_name(self, instance, value):
        self.name_label.text = value
        self.avatar.canvas.clear()
        with self.avatar.canvas:
            Color(0.2, 0.6, 1, 1)
            Ellipse(pos=self.avatar.pos, size=self.avatar.size)
    
    def update_amount(self, instance, value):
        self.amount_label.text = f'R$ {value:.0f}'


class PulseEffect(Widget):
    """Efeito de pulso para elementos importantes"""
    pulse_color = ListProperty([1, 1, 1, 0.3])
    pulse_size = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_pulse()
    
    def start_pulse(self):
        anim = Animation(pulse_size=1.2, duration=1, t='in_out_sine') + \
               Animation(pulse_size=1.0, duration=1, t='in_out_sine')
        anim.repeat = True
        anim.start(self)
    
    def on_pulse_size(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            Color(*self.pulse_color)
            Ellipse(
                pos=(self.x - (self.width * (value - 1) / 2), 
                     self.y - (self.height * (value - 1) / 2)),
                size=(self.width * value, self.height * value)
            )
