import pygame
import sys
import random
import json  # Added
import subprocess  # Added

# Game settings
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Color definitions
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (40, 40, 40)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def random_food():
    return (random.randint(0, COLS - 1) * CELL_SIZE, random.randint(0, ROWS - 1) * CELL_SIZE)

def main():
    snake = [(COLS // 2 * CELL_SIZE, ROWS // 2 * CELL_SIZE)]
    direction = (CELL_SIZE, 0)  # Initial direction: moving right
    food = random_food()
    score = 0
    running = True
    # List for recording state logs
    state_log = []  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # End loop; log will be saved afterward
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check collision with walls
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            running = False

        # Check collision with self
        if new_head in snake:
            running = False

        snake.insert(0, new_head)

        # Check food consumption
        if new_head == food:
            score += 1
            food = random_food()
        else:
            snake.pop()

        # Record state each frame (e.g. head position, snake length, current direction, score)
        state_log.append({
            "head": new_head,
            "length": len(snake),
            "direction": direction,
            "score": score
        })

        # Update display
        screen.fill(BLACK)
        draw_grid()
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
        for pos in snake:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        if len(snake) > 1:
            dx = snake[0][0] - snake[1][0]
            dz = snake[0][1] - snake[1][1]
        else:
            dx, dz = direction
        length_text = font.render(f"Length: {len(snake)}", True, (255, 255, 255))
        dx_dz_text = font.render(f"dx: {dx}, dz: {dz}", True, (255, 255, 255))
        screen.blit(length_text, (10, 40))
        screen.blit(dx_dz_text, (10, 70))
        
        pygame.display.update()
        clock.tick(10)

    # After game over, save state log as a JSON file
    with open("snake_state_log.json", "w") as f:
        json.dump(state_log, f, indent=2)

    # After game over, run the SP1 proof generation command
    result = subprocess.run(
        ["cargo", "prove", "prove"],
        cwd="c:/Users/User/Desktop/SP1/my_project/program",
        capture_output=True,
        text=True
    )
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    # Game over screen
    game_over_text = font.render("Game Over! Press any key to exit.", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
