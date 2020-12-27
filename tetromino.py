class Tetromino:
    def __init__(self, screen, shape, column, row, draw_block, to_grid, grid_free):
        self.screen = screen
        self.matrix = shape
        self.column = column
        self.row = row
        self.draw_block = draw_block
        self.to_grid = to_grid
        self.grid_free = grid_free

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
                if not self.grid_free(c, r):
                    return False
        return True

    def show(self):
        for n, color in enumerate(self.matrix):
            if color:
                c = n % 4
                r = n // 4
                self.draw_block(self.column + c,
                                self.row + r,
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
                self.to_grid(c, r, color)
