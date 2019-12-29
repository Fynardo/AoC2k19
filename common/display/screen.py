class Screen:
    def __init__(self, width=64, height=32, blank=' '):
        self._width = width
        self._height = height
        self._blank = blank
        self._grid = [[self._blank]*self._width for _ in range(self._height)]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def set_tile(self, x, y, tile):
        self._grid[x][y] = tile

    def get_tile(self, x, y):
        return self._grid[x][y]

    def set_text(self, x, y, text):
        for i, c in enumerate(text):
            self.set_tile(x, y+i, c)

    def draw(self):
        for r in self._grid:
            print(''.join(r))

    def reset(self):
        for i in range(self._height):
            for j in range(self._width):
                self.set_tile(i, j, self._blank)

    def _track_tile(self, tile):
        pass
