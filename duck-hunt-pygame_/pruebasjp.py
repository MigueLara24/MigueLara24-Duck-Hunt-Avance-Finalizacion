import pygame
import random
import math

# Inicializar Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Configuracion de pantalla
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Duck Hunt - Ultimate Edition")

# Colores mejorados
SKY_BLUE = (135, 206, 250)
SKY_DARK = (70, 130, 180)
SKY_SUNSET = (255, 150, 100)
SKY_NIGHT = (15, 20, 50)
SKY_HELL = (80, 20, 10)
GRASS_GREEN = (34, 139, 34)
GRASS_LIGHT = (50, 205, 50)
GRASS_DARK = (0, 100, 0)
BUSH_GREEN = (0, 128, 0)
BUSH_DARK = (0, 80, 0)
TREE_BROWN = (139, 69, 19)
TREE_GREEN = (34, 139, 34)
TREE_DARK = (20, 100, 20)
CLOUD_WHITE = (255, 255, 255)
CLOUD_GRAY = (220, 220, 220)
SUN_YELLOW = (255, 223, 0)
SUN_ORANGE = (255, 165, 0)
MOON_WHITE = (240, 240, 220)
MOUNTAIN_FAR = (120, 150, 120)
MOUNTAIN_NEAR = (80, 120, 80)
DUCK_YELLOW = (255, 215, 0)
DUCK_ORANGE = (255, 140, 0)
DUCK_BROWN = (139, 90, 43)
DUCK_WHITE = (255, 255, 255)
DOG_BROWN = (160, 82, 45)
DOG_LIGHT = (210, 180, 140)
DOG_DARK = (101, 67, 33)
DOG_NOSE = (50, 30, 20)
DOG_GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
GOLD = (255, 215, 0)
WATER_BLUE = (64, 164, 223)
WATER_LIGHT = (100, 180, 230)
PURPLE = (150, 100, 200)
HELL_RED = (150, 30, 20)
LAVA_ORANGE = (255, 100, 20)

# Reloj para FPS
clock = pygame.time.Clock()
FPS = 60

# Fuentes
font_title = pygame.font.Font(None, 80)
font_large = pygame.font.Font(None, 52)
font_medium = pygame.font.Font(None, 38)
font_small = pygame.font.Font(None, 26)
font_tiny = pygame.font.Font(None, 20)

# Dimensiones de elementos
DUCK_WIDTH = 55
DUCK_HEIGHT = 45
DOG_WIDTH = 85
DOG_HEIGHT = 75
HUD_HEIGHT = 60
GRASS_HEIGHT = 160

MIN_SPAWN_X = 20
MAX_SPAWN_X = SCREEN_WIDTH - DUCK_WIDTH - 20
MIN_SPAWN_Y = HUD_HEIGHT + 30
MAX_SPAWN_Y = SCREEN_HEIGHT - GRASS_HEIGHT - DUCK_HEIGHT - 30

CURSOR_SPEED = 10

# Puntos minimos requeridos por nivel en modo secreto
SECRET_MODE_REQUIREMENTS = {
    1: 300,
    2: 600,
    3: 1000,
    4: 1500,
    5: 2200,
}

# Bosses del modo secreto
SECRET_BOSSES = [
    {"name": "SOMBRA ALADA", "description": "El guardian de la cueva", "color": (60, 60, 80)},
    {"name": "FENIX OSCURO", "description": "Renace de las cenizas", "color": (200, 50, 30)},
    {"name": "ESPECTRO DEL VACIO", "description": "Maestro de las sombras", "color": (100, 50, 150)},
    {"name": "DEMONIO CARMESI", "description": "Senor del infierno", "color": (180, 20, 20)},
    {"name": "TITAN INFERNAL", "description": "El jefe final", "color": (255, 80, 0)},
]


# ============ SISTEMA DE SONIDO COMPLETO ============
class SoundSystem:
    """Sistema de sonido completo con efectos y ambiente"""
    def __init__(self):
        self.sounds = {}
        self.current_ambient = None
        self.volume = 0.4
        self.generate_all_sounds()
    
    def generate_all_sounds(self):
        """Genera todos los sonidos del juego"""
        try:
            sample_rate = 22050
            
            # ===== SONIDO MENU - Suave y relajante =====
            duration = 4.0
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                val = int(2000 * math.sin(2 * math.pi * 220 * t) * (0.3 + 0.2 * math.sin(2 * math.pi * 0.5 * t)))
                val += int(1500 * math.sin(2 * math.pi * 330 * t) * (0.2 + 0.1 * math.sin(2 * math.pi * 0.3 * t)))
                val += int(1000 * math.sin(2 * math.pi * 440 * t) * 0.1)
                fade = min(1.0, i / (sample_rate * 0.5), (samples - i) / (sample_rate * 0.5))
                arr.append(max(-32767, min(32767, int(val * fade * 0.12))))
            self.sounds['menu'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO TENSION - Graves pulsantes =====
            duration = 3.0
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                val = int(3500 * math.sin(2 * math.pi * 55 * t))
                val += int(2500 * math.sin(2 * math.pi * 110 * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 1.5 * t)))
                val += int(1500 * math.sin(2 * math.pi * 165 * t) * 0.3)
                val += random.randint(-300, 300)
                fade = min(1.0, i / (sample_rate * 0.2), (samples - i) / (sample_rate * 0.2))
                arr.append(max(-32767, min(32767, int(val * fade * 0.1))))
            self.sounds['tension'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO DISPARO =====
            duration = 0.15
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                decay = math.exp(-t * 30)
                noise = random.randint(-8000, 8000) * decay
                bang = int(12000 * math.sin(2 * math.pi * 150 * t) * decay)
                arr.append(max(-32767, min(32767, int((noise + bang) * 0.5))))
            self.sounds['shoot'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO HIT/IMPACTO =====
            duration = 0.1
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                decay = math.exp(-t * 40)
                val = int(10000 * math.sin(2 * math.pi * 400 * t) * decay)
                val += int(5000 * math.sin(2 * math.pi * 800 * t) * decay * 0.5)
                arr.append(max(-32767, min(32767, val)))
            self.sounds['hit'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO RAYO/THUNDER =====
            duration = 0.8
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                if t < 0.1:
                    val = random.randint(-15000, 15000) * (1 - t * 10)
                else:
                    decay = math.exp(-(t - 0.1) * 5)
                    val = int(8000 * math.sin(2 * math.pi * 80 * t) * decay)
                    val += random.randint(-2000, 2000) * decay
                arr.append(max(-32767, min(32767, int(val * 0.6))))
            self.sounds['thunder'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO INTRO/WHOOSH =====
            duration = 0.5
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                freq = 200 + t * 600
                envelope = math.sin(math.pi * t / duration)
                val = int(6000 * math.sin(2 * math.pi * freq * t) * envelope)
                val += random.randint(-1000, 1000) * envelope
                arr.append(max(-32767, min(32767, val)))
            self.sounds['whoosh'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO PERRO LADRAR =====
            duration = 0.25
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                freq = 300 + 200 * math.sin(t * 25)
                decay = math.exp(-t * 8)
                val = int(8000 * math.sin(2 * math.pi * freq * t) * decay)
                arr.append(max(-32767, min(32767, val)))
            self.sounds['bark'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO TEXTO/UI =====
            duration = 0.05
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                val = int(4000 * math.sin(2 * math.pi * 800 * t) * (1 - t / duration))
                arr.append(max(-32767, min(32767, val)))
            self.sounds['text'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO VICTORIA =====
            duration = 0.8
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                val = int(5000 * math.sin(2 * math.pi * 523 * t))
                val += int(4000 * math.sin(2 * math.pi * 659 * t))
                val += int(3000 * math.sin(2 * math.pi * 784 * t))
                fade = min(1.0, (duration - t) / 0.3)
                arr.append(max(-32767, min(32767, int(val * fade * 0.4))))
            self.sounds['victory'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO DESBLOQUEO =====
            duration = 1.2
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                freq = 300 + t * 400
                val = int(6000 * math.sin(2 * math.pi * freq * t))
                val += int(4000 * math.sin(2 * math.pi * freq * 1.5 * t))
                fade = min(1.0, t / 0.1, (duration - t) / 0.2)
                arr.append(max(-32767, min(32767, int(val * fade * 0.35))))
            self.sounds['unlock'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # ===== SONIDO HISTORIA TRISTE =====
            duration = 3.0
            samples = int(sample_rate * duration)
            arr = []
            for i in range(samples):
                t = i / sample_rate
                val = int(2000 * math.sin(2 * math.pi * 220 * t) * (0.4 + 0.3 * math.sin(2 * math.pi * 0.3 * t)))
                val += int(1500 * math.sin(2 * math.pi * 165 * t) * 0.3)
                fade = min(1.0, t / 0.5, (duration - t) / 0.5)
                arr.append(max(-32767, min(32767, int(val * fade * 0.15))))
            self.sounds['sad'] = pygame.mixer.Sound(buffer=bytes(b''.join(v.to_bytes(2, 'little', signed=True) for v in arr)))
            
            # Ajustar volumenes
            self.sounds['menu'].set_volume(self.volume * 0.3)
            self.sounds['tension'].set_volume(self.volume * 0.4)
            self.sounds['shoot'].set_volume(self.volume * 0.6)
            self.sounds['hit'].set_volume(self.volume * 0.5)
            self.sounds['thunder'].set_volume(self.volume * 0.7)
            self.sounds['whoosh'].set_volume(self.volume * 0.4)
            self.sounds['bark'].set_volume(self.volume * 0.5)
            self.sounds['text'].set_volume(self.volume * 0.2)
            self.sounds['victory'].set_volume(self.volume * 0.5)
            self.sounds['unlock'].set_volume(self.volume * 0.6)
            self.sounds['sad'].set_volume(self.volume * 0.35)
            
        except Exception as e:
            print(f"Error generando sonidos: {e}")
    
    def play(self, sound_name):
        """Reproduce un efecto de sonido"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_ambient(self, ambient_type):
        """Reproduce sonido ambiente en loop"""
        self.stop_ambient()
        if ambient_type in self.sounds:
            self.sounds[ambient_type].play(loops=-1)
            self.current_ambient = ambient_type
    
    def stop_ambient(self):
        """Detiene sonido ambiente"""
        if self.current_ambient and self.current_ambient in self.sounds:
            self.sounds[self.current_ambient].stop()
        self.current_ambient = None
    
    def stop_all(self):
        """Detiene todos los sonidos"""
        for sound in self.sounds.values():
            sound.stop()
        self.current_ambient = None


# Alias para compatibilidad
class AmbientSound:
    """Wrapper para compatibilidad con codigo existente"""
    def __init__(self):
        self.sound_system = SoundSystem()
    
    def play_menu(self):
        self.sound_system.play_ambient('menu')
    
    def play_tension(self):
        self.sound_system.play_ambient('tension')
    
    def stop(self):
        self.sound_system.stop_ambient()
    
    def play(self, name):
        self.sound_system.play(name)


# ============ SISTEMA QTE ============
class QTESystem:
    """Sistema de Quick Time Events para modo secreto"""
    def __init__(self):
        self.active = False
        self.keys_sequence = []
        self.current_index = 0
        self.time_limit = 0
        self.timer = 0
        self.success = False
        self.failed = False
        self.penalty_points = 0
        self.display_timer = 0
    
    def start_qte(self, difficulty=1):
        """Inicia un nuevo QTE"""
        self.active = True
        num_keys = min(3 + difficulty, 6)
        self.keys_sequence = [random.choice(['W', 'A', 'S', 'D']) for _ in range(num_keys)]
        self.current_index = 0
        self.time_limit = max(60, 180 - difficulty * 20)  # Frames (60fps)
        self.timer = self.time_limit
        self.success = False
        self.failed = False
        self.penalty_points = 100 + difficulty * 50
        self.display_timer = 0
    
    def update(self):
        """Actualiza el estado del QTE"""
        if not self.active:
            return None
        
        self.timer -= 1
        self.display_timer += 1
        
        if self.timer <= 0 and not self.success:
            self.failed = True
            self.active = False
            return -self.penalty_points
        
        if self.success:
            self.active = False
            return self.penalty_points // 2  # Bonus por completar
        
        return None
    
    def check_key(self, key):
        """Verifica si la tecla presionada es correcta"""
        if not self.active or self.success or self.failed:
            return
        
        key_map = {pygame.K_w: 'W', pygame.K_a: 'A', pygame.K_s: 'S', pygame.K_d: 'D'}
        if key not in key_map:
            return
        
        pressed = key_map[key]
        expected = self.keys_sequence[self.current_index]
        
        if pressed == expected:
            self.current_index += 1
            if self.current_index >= len(self.keys_sequence):
                self.success = True
        else:
            # Tecla incorrecta - falla inmediata
            self.failed = True
            self.active = False
    
    def draw(self, surface):
        """Dibuja el QTE en pantalla"""
        if not self.active and self.display_timer < 60:
            return
        
        # Panel de fondo
        panel_w = 400
        panel_h = 120
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = 150
        
        # Fondo con transparencia
        overlay = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        if self.failed:
            overlay.fill((150, 30, 30, 220))
        elif self.success:
            overlay.fill((30, 150, 30, 220))
        else:
            overlay.fill((30, 30, 50, 220))
        surface.blit(overlay, (panel_x, panel_y))
        
        # Borde
        border_color = RED if self.timer < 60 else GOLD
        pygame.draw.rect(surface, border_color, (panel_x, panel_y, panel_w, panel_h), 3, border_radius=10)
        
        # Titulo
        title = font_medium.render("REACCIONA RAPIDO!", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, panel_y + 10))
        
        # Secuencia de teclas
        key_x = SCREEN_WIDTH // 2 - (len(self.keys_sequence) * 45) // 2
        for i, key in enumerate(self.keys_sequence):
            x = key_x + i * 45
            y = panel_y + 50
            
            if i < self.current_index:
                # Completada
                pygame.draw.rect(surface, GREEN, (x, y, 40, 40), border_radius=5)
            elif i == self.current_index and self.active:
                # Actual - pulsante
                pulse = int(math.sin(self.display_timer * 0.3) * 5)
                pygame.draw.rect(surface, GOLD, (x - pulse, y - pulse, 40 + pulse * 2, 40 + pulse * 2), border_radius=5)
            else:
                # Pendiente
                pygame.draw.rect(surface, (80, 80, 100), (x, y, 40, 40), border_radius=5)
            
            key_text = font_medium.render(key, True, WHITE if i >= self.current_index else BLACK)
            surface.blit(key_text, (x + 20 - key_text.get_width() // 2, y + 8))
        
        # Barra de tiempo
        if self.active:
            bar_width = int((panel_w - 40) * (self.timer / self.time_limit))
            bar_color = GREEN if self.timer > self.time_limit * 0.3 else RED
            pygame.draw.rect(surface, (50, 50, 50), (panel_x + 20, panel_y + 100, panel_w - 40, 10))
            pygame.draw.rect(surface, bar_color, (panel_x + 20, panel_y + 100, bar_width, 10))


class Particle:
    """Sistema de particulas para efectos visuales"""
    def __init__(self, x, y, particle_type='feather'):
        self.x = x
        self.y = y
        self.type = particle_type
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.life = random.randint(40, 80)
        self.max_life = self.life
        self.size = random.randint(3, 8)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-10, 10)
        
        if particle_type == 'feather':
            self.color = random.choice([DUCK_YELLOW, DUCK_ORANGE, WHITE, (200, 200, 200)])
        elif particle_type == 'spark':
            self.color = random.choice([GOLD, (255, 200, 100), (255, 255, 200)])
        elif particle_type == 'blood':
            self.color = (200, 50, 50)
        elif particle_type == 'star':
            self.color = random.choice([GOLD, WHITE, (255, 200, 100)])
            self.vy = random.uniform(-2, 2)
        elif particle_type == 'lightning':
            self.color = (200, 200, 255)
            self.life = random.randint(5, 15)
            self.max_life = self.life
        elif particle_type == 'ember':
            self.color = random.choice([LAVA_ORANGE, RED, (255, 200, 50)])
            self.vy = random.uniform(-4, -1)
            self.life = random.randint(60, 120)
            self.max_life = self.life
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.type not in ['star', 'ember']:
            self.vy += 0.15
        elif self.type == 'ember':
            self.vy -= 0.02  # Sube
            self.vx += random.uniform(-0.1, 0.1)
        self.rotation += self.rot_speed
        self.life -= 1
        return self.life > 0
    
    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        if self.type == 'feather':
            size = self.size * (self.life / self.max_life)
            pygame.draw.ellipse(surface, self.color, 
                              (int(self.x - size), int(self.y - size/2), int(size*2), int(size)))
        elif self.type == 'spark':
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, int(self.size * self.life / self.max_life)))
        elif self.type == 'star':
            size = self.size * (self.life / self.max_life)
            points = []
            for i in range(5):
                angle = math.radians(self.rotation + i * 72)
                points.append((self.x + size * math.cos(angle), self.y + size * math.sin(angle)))
            if len(points) >= 3:
                pygame.draw.polygon(surface, self.color, points)
        elif self.type == 'lightning':
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(2, self.size))
        elif self.type == 'ember':
            size = max(1, int(self.size * (self.life / self.max_life)))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)


class FloatingText:
    """Texto flotante para puntuaciones y mensajes"""
    def __init__(self, x, y, text, color=GOLD, size='medium'):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 60
        self.max_life = 60
        self.font = font_medium if size == 'medium' else font_small
    
    def update(self):
        self.y -= 1.5
        self.life -= 1
        return self.life > 0
    
    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        surface.blit(text_surf, (self.x - text_surf.get_width() // 2, self.y))


class PowerUp:
    """Clase para los power-ups y bonus"""
    def __init__(self):
        self.x = random.randint(120, SCREEN_WIDTH - 120)
        self.y = random.randint(HUD_HEIGHT + 60, SCREEN_HEIGHT - GRASS_HEIGHT - 60)
        self.type = random.choice(['rapid_fire', 'slow_motion', 'extra_ammo', 'double_points', 'shield', 'magnet'])
        self.timer = 360
        self.collected = False
        self.pulse = 0
        self.float_offset = random.uniform(0, math.pi * 2)
    
    def update(self):
        self.timer -= 1
        self.pulse += 0.12
        return self.timer > 0 and not self.collected
    
    def draw(self, surface):
        if self.collected:
            return
        
        float_y = self.y + math.sin(self.pulse + self.float_offset) * 5
        pulse_size = int(math.sin(self.pulse) * 4)
        size = 20 + pulse_size
        
        # Glow effect
        for i in range(3):
            glow_size = size + 15 - i * 5
            glow_alpha = 50 - i * 15
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            
            if self.type == 'rapid_fire':
                pygame.draw.circle(glow_surf, (255, 200, 0, glow_alpha), (glow_size, glow_size), glow_size)
            elif self.type == 'slow_motion':
                pygame.draw.circle(glow_surf, (100, 150, 255, glow_alpha), (glow_size, glow_size), glow_size)
            elif self.type == 'extra_ammo':
                pygame.draw.circle(glow_surf, (255, 150, 50, glow_alpha), (glow_size, glow_size), glow_size)
            elif self.type == 'double_points':
                pygame.draw.circle(glow_surf, (255, 100, 100, glow_alpha), (glow_size, glow_size), glow_size)
            elif self.type == 'shield':
                pygame.draw.circle(glow_surf, (100, 200, 255, glow_alpha), (glow_size, glow_size), glow_size)
            elif self.type == 'magnet':
                pygame.draw.circle(glow_surf, (200, 100, 255, glow_alpha), (glow_size, glow_size), glow_size)
            
            surface.blit(glow_surf, (self.x - glow_size, float_y - glow_size))
        
        # Icon
        if self.type == 'rapid_fire':
            pygame.draw.polygon(surface, GOLD, [
                (self.x - 6, float_y - 18), (self.x + 6, float_y - 6),
                (self.x - 3, float_y - 6), (self.x + 6, float_y + 18),
                (self.x - 6, float_y + 6), (self.x + 3, float_y + 6)
            ])
        elif self.type == 'slow_motion':
            pygame.draw.circle(surface, (50, 100, 200), (self.x, int(float_y)), size - 2)
            pygame.draw.circle(surface, WHITE, (self.x, int(float_y)), size - 5)
            pygame.draw.line(surface, BLACK, (self.x, int(float_y)), (self.x, int(float_y) - 12), 3)
            pygame.draw.line(surface, BLACK, (self.x, int(float_y)), (self.x + 8, int(float_y)), 2)
        elif self.type == 'extra_ammo':
            pygame.draw.rect(surface, (200, 150, 50), (self.x - 12, int(float_y) - 10, 24, 20), border_radius=3)
            pygame.draw.rect(surface, (180, 130, 40), (self.x - 9, int(float_y) - 6, 8, 14))
            pygame.draw.rect(surface, (180, 130, 40), (self.x + 1, int(float_y) - 6, 8, 14))
        elif self.type == 'double_points':
            points = []
            for i in range(10):
                angle = math.radians(i * 36 - 90)
                r = size if i % 2 == 0 else size // 2
                points.append((self.x + r * math.cos(angle), float_y + r * math.sin(angle)))
            pygame.draw.polygon(surface, GOLD, points)
            text = font_small.render("x2", True, BLACK)
            surface.blit(text, (self.x - text.get_width() // 2, float_y - text.get_height() // 2))
        elif self.type == 'shield':
            pygame.draw.polygon(surface, (100, 180, 255), [
                (self.x, float_y - 15), (self.x + 14, float_y - 5),
                (self.x + 10, float_y + 15), (self.x, float_y + 18),
                (self.x - 10, float_y + 15), (self.x - 14, float_y - 5)
            ])
            pygame.draw.polygon(surface, WHITE, [
                (self.x, float_y - 10), (self.x + 8, float_y - 3),
                (self.x + 5, float_y + 8), (self.x, float_y + 10),
                (self.x - 5, float_y + 8), (self.x - 8, float_y - 3)
            ])
        elif self.type == 'magnet':
            pygame.draw.arc(surface, RED, (self.x - 12, float_y - 12, 24, 24), 0, math.pi, 5)
            pygame.draw.rect(surface, RED, (self.x - 12, int(float_y), 8, 12))
            pygame.draw.rect(surface, (50, 50, 200), (self.x + 4, int(float_y), 8, 12))
    
    def check_collect(self, cx, cy, magnet_active=False):
        collect_radius = 80 if magnet_active else 35
        dist = math.sqrt((self.x - cx) ** 2 + (self.y - cy) ** 2)
        if dist < collect_radius:
            self.collected = True
            return self.type
        return None


class Cloud:
    """Clase para las nubes del fondo"""
    def __init__(self, start_random=True):
        if start_random:
            self.x = random.randint(-50, SCREEN_WIDTH + 50)
        else:
            self.x = random.randint(-250, -50)
        self.y = random.randint(HUD_HEIGHT + 10, 200)
        self.speed = random.uniform(0.2, 0.6)
        self.size = random.uniform(0.6, 1.4)
        self.layer = random.randint(0, 2)
    
    def update(self, slow_motion=False):
        speed_mult = 0.3 if slow_motion else 1.0
        self.x += self.speed * speed_mult
        if self.x > SCREEN_WIDTH + 180:
            self.x = random.randint(-250, -100)
            self.y = random.randint(HUD_HEIGHT + 10, 200)
            self.size = random.uniform(0.6, 1.4)
    
    def draw(self, surface, time_of_day='day'):
        if time_of_day == 'night':
            main_color = (60, 60, 80)
            shadow_color = (40, 40, 60)
        elif time_of_day == 'sunset':
            main_color = (255, 200, 180)
            shadow_color = (200, 150, 130)
        elif time_of_day == 'hell':
            main_color = (80, 40, 40)
            shadow_color = (50, 25, 25)
        else:
            main_color = CLOUD_WHITE
            shadow_color = CLOUD_GRAY
        
        base_size = int(35 * self.size)
        
        # Shadow
        pygame.draw.ellipse(surface, shadow_color, 
                          (self.x + 4, self.y + 4, base_size * 2.2, base_size * 0.9))
        pygame.draw.ellipse(surface, shadow_color, 
                          (self.x + base_size * 0.5 + 4, self.y - base_size * 0.35 + 4, base_size * 1.6, base_size * 1.1))
        
        # Main cloud
        pygame.draw.ellipse(surface, main_color, 
                          (self.x, self.y, base_size * 2.2, base_size * 0.9))
        pygame.draw.ellipse(surface, main_color, 
                          (self.x + base_size * 0.5, self.y - base_size * 0.35, base_size * 1.6, base_size * 1.1))
        pygame.draw.ellipse(surface, main_color, 
                          (self.x + base_size * 1.1, self.y + base_size * 0.05, base_size * 1.4, base_size * 0.85))


class Star:
    """Clase para estrellas en modo noche"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(HUD_HEIGHT, SCREEN_HEIGHT - GRASS_HEIGHT - 80)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.03, 0.1)
        self.phase = random.uniform(0, math.pi * 2)
        self.size = random.choice([1, 1, 1, 2, 2, 3])
    
    def update(self):
        self.phase += self.twinkle_speed
    
    def draw(self, surface):
        brightness = int(120 + 135 * math.sin(self.phase) * self.brightness)
        color = (brightness, brightness, min(255, brightness + 30))
        pygame.draw.circle(surface, color, (self.x, self.y), self.size)
        if self.size > 1 and brightness > 200:
            pygame.draw.line(surface, (brightness, brightness, brightness), 
                           (self.x - self.size - 1, self.y), (self.x + self.size + 1, self.y), 1)
            pygame.draw.line(surface, (brightness, brightness, brightness), 
                           (self.x, self.y - self.size - 1), (self.x, self.y + self.size + 1), 1)


class Duck:
    """Clase para los patos con mejoras graficas"""
    def __init__(self, difficulty=1.0, is_boss=False):
        self.x = random.randint(MIN_SPAWN_X, MAX_SPAWN_X)
        self.y = random.randint(MIN_SPAWN_Y, MAX_SPAWN_Y)
        
        self.x = max(MIN_SPAWN_X, min(self.x, MAX_SPAWN_X))
        self.y = max(MIN_SPAWN_Y, min(self.y, MAX_SPAWN_Y))
        
        self.is_boss = is_boss
        base_speed = 2.0 + difficulty * 0.6
        if is_boss:
            base_speed *= 0.7  # Bosses mas lentos pero mas vida
            self.health = 3
        else:
            self.health = 1
        
        self.speed_x = random.choice([-1, 1]) * random.uniform(base_speed, base_speed + 2.5)
        self.speed_y = random.choice([-1, 1]) * random.uniform(base_speed - 0.5, base_speed + 1.5)
        self.base_speed_x = self.speed_x
        self.base_speed_y = self.speed_y
        self.alive = True
        self.falling = False
        self.fall_speed = 0
        self.wing_angle = 0
        self.wing_direction = 1
        self.color_variant = random.choice(['yellow', 'brown', 'white', 'green', 'blue'])
        if is_boss:
            self.color_variant = 'boss'
        self.escape_timer = 0
        self.escaping = False
        self.points = int(100 * difficulty) if not is_boss else int(500 * difficulty)
        self.rotation = 0
        self.scale = 1.0 if not is_boss else 1.5
        self.hit_flash = 0
    
    def update(self, slow_motion=False):
        speed_mult = 0.25 if slow_motion else 1.0
        
        if self.hit_flash > 0:
            self.hit_flash -= 1
        
        if self.falling:
            self.fall_speed += 0.6
            self.y += self.fall_speed
            self.rotation += 8
            self.x += self.speed_x * 0.3
            if self.y > SCREEN_HEIGHT - GRASS_HEIGHT + 20:
                return False
            return True
        
        if self.alive:
            self.escape_timer += 1
            if self.escape_timer > 550:
                self.escaping = True
            
            if self.escaping:
                self.speed_y = -6 * speed_mult
                self.y += self.speed_y
                if self.y < -DUCK_HEIGHT - 20:
                    return False
            else:
                self.x += self.speed_x * speed_mult
                self.y += self.speed_y * speed_mult
                
                if self.x <= 0:
                    self.x = 0
                    self.speed_x = abs(self.speed_x)
                elif self.x >= SCREEN_WIDTH - DUCK_WIDTH:
                    self.x = SCREEN_WIDTH - DUCK_WIDTH
                    self.speed_x = -abs(self.speed_x)
                
                if self.y <= HUD_HEIGHT:
                    self.y = HUD_HEIGHT
                    self.speed_y = abs(self.speed_y)
                elif self.y >= SCREEN_HEIGHT - GRASS_HEIGHT - DUCK_HEIGHT:
                    self.y = SCREEN_HEIGHT - GRASS_HEIGHT - DUCK_HEIGHT
                    self.speed_y = -abs(self.speed_y)
            
            self.wing_angle += 0.5 * self.wing_direction * speed_mult
            if self.wing_angle > 1.3 or self.wing_angle < -1.3:
                self.wing_direction *= -1
        
        return True
    
    def draw(self, surface):
        colors = {
            'yellow': (DUCK_YELLOW, DUCK_ORANGE, (0, 150, 0)),
            'brown': (DUCK_BROWN, (100, 60, 30), (60, 100, 60)),
            'white': (DUCK_WHITE, (200, 200, 200), (180, 180, 180)),
            'green': ((50, 180, 50), (30, 140, 30), (40, 120, 40)),
            'blue': ((100, 150, 220), (70, 120, 180), (60, 100, 160)),
            'boss': ((180, 50, 50), (120, 30, 30), (100, 20, 20))
        }
        
        body_color, wing_color, head_color = colors.get(self.color_variant, colors['yellow'])
        
        if self.hit_flash > 0:
            body_color = WHITE
            wing_color = WHITE
            head_color = WHITE
        
        x, y = int(self.x), int(self.y)
        facing_right = self.speed_x >= 0
        scale = self.scale
        
        if self.falling:
            # Draw falling duck with rotation
            pygame.draw.ellipse(surface, body_color, (x + int(8*scale), y + int(8*scale), int(38*scale), int(28*scale)))
            pygame.draw.circle(surface, head_color, (x + int(28*scale), y + int(35*scale)), int(12*scale))
            pygame.draw.line(surface, BLACK, (x + int(24*scale), y + int(31*scale)), (x + int(30*scale), y + int(37*scale)), 3)
            pygame.draw.line(surface, BLACK, (x + int(30*scale), y + int(31*scale)), (x + int(24*scale), y + int(37*scale)), 3)
            pygame.draw.ellipse(surface, wing_color, (x - int(5*scale), y + int(10*scale), int(20*scale), int(12*scale)))
            pygame.draw.ellipse(surface, wing_color, (x + int(35*scale), y + int(10*scale), int(20*scale), int(12*scale)))
        else:
            if facing_right:
                pygame.draw.ellipse(surface, body_color, (x + int(3*scale), y + int(18*scale), int(42*scale), int(26*scale)))
                pygame.draw.circle(surface, head_color, (x + int(42*scale), y + int(14*scale)), int(14*scale))
                pygame.draw.circle(surface, WHITE, (x + int(47*scale), y + int(11*scale)), int(5*scale))
                pygame.draw.circle(surface, BLACK, (x + int(48*scale), y + int(11*scale)), int(3*scale))
                pygame.draw.circle(surface, WHITE, (x + int(49*scale), y + int(10*scale)), 1)
                pygame.draw.polygon(surface, DUCK_ORANGE, [(x + int(53*scale), y + int(16*scale)), (x + int(66*scale), y + int(18*scale)), (x + int(53*scale), y + int(21*scale))])
                wing_y_offset = int(self.wing_angle * 7 * scale)
                pygame.draw.ellipse(surface, wing_color, (x + int(10*scale), y + int(20*scale) + wing_y_offset, int(26*scale), int(14*scale)))
                pygame.draw.polygon(surface, wing_color, [(x - int(3*scale), y + int(22*scale)), (x + int(8*scale), y + int(28*scale)), (x - int(3*scale), y + int(35*scale))])
            else:
                pygame.draw.ellipse(surface, body_color, (x + int(10*scale), y + int(18*scale), int(42*scale), int(26*scale)))
                pygame.draw.circle(surface, head_color, (x + int(13*scale), y + int(14*scale)), int(14*scale))
                pygame.draw.circle(surface, WHITE, (x + int(8*scale), y + int(11*scale)), int(5*scale))
                pygame.draw.circle(surface, BLACK, (x + int(7*scale), y + int(11*scale)), int(3*scale))
                pygame.draw.circle(surface, WHITE, (x + int(6*scale), y + int(10*scale)), 1)
                pygame.draw.polygon(surface, DUCK_ORANGE, [(x + int(2*scale), y + int(16*scale)), (x - int(11*scale), y + int(18*scale)), (x + int(2*scale), y + int(21*scale))])
                wing_y_offset = int(self.wing_angle * 7 * scale)
                pygame.draw.ellipse(surface, wing_color, (x + int(19*scale), y + int(20*scale) + wing_y_offset, int(26*scale), int(14*scale)))
                pygame.draw.polygon(surface, wing_color, [(x + int(58*scale), y + int(22*scale)), (x + int(47*scale), y + int(28*scale)), (x + int(58*scale), y + int(35*scale))])
        
        # Health bar for bosses
        if self.is_boss and self.health > 0 and not self.falling:
            bar_width = int(50 * scale)
            bar_x = x + int(DUCK_WIDTH * scale // 2) - bar_width // 2
            pygame.draw.rect(surface, (50, 50, 50), (bar_x, y - 10, bar_width, 6))
            health_width = int(bar_width * (self.health / 3))
            pygame.draw.rect(surface, RED, (bar_x, y - 10, health_width, 6))
    
    def check_hit(self, mx, my):
        if self.alive and not self.falling:
            center_x = self.x + DUCK_WIDTH * self.scale // 2
            center_y = self.y + DUCK_HEIGHT * self.scale // 2
            dist = math.sqrt((center_x - mx) ** 2 + (center_y - my) ** 2)
            hit_radius = 35 * self.scale
            if dist < hit_radius:
                self.health -= 1
                self.hit_flash = 10
                if self.health <= 0:
                    self.alive = False
                    self.falling = True
                    return True
                return 'damaged'
        return False


class Dog:
    """Clase para el perro cazador mejorado"""
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - DOG_WIDTH // 2
        self.y = SCREEN_HEIGHT - GRASS_HEIGHT + 40
        self.state = 'hidden'
        self.animation_timer = 0
        self.target_y = self.y
        self.laugh_frame = 0
        self.held_duck_color = 'yellow'
        self.god_mode = False
        self.god_timer = 0
        self.kills = 0
        self.bounce = 0
        self.god_mode_used_this_round = False  # NERF: solo una vez por ronda
    
    def activate_god_mode(self):
        """Activa modo dios - MUY NERFEADO: 2 segundos, una vez por ronda, velocidad reducida"""
        if self.god_mode_used_this_round:
            return False  # Ya se uso esta ronda
        self.god_mode = True
        self.god_timer = 120  # 2 segundos (muy nerfeado)
        self.state = 'god_mode'
        self.animation_timer = 120
        self.target_y = SCREEN_HEIGHT - GRASS_HEIGHT - DOG_HEIGHT - 60
        self.god_mode_used_this_round = True
        return True
    
    def reset_round(self):
        """Resetea el estado para nueva ronda"""
        self.god_mode_used_this_round = False
    
    def show_laugh(self):
        if not self.god_mode:
            self.state = 'laughing'
            self.animation_timer = 180
            self.target_y = SCREEN_HEIGHT - GRASS_HEIGHT - DOG_HEIGHT + 15
    
    def show_celebrate(self, duck_x, duck_color):
        if not self.god_mode:
            self.x = duck_x - DOG_WIDTH // 2
            self.x = max(25, min(self.x, SCREEN_WIDTH - DOG_WIDTH - 25))
            self.state = 'celebrating'
            self.animation_timer = 140
            self.target_y = SCREEN_HEIGHT - GRASS_HEIGHT - DOG_HEIGHT + 15
            self.held_duck_color = duck_color
            self.kills += 1
    
    def update(self, ducks=None):
        self.bounce += 0.15
        
        if self.god_mode:
            self.god_timer -= 1
            if self.god_timer <= 0:
                self.god_mode = False
                self.state = 'hiding'
            else:
                if ducks:
                    for duck in ducks:
                        if duck.alive and not duck.falling:
                            # Velocidad REDUCIDA - ahora 3 en lugar de 7
                            if self.x < duck.x:
                                self.x += 3
                            elif self.x > duck.x:
                                self.x -= 3
                            if abs(self.x - duck.x) < 55:
                                duck.alive = False
                                duck.falling = True
                                self.kills += 1
                                return duck.points
                return 0
        
        if self.state == 'hidden':
            self.y = SCREEN_HEIGHT - GRASS_HEIGHT + 50
            return 0
        
        if self.state in ['laughing', 'celebrating']:
            if self.y > self.target_y:
                self.y -= 5
            
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.state = 'hiding'
        
        if self.state == 'hiding':
            self.y += 5
            if self.y >= SCREEN_HEIGHT - GRASS_HEIGHT + 50:
                self.state = 'hidden'
        
        if self.state == 'laughing':
            self.laugh_frame = (self.laugh_frame + 1) % 30
        
        return 0
    
    def draw(self, surface):
        if self.state == 'hidden':
            return
        
        x, y = int(self.x), int(self.y)
        
        main_color = DOG_GOLD if self.god_mode else DOG_BROWN
        light_color = (255, 240, 150) if self.god_mode else DOG_LIGHT
        dark_color = (200, 170, 50) if self.god_mode else DOG_DARK
        
        # God mode aura
        if self.god_mode:
            for i in range(4):
                alpha = 80 - i * 20
                size = 70 + i * 18
                aura_offset = int(math.sin(self.bounce * 2) * 3)
                glow_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 215, 0, alpha), (size, size), size)
                surface.blit(glow_surf, (x + DOG_WIDTH // 2 - size, y + DOG_HEIGHT // 2 - size + aura_offset))
        
        bounce_offset = int(math.sin(self.bounce) * 2) if self.state in ['celebrating', 'god_mode'] else 0
        y += bounce_offset
        
        # Body
        pygame.draw.ellipse(surface, main_color, (x + 12, y + 38, 60, 35))
        
        # Head
        pygame.draw.ellipse(surface, main_color, (x + 18, y + 8, 52, 42))
        
        # Ears
        pygame.draw.ellipse(surface, dark_color, (x + 8, y + 6, 22, 35))
        pygame.draw.ellipse(surface, dark_color, (x + 55, y + 6, 22, 35))
        pygame.draw.ellipse(surface, (180, 120, 80) if not self.god_mode else (255, 200, 100), (x + 12, y + 12, 14, 25))
        pygame.draw.ellipse(surface, (180, 120, 80) if not self.god_mode else (255, 200, 100), (x + 59, y + 12, 14, 25))
        
        # Snout
        pygame.draw.ellipse(surface, light_color, (x + 28, y + 30, 35, 24))
        
        # Nose
        pygame.draw.ellipse(surface, DOG_NOSE, (x + 40, y + 32, 15, 12))
        pygame.draw.ellipse(surface, (30, 20, 15), (x + 44, y + 35, 8, 6))
        
        if self.state == 'laughing':
            bounce = 4 if self.laugh_frame < 15 else 0
            pygame.draw.arc(surface, BLACK, (x + 26, y + 18 + bounce, 16, 12), 0, 3.14, 3)
            pygame.draw.arc(surface, BLACK, (x + 48, y + 18 + bounce, 16, 12), 0, 3.14, 3)
            pygame.draw.ellipse(surface, (60, 30, 20), (x + 38, y + 44, 20, 12))
            pygame.draw.ellipse(surface, (255, 120, 120), (x + 40, y + 48, 16, 6))
        elif self.god_mode:
            pygame.draw.circle(surface, WHITE, (x + 33, y + 22), 10)
            pygame.draw.circle(surface, WHITE, (x + 55, y + 22), 10)
            pygame.draw.circle(surface, (255, 100, 0), (x + 33, y + 22), 6)
            pygame.draw.circle(surface, (255, 100, 0), (x + 55, y + 22), 6)
            pygame.draw.circle(surface, (255, 200, 0), (x + 33, y + 22), 3)
            pygame.draw.circle(surface, (255, 200, 0), (x + 55, y + 22), 3)
            pygame.draw.polygon(surface, GOLD, [
                (x + 22, y + 2), (x + 28, y - 18), (x + 35, y - 6),
                (x + 43, y - 24), (x + 52, y - 6), (x + 58, y - 18), (x + 65, y + 2)
            ])
            pygame.draw.polygon(surface, (255, 240, 100), [
                (x + 26, y), (x + 30, y - 12), (x + 36, y - 4),
                (x + 43, y - 18), (x + 50, y - 4), (x + 56, y - 12), (x + 60, y)
            ])
            pygame.draw.circle(surface, RED, (x + 43, y - 15), 4)
            pygame.draw.circle(surface, (100, 150, 255), (x + 30, y - 8), 3)
            pygame.draw.circle(surface, (100, 255, 100), (x + 56, y - 8), 3)
        else:
            pygame.draw.circle(surface, WHITE, (x + 33, y + 22), 9)
            pygame.draw.circle(surface, WHITE, (x + 55, y + 22), 9)
            pygame.draw.circle(surface, BLACK, (x + 35, y + 23), 5)
            pygame.draw.circle(surface, BLACK, (x + 57, y + 23), 5)
            pygame.draw.circle(surface, WHITE, (x + 36, y + 22), 2)
            pygame.draw.circle(surface, WHITE, (x + 58, y + 22), 2)
            
            if self.state == 'celebrating':
                pygame.draw.arc(surface, BLACK, (x + 36, y + 42, 22, 14), 3.14, 6.28, 3)
        
        # Legs
        pygame.draw.ellipse(surface, main_color, (x + 15, y + 65, 18, 20))
        pygame.draw.ellipse(surface, main_color, (x + 52, y + 65, 18, 20))
        pygame.draw.ellipse(surface, light_color, (x + 18, y + 78, 12, 10))
        pygame.draw.ellipse(surface, light_color, (x + 55, y + 78, 12, 10))
        
        # Duck in mouth when celebrating
        if self.state == 'celebrating':
            duck_colors = {
                'yellow': DUCK_YELLOW,
                'brown': DUCK_BROWN,
                'white': DUCK_WHITE,
                'green': (50, 180, 50),
                'blue': (100, 150, 220),
                'boss': (180, 50, 50)
            }
            duck_color = duck_colors.get(self.held_duck_color, DUCK_YELLOW)
            pygame.draw.ellipse(surface, duck_color, (x + 28, y - 12, 30, 20))
            pygame.draw.circle(surface, duck_color, (x + 55, y - 4), 10)
            pygame.draw.polygon(surface, DUCK_ORANGE, [(x + 62, y - 4), (x + 75, y - 2), (x + 62, y)])


def draw_background(surface, clouds, time_of_day='day', stars=None, frame=0):
    """Dibuja el fondo mejorado segun la hora del dia"""
    
    if time_of_day == 'night':
        for y_pos in range(SCREEN_HEIGHT - GRASS_HEIGHT):
            ratio = y_pos / (SCREEN_HEIGHT - GRASS_HEIGHT)
            r = int(SKY_NIGHT[0] + ratio * 25)
            g = int(SKY_NIGHT[1] + ratio * 25)
            b = int(SKY_NIGHT[2] + ratio * 40)
            pygame.draw.line(surface, (r, g, b), (0, y_pos), (SCREEN_WIDTH, y_pos))
        
        if stars:
            for star in stars:
                star.update()
                star.draw(surface)
        
        # Moon with glow
        for i in range(4):
            glow_alpha = 30 - i * 7
            glow_size = 55 + i * 15
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (240, 240, 200, glow_alpha), (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (720 - glow_size, 85 - glow_size))
        
        pygame.draw.circle(surface, MOON_WHITE, (720, 85), 40)
        pygame.draw.circle(surface, (210, 210, 190), (708, 78), 10)
        pygame.draw.circle(surface, (200, 200, 180), (732, 95), 8)
        pygame.draw.circle(surface, (195, 195, 175), (718, 100), 5)
        pygame.draw.circle(surface, (190, 190, 170), (705, 92), 4)
        
    elif time_of_day == 'sunset':
        for y_pos in range(SCREEN_HEIGHT - GRASS_HEIGHT):
            ratio = y_pos / (SCREEN_HEIGHT - GRASS_HEIGHT)
            r = int(255 - ratio * 60)
            g = int(140 - ratio * 90)
            b = int(80 + ratio * 60)
            pygame.draw.line(surface, (r, g, b), (0, y_pos), (SCREEN_WIDTH, y_pos))
        
        # Setting sun with glow
        sun_y = SCREEN_HEIGHT - GRASS_HEIGHT - 15
        for i in range(5):
            glow_alpha = 40 - i * 8
            glow_size = 65 + i * 20
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 150, 50, glow_alpha), (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (720 - glow_size, sun_y - glow_size))
        
        pygame.draw.circle(surface, (255, 100, 50), (720, sun_y), 50)
        pygame.draw.circle(surface, (255, 150, 50), (720, sun_y), 40)
        pygame.draw.circle(surface, (255, 200, 100), (720, sun_y), 30)
    
    elif time_of_day == 'hell':
        # Cielo infernal
        for y_pos in range(SCREEN_HEIGHT - GRASS_HEIGHT):
            ratio = y_pos / (SCREEN_HEIGHT - GRASS_HEIGHT)
            r = int(80 + ratio * 60 + math.sin(frame * 0.02 + y_pos * 0.01) * 15)
            g = int(20 + ratio * 15)
            b = int(10 + ratio * 10)
            pygame.draw.line(surface, (min(255, r), g, b), (0, y_pos), (SCREEN_WIDTH, y_pos))
        
        # Rayos ocasionales
        if random.random() < 0.02:
            lx = random.randint(50, SCREEN_WIDTH - 50)
            for i in range(5):
                ly = random.randint(HUD_HEIGHT, 200)
                pygame.draw.line(surface, (255, 200, 100), (lx, ly), (lx + random.randint(-30, 30), ly + 50), 3)
        
    else:  # Day
        for y_pos in range(SCREEN_HEIGHT - GRASS_HEIGHT):
            ratio = y_pos / (SCREEN_HEIGHT - GRASS_HEIGHT)
            r = int(SKY_BLUE[0] * (1 - ratio * 0.3) + SKY_DARK[0] * ratio * 0.3)
            g = int(SKY_BLUE[1] * (1 - ratio * 0.3) + SKY_DARK[1] * ratio * 0.3)
            b = int(SKY_BLUE[2] * (1 - ratio * 0.3) + SKY_DARK[2] * ratio * 0.3)
            pygame.draw.line(surface, (r, g, b), (0, y_pos), (SCREEN_WIDTH, y_pos))
        
        # Sun with glow and rays
        for i in range(4):
            glow_alpha = 35 - i * 8
            glow_size = 60 + i * 18
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 200, glow_alpha), (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (720 - glow_size, 90 - glow_size))
        
        # Sun rays
        for angle in range(0, 360, 20):
            rad = math.radians(angle + frame * 0.3)
            x1 = 720 + int(48 * math.cos(rad))
            y1 = 90 + int(48 * math.sin(rad))
            x2 = 720 + int(70 * math.cos(rad))
            y2 = 90 + int(70 * math.sin(rad))
            pygame.draw.line(surface, (255, 230, 100), (x1, y1), (x2, y2), 3)
        
        pygame.draw.circle(surface, SUN_YELLOW, (720, 90), 40)
        pygame.draw.circle(surface, SUN_ORANGE, (720, 90), 32)
    
    # Clouds
    if time_of_day not in ['night']:
        for cloud in clouds:
            cloud.draw(surface, time_of_day)
    
    # Mountains with layers
    mountain_y = SCREEN_HEIGHT - GRASS_HEIGHT
    
    if time_of_day == 'night':
        mountain_colors = [(40, 50, 60), (30, 40, 50), (20, 30, 40)]
    elif time_of_day == 'sunset':
        mountain_colors = [(120, 80, 100), (90, 60, 80), (60, 40, 60)]
    elif time_of_day == 'hell':
        mountain_colors = [(60, 20, 15), (50, 15, 10), (40, 10, 5)]
    else:
        mountain_colors = [(140, 170, 140), (100, 140, 100), (70, 110, 70)]
    
    # Far mountains
    points_far = [(0, mountain_y)]
    for i in range(0, SCREEN_WIDTH + 100, 80):
        height = 60 + math.sin(i * 0.02) * 40
        points_far.append((i, mountain_y - height))
    points_far.append((SCREEN_WIDTH, mountain_y))
    pygame.draw.polygon(surface, mountain_colors[0], points_far)
    
    # Mid mountains
    points_mid = [(0, mountain_y)]
    for i in range(0, SCREEN_WIDTH + 100, 60):
        height = 45 + math.sin(i * 0.03 + 1) * 30
        points_mid.append((i, mountain_y - height))
    points_mid.append((SCREEN_WIDTH, mountain_y))
    pygame.draw.polygon(surface, mountain_colors[1], points_mid)
    
    # Near mountains
    points_near = [(0, mountain_y)]
    for i in range(0, SCREEN_WIDTH + 100, 50):
        height = 30 + math.sin(i * 0.04 + 2) * 20
        points_near.append((i, mountain_y - height))
    points_near.append((SCREEN_WIDTH, mountain_y))
    pygame.draw.polygon(surface, mountain_colors[2], points_near)
    
    # Lake or lava
    lake_x, lake_y = 580, SCREEN_HEIGHT - GRASS_HEIGHT + 55
    if time_of_day == 'hell':
        lake_color = LAVA_ORANGE
        # Lava bubbles
        for i in range(3):
            bx = lake_x + 30 + i * 35 + int(math.sin(frame * 0.1 + i) * 10)
            by = lake_y + 15 + int(math.sin(frame * 0.15 + i * 2) * 5)
            pygame.draw.circle(surface, (255, 150, 50), (bx, by), 5 + int(math.sin(frame * 0.2 + i) * 2))
    else:
        lake_color = (30, 60, 100) if time_of_day == 'night' else (
            (180, 130, 100) if time_of_day == 'sunset' else WATER_BLUE)
    
    pygame.draw.ellipse(surface, lake_color, (lake_x, lake_y, 140, 50))
    
    # Grass ground
    if time_of_day == 'hell':
        grass_color = (40, 20, 15)
    else:
        grass_color = (15, 60, 15) if time_of_day == 'night' else (
            (80, 100, 40) if time_of_day == 'sunset' else GRASS_GREEN)
    pygame.draw.rect(surface, grass_color, (0, SCREEN_HEIGHT - GRASS_HEIGHT, SCREEN_WIDTH, GRASS_HEIGHT))
    
    # Grass detail
    if time_of_day == 'hell':
        grass_detail = (30, 15, 10)
    else:
        grass_detail = (0, 40, 0) if time_of_day == 'night' else (
            (60, 80, 30) if time_of_day == 'sunset' else GRASS_DARK)
    for i in range(0, SCREEN_WIDTH, 6):
        height = 8 + (i * 7) % 20
        offset = ((i * 13) % 7) - 3
        pygame.draw.line(surface, grass_detail, 
                        (i, SCREEN_HEIGHT - GRASS_HEIGHT),
                        (i + offset, SCREEN_HEIGHT - GRASS_HEIGHT - height), 2)
    
    # Trees (no en infierno)
    if time_of_day != 'hell':
        draw_tree(surface, 35, SCREEN_HEIGHT - GRASS_HEIGHT, time_of_day, 1.2)
        draw_tree(surface, SCREEN_WIDTH - 80, SCREEN_HEIGHT - GRASS_HEIGHT, time_of_day, 0.9)
    else:
        # Arboles muertos en infierno
        draw_dead_tree(surface, 35, SCREEN_HEIGHT - GRASS_HEIGHT, 1.2)
        draw_dead_tree(surface, SCREEN_WIDTH - 80, SCREEN_HEIGHT - GRASS_HEIGHT, 0.9)
    
    # Bushes
    if time_of_day == 'hell':
        bush_color = (50, 20, 15)
        bush_dark = (30, 10, 5)
    else:
        bush_color = (0, 50, 0) if time_of_day == 'night' else (
            (60, 80, 30) if time_of_day == 'sunset' else BUSH_GREEN)
        bush_dark = (0, 30, 0) if time_of_day == 'night' else (
            (40, 60, 20) if time_of_day == 'sunset' else BUSH_DARK)
    
    bush_positions = [(140, 30), (300, 38), (450, 32), (750, 35), (850, 28)]
    for bx, bh in bush_positions:
        by = SCREEN_HEIGHT - GRASS_HEIGHT
        pygame.draw.ellipse(surface, bush_dark, (bx - 28, by - bh + 6, 56, bh + 5))
        pygame.draw.ellipse(surface, bush_color, (bx - 24, by - bh - 4, 48, bh + 8))
        pygame.draw.ellipse(surface, bush_color, (bx - 15, by - bh - 10, 30, bh))


def draw_tree(surface, x, y, time_of_day, scale=1.0):
    """Dibuja un arbol detallado"""
    if time_of_day == 'night':
        trunk_color = (50, 30, 15)
        leaves_color = (10, 60, 10)
        leaves_dark = (5, 40, 5)
    elif time_of_day == 'sunset':
        trunk_color = (100, 50, 25)
        leaves_color = (60, 90, 30)
        leaves_dark = (40, 70, 20)
    else:
        trunk_color = TREE_BROWN
        leaves_color = TREE_GREEN
        leaves_dark = TREE_DARK
    
    trunk_w = int(35 * scale)
    trunk_h = int(130 * scale)
    pygame.draw.rect(surface, trunk_color, (x, y - trunk_h, trunk_w, trunk_h))
    pygame.draw.rect(surface, (trunk_color[0] - 20, trunk_color[1] - 10, trunk_color[2] - 5), 
                    (x + trunk_w - 8, y - trunk_h, 8, trunk_h))
    
    center_x = x + trunk_w // 2
    pygame.draw.circle(surface, leaves_dark, (center_x - 20, y - trunk_h - 10), int(40 * scale))
    pygame.draw.circle(surface, leaves_dark, (center_x + 25, y - trunk_h), int(35 * scale))
    pygame.draw.circle(surface, leaves_color, (center_x, y - trunk_h - 40), int(55 * scale))
    pygame.draw.circle(surface, leaves_color, (center_x - 15, y - trunk_h - 5), int(45 * scale))
    pygame.draw.circle(surface, leaves_color, (center_x + 20, y - trunk_h - 15), int(40 * scale))


def draw_dead_tree(surface, x, y, scale=1.0):
    """Dibuja un arbol muerto para el infierno"""
    trunk_color = (40, 25, 20)
    trunk_w = int(25 * scale)
    trunk_h = int(120 * scale)
    
    # Tronco principal
    pygame.draw.rect(surface, trunk_color, (x, y - trunk_h, trunk_w, trunk_h))
    
    # Ramas muertas
    pygame.draw.line(surface, trunk_color, (x + trunk_w // 2, y - trunk_h + 20), 
                    (x - 30 * scale, y - trunk_h - 20), int(5 * scale))
    pygame.draw.line(surface, trunk_color, (x + trunk_w // 2, y - trunk_h + 40), 
                    (x + 50 * scale, y - trunk_h), int(4 * scale))
    pygame.draw.line(surface, trunk_color, (x + trunk_w // 2, y - trunk_h), 
                    (x + trunk_w // 2, y - trunk_h - 30), int(6 * scale))


def draw_crosshair(surface, cx, cy, rapid_fire=False, magnet=False):
    """Dibuja la mira mejorada"""
    color = GOLD if rapid_fire else (PURPLE if magnet else RED)
    inner_color = (255, 255, 150) if rapid_fire else ((200, 150, 255) if magnet else (255, 120, 120))
    
    # Outer ring with glow
    for i in range(3):
        glow_color = (*color[:3], 60 - i * 20) if len(color) == 3 else color
        pygame.draw.circle(surface, glow_color, (cx, cy), 28 + i * 4, 2)
    
    pygame.draw.circle(surface, color, (cx, cy), 26, 3)
    pygame.draw.circle(surface, color, (cx, cy), 12, 2)
    pygame.draw.circle(surface, inner_color, (cx, cy), 4)
    
    # Crosshair lines
    pygame.draw.line(surface, color, (cx - 35, cy), (cx - 14, cy), 3)
    pygame.draw.line(surface, color, (cx + 14, cy), (cx + 35, cy), 3)
    pygame.draw.line(surface, color, (cx, cy - 35), (cx, cy - 14), 3)
    pygame.draw.line(surface, color, (cx, cy + 14), (cx, cy + 35), 3)
    
    # Corner details
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        x1 = cx + int(20 * math.cos(rad))
        y1 = cy + int(20 * math.sin(rad))
        x2 = cx + int(28 * math.cos(rad))
        y2 = cy + int(28 * math.sin(rad))
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)


def draw_hud(surface, score, ammo, ducks_hit, ducks_total, round_num, chapter, active_powerups, combo_display, high_score, secret_mode=False, required_score=0):
    """Dibuja la interfaz del juego mejorada"""
    # Background gradient
    for y in range(HUD_HEIGHT):
        alpha = 200 - y * 2
        pygame.draw.line(surface, (25, 25, 35), (0, y), (SCREEN_WIDTH, y))
    pygame.draw.line(surface, (80, 80, 100), (0, HUD_HEIGHT - 1), (SCREEN_WIDTH, HUD_HEIGHT - 1), 2)
    
    # Score with style
    score_label = font_small.render("SCORE", True, (150, 150, 150))
    surface.blit(score_label, (20, 5))
    score_text = font_large.render(f"{score:,}", True, GOLD)
    surface.blit(score_text, (20, 22))
    
    # High score
    hi_text = font_tiny.render(f"HI: {high_score:,}", True, (100, 100, 100))
    surface.blit(hi_text, (20, 52))
    
    # Required score for secret mode
    if secret_mode and required_score > 0:
        req_color = GREEN if score >= required_score else RED
        req_text = font_small.render(f"MIN: {required_score}", True, req_color)
        surface.blit(req_text, (150, 35))
    
    # Chapter and Round
    if chapter > 0:
        chapter_text = font_small.render(f"CAPITULO {chapter}", True, (150, 150, 150))
        surface.blit(chapter_text, (SCREEN_WIDTH // 2 - chapter_text.get_width() // 2, 5))
    elif secret_mode:
        secret_text = font_small.render("MODO SECRETO", True, (255, 100, 100))
        surface.blit(secret_text, (SCREEN_WIDTH // 2 - secret_text.get_width() // 2, 5))
    round_text = font_medium.render(f"RONDA {round_num}", True, WHITE)
    surface.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, 25))
    
    # Ammo display
    ammo_label = font_small.render("MUNICION", True, (150, 150, 150))
    surface.blit(ammo_label, (SCREEN_WIDTH - 140, 5))
    
    if ammo > 10:
        ammo_text = font_medium.render(f"{ammo}", True, GOLD)
        surface.blit(ammo_text, (SCREEN_WIDTH - 100, 28))
    else:
        for i in range(3):
            if i < ammo:
                pygame.draw.rect(surface, (255, 200, 50), (SCREEN_WIDTH - 130 + i * 30, 32, 10, 22), border_radius=2)
                pygame.draw.rect(surface, (200, 160, 40), (SCREEN_WIDTH - 132 + i * 30, 26, 14, 8), border_radius=2)
            else:
                pygame.draw.rect(surface, (50, 50, 50), (SCREEN_WIDTH - 130 + i * 30, 32, 10, 22), border_radius=2)
                pygame.draw.rect(surface, (40, 40, 40), (SCREEN_WIDTH - 132 + i * 30, 26, 14, 8), border_radius=2)
    
    # Active power-ups
    powerup_x = 200
    for ptype, timer in active_powerups.items():
        if timer > 0:
            bar_width = 30
            bar_fill = int(bar_width * timer / 600) if ptype == 'double_points' else int(bar_width * timer / 300)
            
            if ptype == 'rapid_fire':
                pygame.draw.rect(surface, GOLD, (powerup_x, 18, 28, 28), border_radius=4)
                pygame.draw.polygon(surface, BLACK, [(powerup_x + 10, 22), (powerup_x + 18, 30), (powerup_x + 10, 38)])
            elif ptype == 'slow_motion':
                pygame.draw.rect(surface, (100, 150, 255), (powerup_x, 18, 28, 28), border_radius=4)
                text = font_small.render("SM", True, BLACK)
                surface.blit(text, (powerup_x + 4, 22))
            elif ptype == 'double_points':
                pygame.draw.rect(surface, (255, 100, 100), (powerup_x, 18, 28, 28), border_radius=4)
                text = font_small.render("x2", True, BLACK)
                surface.blit(text, (powerup_x + 4, 22))
            elif ptype == 'extra_ammo':
                pygame.draw.rect(surface, (255, 180, 50), (powerup_x, 18, 28, 28), border_radius=4)
                text = font_tiny.render("INF", True, BLACK)
                surface.blit(text, (powerup_x + 3, 26))
            elif ptype == 'shield':
                pygame.draw.rect(surface, (100, 200, 255), (powerup_x, 18, 28, 28), border_radius=4)
                text = font_small.render("SH", True, BLACK)
                surface.blit(text, (powerup_x + 4, 22))
            elif ptype == 'magnet':
                pygame.draw.rect(surface, (200, 100, 255), (powerup_x, 18, 28, 28), border_radius=4)
                text = font_small.render("MG", True, BLACK)
                surface.blit(text, (powerup_x + 2, 22))
            
            pygame.draw.rect(surface, (50, 50, 50), (powerup_x, 48, bar_width, 4))
            pygame.draw.rect(surface, GREEN, (powerup_x, 48, bar_fill, 4))
            
            powerup_x += 38
    
    # Duck panel at bottom
    panel_width = ducks_total * 48 + 24
    panel_x = SCREEN_WIDTH // 2 - panel_width // 2
    pygame.draw.rect(surface, (30, 30, 40), (panel_x, SCREEN_HEIGHT - 50, panel_width, 45), border_radius=10)
    pygame.draw.rect(surface, (70, 70, 90), (panel_x, SCREEN_HEIGHT - 50, panel_width, 45), 2, border_radius=10)
    
    for i in range(ducks_total):
        duck_x = panel_x + 32 + i * 48
        if i < ducks_hit:
            pygame.draw.circle(surface, (0, 180, 0), (duck_x, SCREEN_HEIGHT - 28), 16)
            pygame.draw.circle(surface, (0, 255, 0), (duck_x, SCREEN_HEIGHT - 28), 12)
            pygame.draw.line(surface, WHITE, (duck_x - 5, SCREEN_HEIGHT - 28), (duck_x - 1, SCREEN_HEIGHT - 24), 3)
            pygame.draw.line(surface, WHITE, (duck_x - 1, SCREEN_HEIGHT - 24), (duck_x + 7, SCREEN_HEIGHT - 34), 3)
        else:
            pygame.draw.circle(surface, (60, 60, 70), (duck_x, SCREEN_HEIGHT - 28), 16)
            pygame.draw.circle(surface, (45, 45, 55), (duck_x, SCREEN_HEIGHT - 28), 12)
    
    # Combo display
    if combo_display:
        combo_text = font_small.render(f"COMBO: {combo_display}", True, (255, 200, 100))
        pygame.draw.rect(surface, (50, 40, 20), (15, SCREEN_HEIGHT - 85, combo_text.get_width() + 16, 28), border_radius=5)
        surface.blit(combo_text, (23, SCREEN_HEIGHT - 80))
    
    # Controls hint
    hint_text = font_tiny.render("WASD=Mover | ESPACIO=Disparar | R=Recargar", True, (100, 100, 110))
    surface.blit(hint_text, (SCREEN_WIDTH - hint_text.get_width() - 15, SCREEN_HEIGHT - 42))


def draw_intro_screen(surface, frame, menu_selection):
    """Dibuja la pantalla de introduccion mejorada"""
    # Animated background
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        wave = math.sin(y * 0.02 + frame * 0.03) * 10
        r = int(15 + ratio * 25 + wave)
        g = int(30 + ratio * 35 + wave * 0.5)
        b = int(60 + ratio * 50 + wave * 0.3)
        pygame.draw.line(surface, (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))), (0, y), (SCREEN_WIDTH, y))
    
    # Animated stars
    for i in range(60):
        sx = (i * 89 + frame // 2) % SCREEN_WIDTH
        sy = (i * 53) % (SCREEN_HEIGHT - 100)
        twinkle = int(100 + 100 * math.sin(frame * 0.08 + i))
        size = 1 if i % 3 else 2
        pygame.draw.circle(surface, (twinkle, twinkle, min(255, twinkle + 30)), (sx, sy), size)
    
    # Title with shadow and animation
    title_y = 100 + int(math.sin(frame * 0.04) * 12)
    
    # Title shadow
    title_shadow = font_title.render("DUCK HUNT", True, (0, 0, 0))
    surface.blit(title_shadow, (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + 5, title_y + 5))
    
    # Title glow
    for i in range(3):
        glow_surf = font_title.render("DUCK HUNT", True, (255, 200, 50))
        glow_surf.set_alpha(30 - i * 10)
        surface.blit(glow_surf, (SCREEN_WIDTH // 2 - glow_surf.get_width() // 2 - i, title_y - i))
        surface.blit(glow_surf, (SCREEN_WIDTH // 2 - glow_surf.get_width() // 2 + i, title_y + i))
    
    # Main title
    title_text = font_title.render("DUCK HUNT", True, GOLD)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, title_y))
    
    # Subtitle
    subtitle = font_medium.render("ULTIMATE EDITION", True, WHITE)
    surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, title_y + 75))
    
    # Animated duck
    duck_x = SCREEN_WIDTH // 2 - 35 + int(math.sin(frame * 0.06) * 60)
    duck_y = 270 + int(math.cos(frame * 0.045) * 25)
    wing_offset = int(math.sin(frame * 0.35) * 10)
    
    pygame.draw.ellipse(surface, DUCK_YELLOW, (duck_x + 5, duck_y + 18, 55, 32))
    pygame.draw.circle(surface, (0, 160, 0), (duck_x + 58, duck_y + 12), 18)
    pygame.draw.circle(surface, WHITE, (duck_x + 64, duck_y + 8), 6)
    pygame.draw.circle(surface, BLACK, (duck_x + 65, duck_y + 8), 4)
    pygame.draw.polygon(surface, DUCK_ORANGE, [(duck_x + 72, duck_y + 14), (duck_x + 92, duck_y + 16), (duck_x + 72, duck_y + 20)])
    pygame.draw.ellipse(surface, DUCK_ORANGE, (duck_x + 18, duck_y + 24 + wing_offset, 32, 18))
    
    # Menu options with clear selection
    menu_y = 370
    options = ["MODO HISTORIA", "MODO ARCADE", "MODO SECRETO", "CONTROLES"]
    
    for i, option in enumerate(options):
        is_selected = i == menu_selection
        
        opt_text = font_medium.render(option, True, WHITE)
        opt_x = SCREEN_WIDTH // 2 - opt_text.get_width() // 2
        
        if is_selected:
            box_width = opt_text.get_width() + 60
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            
            for g in range(3):
                glow_rect = pygame.Rect(box_x - g * 3, menu_y + i * 50 - 8 - g * 3, box_width + g * 6, 42 + g * 6)
                pygame.draw.rect(surface, (255, 200, 50, 40 - g * 12), glow_rect, border_radius=12)
            
            # Color especial para modo secreto
            box_color = (80, 30, 30) if i == 2 else (80, 60, 20)
            border_color = (255, 100, 100) if i == 2 else GOLD
            
            pygame.draw.rect(surface, box_color, (box_x, menu_y + i * 50 - 8, box_width, 42), border_radius=10)
            pygame.draw.rect(surface, border_color, (box_x, menu_y + i * 50 - 8, box_width, 42), 3, border_radius=10)
            
            arrow_pulse = int(math.sin(frame * 0.15) * 5)
            pygame.draw.polygon(surface, border_color, [
                (box_x - 20 - arrow_pulse, menu_y + i * 50 + 13),
                (box_x - 8 - arrow_pulse, menu_y + i * 50 + 6),
                (box_x - 8 - arrow_pulse, menu_y + i * 50 + 20)
            ])
            pygame.draw.polygon(surface, border_color, [
                (box_x + box_width + 20 + arrow_pulse, menu_y + i * 50 + 13),
                (box_x + box_width + 8 + arrow_pulse, menu_y + i * 50 + 6),
                (box_x + box_width + 8 + arrow_pulse, menu_y + i * 50 + 20)
            ])
            
            selected_text = font_medium.render(option, True, border_color)
            surface.blit(selected_text, (opt_x, menu_y + i * 50))
        else:
            pygame.draw.rect(surface, (35, 35, 55), (opt_x - 25, menu_y + i * 50 - 8, opt_text.get_width() + 50, 42), border_radius=10)
            pygame.draw.rect(surface, (60, 60, 80), (opt_x - 25, menu_y + i * 50 - 8, opt_text.get_width() + 50, 42), 2, border_radius=10)
            surface.blit(opt_text, (opt_x, menu_y + i * 50))
    
    # Instructions
    instr_text = font_small.render("W/S = Navegar | ESPACIO = Seleccionar | ESC = Salir", True, (150, 150, 170))
    surface.blit(instr_text, (SCREEN_WIDTH // 2 - instr_text.get_width() // 2, SCREEN_HEIGHT - 55))
    
    # Version
    version_text = font_tiny.render("v3.0 Ultimate Edition - Python/Pygame", True, (80, 80, 100))
    surface.blit(version_text, (SCREEN_WIDTH // 2 - version_text.get_width() // 2, SCREEN_HEIGHT - 28))


def draw_controls_screen(surface, frame):
    """Dibuja la pantalla de controles mejorada"""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        pygame.draw.line(surface, (int(15 + ratio * 15), int(25 + ratio * 20), int(45 + ratio * 30)), (0, y), (SCREEN_WIDTH, y))
    
    title = font_large.render("CONTROLES", True, GOLD)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))
    
    controls = [
        ("W / A / S / D", "Mover la mira"),
        ("ESPACIO", "Disparar"),
        ("R", "Recargar municion"),
        ("ESC", "Pausar / Menu"),
    ]
    
    combos = [
        ("A-W-S-D", "MODO DIOS (5s, 1/ronda)", GOLD),
        ("D-S-A", "Municion infinita (5s)", (255, 180, 50)),
        ("W-D-S", "Camara lenta (5s)", (100, 150, 255)),
        ("A-D-A-D", "Puntos dobles (10s)", (255, 100, 100)),
    ]
    
    y = 100
    for key, desc in controls:
        pygame.draw.rect(surface, (50, 50, 70), (120, y, 160, 36), border_radius=6)
        pygame.draw.rect(surface, (80, 80, 100), (120, y, 160, 36), 2, border_radius=6)
        key_text = font_medium.render(key, True, WHITE)
        surface.blit(key_text, (130, y + 5))
        
        desc_text = font_small.render(desc, True, (180, 180, 190))
        surface.blit(desc_text, (310, y + 8))
        y += 50
    
    pygame.draw.line(surface, (80, 80, 100), (80, y + 15), (SCREEN_WIDTH - 80, y + 15), 2)
    
    y += 35
    combo_title = font_medium.render("COMBOS SECRETOS", True, (255, 180, 100))
    surface.blit(combo_title, (SCREEN_WIDTH // 2 - combo_title.get_width() // 2, y))
    y += 45
    
    for key, desc, color in combos:
        pulse = int(math.sin(frame * 0.1 + combos.index((key, desc, color))) * 3)
        pygame.draw.rect(surface, (40, 35, 50), (120, y - 2 + pulse, 160, 38), border_radius=6)
        pygame.draw.rect(surface, color, (120, y - 2 + pulse, 160, 38), 2, border_radius=6)
        
        key_text = font_medium.render(key, True, color)
        surface.blit(key_text, (130, y + 3 + pulse))
        
        desc_text = font_small.render(desc, True, (180, 180, 190))
        surface.blit(desc_text, (300, y + 8))
        y += 52
    
    # Power-ups info
    y += 10
    powerup_title = font_medium.render("POWER-UPS", True, (100, 200, 150))
    surface.blit(powerup_title, (SCREEN_WIDTH // 2 - powerup_title.get_width() // 2, y))
    y += 35
    
    powerups_info = [
        ("Rayo", "Disparo rapido", GOLD),
        ("Reloj", "Camara lenta", (100, 150, 255)),
        ("Balas", "Municion extra", (255, 180, 50)),
        ("Estrella x2", "Puntos dobles", (255, 100, 100)),
        ("Escudo", "Proteccion", (100, 200, 255)),
        ("Iman", "Atrae power-ups", PURPLE),
    ]
    
    col = 0
    start_x = 100
    for name, desc, color in powerups_info:
        px = start_x + (col % 3) * 270
        py = y + (col // 3) * 35
        
        pygame.draw.circle(surface, color, (px, py + 10), 8)
        text = font_small.render(f"{name}: {desc}", True, (170, 170, 180))
        surface.blit(text, (px + 18, py))
        col += 1
    
    back_text = font_small.render("Presiona ESC para volver", True, (120, 120, 140))
    surface.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 45))


def draw_chapter_intro(surface, chapter, frame):
    """Dibuja la intro de cada capitulo con animacion"""
    surface.fill((0, 0, 0))
    
    chapter_data = {
        1: ("CAPITULO 1", "El Amanecer del Cazador", (135, 206, 250), "Aprende los controles basicos"),
        2: ("CAPITULO 2", "La Tarde Dorada", (255, 150, 100), "Los patos son mas rapidos"),
        3: ("CAPITULO 3", "Caceria Nocturna", (50, 50, 100), "Visibilidad reducida"),
        4: ("CAPITULO 4", "El Desafio Final", (30, 20, 60), "Pon a prueba tu habilidad"),
    }
    
    title, subtitle, bg_color, hint = chapter_data.get(chapter, ("CAPITULO ?", "Desconocido", (50, 50, 50), ""))
    
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(bg_color[0] * (1 - ratio * 0.7))
        g = int(bg_color[1] * (1 - ratio * 0.7))
        b = int(bg_color[2] * (1 - ratio * 0.7))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    alpha = min(255, frame * 6)
    
    chapter_num_text = font_title.render(str(chapter), True, GOLD)
    chapter_num_text.set_alpha(alpha)
    surface.blit(chapter_num_text, (SCREEN_WIDTH // 2 - chapter_num_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))
    
    title_text = font_large.render(title, True, WHITE)
    title_text.set_alpha(alpha)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
    
    subtitle_text = font_medium.render(subtitle, True, (200, 200, 200))
    subtitle_text.set_alpha(alpha)
    surface.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
    if frame > 30:
        hint_alpha = min(255, (frame - 30) * 5)
        hint_text = font_small.render(hint, True, (150, 150, 150))
        hint_text.set_alpha(hint_alpha)
        surface.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
    
    if frame > 50:
        pulse = int(128 + 127 * math.sin(frame * 0.12))
        continue_text = font_small.render("Presiona ESPACIO para continuar", True, (pulse, pulse, pulse))
        surface.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT - 80))


def draw_story_intro(surface, frame, stage):
    """Dibuja la intro de la historia del perro - VERSION MEJORADA CON MEJOR ESTETICA"""
    
    # Transicion suave entre escenas
    fade_in = min(255, frame * 6)
    
    if stage == 0:  # ESCENA 1: Familia feliz del perro
        # Fondo atardecer con gradiente suave y nubes
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            wave = math.sin(y * 0.01 + frame * 0.02) * 5
            r = int(min(255, 255 - ratio * 80 + wave))
            g = int(min(255, 180 - ratio * 100 + wave * 0.5))
            b = int(min(255, 130 - ratio * 60))
            pygame.draw.line(surface, (max(0, r), max(0, g), max(0, b)), (0, y), (SCREEN_WIDTH, y))
        
        # Sol poniente con brillo
        sun_x, sun_y = 700, 300
        for i in range(5):
            glow_size = 80 + i * 20
            glow_alpha = 60 - i * 12
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 200, 100, glow_alpha), (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (sun_x - glow_size, sun_y - glow_size))
        pygame.draw.circle(surface, (255, 220, 150), (sun_x, sun_y), 50)
        pygame.draw.circle(surface, (255, 240, 200), (sun_x - 10, sun_y - 10), 20)
        
        # Nubes decorativas
        for cx, cy, cs in [(150, 150, 1.2), (400, 100, 0.8), (650, 180, 1.0)]:
            pygame.draw.ellipse(surface, (255, 220, 200), (cx, cy, int(80 * cs), int(30 * cs)))
            pygame.draw.ellipse(surface, (255, 230, 210), (cx + int(20 * cs), cy - int(10 * cs), int(60 * cs), int(25 * cs)))
        
        # Casa con mas detalle
        house_x = 580
        # Sombra de la casa
        pygame.draw.rect(surface, (80, 50, 30), (house_x + 10, 365, 200, 145))
        # Casa principal
        pygame.draw.rect(surface, (140, 95, 60), (house_x, 355, 200, 150))
        # Detalles de madera
        for i in range(5):
            pygame.draw.line(surface, (120, 75, 45), (house_x, 360 + i * 30), (house_x + 200, 360 + i * 30), 2)
        # Techo con sombra
        pygame.draw.polygon(surface, (80, 50, 35), [(house_x - 25, 360), (house_x + 100, 275), (house_x + 225, 360)])
        pygame.draw.polygon(surface, (100, 65, 45), [(house_x - 20, 355), (house_x + 100, 280), (house_x + 220, 355)])
        # Puerta
        pygame.draw.rect(surface, (70, 50, 35), (house_x + 75, 420, 55, 85))
        pygame.draw.circle(surface, (200, 180, 100), (house_x + 115, 465), 5)
        # Ventanas con luz
        pygame.draw.rect(surface, (60, 50, 40), (house_x + 28, 378, 45, 40))
        pygame.draw.rect(surface, (255, 240, 180), (house_x + 32, 382, 37, 32))
        pygame.draw.rect(surface, (60, 50, 40), (house_x + 128, 378, 45, 40))
        pygame.draw.rect(surface, (255, 240, 180), (house_x + 132, 382, 37, 32))
        # Cruces de ventana
        pygame.draw.line(surface, (60, 50, 40), (house_x + 50, 382), (house_x + 50, 414), 2)
        pygame.draw.line(surface, (60, 50, 40), (house_x + 32, 398), (house_x + 69, 398), 2)
        pygame.draw.line(surface, (60, 50, 40), (house_x + 150, 382), (house_x + 150, 414), 2)
        pygame.draw.line(surface, (60, 50, 40), (house_x + 132, 398), (house_x + 169, 398), 2)
        
        # Suelo con pasto detallado
        pygame.draw.rect(surface, (70, 110, 55), (0, 505, SCREEN_WIDTH, 145))
        # Detalles de pasto
        for i in range(0, SCREEN_WIDTH, 20):
            height = 8 + random.randint(0, 5)
            pygame.draw.line(surface, (50, 90, 40), (i, 505), (i - 3, 505 - height), 2)
            pygame.draw.line(surface, (60, 100, 45), (i + 10, 505), (i + 13, 505 - height + 2), 2)
        
        # Perro padre Hunter (mas detallado)
        dog_x = 130 + int(math.sin(frame * 0.025) * 15)
        dog_y = 430
        # Sombra
        pygame.draw.ellipse(surface, (50, 80, 40), (dog_x + 25, dog_y + 55, 75, 20))
        # Cuerpo
        pygame.draw.ellipse(surface, DOG_BROWN, (dog_x + 15, dog_y, 90, 55))
        # Cabeza
        pygame.draw.ellipse(surface, DOG_BROWN, (dog_x + 25, dog_y - 35, 70, 50))
        # Hocico
        pygame.draw.ellipse(surface, DOG_LIGHT, (dog_x + 45, dog_y - 15, 45, 30))
        # Nariz
        pygame.draw.ellipse(surface, (40, 25, 20), (dog_x + 78, dog_y - 8, 14, 10))
        # Ojos (expresivos)
        pygame.draw.circle(surface, WHITE, (dog_x + 50, dog_y - 20), 8)
        pygame.draw.circle(surface, WHITE, (dog_x + 70, dog_y - 20), 8)
        pygame.draw.circle(surface, (60, 40, 30), (dog_x + 52, dog_y - 19), 5)
        pygame.draw.circle(surface, (60, 40, 30), (dog_x + 72, dog_y - 19), 5)
        pygame.draw.circle(surface, WHITE, (dog_x + 53, dog_y - 21), 2)
        pygame.draw.circle(surface, WHITE, (dog_x + 73, dog_y - 21), 2)
        # Orejas
        pygame.draw.ellipse(surface, DOG_DARK, (dog_x + 20, dog_y - 55, 22, 40))
        pygame.draw.ellipse(surface, DOG_DARK, (dog_x + 68, dog_y - 55, 22, 40))
        # Patas
        pygame.draw.ellipse(surface, DOG_BROWN, (dog_x + 20, dog_y + 40, 25, 18))
        pygame.draw.ellipse(surface, DOG_BROWN, (dog_x + 70, dog_y + 40, 25, 18))
        # Cola moviendose
        tail_wave = math.sin(frame * 0.2) * 15
        pygame.draw.ellipse(surface, DOG_BROWN, (dog_x - 5 + tail_wave, dog_y + 10, 30, 15))
        
        # Cachorros (mas detallados y animados)
        puppy_colors = [(DOG_BROWN, DOG_LIGHT), ((180, 140, 100), (220, 200, 170)), ((140, 90, 60), (180, 150, 120))]
        for i in range(3):
            px = dog_x + 140 + i * 60
            py = 460 + int(math.sin(frame * 0.15 + i * 1.5) * 8)
            main_c, light_c = puppy_colors[i]
            # Sombra
            pygame.draw.ellipse(surface, (50, 80, 40), (px + 5, py + 28, 40, 12))
            # Cuerpo
            pygame.draw.ellipse(surface, main_c, (px, py, 50, 30))
            # Cabeza
            pygame.draw.ellipse(surface, main_c, (px + 8, py - 20, 38, 28))
            # Hocico
            pygame.draw.ellipse(surface, light_c, (px + 22, py - 10, 22, 15))
            # Nariz
            pygame.draw.circle(surface, (40, 25, 20), (px + 38, py - 5), 4)
            # Ojos brillantes
            pygame.draw.circle(surface, BLACK, (px + 22, py - 12), 4)
            pygame.draw.circle(surface, BLACK, (px + 34, py - 12), 4)
            pygame.draw.circle(surface, WHITE, (px + 23, py - 13), 1)
            pygame.draw.circle(surface, WHITE, (px + 35, py - 13), 1)
            # Orejas
            pygame.draw.ellipse(surface, main_c, (px + 5, py - 28, 14, 20))
            pygame.draw.ellipse(surface, main_c, (px + 30, py - 28, 14, 20))
        
        # Corazones flotantes (amor familiar)
        for i in range(3):
            hx = 200 + i * 80 + int(math.sin(frame * 0.05 + i) * 10)
            hy = 380 - int(frame * 0.3) % 100 + i * 20
            if hy > 280:
                size = 8 + int(math.sin(frame * 0.1 + i) * 2)
                # Corazon simple
                pygame.draw.circle(surface, (255, 150, 150), (hx - 4, hy), size // 2)
                pygame.draw.circle(surface, (255, 150, 150), (hx + 4, hy), size // 2)
                pygame.draw.polygon(surface, (255, 150, 150), [(hx - 8, hy + 2), (hx, hy + 12), (hx + 8, hy + 2)])
        
        # Panel de texto elegante
        panel_y = 60
        panel_surf = pygame.Surface((500, 100), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 120), (0, 0, 500, 100), border_radius=15)
        surface.blit(panel_surf, (SCREEN_WIDTH // 2 - 250, panel_y))
        
        # Texto con borde
        alpha = min(255, frame * 5)
        text1 = font_large.render("La Familia de Hunter", True, GOLD)
        text1.set_alpha(alpha)
        surface.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, panel_y + 15))
        
        if frame > 50:
            alpha2 = min(255, (frame - 50) * 5)
            text2 = font_medium.render("Un padre dedicado a sus cachorros", True, WHITE)
            text2.set_alpha(alpha2)
            surface.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, panel_y + 55))
    
    elif stage == 1:  # ESCENA 2: Tiempos dificiles (mas emotiva)
        # Fondo triste - noche lluviosa
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            pulse = math.sin(frame * 0.02 + y * 0.005) * 3
            r = int(30 + ratio * 15 + pulse)
            g = int(35 + ratio * 20 + pulse)
            b = int(55 + ratio * 35 + pulse)
            pygame.draw.line(surface, (max(0, r), max(0, g), max(0, b)), (0, y), (SCREEN_WIDTH, y))
        
        # Lluvia sutil
        for i in range(30):
            rx = (i * 37 + frame * 4) % SCREEN_WIDTH
            ry = (i * 23 + frame * 6) % (SCREEN_HEIGHT - 150)
            pygame.draw.line(surface, (100, 110, 140, 100), (rx, ry), (rx - 1, ry + 12), 1)
        
        # Interior de la casa (oscuro)
        pygame.draw.rect(surface, (40, 35, 30), (0, 300, SCREEN_WIDTH, 350))
        
        # Platos vacios con detalle
        for px, py in [(280, 420), (520, 420)]:
            # Sombra del plato
            pygame.draw.ellipse(surface, (30, 25, 22), (px + 5, py + 5, 100, 28))
            # Plato
            pygame.draw.ellipse(surface, (80, 75, 70), (px, py, 100, 28))
            pygame.draw.ellipse(surface, (100, 95, 90), (px + 10, py + 5, 80, 18))
            # Brillo
            pygame.draw.arc(surface, (120, 115, 110), (px + 20, py + 8, 60, 10), 0, 3.14, 2)
        
        # Cachorros tristes (muy detallados)
        for i in range(3):
            px = 250 + i * 130
            py = 350
            bounce = int(math.sin(frame * 0.03 + i) * 3)
            
            # Sombra
            pygame.draw.ellipse(surface, (25, 22, 18), (px + 5, py + 50, 55, 15))
            # Cuerpo encogido
            pygame.draw.ellipse(surface, DOG_BROWN, (px, py + 15 + bounce, 60, 35))
            # Cabeza agachada
            pygame.draw.ellipse(surface, DOG_BROWN, (px + 12, py - 10 + bounce, 45, 35))
            # Hocico
            pygame.draw.ellipse(surface, DOG_LIGHT, (px + 30, py + 5 + bounce, 25, 18))
            # Nariz
            pygame.draw.circle(surface, (40, 25, 20), (px + 48, py + 10 + bounce), 4)
            # Ojos tristes (mirando hacia abajo)
            pygame.draw.ellipse(surface, BLACK, (px + 24, py - 2 + bounce, 8, 5))
            pygame.draw.ellipse(surface, BLACK, (px + 38, py - 2 + bounce, 8, 5))
            # Cejas tristes
            pygame.draw.line(surface, (80, 50, 35), (px + 22, py - 8 + bounce), (px + 30, py - 5 + bounce), 2)
            pygame.draw.line(surface, (80, 50, 35), (px + 48, py - 5 + bounce), (px + 40, py - 8 + bounce), 2)
            # Orejas caidas
            pygame.draw.ellipse(surface, DOG_DARK, (px + 10, py - 5 + bounce, 15, 25))
            pygame.draw.ellipse(surface, DOG_DARK, (px + 40, py - 5 + bounce, 15, 25))
            # Lagrima
            tear_y = py + 8 + bounce + (frame % 40) * 0.5
            if tear_y < py + 30:
                pygame.draw.circle(surface, (150, 180, 220), (px + 28, int(tear_y)), 2)
        
        # Panel de texto
        panel_y = 80
        panel_surf = pygame.Surface((550, 130), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 150), (0, 0, 550, 130), border_radius=15)
        surface.blit(panel_surf, (SCREEN_WIDTH // 2 - 275, panel_y))
        
        alpha = min(255, frame * 5)
        text1 = font_large.render("Los tiempos son dificiles...", True, (200, 180, 160))
        text1.set_alpha(alpha)
        surface.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, panel_y + 20))
        
        if frame > 50:
            alpha2 = min(255, (frame - 50) * 5)
            text2 = font_medium.render("La familia necesita comida", True, (180, 170, 160))
            text2.set_alpha(alpha2)
            surface.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, panel_y + 65))
        
        if frame > 80:
            alpha3 = min(255, (frame - 80) * 5)
            text3 = font_small.render("Los platos estan vacios...", True, (150, 140, 130))
            text3.set_alpha(alpha3)
            surface.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, panel_y + 100))
    
    elif stage == 2:  # ESCENA 3: La decision heroica
        # Fondo amanecer dramatico
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            if y < SCREEN_HEIGHT * 0.6:
                r = int(80 + (1 - ratio) * 100 + math.sin(frame * 0.02) * 10)
                g = int(60 + (1 - ratio) * 80)
                b = int(100 + (1 - ratio) * 60)
            else:
                r = int(40 + ratio * 20)
                g = int(60 + ratio * 30)
                b = int(50 + ratio * 25)
            pygame.draw.line(surface, (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))), (0, y), (SCREEN_WIDTH, y))
        
        # Sol naciente epico
        sun_y = 350 - int(frame * 0.3)
        if sun_y > 250:
            sun_y = max(250, sun_y)
        # Rayos de luz
        for i in range(12):
            angle = math.radians(i * 30 + frame * 0.5)
            length = 200 + math.sin(frame * 0.1 + i) * 30
            end_x = SCREEN_WIDTH // 2 + int(length * math.cos(angle))
            end_y = sun_y + int(length * math.sin(angle))
            for w in range(3):
                pygame.draw.line(surface, (255, 220, 150, 50 - w * 15), (SCREEN_WIDTH // 2, sun_y), (end_x, end_y), 4 - w)
        # Sol
        for i in range(4):
            glow_size = 80 + i * 25
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 220, 150, 50 - i * 12), (glow_size, glow_size), glow_size)
            surface.blit(glow_surf, (SCREEN_WIDTH // 2 - glow_size, sun_y - glow_size))
        pygame.draw.circle(surface, (255, 230, 180), (SCREEN_WIDTH // 2, sun_y), 55)
        pygame.draw.circle(surface, (255, 245, 220), (SCREEN_WIDTH // 2 - 15, sun_y - 15), 25)
        
        # Colinas en silueta
        for hx, hw, hh in [(0, 400, 120), (300, 350, 100), (550, 400, 140)]:
            pygame.draw.ellipse(surface, (40, 55, 45), (hx, SCREEN_HEIGHT - hh - 30, hw, hh))
        
        # Suelo
        pygame.draw.rect(surface, (45, 65, 50), (0, 490, SCREEN_WIDTH, 160))
        
        # Hunter en silueta heroica mirando al horizonte
        dog_x = 180
        dog_y = 400
        silhouette_color = (25, 30, 35)
        
        # Sombra larga dramatica
        pygame.draw.ellipse(surface, (30, 40, 35), (dog_x + 20, dog_y + 100, 150, 25))
        
        # Cuerpo en posicion heroica
        pygame.draw.ellipse(surface, silhouette_color, (dog_x + 10, dog_y + 35, 110, 70))
        # Cabeza levantada
        pygame.draw.ellipse(surface, silhouette_color, (dog_x + 30, dog_y - 25, 80, 70))
        # Hocico apuntando al horizonte
        pygame.draw.ellipse(surface, silhouette_color, (dog_x + 80, dog_y + 5, 50, 30))
        # Orejas alertas
        pygame.draw.ellipse(surface, silhouette_color, (dog_x + 30, dog_y - 50, 25, 45))
        pygame.draw.ellipse(surface, silhouette_color, (dog_x + 70, dog_y - 50, 25, 45))
        # Patas firmes
        pygame.draw.rect(surface, silhouette_color, (dog_x + 25, dog_y + 85, 25, 35))
        pygame.draw.rect(surface, silhouette_color, (dog_x + 80, dog_y + 85, 25, 35))
        # Ojo determinado (brillo)
        pygame.draw.circle(surface, (255, 220, 180), (dog_x + 95, dog_y + 5), 4)
        
        # Patos volando en la distancia
        for i in range(4):
            px = 550 + i * 60 + int(math.sin(frame * 0.1 + i) * 10)
            py = 200 + i * 25 + int(math.cos(frame * 0.08 + i) * 8)
            wing = int(math.sin(frame * 0.3 + i) * 5)
            pygame.draw.ellipse(surface, (60, 70, 80), (px, py, 20, 10))
            pygame.draw.line(surface, (60, 70, 80), (px + 5, py + 5), (px - 5, py - wing), 2)
            pygame.draw.line(surface, (60, 70, 80), (px + 15, py + 5), (px + 25, py - wing), 2)
        
        # Panel de texto epico
        panel_y = 50
        panel_surf = pygame.Surface((600, 160), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (0, 0, 0, 140), (0, 0, 600, 160), border_radius=15)
        surface.blit(panel_surf, (SCREEN_WIDTH // 2 - 300, panel_y))
        
        alpha = min(255, frame * 5)
        text1 = font_large.render("Hunter toma una decision", True, GOLD)
        text1.set_alpha(alpha)
        surface.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, panel_y + 15))
        
        if frame > 50:
            alpha2 = min(255, (frame - 50) * 5)
            text2 = font_medium.render("Cazara patos para alimentar a su familia", True, WHITE)
            text2.set_alpha(alpha2)
            surface.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, panel_y + 60))
        
        if frame > 90:
            alpha3 = min(255, (frame - 90) * 5)
            text3 = font_small.render("Asi comienza la leyenda del mejor cazador...", True, (200, 200, 200))
            text3.set_alpha(alpha3)
            surface.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, panel_y + 100))
        
        if frame > 120:
            alpha4 = min(255, (frame - 120) * 5)
            text4 = font_small.render("Por su familia, por su honor", True, (255, 200, 150))
            text4.set_alpha(alpha4)
            surface.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, panel_y + 130))
    
    # Prompt para continuar (mejorado)
    if frame > 90:
        pulse = int(128 + 127 * math.sin(frame * 0.12))
        # Fondo del boton
        btn_surf = pygame.Surface((300, 40), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (255, 255, 255, 30), (0, 0, 300, 40), border_radius=20)
        surface.blit(btn_surf, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 70))
        
        continue_text = font_small.render("ESPACIO para continuar", True, (pulse, pulse, pulse))
        surface.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT - 60))


def draw_secret_mode_intro(surface, frame, stage, particles):
    """Dibuja la intro del modo secreto con cueva y rayo"""
    surface.fill((0, 0, 0))
    
    if stage == 0:  # Saliendo de la cueva
        # Fondo de cueva oscura
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            darkness = max(0, min(255, int(20 + ratio * 30)))
            pygame.draw.line(surface, (darkness, darkness // 2, darkness // 3), (0, y), (SCREEN_WIDTH, y))
        
        # Luz al final de la cueva
        light_x = SCREEN_WIDTH // 2
        light_intensity = min(1.0, frame / 120)
        
        for i in range(5):
            radius = 150 + i * 40
            alpha = int(50 * light_intensity - i * 10)
            if alpha > 0:
                glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (200, 180, 150, alpha), (radius, radius), radius)
                surface.blit(glow_surf, (light_x - radius, 200 - radius))
        
        # Paredes de la cueva
        # Izquierda
        cave_points_left = [(0, 0), (200, 0), (250, 150), (280, 300), (260, 450), (200, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)]
        pygame.draw.polygon(surface, (30, 25, 20), cave_points_left)
        # Derecha
        cave_points_right = [(SCREEN_WIDTH, 0), (700, 0), (650, 150), (620, 300), (640, 450), (700, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)]
        pygame.draw.polygon(surface, (30, 25, 20), cave_points_right)
        
        # Estalactitas
        for i in range(8):
            sx = 200 + i * 70 + random.randint(-10, 10)
            sh = 30 + random.randint(0, 40)
            pygame.draw.polygon(surface, (50, 40, 35), [(sx - 10, 0), (sx + 10, 0), (sx, sh)])
        
        # Perro caminando hacia la luz
        dog_x = min(400, 50 + frame * 2)
        dog_y = 400
        pygame.draw.ellipse(surface, DOG_BROWN, (dog_x, dog_y, 80, 50))
        pygame.draw.ellipse(surface, DOG_BROWN, (dog_x + 20, dog_y - 30, 50, 40))
        pygame.draw.ellipse(surface, DOG_DARK, (dog_x + 10, dog_y - 40, 18, 30))
        pygame.draw.ellipse(surface, DOG_DARK, (dog_x + 45, dog_y - 40, 18, 30))
        
        # Texto
        if frame > 60:
            alpha = min(255, (frame - 60) * 5)
            text = font_large.render("Un lugar desconocido...", True, (200, 180, 150))
            text.set_alpha(alpha)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
    
    elif stage == 1:  # El rayo y tormenta
        # Cielo tormentoso
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            flash = 50 if (frame % 30 < 3 and frame > 30) else 0
            r = int(30 + ratio * 20 + flash)
            g = int(25 + ratio * 15 + flash)
            b = int(40 + ratio * 30 + flash)
            pygame.draw.line(surface, (min(255, r), min(255, g), min(255, b)), (0, y), (SCREEN_WIDTH, y))
        
        # Nubes de tormenta
        for i in range(5):
            cx = 100 + i * 180
            cy = 120 + int(math.sin(frame * 0.02 + i) * 10)
            pygame.draw.ellipse(surface, (40, 35, 50), (cx, cy, 150, 60))
            pygame.draw.ellipse(surface, (45, 40, 55), (cx + 30, cy - 20, 100, 50))
        
        # Rayo principal
        if frame > 60 and frame < 90:
            # Dibujar rayo
            lightning_x = SCREEN_WIDTH // 2
            points = [(lightning_x, 100)]
            y = 100
            while y < 400:
                y += 30
                x_offset = random.randint(-30, 30)
                points.append((lightning_x + x_offset, y))
                lightning_x += x_offset // 2
            
            # Glow del rayo
            for p in points:
                pygame.draw.circle(surface, (255, 255, 200), p, 15)
            
            # Rayo
            if len(points) > 1:
                pygame.draw.lines(surface, WHITE, False, points, 5)
                pygame.draw.lines(surface, (200, 200, 255), False, points, 3)
            
            # Particulas de rayo
            for _ in range(5):
                particles.append(Particle(points[-1][0], points[-1][1], 'lightning'))
        
        # Lluvia
        for i in range(50):
            rx = (i * 47 + frame * 5) % SCREEN_WIDTH
            ry = (i * 31 + frame * 8) % SCREEN_HEIGHT
            pygame.draw.line(surface, (150, 150, 180), (rx, ry), (rx - 2, ry + 15), 1)
        
        # Suelo
        pygame.draw.rect(surface, (40, 50, 40), (0, 450, SCREEN_WIDTH, 200))
        
        # Texto
        if frame > 90:
            alpha = min(255, (frame - 90) * 5)
            text = font_large.render("El portal se abre...", True, (255, 200, 100))
            text.set_alpha(alpha)
            surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 80))
    
    elif stage == 2:  # Entrada al infierno
        # Cielo infernal
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            pulse = math.sin(frame * 0.05 + y * 0.01) * 20
            r = int(100 + ratio * 80 + pulse)
            g = int(20 + ratio * 10)
            b = int(10 + ratio * 5)
            pygame.draw.line(surface, (min(255, max(0, r)), g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Portal infernal
        portal_x = SCREEN_WIDTH // 2
        portal_y = SCREEN_HEIGHT // 2
        for i in range(8):
            radius = 150 - i * 15
            color = (min(255, 150 + i * 15), max(0, 50 - i * 5), 0)
            pygame.draw.circle(surface, color, (portal_x, portal_y), radius, 3)
        
        # Particulas de fuego subiendo
        if frame % 3 == 0:
            for _ in range(3):
                particles.append(Particle(
                    portal_x + random.randint(-100, 100),
                    portal_y + random.randint(-50, 50),
                    'ember'
                ))
        
        # Montanas oscuras
        for i in range(0, SCREEN_WIDTH, 100):
            height = 80 + math.sin(i * 0.03) * 40
            pygame.draw.polygon(surface, (30, 15, 10), [
                (i, SCREEN_HEIGHT),
                (i + 50, SCREEN_HEIGHT - height),
                (i + 100, SCREEN_HEIGHT)
            ])
        
        # Texto
        alpha = min(255, frame * 4)
        text = font_large.render("BIENVENIDO AL INFIERNO", True, (255, 100, 50))
        text.set_alpha(alpha)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 80))
        
        if frame > 60:
            alpha2 = min(255, (frame - 60) * 4)
            text2 = font_medium.render("Aqui moran los demonios alados...", True, (200, 150, 100))
            text2.set_alpha(alpha2)
            surface.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 140))
    
    # Actualizar y dibujar particulas
    particles[:] = [p for p in particles if p.update()]
    for p in particles:
        p.draw(surface)
    
    # Prompt para continuar
    if frame > 90:
        pulse = int(128 + 127 * math.sin(frame * 0.12))
        continue_text = font_small.render("ESPACIO para continuar", True, (pulse, pulse // 2, pulse // 4))
        surface.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT - 60))


def draw_boss_presentation(surface, frame, boss_index, particles):
    """Dibuja la presentacion de un boss"""
    boss = SECRET_BOSSES[boss_index] if boss_index < len(SECRET_BOSSES) else SECRET_BOSSES[0]
    
    # Fondo infernal
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        pulse = math.sin(frame * 0.03 + y * 0.005) * 15
        r = int(60 + ratio * 40 + pulse)
        g = int(15 + ratio * 10)
        b = int(10 + ratio * 5)
        pygame.draw.line(surface, (min(255, max(0, r)), g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Silueta del boss
    boss_x = SCREEN_WIDTH // 2
    boss_y = SCREEN_HEIGHT // 2 - 50
    scale = 2.5
    
    # Aura
    for i in range(5):
        radius = int(80 + i * 20 + math.sin(frame * 0.1) * 10)
        alpha = 80 - i * 15
        glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*boss["color"], alpha), (radius, radius), radius)
        surface.blit(glow_surf, (boss_x - radius, boss_y - radius))
    
    # Boss (pato demonico grande)
    pygame.draw.ellipse(surface, boss["color"], (boss_x - 60, boss_y - 20, 120, 70))
    pygame.draw.circle(surface, boss["color"], (boss_x + 50, boss_y - 40), 35)
    # Ojos rojos brillantes
    pygame.draw.circle(surface, (255, 50, 50), (boss_x + 55, boss_y - 50), 10)
    pygame.draw.circle(surface, (255, 255, 100), (boss_x + 55, boss_y - 50), 5)
    # Pico
    pygame.draw.polygon(surface, (150, 80, 30), [
        (boss_x + 75, boss_y - 35),
        (boss_x + 110, boss_y - 30),
        (boss_x + 75, boss_y - 25)
    ])
    # Alas demoniacas
    wing_offset = int(math.sin(frame * 0.15) * 15)
    pygame.draw.polygon(surface, (boss["color"][0] - 30, boss["color"][1] - 10, boss["color"][2] - 10), [
        (boss_x - 50, boss_y),
        (boss_x - 120, boss_y - 60 + wing_offset),
        (boss_x - 100, boss_y + 20)
    ])
    pygame.draw.polygon(surface, (boss["color"][0] - 30, boss["color"][1] - 10, boss["color"][2] - 10), [
        (boss_x + 30, boss_y),
        (boss_x + 100, boss_y - 60 - wing_offset),
        (boss_x + 80, boss_y + 20)
    ])
    
    # Particulas de fuego
    if frame % 5 == 0:
        particles.append(Particle(boss_x + random.randint(-50, 50), boss_y + 30, 'ember'))
    
    # Nombre del boss
    alpha = min(255, frame * 5)
    name_text = font_title.render(boss["name"], True, (255, 100, 50))
    name_text.set_alpha(alpha)
    surface.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 80))
    
    # Descripcion
    if frame > 40:
        alpha2 = min(255, (frame - 40) * 5)
        desc_text = font_medium.render(boss["description"], True, (200, 150, 100))
        desc_text.set_alpha(alpha2)
        surface.blit(desc_text, (SCREEN_WIDTH // 2 - desc_text.get_width() // 2, 150))
    
    # Nivel
    if frame > 60:
        alpha3 = min(255, (frame - 60) * 5)
        level_text = font_small.render(f"NIVEL {boss_index + 1}", True, (255, 200, 100))
        level_text.set_alpha(alpha3)
        surface.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT - 120))
    
    # Actualizar particulas
    particles[:] = [p for p in particles if p.update()]
    for p in particles:
        p.draw(surface)
    
    # Prompt
    if frame > 80:
        pulse = int(128 + 127 * math.sin(frame * 0.12))
        continue_text = font_small.render("ESPACIO para enfrentar", True, (pulse, pulse // 2, 0))
        surface.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT - 60))


def main():
    """Funcion principal del juego"""
    running = True
    game_state = 'intro'
    menu_selection = 0
    intro_frame = 0
    chapter_frame = 0
    game_frame = 0
    
    # Variables de juego
    score = 0
    high_score = 0
    ammo = 3
    round_num = 1
    chapter = 1
    ducks_per_round = 5
    ducks_hit = 0
    ducks_spawned = 0
    
    cursor_x = SCREEN_WIDTH // 2
    cursor_y = SCREEN_HEIGHT // 2
    
    # Combo system mejorado
    combo_keys = []
    combo_timer = 0
    combo_display = ""
    
    # Power-ups con duraciones estabilizadas
    POWERUP_DURATION_STANDARD = 300  # 5 segundos a 60fps
    POWERUP_DURATION_DOUBLE = 600    # 10 segundos para double points
    
    active_powerups = {
        'rapid_fire': 0,
        'slow_motion': 0,
        'extra_ammo': 0,
        'double_points': 0,
        'shield': 0,
        'magnet': 0
    }
    powerups = []
    
    # Visual effects
    particles = []
    floating_texts = []
    
    # Environment
    clouds = [Cloud(start_random=True) for _ in range(7)]
    stars = [Star() for _ in range(50)]
    ducks = []
    dog = Dog()
    time_of_day = 'day'
    
    # Sistema de sonido ambiente
    ambient_sound = AmbientSound()
    ambient_sound.play_menu()
    
    # Sistema QTE para modo secreto
    qte_system = QTESystem()
    
    # Variables modo secreto
    secret_mode = False
    secret_mode_unlocked = False  # Si el modo secreto esta desbloqueado
    secret_unlock_sequence = []   # Secuencia para desbloquear: WSADWSAD (dos veces)
    secret_unlock_timer = 0       # Timer para la secuencia
    secret_intro_stage = 0
    story_intro_stage = 0
    boss_presentation_index = 0
    required_score = 0
    showing_unlock_animation = False  # Mostrar animacion de desbloqueo
    unlock_animation_frame = 0
    
    pygame.mouse.set_visible(False)
    
    while running:
        keys_pressed = pygame.key.get_pressed()
        
        # Cursor movement with WASD (solo en juego)
        if game_state == 'playing':
            if keys_pressed[pygame.K_w]:
                cursor_y -= CURSOR_SPEED
            if keys_pressed[pygame.K_s]:
                cursor_y += CURSOR_SPEED
            if keys_pressed[pygame.K_a]:
                cursor_x -= CURSOR_SPEED
            if keys_pressed[pygame.K_d]:
                cursor_x += CURSOR_SPEED
            
            cursor_x = max(20, min(cursor_x, SCREEN_WIDTH - 20))
            cursor_y = max(HUD_HEIGHT + 20, min(cursor_y, SCREEN_HEIGHT - 70))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # QTE check (tiene prioridad en modo secreto)
                if qte_system.active:
                    qte_system.check_key(event.key)
                    continue
                
                if game_state == 'intro':
                    if event.key == pygame.K_w:
                        menu_selection = (menu_selection - 1) % 4
                    elif event.key == pygame.K_s:
                        menu_selection = (menu_selection + 1) % 4
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if menu_selection == 0:  # Story Mode
                            game_state = 'story_intro'
                            story_intro_stage = 0
                            chapter_frame = 0
                            score = 0
                            round_num = 1
                            ducks_hit = 0
                            ducks_spawned = 0
                            secret_mode = False
                            ambient_sound.stop()
                        elif menu_selection == 1:  # Arcade Mode
                            game_state = 'playing'
                            chapter = 0
                            time_of_day = 'day'
                            ducks = [Duck()]
                            ducks_spawned = 1
                            ducks_hit = 0
                            round_num = 1
                            score = 0
                            ammo = 3
                            secret_mode = False
                            dog.reset_round()
                            ambient_sound.stop()
                        elif menu_selection == 2:  # Secret Mode
                            game_state = 'secret_intro'
                            secret_intro_stage = 0
                            chapter_frame = 0
                            score = 0
                            round_num = 1
                            ducks_hit = 0
                            ducks_spawned = 0
                            secret_mode = True
                            particles = []
                            ambient_sound.play_tension()
                        elif menu_selection == 3:  # Controls
                            game_state = 'controls'
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                
                elif game_state == 'controls':
                    if event.key == pygame.K_ESCAPE:
                        game_state = 'intro'
                
                elif game_state == 'story_intro':
                    if event.key == pygame.K_SPACE and chapter_frame > 90:
                        story_intro_stage += 1
                        chapter_frame = 0
                        if story_intro_stage > 2:
                            game_state = 'chapter_intro'
                            chapter = 1
                            chapter_frame = 0
                
                elif game_state == 'secret_intro':
                    if event.key == pygame.K_SPACE and chapter_frame > 90:
                        secret_intro_stage += 1
                        chapter_frame = 0
                        if secret_intro_stage > 2:
                            game_state = 'boss_presentation'
                            boss_presentation_index = 0
                            chapter_frame = 0
                
                elif game_state == 'boss_presentation':
                    if event.key == pygame.K_SPACE and chapter_frame > 80:
                        boss_presentation_index += 1
                        chapter_frame = 0
                        if boss_presentation_index >= len(SECRET_BOSSES):
                            # Iniciar modo secreto
                            game_state = 'playing'
                            chapter = 0
                            time_of_day = 'hell'
                            round_num = 1
                            required_score = SECRET_MODE_REQUIREMENTS.get(round_num, 500)
                            ducks = [Duck(difficulty=2, is_boss=True)]
                            ducks_spawned = 1
                            ducks_hit = 0
                            ammo = 3
                            dog.reset_round()
                
                elif game_state == 'chapter_intro':
                    if event.key == pygame.K_SPACE and chapter_frame > 50:
                        game_state = 'playing'
                        times = {1: 'day', 2: 'sunset', 3: 'night', 4: 'night'}
                        time_of_day = times.get(chapter, 'day')
                        ducks = [Duck(difficulty=chapter)]
                        ducks_spawned = 1
                        ducks_hit = 0
                        ammo = 3
                        particles = []
                        floating_texts = []
                        dog.reset_round()
                
                elif game_state == 'playing':
                    # Combo detection
                    key_map = {pygame.K_w: 'W', pygame.K_a: 'A', pygame.K_s: 'S', pygame.K_d: 'D'}
                    if event.key in key_map:
                        combo_keys.append(key_map[event.key])
                        combo_timer = 90
                        
                        if len(combo_keys) > 6:
                            combo_keys = combo_keys[-6:]
                        
                        combo_str = ''.join(combo_keys)
                        combo_display = combo_str
                        
                        # Check combos
                        if combo_str.endswith('AWSD'):
                            if dog.activate_god_mode():  # Solo si no se ha usado esta ronda
                                combo_keys = []
                                combo_display = ""
                                floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 200, "MODO DIOS! (5s)", GOLD, 'medium'))
                                for _ in range(20):
                                    particles.append(Particle(dog.x + DOG_WIDTH // 2, dog.y, 'star'))
                            else:
                                floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 200, "YA USADO!", RED, 'medium'))
                                combo_keys = []
                                combo_display = ""
                        elif combo_str.endswith('DSA'):
                            active_powerups['extra_ammo'] = POWERUP_DURATION_STANDARD
                            ammo = 99
                            combo_keys = []
                            combo_display = ""
                            floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 200, "MUNICION INFINITA!", (255, 180, 50), 'medium'))
                        elif combo_str.endswith('WDS'):
                            active_powerups['slow_motion'] = POWERUP_DURATION_STANDARD
                            combo_keys = []
                            combo_display = ""
                            floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 200, "CAMARA LENTA!", (100, 150, 255), 'medium'))
                        elif combo_str.endswith('ADAD'):
                            active_powerups['double_points'] = POWERUP_DURATION_DOUBLE
                            combo_keys = []
                            combo_display = ""
                            floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 200, "PUNTOS x2!", (255, 100, 100), 'medium'))
                        
                        # COMBO SECRETO PARA DESBLOQUEAR MODO SECRETO: WSADWSAD (dos veces la secuencia WSAD)
                        if not secret_mode_unlocked and combo_str.endswith('WSADWSAD'):
                            secret_mode_unlocked = True
                            showing_unlock_animation = True
                            unlock_animation_frame = 0
                            combo_keys = []
                            combo_display = ""
                            ambient_sound.play('unlock')
                            for _ in range(30):
                                particles.append(Particle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 'star'))
                    
                    # Shoot
                    if event.key == pygame.K_SPACE and ammo > 0 and not showing_unlock_animation:
                        if active_powerups['extra_ammo'] <= 0:
                            ammo -= 1
                        ambient_sound.play('shoot')  # Sonido de disparo
                        
                        for _ in range(5):
                            particles.append(Particle(cursor_x, cursor_y, 'spark'))
                        
                        hit = False
                        for duck in ducks:
                            result = duck.check_hit(cursor_x, cursor_y)
                            if result == True:  # Kill
                                points = duck.points
                                if active_powerups['double_points'] > 0:
                                    points *= 2
                                score += points
                                ducks_hit += 1
                                hit = True
                                
                                for _ in range(12):
                                    particles.append(Particle(duck.x + DUCK_WIDTH // 2, duck.y + DUCK_HEIGHT // 2, 'feather'))
                                floating_texts.append(FloatingText(duck.x + DUCK_WIDTH // 2, duck.y, f"+{points}", GOLD))
                                dog.show_celebrate(duck.x, duck.color_variant)
                                ambient_sound.play('hit')  # Sonido de impacto
                                ambient_sound.play('bark')  # Perro ladra
                                break
                            elif result == 'damaged':  # Boss damaged
                                hit = True
                                ambient_sound.play('hit')  # Sonido de impacto
                                floating_texts.append(FloatingText(duck.x + DUCK_WIDTH // 2, duck.y, "HIT!", RED))
                                for _ in range(5):
                                    particles.append(Particle(duck.x + DUCK_WIDTH // 2, duck.y + DUCK_HEIGHT // 2, 'spark'))
                                break
                        
                        # Collect power-ups
                        magnet_active = active_powerups['magnet'] > 0
                        for powerup in powerups[:]:
                            ptype = powerup.check_collect(cursor_x, cursor_y, magnet_active)
                            if ptype:
                                if ptype == 'rapid_fire':
                                    active_powerups['rapid_fire'] = POWERUP_DURATION_STANDARD
                                    floating_texts.append(FloatingText(powerup.x, powerup.y, "DISPARO RAPIDO!", GOLD))
                                elif ptype == 'slow_motion':
                                    active_powerups['slow_motion'] = POWERUP_DURATION_STANDARD
                                    floating_texts.append(FloatingText(powerup.x, powerup.y, "CAMARA LENTA!", (100, 150, 255)))
                                elif ptype == 'extra_ammo':
                                    ammo = min(ammo + 5, 99)
                                    floating_texts.append(FloatingText(powerup.x, powerup.y, "+5 BALAS!", (255, 180, 50)))
                                elif ptype == 'double_points':
                                    active_powerups['double_points'] = POWERUP_DURATION_DOUBLE
                                    floating_texts.append(FloatingText(powerup.x, powerup.y, "x2 PUNTOS!", (255, 100, 100)))
                                elif ptype == 'shield':
                                    active_powerups['shield'] = POWERUP_DURATION_STANDARD
                                    floating_texts.append(FloatingText(powerup.x, powerup.y, "ESCUDO!", (100, 200, 255)))
                                elif ptype == 'magnet':
                                    active_powerups['magnet'] = POWERUP_DURATION_STANDARD
                                    floating_texts.append(FloatingText(powerup.x, powerup.y, "IMAN!", PURPLE))
                                
                                for _ in range(8):
                                    particles.append(Particle(powerup.x, powerup.y, 'star'))
                                powerups.remove(powerup)
                        
                        if not hit and ammo == 0:
                            dog.show_laugh()
                    
                    # Reload
                    if event.key == pygame.K_r:
                        if active_powerups['extra_ammo'] <= 0:
                            ammo = 3
                        else:
                            ammo = 99
                    
                    # Pause/Menu
                    if event.key == pygame.K_ESCAPE:
                        if score > high_score:
                            high_score = score
                        game_state = 'intro'
                        ambient_sound.play_menu()
                
                elif game_state == 'round_end':
                    if event.key == pygame.K_SPACE:
                        round_num += 1
                        dog.reset_round()
                        
                        if secret_mode:
                            required_score = SECRET_MODE_REQUIREMENTS.get(round_num, required_score + 500)
                            if round_num > 5:
                                game_state = 'victory'
                            else:
                                ducks_hit = 0
                                ducks_spawned = 1
                                ammo = 3
                                ducks = [Duck(difficulty=round_num + 1, is_boss=(round_num % 2 == 0))]
                                game_state = 'playing'
                        elif round_num > 3 and chapter > 0:
                            chapter += 1
                            if chapter > 4:
                                game_state = 'victory'
                            else:
                                game_state = 'chapter_intro'
                                chapter_frame = 0
                                round_num = 1
                        else:
                            ducks_hit = 0
                            ducks_spawned = 1
                            ammo = 3
                            difficulty = chapter if chapter > 0 else 1 + round_num * 0.2
                            ducks = [Duck(difficulty=difficulty)]
                            game_state = 'playing'
                
                elif game_state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        if score > high_score:
                            high_score = score
                        game_state = 'intro'
                        ambient_sound.play_menu()
                
                elif game_state == 'victory':
                    if event.key == pygame.K_SPACE:
                        if score > high_score:
                            high_score = score
                        game_state = 'intro'
                        ambient_sound.play_menu()
        
        # Update logic
        if game_state == 'intro':
            intro_frame += 1
        
        elif game_state == 'controls':
            intro_frame += 1
        
        elif game_state == 'story_intro':
            chapter_frame += 1
        
        elif game_state == 'secret_intro':
            chapter_frame += 1
        
        elif game_state == 'boss_presentation':
            chapter_frame += 1
        
        elif game_state == 'chapter_intro':
            chapter_frame += 1
        
        elif game_state == 'playing':
            game_frame += 1
            
            # Combo timer
            if combo_timer > 0:
                combo_timer -= 1
            else:
                combo_keys = []
                combo_display = ""
            
            # Update power-ups timers
            slow_motion = active_powerups['slow_motion'] > 0
            for key in active_powerups:
                if active_powerups[key] > 0:
                    active_powerups[key] -= 1
            
            # QTE system for secret mode
            if secret_mode and not qte_system.active:
                # 2% de probabilidad de iniciar QTE cada frame
                if random.random() < 0.002:
                    qte_system.start_qte(round_num)
            
            # Update QTE
            qte_result = qte_system.update()
            if qte_result is not None:
                score = max(0, score + qte_result)
                if qte_result > 0:
                    floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 250, f"+{qte_result} BONUS!", GREEN))
                else:
                    floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 250, f"{qte_result} PENALIZACION!", RED))
            
            # Spawn power-ups
            if random.random() < 0.003 and len(powerups) < 3:
                powerups.append(PowerUp())
            
            # Update power-ups
            powerups = [p for p in powerups if p.update()]
            
            # Update clouds
            for cloud in clouds:
                cloud.update(slow_motion)
            
            # Update particles
            particles = [p for p in particles if p.update()]
            
            # Update floating texts
            floating_texts = [t for t in floating_texts if t.update()]
            
            # Update ducks
            for duck in ducks[:]:
                if not duck.update(slow_motion):
                    ducks.remove(duck)
            
            # Dog god mode
            god_points = dog.update(ducks)
            if god_points > 0:
                if active_powerups['double_points'] > 0:
                    god_points *= 2
                score += god_points
                ducks_hit += 1
                floating_texts.append(FloatingText(dog.x + DOG_WIDTH // 2, dog.y - 20, f"+{god_points}", GOLD))
            
            # Check round status
            alive_ducks = [d for d in ducks if d.alive and not d.falling]
            falling_ducks = [d for d in ducks if d.falling]
            
            if len(alive_ducks) == 0 and len(falling_ducks) == 0:
                if ducks_spawned >= ducks_per_round:
                    # Verificar requisitos de modo secreto
                    if secret_mode:
                        if score >= required_score:
                            game_state = 'round_end'
                        else:
                            game_state = 'game_over'
                            dog.show_laugh()
                            floating_texts.append(FloatingText(SCREEN_WIDTH // 2, 200, f"NECESITABAS {required_score} PTS!", RED))
                    else:
                        required = 3 if chapter == 0 else 2 + chapter
                        if ducks_hit >= required:
                            game_state = 'round_end'
                        else:
                            game_state = 'game_over'
                            dog.show_laugh()
                elif ducks_spawned < ducks_per_round:
                    difficulty = chapter if chapter > 0 else 1 + round_num * 0.2
                    if secret_mode:
                        difficulty = round_num + 1
                        is_boss = (ducks_spawned + 1) == ducks_per_round  # Ultimo es boss
                        ducks.append(Duck(difficulty=difficulty, is_boss=is_boss))
                    else:
                        ducks.append(Duck(difficulty=difficulty))
                    ducks_spawned += 1
                    if active_powerups['extra_ammo'] <= 0:
                        ammo = 3
        
        else:
            dog.update()
        
        # Drawing
        if game_state == 'intro':
            draw_intro_screen(screen, intro_frame, menu_selection)
        
        elif game_state == 'controls':
            draw_controls_screen(screen, intro_frame)
        
        elif game_state == 'story_intro':
            draw_story_intro(screen, chapter_frame, story_intro_stage)
        
        elif game_state == 'secret_intro':
            draw_secret_mode_intro(screen, chapter_frame, secret_intro_stage, particles)
        
        elif game_state == 'boss_presentation':
            draw_boss_presentation(screen, chapter_frame, boss_presentation_index, particles)
        
        elif game_state == 'chapter_intro':
            draw_chapter_intro(screen, chapter, chapter_frame)
        
        elif game_state in ['playing', 'round_end', 'game_over']:
            draw_background(screen, clouds, time_of_day, stars if time_of_day == 'night' else None, game_frame)
            
            for powerup in powerups:
                powerup.draw(screen)
            
            for duck in ducks:
                duck.draw(screen)
            
            for particle in particles:
                particle.draw(screen)
            
            dog.draw(screen)
            
            for text in floating_texts:
                text.draw(screen)
            
            draw_hud(screen, score, ammo, ducks_hit, ducks_per_round, round_num, chapter, active_powerups, combo_display, high_score, secret_mode, required_score)
            draw_crosshair(screen, cursor_x, cursor_y, active_powerups['rapid_fire'] > 0, active_powerups['magnet'] > 0)
            
            # QTE overlay
            if qte_system.active or qte_system.display_timer < 60:
                qte_system.draw(screen)
            
            # ANIMACION DE DESBLOQUEO MODO SECRETO
            if showing_unlock_animation:
                unlock_animation_frame += 1
                
                # Overlay oscuro
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, min(200, unlock_animation_frame * 3)))
                screen.blit(overlay, (0, 0))
                
                # Rayo desde arriba
                if unlock_animation_frame > 30 and unlock_animation_frame < 90:
                    ambient_sound.play('thunder')
                    lightning_x = SCREEN_WIDTH // 2
                    points = [(lightning_x, 0)]
                    y = 0
                    while y < SCREEN_HEIGHT // 2:
                        y += 25
                        x_offset = random.randint(-40, 40)
                        points.append((lightning_x + x_offset, y))
                        lightning_x += x_offset // 2
                    
                    # Glow
                    for p in points:
                        pygame.draw.circle(screen, (255, 255, 200), p, 20)
                    if len(points) > 1:
                        pygame.draw.lines(screen, WHITE, False, points, 6)
                        pygame.draw.lines(screen, (200, 200, 255), False, points, 3)
                    
                    # Flash
                    if unlock_animation_frame % 5 < 2:
                        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                        flash.fill((255, 255, 255, 100))
                        screen.blit(flash, (0, 0))
                
                # Texto de descubrimiento
                if unlock_animation_frame > 100:
                    alpha = min(255, (unlock_animation_frame - 100) * 5)
                    
                    text1 = font_large.render("HAS DESCUBIERTO", True, (255, 100, 50))
                    text1.set_alpha(alpha)
                    screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, 180))
                    
                    text2 = font_title.render("LO DESCONOCIDO", True, (255, 200, 100))
                    text2.set_alpha(alpha)
                    screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 240))
                
                if unlock_animation_frame > 180:
                    alpha2 = min(255, (unlock_animation_frame - 180) * 5)
                    
                    text3 = font_large.render("FELICIDADES!", True, GOLD)
                    text3.set_alpha(alpha2)
                    screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, 350))
                    
                    text4 = font_medium.render("MODO SECRETO DESBLOQUEADO", True, (255, 150, 100))
                    text4.set_alpha(alpha2)
                    screen.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, 410))
                
                # Opciones
                if unlock_animation_frame > 280:
                    pulse = int(128 + 127 * math.sin(unlock_animation_frame * 0.1))
                    
                    text5 = font_small.render("ESPACIO = Ir al Modo Secreto | ESC = Continuar jugando", True, (pulse, pulse, pulse))
                    screen.blit(text5, (SCREEN_WIDTH // 2 - text5.get_width() // 2, SCREEN_HEIGHT - 80))
                
                # Particulas de estrella
                if unlock_animation_frame % 3 == 0:
                    particles.append(Particle(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 200), 'star'))
                
                # Manejo de input para la animacion
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and unlock_animation_frame > 280:
                        if event.key == pygame.K_SPACE:
                            # Ir directo al modo secreto
                            showing_unlock_animation = False
                            game_state = 'secret_intro'
                            secret_intro_stage = 0
                            chapter_frame = 0
                            score = 0
                            round_num = 1
                            ducks_hit = 0
                            ducks_spawned = 0
                            secret_mode = True
                            particles = []
                            ambient_sound.play_tension()
                        elif event.key == pygame.K_ESCAPE:
                            # Continuar jugando normal
                            showing_unlock_animation = False
            
            if game_state == 'round_end':
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                screen.blit(overlay, (0, 0))
                
                panel_w, panel_h = 450, 220
                panel_x = SCREEN_WIDTH // 2 - panel_w // 2
                panel_y = SCREEN_HEIGHT // 2 - panel_h // 2
                
                pygame.draw.rect(screen, (30, 50, 30), (panel_x, panel_y, panel_w, panel_h), border_radius=15)
                pygame.draw.rect(screen, (100, 200, 100), (panel_x, panel_y, panel_w, panel_h), 4, border_radius=15)
                
                text = font_large.render(f"RONDA {round_num} COMPLETADA!", True, GREEN)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, panel_y + 30))
                
                text2 = font_medium.render(f"Patos cazados: {ducks_hit}/{ducks_per_round}", True, WHITE)
                screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, panel_y + 90))
                
                text3 = font_medium.render(f"Puntuacion: {score:,}", True, GOLD)
                screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, panel_y + 130))
                
                text4 = font_small.render("Presiona ESPACIO para continuar", True, (180, 180, 180))
                screen.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, panel_y + 175))
            
            elif game_state == 'game_over':
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                panel_w, panel_h = 450, 280
                panel_x = SCREEN_WIDTH // 2 - panel_w // 2
                panel_y = SCREEN_HEIGHT // 2 - panel_h // 2
                
                pygame.draw.rect(screen, (50, 30, 30), (panel_x, panel_y, panel_w, panel_h), border_radius=15)
                pygame.draw.rect(screen, (200, 100, 100), (panel_x, panel_y, panel_w, panel_h), 4, border_radius=15)
                
                text = font_large.render("GAME OVER", True, RED)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, panel_y + 30))
                
                text2 = font_medium.render(f"Puntuacion Final: {score:,}", True, WHITE)
                screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, panel_y + 100))
                
                if secret_mode:
                    req_text = font_small.render(f"Requerias: {required_score} puntos", True, (255, 150, 150))
                    screen.blit(req_text, (SCREEN_WIDTH // 2 - req_text.get_width() // 2, panel_y + 140))
                
                if score > high_score:
                    new_record = font_medium.render("NUEVO RECORD!", True, GOLD)
                    screen.blit(new_record, (SCREEN_WIDTH // 2 - new_record.get_width() // 2, panel_y + 175))
                else:
                    hi_text = font_small.render(f"Record: {high_score:,}", True, (150, 150, 150))
                    screen.blit(hi_text, (SCREEN_WIDTH // 2 - hi_text.get_width() // 2, panel_y + 180))
                
                text3 = font_small.render("Presiona ESPACIO para volver al menu", True, (180, 180, 180))
                screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, panel_y + 230))
        
        elif game_state == 'victory':
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                r = int(20 + ratio * 30 + math.sin(game_frame * 0.05 + y * 0.01) * 10)
                g = int(40 + ratio * 40 + math.sin(game_frame * 0.05 + y * 0.01) * 10)
                b = int(30 + ratio * 35)
                screen.fill((r, g, b), (0, y, SCREEN_WIDTH, 1))
            
            game_frame += 1
            
            if game_frame % 5 == 0:
                particles.append(Particle(random.randint(0, SCREEN_WIDTH), -10, 'star'))
            
            particles = [p for p in particles if p.update()]
            for p in particles:
                p.draw(screen)
            
            title_y = 150 + int(math.sin(game_frame * 0.05) * 10)
            
            text = font_title.render("FELICIDADES!", True, GOLD)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, title_y))
            
            if secret_mode:
                text2 = font_large.render("Has conquistado el infierno!", True, (255, 150, 100))
            else:
                text2 = font_large.render("Has completado todos los capitulos!", True, WHITE)
            screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, title_y + 90))
            
            text3 = font_large.render(f"Puntuacion Final: {score:,}", True, GOLD)
            screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, title_y + 160))
            
            if score > high_score:
                record_text = font_medium.render("NUEVO RECORD MUNDIAL!", True, (255, 100, 100))
                screen.blit(record_text, (SCREEN_WIDTH // 2 - record_text.get_width() // 2, title_y + 220))
            
            text4 = font_small.render("Presiona ESPACIO para volver al menu", True, (180, 180, 180))
            screen.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, SCREEN_HEIGHT - 80))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    ambient_sound.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
