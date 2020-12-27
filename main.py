# tetris in pygame
import random

import pygame

from common import COLUMNS, ROWS, WIDTH, HEIGHT, tetrominoes, EV_ADVANCEGAME, grid, draw_score, draw_gameover, \
    draw_block, empty_grid
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
    quitting = False
    game_over = False
    score = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quitting = True
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

    # "Press any key to continue"
    while not quitting:
        for event in pygame.event.get():
            clock.tick(10)
            if event.type == pygame.KEYDOWN:
                game_over = False
                quitting = False
            if event.type == pygame.QUIT:
                game_over = True
                quitting = True

    return quitting


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
        draw_block(screen, col, row, color=c)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    pygame.key.set_repeat(200, 50)
    pygame.time.set_timer(EV_ADVANCEGAME, ADVANCE_DELAY)
    while True:
        empty_grid()
        draw_screen(screen)
        quitting = mainloop(screen)
        if quitting:
            break
    pygame.quit()


if __name__ == '__main__':
    run_game()
