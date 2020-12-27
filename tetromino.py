from common import COLUMNS, ROWS, draw_block, colors, grid


class Tetromino:
    def __init__(self, screen, shape, column, row):
        self.screen = screen
        self.matrix = shape
        self.column = column
        self.row = row

    def _to_shape(self):
        return [
            ''.join([{False: '.', True: 'X'}[bool(x)] for x in row])
            for row in self.matrix
        ]

    def __str__(self):
        return "\n".join(self._to_shape())

    def rotate(self):
        saved_matrix = self.matrix.copy()
        for n, color in enumerate(saved_matrix):
            column = n % 4
            row = n // 4
            self.matrix[(2 - column) * 4 + row] = color
        if not self.valid(self.row, self.column):
            self.matrix = saved_matrix

    def valid(self, row, column):
        for n, color in enumerate(self.matrix):
            if color:
                c = column + n % 4
                r = row + n // 4
                if c < 0 or c >= COLUMNS or r >= ROWS or grid[r * COLUMNS + c]:
                    return False
        return True

    def show(self):
        for n, color in enumerate(self.matrix):
            if color:
                c = n % 4
                r = n // 4
                draw_block(self.screen,
                           (self.column + c) % COLUMNS,
                           (self.row + r) % ROWS,
                           color)

    def move(self, dx, dy):
        new_c = self.column + dx
        new_r = self.row + dy
        if self.valid(new_r, new_c):
            self.column = new_c
            self.row = new_r
            return True
        return False

    def freeze(self):
        for n, color in enumerate(self.matrix):
            if color:
                c = (n % 4) + self.column
                r = (n // 4) + self.row
                grid[r*COLUMNS + c] = color
