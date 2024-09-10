import pygame
import sys
import random
import time

# Sudoku board
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Store the initial state of the board
initial_board = [row[:] for row in board]

# Fill a random number of cells (3 filled cells per 3x3 box)
def fill_random_cells(board, num_cells):
    for _ in range(num_cells):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        while not is_number_allowed(board, row, col, num) or board[row][col] != 0 or count_cells_in_box(board, row, col) >= 3:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            num = random.randint(1, 9)
        board[row][col] = num
        initial_board[row][col] = num  # Update initial_board

# Check if a number can be placed in a certain cell
def is_number_allowed(board, row, col, num):
    # Row and column check
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Box check
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

# Count the number of filled cells in a 3x3 box
def count_cells_in_box(board, row, col):
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    count = 0
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] != 0:
                count += 1
    return count

# Check if a number violates the rules of Sudoku
def is_error(board, row, col, num):
    # Check row, column, and box
    return not is_number_allowed(board, row, col, num)

# Elimination method for error checking
def elimination_method(board, row, col):
    if initial_board[row][col] != 0:
        return []  # No tips for numbers in the initial state

    possible_numbers = 0b000000000

    # Check for possible numbers using elimination method
    for i in range(9):
        guess = i + 1
        valid_guess = True

        # Check row and column
        for j in range(9):
            if board[row][j] == guess or board[j][col] == guess:
                valid_guess = False
                break

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for j in range(box_row, box_row + 3):
            for k in range(box_col, box_col + 3):
                if board[j][k] == guess:
                    valid_guess = False
                    break

        if valid_guess:
            possible_numbers |= (1 << i)  # Turn on the corresponding bit for valid guesses

    return [i + 1 for i in range(9) if (possible_numbers >> i) & 1]

# Pygame initialization
pygame.init()

# Fill the board with random numbers
fill_random_cells(board, 27)

# Board dimensions and cell size
BOARD_SIZE = 9
CELL_SIZE = 50
LINE_WIDTH = 3  # Line thickness
EMPTY_AREA_HEIGHT = 200  # Height of the empty area below the board
HELP_BUTTON_SIZE = 60  # Size of the help button

# Screen size and title
screen_size = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE + EMPTY_AREA_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Sudoku Game")

# Font settings
font = pygame.font.Font(None, 36)

# Helper functions
def draw_board(selected_cell, error_cells, error_message, help_text):
    for i in range(BOARD_SIZE + 1):
        line_start = i * CELL_SIZE
        # Vertical lines
        pygame.draw.line(screen, (0, 0, 0), (line_start, 0), (line_start, BOARD_SIZE * CELL_SIZE), LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(screen, (0, 0, 0), (0, line_start), (BOARD_SIZE * CELL_SIZE, line_start), LINE_WIDTH)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            if initial_board[i][j] != 0:
                color = (0, 0, 255)  # Blue color for initial numbers
            else:
                color = (0, 0, 0)

            if board[i][j] != 0:
                if (i, j) in error_cells:
                    color = (255, 0, 0)  # Show cells with errors in red
                text = font.render(str(board[i][j]), True, color)
                screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 3, i * CELL_SIZE + CELL_SIZE // 4))

    if selected_cell:
        rect = pygame.Rect(selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), rect, 3)

    # Draw help button
    help_button_rect = pygame.Rect(BOARD_SIZE * CELL_SIZE // 2 - HELP_BUTTON_SIZE // 2, BOARD_SIZE * CELL_SIZE + 20, HELP_BUTTON_SIZE, HELP_BUTTON_SIZE)
    pygame.draw.rect(screen, (0, 255, 0), help_button_rect)
    help_button_text = font.render("Help", True, (0, 0, 0))
    screen.blit(help_button_text, (help_button_rect.centerx - help_button_text.get_width() // 2, help_button_rect.centery - help_button_text.get_height() // 2))

    # Display error message
    if error_message:
        error_message_surface = font.render(error_message, True, (255, 0, 0))
        error_message_rect = error_message_surface.get_rect(center=(screen.get_width() // 2, BOARD_SIZE * CELL_SIZE + 120))
        screen.blit(error_message_surface, error_message_rect)

    # Display help text
    if help_text:
        help_text_surface = font.render("Possible Numbers: " + ', '.join(map(str, help_text)), True, (0, 0, 0))
        help_text_rect = help_text_surface.get_rect(center=(screen.get_width() // 2, BOARD_SIZE * CELL_SIZE + 160))
        screen.blit(help_text_surface, help_text_rect)

# Game loop
running = True
selected_cell = None
error_cells = set()
error_message = ""
help_text = ""
help_timer_start = None
invalid_number_timer_start = None

# Define help button rect outside the event loop
help_button_rect = pygame.Rect(BOARD_SIZE * CELL_SIZE // 2 - HELP_BUTTON_SIZE // 2, BOARD_SIZE * CELL_SIZE + 20, HELP_BUTTON_SIZE, HELP_BUTTON_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            # Check if the click is within the Sudoku board bounds
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                selected_cell = (row, col)

            # Check if the click is on the help button
            elif help_button_rect.collidepoint(x, y):
                if selected_cell is not None:
                    help_text = elimination_method(board, *selected_cell)
                    help_timer_start = time.time()

        if event.type == pygame.KEYDOWN and selected_cell:
            if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                number = int(event.unicode)

                # Check if the cell is part of the initial state
                if initial_board[selected_cell[0]][selected_cell[1]] == 0:
                    if is_error(board, selected_cell[0], selected_cell[1], number):
                        error_cells.add(selected_cell)
                        error_message = "Error: Invalid number!"
                        invalid_number_timer_start = time.time()
                    elif selected_cell in error_cells:
                        error_cells.remove(selected_cell)
                        error_message = ""
                    else:
                        error_message = ""

                    board[selected_cell[0]][selected_cell[1]] = number

    # Check if the help text timer has expired
    if help_timer_start is not None and time.time() - help_timer_start > 1:
        help_text = ""

    # Check if the invalid number timer has expired
    if invalid_number_timer_start is not None and time.time() - invalid_number_timer_start > 1:
        error_message = ""

    screen.fill((255, 255, 255))
    draw_board(selected_cell, error_cells, error_message, help_text)
    pygame.display.flip()

pygame.quit()
sys.exit()

