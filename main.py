# tetris in pygame
import random

import pygame

from common import VOFFSET, BLOCKSIZE, COLUMNS, ROWS, WIDTH, HEIGHT, tetrominoes, EV_ADVANCEGAME, grid, colors, \
    grid2screen, draw_score, draw_gameover
from tetromino import Tetromino

clock = pygame.time.Clock()
FPS = 30
ADVANCE_DELAY = 500
game_over = False
score = 0


def remove_rows():
    removed = 0
    for r in range(ROWS):
        if all(grid[r * COLUMNS:(r + 1) * COLUMNS]):
            del grid[r * COLUMNS:(r + 1) * COLUMNS]
            grid[0:0] = [0] * COLUMNS
            removed += 1
    return removed


def mainloop(screen):
    global game_over, score
    player = Tetromino(screen, random.choice(tetrominoes), COLUMNS // 2 - 2, 0)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == EV_ADVANCEGAME:
                if not player.move(0, 1):
                    player.freeze()
                    n = remove_rows()
                    score += n*n * 100
                    print(score)
                    player = Tetromino(screen, random.choice(tetrominoes), COLUMNS // 2 - 2, 0, )
                    valid = player.valid(player.row, player.column)
                    if not valid:
                        game_over = True
                        done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                if event.key == pygame.K_DOWN:
                    player.move(0, 1)
                if event.key == pygame.K_UP:
                    player.rotate()

        draw_screen(screen)
        player.show()
        pygame.display.flip()
        clock.tick(FPS)

    done = False
    # "Press any key to continue"
    while not done:
        for event in pygame.event.get():
            clock.tick(10)
            if event.type == pygame.KEYDOWN:
                game_over = False
                done = True
            if event.type == pygame.QUIT:
                game_over = True
                done = True


def draw_screen(screen):
    screen.fill((0, 0, 0))
    draw_grid(screen)
    draw_score(screen, score)
    if game_over:
        draw_gameover(screen)


def draw_grid(screen):
    for n, c in enumerate(grid):
        col = n % COLUMNS
        row = n // COLUMNS
        x, y = grid2screen(col, row)
        pygame.draw.rect(screen,
                         color=colors[c],
                         rect=(x, y, BLOCKSIZE, BLOCKSIZE),
                         )


def draw_lattice(screen):
    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, color=(50, 10, 150), rect=(col * BLOCKSIZE, VOFFSET + row * BLOCKSIZE, BLOCKSIZE,
                                                                BLOCKSIZE), width=1)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    pygame.key.set_repeat(200, 50)
    pygame.time.set_timer(EV_ADVANCEGAME, ADVANCE_DELAY)
    draw_screen(screen)
    while not game_over:
        mainloop(screen)
    pygame.quit()


if __name__ == '__main__':
    run_game()
