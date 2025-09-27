"""
PERMANENT JOYSTICK HANDLER - DO NOT MODIFY THIS FILE!
This file contains bulletproof joystick code that should never be changed.
"""
import pygame

def get_joystick_movement(joystick, player_speed):
    """
    Returns the velocity for Mario based on joystick input.
    This function is BULLETPROOF and should never be modified.
    """
    if not joystick:
        return 0
    
    pygame.event.pump()
    
    # Try axis 0 first (most common)
    x_val = joystick.get_axis(0)
    if abs(x_val) > 0.3:
        return x_val * player_speed
    
    # Try D-pad if axis didn't work  
    if joystick.get_numhats() > 0:
        hat_x, hat_y = joystick.get_hat(0)
        if hat_x != 0:
            return hat_x * player_speed
    
    # Try shoulder buttons as last resort
    if joystick.get_button(4):  # Left shoulder
        return -player_speed
    elif joystick.get_button(5):  # Right shoulder
        return player_speed
    
    return 0

def get_joystick_jump(joystick):
    """
    Returns True if jump button is pressed.
    """
    if not joystick:
        return False
    
    return joystick.get_button(0) or joystick.get_button(1)

def get_joystick_shoot(joystick):
    """
    Returns True if shoot button is pressed.
    """
    if not joystick:
        return False
    
    return joystick.get_button(2) or joystick.get_button(3)
