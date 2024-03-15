import time


class TheLife():
    def __init__(self, resolution):
        self.h, self.w = [int(x) for x in resolution.split('x')]
        self.map = Map(self.h, self.w)

    def print(self):
        [print(' '.join(x)) for x in self.map.field]


class Map():
    def __init__(self, height, width):
        self.h, self.w = height, width
        self.field = [['*' for x in range(width)] for y in range(height)]

    def run(self):
        self.next = self.field.copy()
        


life = TheLife('10x30')
life.print()
