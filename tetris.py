import pygame
import random

# Define constants
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]]   # S
]

# Define classes
class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Tetris:
    def __init__(self):
        self.grid = [[BLACK] * COLS for _ in range(ROWS)]
        self.current_block = self.new_block()
        self.score = 0

    def new_block(self):
        shape = random.choice(SHAPES)
        color = random.choice([RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE])
        block = Block(3, 0, color)
        return block

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw(self):
        self.draw_grid()
        self.current_block.draw()

    def update(self):
        self.current_block.move(0, 1)
        if self.collide():
            self.add_to_grid()
            self.current_block = self.new_block()
            if self.game_over():
                self.__init__()

    def collide(self):
        shape = SHAPES.index(self.current_block.shape())
        for y, row in enumerate(self.current_block.shape()):
            for x, cell in enumerate(row):
                if cell:
                    if (
                        self.current_block.y + y >= ROWS
                        or self.current_block.x + x < 0
                        or self.current_block.x + x >= COLS
                        or self.grid[self.current_block.y + y][self.current_block.x + x] != BLACK
                    ):
                        return True
        return False

    def add_to_grid(self):
        for y, row in enumerate(self.current_block.shape()):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_block.y + y][self.current_block.x + x] = self.current_block.color

    def game_over(self):
        for cell in self.grid[0]:
            if cell != BLACK:
                return True
        return False

    def clear_lines(self):
        lines_to_clear = []
        for i, row in enumerate(self.grid):
            if all(cell != BLACK for cell in row):
                lines_to_clear.append(i)
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [BLACK] * COLS)
        self.score += len(lines_to_clear) ** 2

    def handle_input(self, key):
        if key == pygame.K_LEFT:
            self.current_block.move(-1, 0)
            if self.collide():
                self.current_block.move(1, 0)
        elif key == pygame.K_RIGHT:
            self.current_block.move(1, 0)
            if self.collide():
                self.current_block.move(-1, 0)
        elif key == pygame.K_DOWN:
            self.current_block.move(0, 1)
            if self.collide():
                self.current_block.move(0, -1)
        elif key == pygame.K_UP:
            self.current_block.rotate()
            if self.collide():
                self.current_block.rotate(-1)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game loop
tetris = Tetris()
running = True
while running:
    screen.fill(BLACK)
    tetris.draw()
    tetris.update()
    pygame.display.flip()
    clock.tick(5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            tetris.handle_input(event.key)

pygame.quit()
