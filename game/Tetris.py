import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
]

# Bentuk Tetris
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# Mengaitkan bentuk dengan warna
SHAPE_COLORS = {
    0: (0, 255, 255),  # I
    1: (255, 165, 0),  # T
    2: (255, 0, 0),    # O
    3: (0, 255, 0),    # S
    4: (0, 0, 255),    # Z
    5: (255, 255, 0),  # L
    6: (128, 0, 128),  # J
}

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.current_position = [0, GRID_WIDTH // 2 - 1]
        self.score = 0

    def new_piece(self):
        shape_index = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[shape_index]
        color = SHAPE_COLORS[shape_index]
        return shape, color

    
    def rotate_piece(self):
        shape, color = self.current_piece
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
        self.current_piece = (rotated_shape, color)

    def valid_position(self, offset):
        for y, row in enumerate(self.current_piece[0]):
            for x, value in enumerate(row):
                if value:
                    new_x = self.current_position[1] + x + offset[1]
                    new_y = self.current_position[0] + y + offset[0]
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or self.grid[new_y][new_x]:
                        return False
        return True

    def merge_piece(self):
        for y, row in enumerate(self.current_piece[0]):
            for x, value in enumerate(row):
                if value:
                    self.grid[self.current_position[0] + y][self.current_position[1] + x] = self.current_piece[1]

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        self.score += len(lines_to_clear)

    def drop_piece(self):
        if self.valid_position((1, 0)):
            self.current_position[0] += 1
        else:
            self.merge_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            self.current_position = [0, GRID_WIDTH // 2 - 1]
            if not self.valid_position((0, 0)):
                return False
        return True

    def draw_current_piece(self, screen):
        shape, color = self.current_piece
        for y, row in enumerate(shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, color, ((self.current_position[1] + x) * BLOCK_SIZE, 
                                                       (self.current_position[0] + y) * BLOCK_SIZE, 
                                                       BLOCK_SIZE, BLOCK_SIZE))

def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris Sederhana")
    clock = pygame.time.Clock()
    tetris = Tetris()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if tetris.valid_position((0, -1)):
                        tetris.current_position[1] -= 1
                if event.key == pygame.K_RIGHT:
                    if tetris.valid_position((0, 1)):
                        tetris.current_position[1] += 1
                if event.key == pygame.K_DOWN:
                    tetris.drop_piece()
                if event.key == pygame.K_UP:
                    tetris.rotate_piece()
                    if not tetris.valid_position((0, 0)):
                        tetris.rotate_piece()  # Undo rotation if invalid

        if not tetris.drop_piece():
            print("Game Over! Your score:", tetris.score)
            pygame.quit()
            return

        screen.fill(BLACK)
        draw_grid(screen, tetris.grid)
        tetris.draw_current_piece(screen)  # Draw the current piece
        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()