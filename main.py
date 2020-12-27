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


class Tetris:
    def __init__(self, num_columns=COLUMNS, num_rows=ROWS):
        self.game_over = False
        self.score = 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.columns = num_columns
        self.rows = num_rows
        self.grid = [0] * num_columns * num_rows
        self.quitting = False

    def run(self):
        self.start()
        self.mainloop()
        return self.stop()

    def start(self):
        pygame.time.set_timer(EV_ADVANCEGAME, ADVANCE_DELAY)

    def stop(self):
        # Disable timer by setting delay to 0
        pygame.time.set_timer(EV_ADVANCEGAME, 0)
        # TODO: Show "Game Over" and highscore table
        if self.quitting:
            return False
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            # quit if ESC otherwise start a new game
            return not event.key == pygame.K_ESCAPE

    def mainloop(self):
        player = Tetromino(self.screen, random.choice(tetrominoes), self.columns // 2 - 2, 0,
                           self.draw_block, self.block_to_grid, self.is_free)
        done = False
        self.game_over = False
        self.score = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    self.quitting = True
                if event.type == EV_ADVANCEGAME:
                    if not player.move(0, 1):
                        player.freeze()
                        n = self.remove_rows()
                        self.score += n * n * 100
                        player = Tetromino(self.screen, random.choice(tetrominoes), self.columns // 2 - 2, 0,
                                           self.draw_block, self.block_to_grid, self.is_free)
                        valid = player.valid(player.row, player.column)
                        if not valid:
                            self.game_over = True
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

            self.draw_screen()
            player.show()
            pygame.display.flip()
            clock.tick(FPS)

    def draw_block(self, col, row, color):
        draw_block(self.screen, col, row, color)

    def block_to_grid(self, col, row, color):
        self.grid[row * self.columns + col] = color

    def is_free(self, col, row):
        free = self._is_free(col, row)
        return free

    def _is_free(self, col, row):
        if (col < 0 or col >= self.columns
                or row >= self.rows
                or self.grid[row * self.columns + col]):
            return False
        return True

    def remove_rows(self):
        removed = 0
        for r in range(self.rows):
            if all(self.grid[r * self.columns: (r + 1) * self.columns]):
                del self.grid[r * self.columns: (r + 1) * self.columns]
                self.grid[0:0] = [0] * self.columns
                removed += 1
        return removed

    def draw_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        draw_score(self.screen, self.score)
        if game_over:
            draw_gameover(self.screen)

    def draw_grid(self):
        for n, c in enumerate(self.grid):
            col = n % self.columns
            row = n // self.columns
            draw_block(self.screen, col, row, color=c)


def run_game():
    pygame.init()
    pygame.display.set_caption("Tetris")
    pygame.key.set_repeat(200, 50)
    repeat = True
    while repeat:
        tetris = Tetris()
        repeat = tetris.run()
    pygame.quit()


if __name__ == '__main__':
    run_game()
