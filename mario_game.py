import pygame
import random
import numpy as np

# Import permanent joystick handler
from joystick_handler import get_joystick_movement, get_joystick_jump, get_joystick_shoot

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.joystick.init()

# Initialize joystick if available
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick connected: {joystick.get_name()}")
    print(f"Axes: {joystick.get_numaxes()}, Buttons: {joystick.get_numbuttons()}, Hats: {joystick.get_numhats()}")
else:
    print("No joystick detected")

def generate_tone(frequency, duration, sample_rate=22050, volume=0.3):
    """Generate a musical tone"""
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    for i in range(frames):
        wave = volume * np.sin(2 * np.pi * frequency * i / sample_rate)
        arr[i] = [wave, wave]
    
    return (arr * 32767).astype(np.int16)

def play_mario_theme():
    """Play the classic Mario theme melody - slower and longer"""
    # Mario theme notes
    notes = {
        'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77, 
        'C6': 1046.50, 'D6': 1174.66, 'E6': 1318.51, 'C5': 523.25, 'D5': 587.33, 
        'F5s': 739.99, 'A5s': 932.33, 'F6': 1396.91, 'G6': 1567.98, 'A6': 1760.00
    }
    
    # Mario theme melody (slower tempo)
    melody = [
        ('E6', 0.4), ('E6', 0.4), ('REST', 0.4), ('E6', 0.4),
        ('REST', 0.4), ('C6', 0.4), ('E6', 0.4), ('REST', 0.4),
        ('G6', 0.4), ('REST', 1.2), ('G5', 0.4), ('REST', 1.2),
        
        ('C6', 0.4), ('REST', 0.8), ('G5', 0.4), ('REST', 0.8),
        ('E5', 0.4), ('REST', 0.8), ('A5', 0.4), ('REST', 0.4),
        ('B5', 0.4), ('REST', 0.4), ('A5s', 0.4), ('A5', 0.4),
        
        ('G5', 0.6), ('E6', 0.6), ('G6', 0.6), ('A6', 0.4),
        ('REST', 0.4), ('F6', 0.4), ('G6', 0.4), ('REST', 0.4),
        ('E6', 0.4), ('REST', 0.4), ('C6', 0.4), ('D6', 0.4), ('B5', 0.4),
        
        # Repeat main melody for longer play
        ('C6', 0.4), ('REST', 0.8), ('G5', 0.4), ('REST', 0.8),
        ('E5', 0.4), ('REST', 0.8), ('A5', 0.4), ('REST', 0.4),
        ('B5', 0.4), ('REST', 0.4), ('A5s', 0.4), ('A5', 0.4),
        ('G5', 0.6), ('E6', 0.6), ('G6', 0.6), ('A6', 0.4),
        ('REST', 2.0)  # Long pause before loop
    ]
    
    # Generate and play the melody
    full_song = np.array([], dtype=np.int16).reshape(0, 2)
    
    for note, duration in melody:
        if note == 'REST':
            tone = np.zeros((int(duration * 22050), 2), dtype=np.int16)
        else:
            tone = generate_tone(notes[note], duration, volume=0.15)  # Lower volume
        
        full_song = np.vstack([full_song, tone])
    
    # Play the generated music
    sound = pygame.sndarray.make_sound(full_song)
    sound.play(-1)  # Loop indefinitely
    return sound

def generate_jump_sound():
    """Generate Mario jump sound effect"""
    duration = 0.1
    sample_rate = 22050
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    for i in range(frames):
        # Rising pitch for jump effect
        freq = 400 + (i / frames) * 200
        wave = 0.3 * np.sin(2 * np.pi * freq * i / sample_rate) * (1 - i / frames)
        arr[i] = [wave, wave]
    
    return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))

def generate_coin_sound():
    """Generate coin collection sound"""
    duration = 0.2
    sample_rate = 22050
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    for i in range(frames):
        # Two-tone coin sound
        freq1 = 1000 if i < frames // 2 else 1500
        wave = 0.3 * np.sin(2 * np.pi * freq1 * i / sample_rate) * (1 - i / frames)
        arr[i] = [wave, wave]
    
    return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))

def generate_death_sound():
    """Generate death sound"""
    duration = 1.0
    sample_rate = 22050
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    # Descending tone sequence
    frequencies = [330, 294, 262, 220, 196]
    segment_length = frames // len(frequencies)
    
    for i, freq in enumerate(frequencies):
        start = i * segment_length
        end = min(start + segment_length, frames)
        t = np.linspace(0, (end - start) / sample_rate, end - start)
        wave = np.sin(2 * np.pi * freq * t) * 0.3 * np.exp(-t * 2)
        arr[start:end, 0] = wave
        arr[start:end, 1] = wave
    
    return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))

def generate_victory_sound():
    """Generate victory sound"""
    duration = 1.5
    sample_rate = 22050
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    # Victory fanfare
    notes = [262, 330, 392, 523, 659]  # C, E, G, C, E
    segment_length = frames // len(notes)
    
    for i, freq in enumerate(notes):
        start = i * segment_length
        end = min(start + segment_length, frames)
        t = np.linspace(0, (end - start) / sample_rate, end - start)
        wave = np.sin(2 * np.pi * freq * t) * 0.4
        arr[start:end, 0] = wave
        arr[start:end, 1] = wave
    
    return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))

def generate_enemy_stomp_sound():
    """Generate enemy stomp sound"""
    duration = 0.15
    sample_rate = 22050
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    
    for i in range(frames):
        # Low thump sound
        freq = 150 - (i / frames) * 50
        wave = 0.4 * np.sin(2 * np.pi * freq * i / sample_rate) * (1 - i / frames)
        arr[i] = [wave, wave]
    
    return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))

# Generate sound effects
jump_sound = generate_jump_sound()
coin_sound = generate_coin_sound()
stomp_sound = generate_enemy_stomp_sound()
death_sound = generate_death_sound()
victory_sound = generate_victory_sound()

# Start playing Mario theme
mario_theme_sound = None

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)  # Sky blue
GREEN = (34, 139, 34)   # Ground green
RED = (255, 0, 0)       # Mario red
BROWN = (139, 69, 19)   # Platform brown
YELLOW = (255, 215, 0)  # Coin yellow
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario-like Platformer")
clock = pygame.time.Clock()

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.power_type = power_type  # 'mushroom' or 'fire_flower'
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
        self.vel_x = 2 if power_type == 'mushroom' else 0  # Mushrooms move
        self.direction = 1
    
    def update(self):
        if self.power_type == 'mushroom' and not self.collected:
            self.x += self.vel_x * self.direction
            # Bounce off screen edges
            if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
                self.direction *= -1
            self.rect.x = self.x
    
    def draw(self, screen, camera_x=0):
        if not self.collected:
            if self.power_type == 'mushroom':
                # Red mushroom with white spots
                rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
                pygame.draw.ellipse(screen, RED, rect)
                pygame.draw.circle(screen, WHITE, (self.x + 8 - camera_x, self.y + 8), 3)
                pygame.draw.circle(screen, WHITE, (self.x + 17 - camera_x, self.y + 12), 2)
                pygame.draw.circle(screen, WHITE, (self.x + 12 - camera_x, self.y + 18), 2)
            elif self.power_type == 'fire_flower':
                # Orange flower with petals
                pygame.draw.circle(screen, (255, 165, 0), (self.x + 12 - camera_x, self.y + 12), 12)  # Orange center
                # Petals
                for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                    petal_x = self.x + 12 + 8 * np.cos(np.radians(angle)) - camera_x
                    petal_y = self.y + 12 + 8 * np.sin(np.radians(angle))
                    pygame.draw.circle(screen, RED, (int(petal_x), int(petal_y)), 4)

class Fireball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.vel_x = 8 * direction
        self.vel_y = -3
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.active = True
    
    def update(self):
        if self.active:
            self.x += self.vel_x
            self.y += self.vel_y
            self.vel_y += 0.3  # Gravity
            
            # Bounce on ground
            if self.y + self.height >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
                self.vel_y = -3
            
            # Remove if off screen
            if self.x < 0 or self.x > SCREEN_WIDTH:
                self.active = False
            
            self.rect.x = self.x
            self.rect.y = self.y
    
    def draw(self, screen, camera_x=0):
        if self.active:
            pygame.draw.circle(screen, (255, 100, 0), (self.x + 4 - camera_x, self.y + 4), 4)
            pygame.draw.circle(screen, YELLOW, (self.x + 4 - camera_x, self.y + 4), 2)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30  # Small Mario height
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.score = 0
        self.power_state = 'small'  # 'small', 'super', 'fire'
        self.facing_right = True
    
    def power_up(self, power_type):
        if power_type == 'mushroom' and self.power_state == 'small':
            self.power_state = 'super'
            old_y = self.y + self.height  # Bottom position
            self.height = 50  # Taller Mario
            self.y = old_y - self.height  # Keep feet at same position
            self.score += 100
        elif power_type == 'fire_flower':
            if self.power_state == 'small':
                old_y = self.y + self.height
                self.height = 50
                self.y = old_y - self.height
            self.power_state = 'fire'
            self.score += 200
    
    def take_damage(self):
        if self.power_state == 'fire':
            self.power_state = 'super'
            # Height stays 50 for super
        elif self.power_state == 'super':
            self.power_state = 'small'
            old_y = self.y + self.height  # Bottom position
            self.height = 30  # Small Mario height
            self.y = old_y - self.height  # Keep feet at same position
        else:
            # Small Mario dies
            death_sound.play()
            global game_paused, pause_timer, enemies
            game_paused = True
            pause_timer = pygame.time.get_ticks()
            enemies.clear()  # Clear all enemies on death
            self.x = 50
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.vel_x = 0
            self.vel_y = 0
            self.score = max(0, self.score - 50)
    
    def shoot_fireball(self):
        if self.power_state == 'fire':
            direction = 1 if self.facing_right else -1
            return Fireball(self.x + self.width//2, self.y + self.height//2, direction)
        return None
    
    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Only reset on_ground if we're moving upward (jumping)
        if self.vel_y < 0:
            self.on_ground = False
        
        # Ground collision
        if self.y + self.height >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
    
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            jump_sound.play()  # Play jump sound
    
    def draw(self, screen, camera_x=0):
        # Draw Mario based on power state
        if self.power_state == 'small':
            # Small Mario - red
            pygame.draw.rect(screen, RED, (self.x - camera_x, self.y, self.width, self.height))
            pygame.draw.rect(screen, RED, (self.x - 5 - camera_x, self.y, self.width + 10, 10))  # Hat
        elif self.power_state == 'super':
            # Super Mario - red and brown (visible on blue background)
            shirt_height = 25  # Top half
            pants_height = 25  # Bottom half
            pygame.draw.rect(screen, RED, (self.x - camera_x, self.y, self.width, shirt_height))  # Red shirt
            pygame.draw.rect(screen, BROWN, (self.x - camera_x, self.y + shirt_height, self.width, pants_height))  # Brown overalls
            pygame.draw.rect(screen, RED, (self.x - 5 - camera_x, self.y - 5, self.width + 10, 10))  # Hat (higher)
        elif self.power_state == 'fire':
            # Fire Mario - white and red (full body visible)
            shirt_height = 25  # Top half
            pants_height = 25  # Bottom half
            pygame.draw.rect(screen, WHITE, (self.x - camera_x, self.y, self.width, shirt_height))  # White shirt
            pygame.draw.rect(screen, RED, (self.x - camera_x, self.y + shirt_height, self.width, pants_height))  # Red overalls
            pygame.draw.rect(screen, WHITE, (self.x - 5 - camera_x, self.y - 5, self.width + 10, 10))  # White hat (higher)

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen, camera_x=0):
        pygame.draw.rect(screen, BROWN, (self.x - camera_x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x - camera_x, self.y, self.width, self.height), 2)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
    
    def draw(self, screen, camera_x=0):
        if not self.collected:
            pygame.draw.circle(screen, YELLOW, (self.x + 10 - camera_x, self.y + 10), 10)
            pygame.draw.circle(screen, BLACK, (self.x + 10 - camera_x, self.y + 10), 10, 2)

class Flagpole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 200
        self.flag_y = y + 20  # Flag position on pole
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.touched = False
    
    def draw(self, screen, camera_x=0):
        # Draw pole
        pygame.draw.rect(screen, BLACK, (self.x - camera_x, self.y, self.width, self.height))
        # Draw flag
        flag_points = [
            (self.x + 10 - camera_x, self.flag_y),
            (self.x + 50 - camera_x, self.flag_y + 15),
            (self.x + 10 - camera_x, self.flag_y + 30)
        ]
        pygame.draw.polygon(screen, RED, flag_points)

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 80
        self.vel_x = -2
        self.direction = -1
        self.health = 3
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.attack_timer = 0
        self.fireballs = []
    
    def update(self):
        # Move back and forth
        self.x += self.vel_x * self.direction
        
        # Bounce off edges
        if self.x <= 500 or self.x + self.width >= 750:
            self.direction *= -1
        
        # Attack every 2 seconds
        self.attack_timer += 1
        if self.attack_timer >= 120:  # 2 seconds at 60 FPS
            self.shoot_fireball()
            self.attack_timer = 0
        
        # Update boss fireballs
        for fireball in self.fireballs[:]:
            fireball.update()
            if not fireball.active:
                self.fireballs.remove(fireball)
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def shoot_fireball(self):
        # Shoot fireball toward Mario
        fireball = Fireball(self.x + self.width//2, self.y + self.height//2, -1)
        self.fireballs.append(fireball)
    
    def take_damage(self):
        self.health -= 1
        return self.health <= 0  # Return True if boss is defeated
    
    def draw(self, screen, camera_x=0):
        # Draw boss (large enemy)
        pygame.draw.rect(screen, (100, 0, 0), (self.x - camera_x, self.y, self.width, self.height))  # Dark red
        pygame.draw.rect(screen, BLACK, (self.x - camera_x, self.y, self.width, self.height), 3)
        
        # Eyes
        pygame.draw.circle(screen, RED, (self.x + 15 - camera_x, self.y + 20), 8)
        pygame.draw.circle(screen, RED, (self.x + 45 - camera_x, self.y + 20), 8)
        pygame.draw.circle(screen, BLACK, (self.x + 15 - camera_x, self.y + 20), 4)
        pygame.draw.circle(screen, BLACK, (self.x + 45 - camera_x, self.y + 20), 4)
        
        # Health indicator
        for i in range(self.health):
            pygame.draw.circle(screen, RED, (self.x + 10 + i*15 - camera_x, self.y - 10), 5)
        
        # Draw boss fireballs
        for fireball in self.fireballs:
            fireball.draw(screen, camera_x)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = 2
        self.direction = 1
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self):
        self.x += self.speed * self.direction
        
        # Bounce off screen edges
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.direction *= -1
        
        self.rect.x = self.x
    
    def draw(self, screen, camera_x=0):
        pygame.draw.rect(screen, BLACK, (self.x - camera_x, self.y, self.width, self.height))
        # Eyes
        pygame.draw.circle(screen, WHITE, (self.x + 8 - camera_x, self.y + 8), 3)
        pygame.draw.circle(screen, WHITE, (self.x + 17 - camera_x, self.y + 8), 3)

# Game variables
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
running = True
current_world = 1
current_level = 1
level_complete = False
level_timer = 0
joystick_x = 0  # Track joystick movement state
camera_x = 0  # Camera position
drop_through = False  # Drop through platforms flag
game_paused = False  # Game pause state
pause_timer = 0  # Pause duration timer

def create_level(world, level):
    """Create platforms, coins, enemies, powerups, boss, and flagpole for specific world-level"""
    platforms = []
    coins = []
    enemies = []
    powerups = []
    boss = None
    flagpole = None
    
    if world == 1:  # World 1
        if level == 1:  # 1-1
            platforms = [
                Platform(200, 450, 100, 20),
                Platform(400, 350, 100, 20),
                Platform(600, 250, 100, 20),
            ]
            coins = [
                Coin(230, 420), Coin(430, 320), Coin(630, 220),
                Coin(300, 550), Coin(500, 550),
            ]
            enemies = [Enemy(300, SCREEN_HEIGHT - GROUND_HEIGHT - 25)]
            powerups = [PowerUp(250, 425, 'mushroom')]  # Mushroom on first platform
            flagpole = Flagpole(750, SCREEN_HEIGHT - GROUND_HEIGHT - 200)
            
        elif level == 2:  # 1-2
            platforms = [
                Platform(150, 500, 80, 20),
                Platform(300, 400, 120, 20),
                Platform(500, 300, 100, 20),
                Platform(650, 200, 80, 20),
            ]
            coins = [
                Coin(170, 470), Coin(330, 370), Coin(530, 270),
                Coin(670, 170), Coin(400, 550), Coin(100, 550),
            ]
            enemies = [
                Enemy(250, SCREEN_HEIGHT - GROUND_HEIGHT - 25),
                Enemy(450, SCREEN_HEIGHT - GROUND_HEIGHT - 25),
            ]
            powerups = [PowerUp(350, 375, 'fire_flower')]  # Fire flower on second platform
            flagpole = Flagpole(750, SCREEN_HEIGHT - GROUND_HEIGHT - 200)
            
        elif level == 3:  # 1-3
            platforms = [
                Platform(100, 450, 60, 20),
                Platform(250, 350, 80, 20),
                Platform(450, 250, 100, 20),
                Platform(600, 400, 80, 20),
                Platform(300, 500, 60, 20),
            ]
            coins = [
                Coin(120, 420), Coin(270, 320), Coin(480, 220),
                Coin(620, 370), Coin(320, 470), Coin(700, 550),
            ]
            enemies = [
                Enemy(200, SCREEN_HEIGHT - GROUND_HEIGHT - 25),
                Enemy(400, SCREEN_HEIGHT - GROUND_HEIGHT - 25),
                Enemy(600, SCREEN_HEIGHT - GROUND_HEIGHT - 25),
            ]
            powerups = [
                PowerUp(270, 325, 'mushroom'),  # Mushroom
                PowerUp(480, 225, 'fire_flower')  # Fire flower
            ]
            flagpole = Flagpole(750, SCREEN_HEIGHT - GROUND_HEIGHT - 200)
            
        elif level == 4:  # 1-4 (Boss level)
            platforms = [
                Platform(200, 400, 100, 20),
                Platform(400, 300, 100, 20),
                Platform(600, 200, 100, 20),
                Platform(350, 500, 150, 20),
            ]
            coins = [
                Coin(230, 370), Coin(430, 270), Coin(630, 170),
                Coin(400, 470), Coin(450, 470), Coin(500, 470),
            ]
            enemies = [
                Enemy(150, SCREEN_HEIGHT - GROUND_HEIGHT - 25),
                Enemy(300, SCREEN_HEIGHT - GROUND_HEIGHT - 25),
            ]
            powerups = [PowerUp(430, 275, 'fire_flower')]  # Fire flower for boss fight
            boss = Boss(600, SCREEN_HEIGHT - GROUND_HEIGHT - 80)  # Boss enemy
            flagpole = Flagpole(750, SCREEN_HEIGHT - GROUND_HEIGHT - 200)
    
    return platforms, coins, enemies, powerups, boss, flagpole

def check_level_complete(coins, flagpole):
    """Check if flagpole is touched to complete level"""
    return flagpole and flagpole.touched

def next_level():
    """Progress to next level or world"""
    global current_world, current_level, level_complete, level_timer
    
    if current_level < 4:
        current_level += 1
    else:
        current_world += 1
        current_level = 1
    
    level_complete = False
    level_timer = 0
    
    # Reset player position
    player.x = 50
    player.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40
    player.vel_x = 0
    player.vel_y = 0
    
    return create_level(current_world, current_level)

# Create initial level
platforms, coins, enemies, powerups, boss, flagpole = create_level(current_world, current_level)

# Create game objects
player = Player(50, SCREEN_HEIGHT - GROUND_HEIGHT - 40)
fireballs = []

# Game loop
mario_theme_sound = play_mario_theme()  # Start the Mario theme (now loops automatically)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                drop_through = True  # Drop through platforms
            elif event.key == pygame.K_x:  # X key to shoot fireball
                fireball = player.shoot_fireball()
                if fireball:
                    fireballs.append(fireball)
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                drop_through = False  # Stop dropping
        
        # Joystick button events
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 or event.button == 1:  # A or B button
                player.jump()
            elif event.button == 2 or event.button == 3:  # X or Y button to shoot fireball
                fireball = player.shoot_fireball()
                if fireball:
                    fireballs.append(fireball)
            # Try buttons for movement too
            elif event.button == 4:  # Left shoulder
                joystick_x = -1
            elif event.button == 5:  # Right shoulder  
                joystick_x = 1
        
        # Joystick hat (D-pad) events
        elif event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            joystick_x = hat_x  # -1, 0, or 1
        
        # Joystick axis motion events
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:  # X-axis
                if abs(event.value) > 0.3:
                    joystick_x = event.value
                else:
                    joystick_x = 0
    
    # Handle game pause (for death/victory)
    if game_paused:
        if pygame.time.get_ticks() - pause_timer > 2000:  # 2 second pause
            game_paused = False
        else:
            # Skip game updates during pause
            screen.fill((135, 206, 235))  # Light blue sky
            # Still draw everything but don't update
            pygame.draw.rect(screen, GREEN, (0 - camera_x, SCREEN_HEIGHT - GROUND_HEIGHT, 1200, GROUND_HEIGHT))
            for platform in platforms:
                platform.draw(screen, camera_x)
            for coin in coins:
                coin.draw(screen, camera_x)
            for powerup in powerups:
                powerup.draw(screen, camera_x)
            if flagpole:
                flagpole.draw(screen, camera_x)
            player.draw(screen, camera_x)
            
            # Draw UI
            score_text = font.render(f"Score: {player.score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            power_text = small_font.render(f"Power: {player.power_state.title()}", True, BLACK)
            screen.blit(power_text, (10, 50))
            level_text = small_font.render(f"World {current_world}-{current_level}", True, BLACK)
            screen.blit(level_text, (10, 70))
            
            pygame.display.flip()
            clock.tick(60)
            continue
    
    # Handle continuous movement
    player.vel_x = 0
    
    # Use permanent joystick handler (NEVER MODIFY THIS LINE!)
    joystick_vel = get_joystick_movement(joystick, PLAYER_SPEED)
    if joystick_vel != 0:
        player.vel_x = joystick_vel
    
    # Keyboard controls (can override joystick)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.vel_x = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.vel_x = PLAYER_SPEED
    
    # Update game objects
    for enemy in enemies:
        enemy.update()
    
    # Update boss
    if boss:
        boss.update()
    
    # Update power-ups
    for powerup in powerups:
        powerup.update()
    
    # Update fireballs
    for fireball in fireballs[:]:
        fireball.update()
        if not fireball.active:
            fireballs.remove(fireball)
    
    # Update player
    player.update()
    
    # Update camera to follow Mario
    target_camera_x = player.x - SCREEN_WIDTH // 3  # Mario at 1/3 of screen
    camera_x += (target_camera_x - camera_x) * 0.1  # Smooth camera movement
    
    # Keep camera within bounds
    camera_x = max(0, min(camera_x, 1200 - SCREEN_WIDTH))  # Assuming level width of 1200
    
    # Platform collisions (AFTER player update)
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    on_platform = False  # Track if Mario is on any platform
    
    for platform in platforms:
        # Check if Mario is standing on top of platform
        if (player.x + player.width > platform.x and player.x < platform.x + platform.width and
            player.y + player.height >= platform.y and player.y + player.height <= platform.y + 15 and
            player.vel_y >= 0 and not drop_through):
            player.y = platform.y - player.height
            player.vel_y = 0
            player.on_ground = True
            on_platform = True
    
    # If not on any platform and not on ground, Mario should fall
    if not on_platform and player.y + player.height < SCREEN_HEIGHT - GROUND_HEIGHT:
        if player.vel_y >= 0:  # Only reset if falling, not jumping
            player.on_ground = False
    
    # Check level completion
    if check_level_complete(coins, flagpole) and not level_complete:
        level_complete = True
        level_timer = pygame.time.get_ticks()
        player.score += 100  # Bonus for completing level
    
    # Auto-advance to next level after 2 seconds
    if level_complete and pygame.time.get_ticks() - level_timer > 2000:
        platforms, coins, enemies, powerups, boss, flagpole = next_level()
        fireballs.clear()  # Clear fireballs when changing levels
    
    # Flagpole collision
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    if flagpole and player_rect.colliderect(flagpole.rect) and not flagpole.touched:
        flagpole.touched = True
        level_complete = True
        level_timer = pygame.time.get_ticks()
        player.score += 200  # Bonus for reaching flagpole
        victory_sound.play()
        enemies.clear()  # Clear all enemies on level complete
        if boss:
            boss = None  # Remove boss
        game_paused = True  # Pause game briefly
        pause_timer = pygame.time.get_ticks()
    
    # Power-up collection
    for powerup in powerups:
        if not powerup.collected and player_rect.colliderect(powerup.rect):
            powerup.collected = True
            player.power_up(powerup.power_type)
            coin_sound.play()  # Use coin sound for power-ups
    
    # Coin collection
    for coin in coins:
        if not coin.collected and player_rect.colliderect(coin.rect):
            coin.collected = True
            player.score += 10
            coin_sound.play()  # Play coin sound
    for coin in coins:
        if not coin.collected and player_rect.colliderect(coin.rect):
            coin.collected = True
            player.score += 10
            coin_sound.play()  # Play coin sound
    
    # Enemy collision
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for enemy in enemies[:]:  # Use slice to avoid modifying list during iteration
        if player_rect.colliderect(enemy.rect):
            # Check if Mario is falling down and hits enemy from above
            if player.vel_y > 0 and player.y < enemy.y:
                # Mario jumped on enemy - kill enemy and bounce
                enemies.remove(enemy)
                player.vel_y = -8  # Small bounce
                player.score += 50  # Points for killing enemy
                stomp_sound.play()  # Play stomp sound
            else:
                # Side collision - take damage
                player.take_damage()
    
    # Boss collision
    if boss:
        if player_rect.colliderect(boss.rect):
            # Check if Mario is falling down and hits boss from above
            if player.vel_y > 0 and player.y < boss.y:
                # Mario jumped on boss - damage boss and bounce
                if boss.take_damage():
                    boss = None  # Boss defeated
                    player.score += 500  # Big bonus for defeating boss
                player.vel_y = -8  # Small bounce
                stomp_sound.play()
            else:
                # Side collision - take damage
                player.take_damage()
        
        # Boss fireball collision with Mario
        if boss:
            for fireball in boss.fireballs[:]:
                if fireball.active and fireball.rect.colliderect(player_rect):
                    player.take_damage()
                    fireball.active = False
    
    # Fireball-enemy collision
    for fireball in fireballs[:]:
        for enemy in enemies[:]:
            if fireball.active and fireball.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                fireball.active = False
                player.score += 50
                stomp_sound.play()
        
        # Fireball vs boss
        if boss and fireball.active and fireball.rect.colliderect(boss.rect):
            if boss.take_damage():
                boss = None  # Boss defeated
                player.score += 500
            fireball.active = False
            stomp_sound.play()
    
    # Draw everything
    screen.fill(BLUE)  # Sky
    
    # Draw ground
    pygame.draw.rect(screen, GREEN, (0 - camera_x, SCREEN_HEIGHT - GROUND_HEIGHT, 1200, GROUND_HEIGHT))
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen, camera_x)
    
    # Draw coins
    for coin in coins:
        coin.draw(screen, camera_x)
    
    # Draw power-ups
    for powerup in powerups:
        powerup.draw(screen, camera_x)
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen, camera_x)
    
    # Draw boss
    if boss:
        boss.draw(screen, camera_x)
    
    # Draw fireballs
    for fireball in fireballs:
        fireball.draw(screen, camera_x)
    
    # Draw flagpole
    if flagpole:
        flagpole.draw(screen, camera_x)
    
    # Draw player
    player.draw(screen, camera_x)
    
    # Draw UI
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Power state display
    power_text = small_font.render(f"Power: {player.power_state.title()}", True, BLACK)
    screen.blit(power_text, (10, 50))
    
    # World and level display
    level_text = font.render(f"World {current_world}-{current_level}", True, BLACK)
    screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
    
    # Level complete message
    if level_complete:
        complete_text = font.render("LEVEL COMPLETE!", True, GREEN)
        text_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(complete_text, text_rect)
        
        bonus_text = small_font.render("+100 Bonus Points!", True, GREEN)
        bonus_rect = bonus_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        screen.blit(bonus_text, bonus_rect)
    
    # Control instructions
    if joystick:
        controls_text = pygame.font.Font(None, 16).render("KB: Arrow/WASD+Space+X+ESC | Joy: Stick/D-pad+A/B+X", True, BLACK)
    else:
        controls_text = pygame.font.Font(None, 18).render("Arrow/WASD: Move, Space: Jump, X: Fireball, ESC: Quit", True, BLACK)
    screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
