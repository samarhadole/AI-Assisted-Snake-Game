import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Arrow Key Game!")
clock = pygame.time.Clock()

# Player
player_x = 300
player_y = 200
player_size = 30

# Star
star_x = random.randint(50, 550)
star_y = random.randint(50, 350)
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Arrow key controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < 570:
        player_x += 5
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= 5
    if keys[pygame.K_DOWN] and player_y < 370:
        player_y += 5
    
    # Check if player touches star
    if abs(player_x - star_x) < 30 and abs(player_y - star_y) < 30:
        score += 1
        star_x = random.randint(50, 550)
        star_y = random.randint(50, 350)
    
    # Draw everything
    screen.fill((0, 50, 100))  # Dark blue background
    pygame.draw.rect(screen, (255, 255, 0), (player_x, player_y, player_size, player_size))  # Yellow player
    pygame.draw.circle(screen, (255, 255, 255), (star_x, star_y), 15)  # White star
    
    # Show score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Stars: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
