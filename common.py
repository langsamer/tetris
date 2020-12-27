import os.path

import pygame

RESOURCE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')

tetrominoes = [
    [0, 1, 1, 0,  # O
     0, 1, 1, 0,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 3, 0, 0,
     0, 3, 0, 0,  # I
     0, 3, 0, 0,
     0, 3, 0, 0],
    [0, 0, 0, 0,  # J
     5, 5, 5, 0,
     0, 0, 5, 0,
     0, 0, 0, 0],
    [0, 0, 7, 0,  # L
     7, 7, 7, 0,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 2, 2, 0,  # S
     2, 2, 0, 0,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [4, 4, 0, 0,  # Z
     0, 4, 4, 0,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 6, 0, 0,  # T
     6, 6, 6, 0,
     0, 0, 0, 0,
     0, 0, 0, 0]
]
colors = [
    (0, 0, 0),
    (240, 240, 0),  # O
    (0, 240, 240),  # I
    (0, 0, 240),  # J
    (240, 0, 160),  # L
    (0, 240, 0),  # S
    (240, 0, 0),  # Z
    (160, 0, 240),  # T
]
VOFFSET = 50
COLUMNS = 10
WIDTH = 200
BLOCKSIZE = WIDTH // COLUMNS
ROWS = 20
HEIGHT = 450

EV_ADVANCEGAME = pygame.USEREVENT + 1

grid = [0] * COLUMNS * ROWS
blocks = [
    pygame.transform.scale(
        pygame.image.load(
            os.path.join(RESOURCE_DIRECTORY, 'blocks', f'Teil_11_tt3_{n}.gif')), (BLOCKSIZE, BLOCKSIZE))
    for n in range(8)
]


def grid2screen(column, row):
    return column * BLOCKSIZE, VOFFSET + row * BLOCKSIZE


def empty_grid():
    global grid
    grid = [0] * COLUMNS * ROWS


def draw_block(screen, column, row, color=0):
    x, y = grid2screen(column, row)
    screen.blit(blocks[color], (x, y))


def draw_gameover(screen):
    gameover_sf = pygame.font.SysFont("Impact", 32, bold=False).render(
        "Game Over", True, (200, 200, 200))
    screen.blit(gameover_sf, ((WIDTH - gameover_sf.get_width()) // 2, (HEIGHT - gameover_sf.get_height()) // 2))


def draw_score(screen, score, level=1):
    score_sf = pygame.font.SysFont("Verdana", 20).render(
        f"{score:,}", True, (100, 255, 100))
    screen.blit(score_sf, (WIDTH - score_sf.get_width() - 10, 5))
