import numpy as np
import pygame
import time

# Define constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connected Components in Conway's Game of Life")

# Create the initial grid with a glider
grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=bool)
glider = np.array([[0, 1, 0],
                   [0, 0, 1],
                   [1, 1, 1]], dtype=bool)
grid[1:4, 1:4] = glider

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Variable to track drawing mode (True for drawing, False for erasing)
drawing = False

# Function to update the grid
def update_grid():
    global grid
    new_grid = np.copy(grid)
    for x in range(1, GRID_WIDTH - 1):
        for y in range(1, GRID_HEIGHT - 1):
            # Count live neighbors
            neighbors = np.sum(grid[x - 1 : x + 2, y - 1 : y + 2]) - grid[x, y]
            if grid[x, y]:
                # Any live cell with fewer than two live neighbors dies
                # Any live cell with more than three live neighbors dies
                if neighbors < 2 or neighbors > 3:
                    new_grid[x, y] = False
            else:
                # Any dead cell with exactly three live neighbors becomes a live cell
                if neighbors == 3:
                    new_grid[x, y] = True
    grid = new_grid

# Function to perform DFS and label connected components
def label_connected_components(x, y, component_label):
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[x, y] and labels[x, y] == -1:
        labels[x, y] = component_label
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    label_connected_components(x + dx, y + dy, component_label)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button (draw)
                drawing = True
            elif event.button == 3:  # Right mouse button (erase)
                drawing = False
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    screen.fill(BLACK)

    # Handle drawing cells
    if drawing:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            grid[grid_x, grid_y] = True

    # Initialize labels for connected components
    labels = np.full((GRID_WIDTH, GRID_HEIGHT), -1, dtype=int)
    component_label = 0

    # Traverse the grid and label connected components
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y] and labels[x, y] == -1:
                label_connected_components(x, y, component_label)
                component_label += 1

    # Assign colors to connected components
    colors = [pygame.Color(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)) for _ in range(component_label)]

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y]:
                pygame.draw.rect(screen, colors[labels[x, y]], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    update_grid()
    pygame.display.flip()
    clock.tick(FPS)
    time.sleep(0.01)

pygame.quit()
