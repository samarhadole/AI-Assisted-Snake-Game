import pygame
import time

pygame.init()
pygame.joystick.init()

# Initialize joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Testing: {joystick.get_name()}")
print("Move joystick and press buttons. Press Ctrl+C to stop.\n")

try:
    while True:
        pygame.event.pump()  # Update joystick state
        
        # Check buttons
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                print(f"Button {i} pressed!")
        
        # Check axes (analog sticks)
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)
            if abs(axis_value) > 0.1:  # Only show significant movement
                print(f"Axis {i}: {axis_value:.2f}")
        
        # Check hats (D-pad)
        for i in range(joystick.get_numhats()):
            hat_value = joystick.get_hat(i)
            if hat_value != (0, 0):
                print(f"D-pad {i}: {hat_value}")
        
        time.sleep(0.1)  # Small delay

except KeyboardInterrupt:
    print("\nJoystick test stopped.")
    pygame.quit()
