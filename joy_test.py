import pygame
import sys

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick found")
    sys.exit()

joy = pygame.joystick.Joystick(0)
joy.init()
print(f"Testing: {joy.get_name()}")
print("Move joystick or press buttons...")

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")
        elif event.type == pygame.JOYAXISMOTION:
            if abs(event.value) > 0.1:
                print(f"Axis {event.axis}: {event.value:.2f}")
        elif event.type == pygame.JOYHATMOTION:
            print(f"Hat: {event.value}")
    
    pygame.event.pump()
    
    # Check all axes directly
    for i in range(joy.get_numaxes()):
        val = joy.get_axis(i)
        if abs(val) > 0.1:
            print(f"Direct axis {i}: {val:.2f}")
    
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(10)
