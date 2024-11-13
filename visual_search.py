import pygame
import random
import time
import sys
import csv

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BG_COLOR = (255, 255, 255)
PADDING = 10  # Padding between square cells

# Load images
blue_rectangle = pygame.image.load("blue_rectangle.png")
red_rectangle = pygame.image.load("red_rectangle.png")

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Human Visual Search Experiment")

def display_message(message, duration=3):
    """Display a message on the screen for a specified duration."""
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(BG_COLOR)
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(duration)

def create_grid(grid_size):
    """Create a random grid with one blue rectangle."""
    blue_position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    grid = [['red' for _ in range(grid_size)] for _ in range(grid_size)]
    grid[blue_position[0]][blue_position[1]] = 'blue'
    return grid, blue_position

def draw_grid(grid):
    """Draw the grid on the screen with rectangles centered in square cells."""
    screen.fill(BG_COLOR)
    grid_size = len(grid)

    # Calculate the square cell size to fit the entire grid on the screen with padding
    cell_size = (min(SCREEN_WIDTH, SCREEN_HEIGHT) - PADDING * (grid_size + 1)) // grid_size

    # Calculate offsets to center the grid
    x_offset = (SCREEN_WIDTH - (grid_size * cell_size + (grid_size + 1) * PADDING)) // 2
    y_offset = (SCREEN_HEIGHT - (grid_size * cell_size + (grid_size + 1) * PADDING)) // 2

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            # Calculate top-left position of each square cell
            x = j * (cell_size + PADDING) + x_offset + PADDING
            y = i * (cell_size + PADDING) + y_offset + PADDING

            # Scale rectangle to fit within square cell, leaving some margin
            rect_width = int(cell_size * 0.8)  # Adjust scaling as needed
            rect_height = int(cell_size * 0.5)  # Adjust scaling as needed
            rect = pygame.transform.scale(blue_rectangle if cell == 'blue' else red_rectangle, (rect_width, rect_height))

            # Center the rectangle within the square cell
            rect_x = x + (cell_size - rect_width) // 2
            rect_y = y + (cell_size - rect_height) // 2
            screen.blit(rect, (rect_x, rect_y))
    pygame.display.flip()
    return cell_size, x_offset, y_offset  # Return values for use in main function

def log_experiment(grid_size, reaction_time):
    """Log the grid size and reaction time to a CSV file."""
    with open("experiment_1.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([grid_size, reaction_time])

def main():
    running = True
    display_message("This app will explore aspects of human visual search by having the user perform various visual search tasks.", 3)
    display_message("In each task, you will be tasked with finding a specific feature among a number of items.", 3)

    # Create CSV header if the file is new
    with open("experiment_1.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Grid Size", "Reaction Time (seconds)"])

    display_message("Press the Blue box", 3)
    for test_round in range(3):  # Three test rounds
        grid_size = random.randint(3, 10)
        grid, blue_position = create_grid(grid_size)

        blue_clicked = False
        start_time = time.time()  # Record the start time

        # Draw the grid and get cell dimensions and offsets
        cell_size, x_offset, y_offset = draw_grid(grid)

        while not blue_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - x_offset - PADDING) // (cell_size + PADDING)
                    row = (mouse_y - y_offset - PADDING) // (cell_size + PADDING)

                    if 0 <= row < grid_size and 0 <= col < grid_size:
                        if grid[row][col] == 'blue':
                            blue_clicked = True
                            reaction_time = time.time() - start_time  # Calculate reaction time
                            log_experiment(grid_size, reaction_time)  # Log data
                            display_message("You clicked the Blue box!", 2)
            if not running:
                break

    display_message("Experiment Complete", 3)
    pygame.quit()

if __name__ == "__main__":
    main()
