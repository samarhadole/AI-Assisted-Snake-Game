import pygame
import random
import numpy as np
import os

# Create .temp directory if it doesn't exist
os.makedirs('.temp', exist_ok=True)

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.joystick.init()

# Initialize joystick if available
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick connected: {joystick.get_name()}")

screen = pygame.display.set_mode((800, 600))  # Wider screen for sidebar
pygame.display.set_caption("Snake Game!")
clock = pygame.time.Clock()

# Game area dimensions
GAME_WIDTH = 600
GAME_HEIGHT = 600
SIDEBAR_WIDTH = 200

# Create simple sound effects
def create_beep(frequency, duration):
    sample_rate = 22050
    frames = int(duration * sample_rate)
    arr = np.zeros((frames, 2))
    arr[:, 0] = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
    arr[:, 1] = arr[:, 0]
    arr = (arr * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(arr)

eat_sound = create_beep(800, 0.1)  # High beep for eating
game_over_sound = create_beep(200, 0.5)  # Low tone for game over
move_sound = create_beep(300, 0.05)  # Subtle movement sound
move_sound.set_volume(0.1)  # Lower volume for movement

# Load high score
try:
    with open('.temp/highscore.txt', 'r') as f:
        high_score = int(f.read())
except:
    high_score = 0

# Snake starts in the middle
snake = [[300, 300]]
direction = [20, 0]  # Moving right

# Food
food = [random.randint(0, 29) * 20, random.randint(0, 29) * 20]
score = 0
paused = False
food_blink = 0  # For food animation
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_over and event.key == pygame.K_r:
                # Restart game
                snake = [[300, 300]]
                direction = [20, 0]
                food = [random.randint(0, 29) * 20, random.randint(0, 29) * 20]
                score = 0
                game_over = False
                food_blink = 0
            elif event.key == pygame.K_SPACE and not game_over:
                paused = not paused
            elif not paused and not game_over:
                if event.key == pygame.K_UP and direction != [0, 20]:
                    direction = [0, -20]
                elif event.key == pygame.K_DOWN and direction != [0, -20]:
                    direction = [0, 20]
                elif event.key == pygame.K_LEFT and direction != [20, 0]:
                    direction = [-20, 0]
                elif event.key == pygame.K_RIGHT and direction != [-20, 0]:
                    direction = [20, 0]
        
        # Joystick button events
        elif event.type == pygame.JOYBUTTONDOWN and not game_over:
            if event.button == 0:  # Button 0 for pause (usually X or A button)
                paused = not paused
        
        # Joystick hat (D-pad) events
        elif event.type == pygame.JOYHATMOTION and not paused and not game_over:
            hat_x, hat_y = event.value
            if hat_y == 1 and direction != [0, 20]:  # Up
                direction = [0, -20]
            elif hat_y == -1 and direction != [0, -20]:  # Down
                direction = [0, 20]
            elif hat_x == -1 and direction != [20, 0]:  # Left
                direction = [-20, 0]
            elif hat_x == 1 and direction != [-20, 0]:  # Right
                direction = [20, 0]
    
    # Check joystick analog stick for movement (if joystick is connected)
    if joystick and not paused and not game_over:
        # Get left analog stick values (axes 0 and 1)
        x_axis = joystick.get_axis(0)  # Left/Right
        y_axis = joystick.get_axis(1)  # Up/Down
        
        # Only respond to significant movement (deadzone)
        if abs(x_axis) > 0.3 or abs(y_axis) > 0.3:  # Lower threshold for better response
            if abs(x_axis) > abs(y_axis):  # Horizontal movement is stronger
                if x_axis > 0.3 and direction != [-20, 0]:  # Right
                    direction = [20, 0]
                elif x_axis < -0.3 and direction != [20, 0]:  # Left
                    direction = [-20, 0]
            else:  # Vertical movement is stronger
                if y_axis > 0.3 and direction != [0, -20]:  # Down (joystick Y is inverted)
                    direction = [0, 20]
                elif y_axis < -0.3 and direction != [0, 20]:  # Up
                    direction = [0, -20]
    
    if not paused and not game_over:
        # Move snake
        head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        move_sound.play()  # Play movement sound
        
        # Check walls
        if head[0] < 0 or head[0] >= GAME_WIDTH or head[1] < 0 or head[1] >= GAME_HEIGHT:
            game_over_sound.play()
            game_over = True
        
        # Check if snake hits itself
        if head in snake:
            game_over_sound.play()
            game_over = True
        
        snake.insert(0, head)
        
        # Check if snake eats food
        if head == food:
            # Different pitch for each food eaten
            pitch = 800 + (score * 50)  # Higher pitch as score increases
            eat_sound = create_beep(pitch, 0.1)
            eat_sound.play()
            score += 1
            food = [random.randint(0, 29) * 20, random.randint(0, 29) * 20]
        else:
            snake.pop()  # Remove tail if no food eaten
    
    # Draw everything
    screen.fill((0, 0, 0))  # Black background
    
    # Draw grid lines
    for x in range(0, GAME_WIDTH, 20):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, GAME_HEIGHT))
    for y in range(0, GAME_HEIGHT, 20):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (GAME_WIDTH, y))
    
    # Draw game area border
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, GAME_WIDTH, GAME_HEIGHT), 2)
    
    # Draw snake
    for i, segment in enumerate(snake):
        if i == 0:  # Head
            pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], 20, 20))  # Bright green head
            pygame.draw.rect(screen, (255, 255, 255), (segment[0], segment[1], 20, 20), 2)  # White border
        else:  # Body
            pygame.draw.rect(screen, (0, 180, 0), (segment[0], segment[1], 20, 20))  # Darker green body
            pygame.draw.rect(screen, (0, 100, 0), (segment[0], segment[1], 20, 20), 1)  # Dark green border
    
    # Draw food (blinking)
    food_blink += 1
    if food_blink % 10 < 5:  # Blink every 10 frames
        pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], 20, 20))  # Red
    else:
        pygame.draw.rect(screen, (255, 100, 100), (food[0], food[1], 20, 20))  # Light red
    
    # Sidebar UI
    font = pygame.font.Font(None, 36)
    
    # Show score
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (GAME_WIDTH + 10, 50))
    
    # Show speed
    speed = 5 + score // 3
    speed_text = font.render(f"Speed: {speed}", True, (255, 255, 255))
    screen.blit(speed_text, (GAME_WIDTH + 10, 100))
    
    # Show high score
    high_text = font.render(f"High: {high_score}", True, (255, 215, 0))
    screen.blit(high_text, (GAME_WIDTH + 10, 150))
    
    # Instructions
    small_font = pygame.font.Font(None, 20)
    instructions = [
        "Controls:",
        "Arrow Keys - Move",
        "SPACE - Pause",
        "ESC - Quit"
    ]
    
    # Add joystick instructions if connected
    if joystick:
        instructions.extend([
            "",
            "Joystick:",
            "D-pad/Stick - Move",
            "Button 0 - Pause"
        ])
    
    for i, instruction in enumerate(instructions):
        if instruction == "":  # Skip empty lines
            continue
        color = (200, 200, 200) if instruction.endswith(":") else (150, 150, 150)
        inst_text = small_font.render(instruction, True, color)
        screen.blit(inst_text, (GAME_WIDTH + 10, 400 + i * 20))
    
    if paused:
        pause_text = font.render("PAUSED", True, (255, 255, 0))
        screen.blit(pause_text, (GAME_WIDTH + 10, 250))
        pause_help = pygame.font.Font(None, 24).render("Press SPACE", True, (255, 255, 0))
        screen.blit(pause_help, (GAME_WIDTH + 10, 280))
    
    if game_over:
        # Update high score
        if score > high_score:
            high_score = score
            with open('.temp/highscore.txt', 'w') as f:
                f.write(str(high_score))
        
        # Game over screen
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (200, 250))
        restart_text = pygame.font.Font(None, 24).render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (200, 300))
        quit_text = pygame.font.Font(None, 24).render("Press ESC to Quit", True, (255, 255, 255))
        screen.blit(quit_text, (200, 330))
    
    pygame.display.flip()
    clock.tick(5 + score // 3)  # Speed increases every 3 points

pygame.quit()
