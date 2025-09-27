import pygame
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(f"Testing: {joy.get_name()}")
    
    for i in range(100):  # Test for 10 seconds
        pygame.event.pump()
        x = joy.get_axis(0)
        if abs(x) > 0.1:
            print(f"Axis 0: {x:.2f}")
        time.sleep(0.1)
else:
    print("No joystick")
