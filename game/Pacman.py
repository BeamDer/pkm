import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLOCK_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Warna
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Labirin
maze = [
    "####################",
    "#........#........#",
    "#.######.#.######.#",
    "#.................#",
    "######.##########.#",
    "#........#........#",
    "#.######.#.######.#",
    "#........#........#",
    "####################"
]

# Fungsi untuk menggambar labirin
def draw_maze(screen):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 3)

# Kelas untuk Pac-Man
class PacMan:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.score = 0

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if maze[new_y][new_x] != '#':
            self.x = new_x
            self.y = new_y
            if maze[new_y][new_x] == '.':
                self.score += 1
                maze[new_y] = maze[new_y][:new_x] + ' ' + maze[new_y][new_x + 1:]

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x * BLOCK_SIZE + BLOCK_SIZE // 2, self.y * BLOCK_SIZE + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

# Kelas untuk Hantu
class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # Gerakan acak

    def move(self):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if maze[new_y][new_x] != '#':
            self.x = new_x
            self.y = new_y
        else:
            # Ubah arah jika bertemu dinding
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x * BLOCK_SIZE + BLOCK_SIZE // 2, self.y * BLOCK_SIZE + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

def reset_game():
    global pacman, ghosts, maze
    pacman = PacMan()
    ghosts = [Ghost(5, 5)]  # Tambahkan satu hantu
    # Reset maze jika diperlukan
    maze = [
        "####################",
        "#........#........#",
        "#.######.#.######.#",
        "#.................#",
        "######.##########.#",
        "#........#........#",
        "#.######.#.######.#",
        "#........#........#",
        "####################"
    ]

def main():
    global pacman, ghosts
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man Sederhana")
    clock = pygame.time.Clock()
    reset_game()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                pacman.move(-1, 0)
            if keys[pygame.K_RIGHT]:
                pacman.move(1, 0)
            if keys[pygame.K_UP]:
                pacman.move(0, -1)
            if keys[pygame.K_DOWN]:
                pacman.move(0, 1)

            # Gerakkan hantu
            for ghost in ghosts:
                ghost.move()

            # Cek tabrakan antara Pac-Man dan hantu
            for ghost in ghosts:
                if pacman.x == ghost.x and pacman.y == ghost.y:
                    game_over = True

            screen.fill(BLACK)
            draw_maze(screen)
            pacman.draw(screen)
            for ghost in ghosts:
                ghost.draw(screen)

            # Tampilkan skor
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {pacman.score}', True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(10)
        else:
            # Tampilkan pesan Game Over
            font = pygame.font.Font(None, 48)
            game_over_text = font.render('Game Over! Press R to Restart or Q to Quit', True, WHITE)
            screen.fill(BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()

            # Tunggu input pengguna
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                reset_game()
                game_over = False
            if keys[pygame.K_q]:
                pygame.quit()
                return

if __name__ == "__main__":
    main()