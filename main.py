import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Game settings
enemy_spawn_rate = 60  # Adjust this value to control spawn frequency

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 10
player_speed = 4  # Further increased speed

# Enemy settings
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
enemy_speed = 2  # Further increased speed
enemies = []

# Bullet settings
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
bullet_speed = 5
bullets = []

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT))

    def move(self):
        self.y += enemy_speed

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(window, (255, 255, 0), (self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT))

    def move(self):
        self.y -= bullet_speed

def spawn_enemies():
    if len(enemies) < 5:  # Adjust the number of enemies as needed
        if pygame.time.get_ticks() % enemy_spawn_rate == 0:
            x = random.randint(0, WIDTH - ENEMY_WIDTH)
            enemies.append(Enemy(x, 0))

def draw_player():
    pygame.draw.rect(window, (0, 255, 0), (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

def check_collision(bullet, enemy):
    return (bullet.x < enemy.x + ENEMY_WIDTH and
            bullet.x + BULLET_WIDTH > enemy.x and
            bullet.y < enemy.y + ENEMY_HEIGHT and
            bullet.y + BULLET_HEIGHT > enemy.y)

def check_player_collision(enemy):
    return (player_x < enemy.x + ENEMY_WIDTH and
            player_x + PLAYER_WIDTH > enemy.x and
            player_y < enemy.y + ENEMY_HEIGHT and
            player_y + PLAYER_HEIGHT > enemy.y)

def main():
    global player_x
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player_x + PLAYER_WIDTH // 2, player_y))

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_speed > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed < WIDTH - PLAYER_WIDTH:
            player_x += player_speed

        # Spawn enemies
        spawn_enemies()

        # Move bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy.move()
            if enemy.y > HEIGHT:
                enemies.remove(enemy)

        # Check for collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if check_collision(bullet, enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Check for player collision with enemies
        for enemy in enemies:
            if check_player_collision(enemy):
                running = False  # End the game if an enemy touches the player

        # Fill the screen with a color (e.g., black)
        window.fill((0, 0, 0))

        # Draw the player
        draw_player()

        # Draw bullets
        for bullet in bullets:
            bullet.draw()

        # Draw enemies
        for enemy in enemies:
            enemy.draw()

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)  # Maintain the frame rate at 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()