"""
Sistema de cores e temas modernos para o jogo
Inspirado em designs React modernos
"""

# Paleta de cores moderna
class ModernColors:
    # Cores principais
    PRIMARY = [0.2, 0.6, 1.0, 1.0]  # Azul vibrante
    SECONDARY = [0.8, 0.2, 0.8, 1.0]  # Magenta
    SUCCESS = [0.2, 0.8, 0.4, 1.0]  # Verde neon
    WARNING = [1.0, 0.6, 0.2, 1.0]  # Laranja
    DANGER = [1.0, 0.2, 0.4, 1.0]  # Vermelho vibrante
    
    # Cores de fundo
    BACKGROUND_DARK = [0.05, 0.05, 0.1, 1.0]  # Preto azulado
    BACKGROUND_CARD = [0.1, 0.1, 0.15, 1.0]  # Cinza escuro
    BACKGROUND_ELEVATED = [0.15, 0.15, 0.2, 1.0]  # Cinza mais claro
    
    # Cores de texto
    TEXT_PRIMARY = [1.0, 1.0, 1.0, 1.0]  # Branco
    TEXT_SECONDARY = [0.8, 0.8, 0.9, 1.0]  # Cinza claro
    TEXT_MUTED = [0.6, 0.6, 0.7, 1.0]  # Cinza médio
    
    # Cores especiais
    GLOW_BLUE = [0.0, 0.8, 1.0, 0.5]  # Azul com brilho
    GLOW_GREEN = [0.2, 1.0, 0.4, 0.5]  # Verde com brilho
    GLOW_PURPLE = [0.8, 0.2, 1.0, 0.5]  # Roxo com brilho
    
    # Gradientes (simulados com cores)
    GRADIENT_1 = [0.1, 0.1, 0.2, 1.0]  # Azul escuro
    GRADIENT_2 = [0.2, 0.1, 0.3, 1.0]  # Roxo escuro
    GRADIENT_3 = [0.1, 0.2, 0.3, 1.0]  # Azul acinzentado

# Configurações de animação
class AnimationConfig:
    # Durações
    FAST = 0.2
    NORMAL = 0.3
    SLOW = 0.5
    VERY_SLOW = 1.0
    
    # Tipos de transição
    EASE_OUT = 'out_cubic'
    EASE_IN = 'in_cubic'
    EASE_IN_OUT = 'in_out_cubic'
    BOUNCE = 'out_bounce'
    ELASTIC = 'out_elastic'

# Configurações de elevação e sombras
class ElevationConfig:
    # Níveis de elevação
    NONE = 0
    LOW = 2
    MEDIUM = 4
    HIGH = 8
    VERY_HIGH = 12
    
    # Cores de sombra
    SHADOW_LIGHT = [0, 0, 0, 0.1]
    SHADOW_MEDIUM = [0, 0, 0, 0.2]
    SHADOW_DARK = [0, 0, 0, 0.3]

# Configurações de tipografia
class TypographyConfig:
    # Tamanhos de fonte
    TINY = '10sp'
    SMALL = '12sp'
    BODY = '14sp'
    MEDIUM = '16sp'
    LARGE = '20sp'
    XLARGE = '24sp'
    HUGE = '32sp'
    MASSIVE = '48sp'
    ENORMOUS = '64sp'
    GIGANTIC = '96sp'
    
    # Pesos de fonte
    LIGHT = 'Light'
    REGULAR = 'Regular'
    MEDIUM_WEIGHT = 'Medium'
    BOLD = 'Bold'
    BLACK = 'Black'

# Configurações de espaçamento
class SpacingConfig:
    # Espaçamentos em dp
    TINY = '4dp'
    SMALL = '8dp'
    MEDIUM = '12dp'
    LARGE = '16dp'
    XLARGE = '20dp'
    HUGE = '24dp'
    MASSIVE = '32dp'
    
    # Raios de borda
    RADIUS_SMALL = 4
    RADIUS_MEDIUM = 8
    RADIUS_LARGE = 12
    RADIUS_XLARGE = 16
    RADIUS_ROUND = 50

# Efeitos especiais
class EffectConfig:
    # Configurações de blur (simulado)
    BLUR_LIGHT = 2
    BLUR_MEDIUM = 4
    BLUR_HEAVY = 8
    
    # Configurações de glow
    GLOW_INTENSITY_LOW = 0.3
    GLOW_INTENSITY_MEDIUM = 0.5
    GLOW_INTENSITY_HIGH = 0.8
    
    # Configurações de pulso
    PULSE_SPEED_SLOW = 2.0
    PULSE_SPEED_NORMAL = 1.0
    PULSE_SPEED_FAST = 0.5

# Tema completo
class ModernTheme:
    def __init__(self):
        self.colors = ModernColors()
        self.animation = AnimationConfig()
        self.elevation = ElevationConfig()
        self.typography = TypographyConfig()
        self.spacing = SpacingConfig()
        self.effects = EffectConfig()
    
    def get_card_style(self, elevation_level=ElevationConfig.MEDIUM):
        """Retorna estilo para cards"""
        return {
            'md_bg_color': self.colors.BACKGROUND_CARD,
            'elevation': elevation_level,
            'radius': [self.spacing.RADIUS_LARGE],
            'shadow_color': self.elevation.SHADOW_MEDIUM
        }
    
    def get_button_style(self, button_type='primary'):
        """Retorna estilo para botões"""
        styles = {
            'primary': {
                'md_bg_color': self.colors.PRIMARY,
                'elevation': self.elevation.MEDIUM,
                'radius': [self.spacing.RADIUS_MEDIUM]
            },
            'success': {
                'md_bg_color': self.colors.SUCCESS,
                'elevation': self.elevation.MEDIUM,
                'radius': [self.spacing.RADIUS_MEDIUM]
            },
            'danger': {
                'md_bg_color': self.colors.DANGER,
                'elevation': self.elevation.MEDIUM,
                'radius': [self.spacing.RADIUS_MEDIUM]
            },
            'warning': {
                'md_bg_color': self.colors.WARNING,
                'elevation': self.elevation.MEDIUM,
                'radius': [self.spacing.RADIUS_MEDIUM]
            }
        }
        return styles.get(button_type, styles['primary'])
    
    def get_text_style(self, text_type='primary'):
        """Retorna estilo para textos"""
        styles = {
            'primary': {
                'theme_text_color': 'Custom',
                'text_color': self.colors.TEXT_PRIMARY,
                'font_size': self.typography.BODY
            },
            'secondary': {
                'theme_text_color': 'Custom',
                'text_color': self.colors.TEXT_SECONDARY,
                'font_size': self.typography.SMALL
            },
            'muted': {
                'theme_text_color': 'Custom',
                'text_color': self.colors.TEXT_MUTED,
                'font_size': self.typography.SMALL
            },
            'large': {
                'theme_text_color': 'Custom',
                'text_color': self.colors.TEXT_PRIMARY,
                'font_size': self.typography.LARGE,
                'bold': True
            },
            'huge': {
                'theme_text_color': 'Custom',
                'text_color': self.colors.TEXT_PRIMARY,
                'font_size': self.typography.HUGE,
                'bold': True
            }
        }
        return styles.get(text_type, styles['primary'])

# Instância global do tema
theme = ModernTheme()
