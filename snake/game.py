import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 48)

# Globale Variablen für Spielzustand
snake = []
snake_dir = (CELL_SIZE, 0)
food = (0, 0)
game_over = False

def reset_game():
    global snake, snake_dir, food, game_over
    snake = [(100, 100)]
    snake_dir = (CELL_SIZE, 0)
    food = (
        random.randrange(0, WIDTH, CELL_SIZE),
        random.randrange(0, HEIGHT, CELL_SIZE)
    )
    game_over = False

def draw():
    screen.fill(WHITE)
    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
    
    if game_over:
        text = font.render("Game Over", True, BLACK)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, rect)

        restart_text = pygame.font.SysFont(None, 24).render("Press ENTER to restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

def move_snake():
    global food, game_over
    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    # Kollision mit Rand
    if (
        head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT
    ):
        game_over = True
        return

    # Kollision mit sich selbst
    if head in snake:
        game_over = True
        return

    snake.insert(0, head)

    if head == food:
        food = (
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE)
        )
    else:
        snake.pop()

# Spiel starten
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Wenn Game Over ist: Enter gedrückt?
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
            snake_dir = (0, -CELL_SIZE)
        elif keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
            snake_dir = (0, CELL_SIZE)
        elif keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
            snake_dir = (-CELL_SIZE, 0)
        elif keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
            snake_dir = (CELL_SIZE, 0)

        move_snake()

    draw()
    clock.tick(FPS)
