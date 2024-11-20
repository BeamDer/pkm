import pygame
import random

# Inisialisasi pygame
pygame.init()

# Warna
putih = (255, 255, 255)
hitam = (0, 0, 0)
merah = (213, 50, 80)
hijau = (0, 255, 0)
biru = (50, 153, 213)

# Ukuran layar
lebar_layar = 800
tinggi_layar = 600
layar = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption('Game Snake')

# Kecepatan ular
clock = pygame.time.Clock()
kecepatan_ular = 15
ukuran_blok = 10

# Font
font_style = pygame.font.SysFont("bahnschrift", 25)
skor_font = pygame.font.SysFont("comicsansms", 35)

class Snake:
    def __init__(self):
        self.ukuran_blok = ukuran_blok
        self.ular_list = []
        self.panjang_ular = 1
        self.x = lebar_layar / 2
        self.y = tinggi_layar / 2
        self.x_change = 0
        self.y_change = 0

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

    def grow(self):
        self.panjang_ular += 1

    def reset(self):
        self.ular_list = []
        self.panjang_ular = 1
        self.x = lebar_layar / 2
        self.y = tinggi_layar / 2
        self.x_change = 0
        self.y_change = 0

    def draw(self):
        for segment in self.ular_list:
            pygame.draw.rect(layar, hijau, [segment[0], segment[1], self.ukuran_blok, self.ukuran_blok])

class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x = round(random.randrange(0, lebar_layar - ukuran_blok) / 10.0) * 10.0
        self.y = round(random.randrange(0, tinggi_layar - ukuran_blok) / 10.0) * 10.0

def tampilkan_skor(skor):
    nilai = skor_font.render("Skor: " + str(skor), True, hitam)
    layar.blit(nilai, [0, 0])

def pesan(msg, warna):
    pesan = font_style.render(msg, True, warna)
    layar.blit(pesan, [lebar_layar / 6, tinggi_layar / 3])

def game_loop():
    game_over = False
    game_close = False

    snake = Snake()
    food = Food()

    while not game_over:
        while game_close:
            layar.fill(biru)
            pesan("Game Over! Tekan C untuk main lagi atau Q untuk keluar", merah)
            tampilkan_skor(snake.panjang_ular - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake.reset()
                        food.spawn()
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.x_change = -snake.ukuran_blok
                    snake.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake.x_change = snake.ukuran_blok
                    snake.y_change = 0
                elif event.key == pygame.K_UP:
                    snake.y_change = -snake.ukuran_blok
                    snake.x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake.y_change = snake.ukuran_blok
                    snake.x_change = 0

        if snake.x >= lebar_layar or snake.x < 0 or snake.y >= tinggi_layar or snake.y < 0:
            game_close = True

        snake.move()
        layar.fill(biru)
        # pygame.draw.rect(layar, merah, [food.x, food.y, ukuran_blok, ukuran_blok])
        
        # Men ampilkan ular
        snake.ular_list.append((snake.x, snake.y))
        if len(snake.ular_list) > snake.panjang_ular:
            del snake.ular_list[0]

        for segment in snake.ular_list[:-1]:
            if segment == (snake.x, snake.y):
                game_close = True

        snake.draw()
        # tampilkan_skor(snake.panjang_ular - 1)

        pygame.display.update()

        if snake.x == food.x and snake.y == food.y:
            snake.grow()
            food.spawn()

        clock.tick(kecepatan_ular)

    pygame.quit()
    quit()

game_loop()