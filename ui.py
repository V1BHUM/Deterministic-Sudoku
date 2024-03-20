import pygame
import sys
from deterministic_sudoku import Sudoku

# Define constants
THIN_LINE = 2
THICK_LINE = 6
CELL_SIZE = 70
GRID_SIZE = 9
SIDE = CELL_SIZE*GRID_SIZE + THICK_LINE//2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (230, 230, 230)
LIGHT_BLUE = (173, 216, 230)
RED = (173, 10, 50)

# Initialize Pygame
pygame.init()
sudo = Sudoku()
screen = pygame.display.set_mode((SIDE, SIDE))
pygame.display.set_caption("Sudoku")

# Create an empty Sudoku grid
sudoku_board = [['-' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to draw the Sudoku grid
def draw_grid():
    for i in range(GRID_SIZE+1):
        thickness = THICK_LINE if (i % 3 == 0) else THIN_LINE
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SIDE), thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SIDE, i * CELL_SIZE), thickness)

# Function to draw the Sudoku numbers
def draw_numbers():
    font = pygame.font.SysFont(None, 40)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if sudoku_board[i][j] != '-':
                number = font.render(str(sudoku_board[i][j]), True, BLACK)
                x = j * CELL_SIZE + CELL_SIZE // 2 - number.get_width() // 2
                y = i * CELL_SIZE + CELL_SIZE // 2 - number.get_height() // 2
                screen.blit(number, (x, y))

# Function to highlight the selected cell
def highlight_cell(row, col, color):
    pygame.draw.rect(screen, color, (col * CELL_SIZE+THIN_LINE, row * CELL_SIZE+THIN_LINE, CELL_SIZE-THIN_LINE, CELL_SIZE-THIN_LINE))

# Main game loop
running = True
solving = False
tick = None
selected_row, selected_col = -1, -1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (not solving) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
            x, y = pygame.mouse.get_pos()
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                selected_row, selected_col = row, col
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                sudoku_board = [['-' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                sudo = Sudoku()
                solving = False
            elif (not solving and event.key == pygame.K_RETURN):
                solving = True
                tick = None
                selected_row, selected_col = -1, -1
            elif (solving and event.key == pygame.K_SPACE):
                sudo.input_grid(sudoku_board)
                tick = sudo.solve()
                sudoku_board = sudo.grid
            elif selected_row != -1 and selected_col != -1:
                # Enter number in the selected cell
                number = event.unicode
                if '1' <= number <= '9' or number == '-':
                    sudoku_board[selected_row][selected_col] = number
                    selected_row, selected_col = -1, -1
    color = WHITE if not solving else GREY
    screen.fill(color)
    draw_grid()
    if solving:
        if (tick):
            blocks = []
            if tick[0] == 'row':
                blocks = sudo.get_row(tick[1])
            elif tick[0] == 'col':
                blocks = sudo.get_column(tick[1])
            else:
                blocks = sudo.get_block(*tick[1])
            for block in blocks:
                highlight_cell(block[0], block[1], LIGHT_BLUE)
            Y, X = tick[2]
            highlight_cell(Y, X, RED)
    draw_numbers()
    if selected_row != -1 and selected_col != -1:
        highlight_cell(selected_row, selected_col, LIGHT_BLUE)
    pygame.display.flip()

pygame.quit()
sys.exit()
