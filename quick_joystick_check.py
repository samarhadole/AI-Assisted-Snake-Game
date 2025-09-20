import pygame

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick: {joystick.get_name()}")
print("Current state snapshot:")

pygame.event.pump()  # Update state

# Check current button states
pressed_buttons = []
for i in range(joystick.get_numbuttons()):
    if joystick.get_button(i):
        pressed_buttons.append(i)

if pressed_buttons:
    print(f"Buttons currently pressed: {pressed_buttons}")
else:
    print("No buttons currently pressed")

# Check axis positions
print("Axis positions:")
for i in range(joystick.get_numaxes()):
    value = joystick.get_axis(i)
    print(f"  Axis {i}: {value:.2f}")

# Check D-pad
print("D-pad positions:")
for i in range(joystick.get_numhats()):
    value = joystick.get_hat(i)
    print(f"  Hat {i}: {value}")

pygame.quit()
print("\nTry pressing buttons or moving sticks while running this test!")
