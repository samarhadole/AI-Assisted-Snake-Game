import pygame
import sys

pygame.init()
pygame.joystick.init()

# Check for joysticks
joystick_count = pygame.joystick.get_count()
print(f"Number of joysticks connected: {joystick_count}")

if joystick_count == 0:
    print("No joystick found! Please connect your joystick and try again.")
    sys.exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of hats: {joystick.get_numhats()}")
print("\nPress buttons and move joystick. Press Ctrl+C to exit.\n")

# Simple test window
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Joystick Test")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Joystick button events
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")
        elif event.type == pygame.JOYBUTTONUP:
            print(f"Button {event.button} released")
        
        # Joystick axis events
        elif event.type == pygame.JOYAXISMOTION:
            print(f"Axis {event.axis} moved to {event.value:.2f}")
        
        # Joystick hat events (D-pad)
        elif event.type == pygame.JOYHATMOTION:
            print(f"Hat {event.hat} moved to {event.value}")
    
    # Clear screen
    screen.fill((0, 0, 0))
    
    # Display current joystick state
    font = pygame.font.Font(None, 24)
    y_pos = 20
    
    # Show axis values
    for i in range(joystick.get_numaxes()):
        axis_value = joystick.get_axis(i)
        text = font.render(f"Axis {i}: {axis_value:.2f}", True, (255, 255, 255))
        screen.blit(text, (10, y_pos))
        y_pos += 25
    
    # Show button states
    for i in range(joystick.get_numbuttons()):
        button_pressed = joystick.get_button(i)
        color = (0, 255, 0) if button_pressed else (255, 255, 255)
        text = font.render(f"Button {i}: {'ON' if button_pressed else 'OFF'}", True, color)
        screen.blit(text, (200, 20 + i * 25))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
