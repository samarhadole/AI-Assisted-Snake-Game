import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick: {joystick.get_name()}")
    print(f"Axes: {joystick.get_numaxes()}")
    print(f"Buttons: {joystick.get_numbuttons()}")
    print(f"Hats: {joystick.get_numhats()}")
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        pygame.event.pump()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > 0.1:
                    print(f"Axis {event.axis}: {event.value:.2f}")
            elif event.type == pygame.JOYHATMOTION:
                print(f"Hat: {event.value}")
        
        # Check axis values directly
        x_axis = joystick.get_axis(0)
        if abs(x_axis) > 0.1:
            print(f"Direct axis 0: {x_axis:.2f}")
        
        clock.tick(60)
else:
    print("No joystick found")

pygame.quit()
