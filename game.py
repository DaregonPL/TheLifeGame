import time


class TheLife():
    def __init__(self):
        self.height, self.width = 25, 25

    def setup(self, **kw):
        for n, v in kw.items():
            if n == 'height':
                self.height = v
            elif n == 'width':
                self.width = v

    def run(self):
        self.map = Map(self.height, self.width)
        while True:
            print(self.map.frames)
            print('\n'.join([' '.join(x) for x in
                             self.apply_cord(self.map.lastframe())]))
            self.map.mark(*input().split(';'))

    def apply_cord(self, matrix):
        mtx = matrix.copy()
        return [[' '] + [str(x) for x in range(self.width)]] + \
               [[str(x)] + mtx[x] for x in range(self.height)]


class Map():
    def __init__(self, height, width):
        self.h, self.w = height, width
        self.field = [['□' for x in range(width)] for y in range(height)]
        self.frames = []

    def generate(self):
        self.frames.append([x for x in self.field])

    def mark(self, x, y):
        self.field[int(x)][int(y)] = '■'

    def lastframe(self):
        return [x for x in self.field]


life = TheLife()
life.setup(height=2, width=5)
life.run()
