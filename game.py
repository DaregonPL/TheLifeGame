import time
import os
import copy


class TheLife():
    glider = [(2, 0), (2, 1), (2, 2), (1, 2), (0, 1)]
    speedlist = [0.5, 0.75, 1, 1.5, 2, 5, 10]
    
    def __init__(self):
        self.height, self.width = 10, 10
        self.cls = False
        self.speed = 1
        self.allow_repeat = True

    def setup(self, **kw):
        for n, v in kw.items():
            if n == 'height':
                self.height = v
            elif n == 'width':
                self.width = v

    def run(self):
        print('TheLifeGame CR: VovLer Games;\nSettings:')
        print(f' x:{self.width};\n y:{self.height}')
        print(f' speed{self.speed};\n cls:{self.cls};\n' +
              f'allow_repeat: {self.allow_repeat}')
        self.map = Map(self.height, self.width)
        self.set_marks()
        print('Limit of generations: (do not type anything to skip)')
        limit = input()
        limit = int(limit) if limit.isdigit() else None
        self.generate(limit, self.allow_repeat)

    def generate(self, limit=None, repeat_ok=True):
        framenum = 0
        delay = 0.25 / self.speed
        while 1:
            framenum += 1
            os.system('cls') if self.cls else print('\n\n\n')
            self.map.generate()
            [print(' '.join(x).replace('□', ' ')) for x in
                     self.map.lastframe()]
            if limit and framenum == limit:
                break
            elif not repeat_ok and self.map.lastframe() in self.map.frames:
                break
            self.map.save()
            time.sleep(delay)

    def set_marks(self):
        sepcol = ' ' * len(str(self.width - 1))
        maxrow = len(str(len(self.map.lastframe()) - 1))
        while True:
            print('\n= Setup: Enter {row};{column} to fill' +
                  ' a cell or nothin if you\'re done =')
            print('commands:')
            print('"glider" - create glider')
            print('"cls" - enable/disable cleaning console')
            print('"speed" - change speed')
            print('"allow_repeat" - allow/prohibit repeating frames')
            print('Settings:')
            print(f' speed: {self.speed};\n cls: {self.cls};\n' +
                  f' allow_repeat: {self.allow_repeat}')
            print('')
            field = self.apply_cord(self.map.lastframe())
            for r in field:
                r[0] = r[0] + ' ' * (maxrow - len(r[0]))
            cols = ''
            for x in field.pop(0):
                if ' ' not in x:
                    cols += x + ' ' * (len(sepcol) + 1 - len(x))
                else:
                    cols += ' ' * maxrow + sepcol
            print(cols)
            print('\n'.join([sepcol.join(x) for x in
                             field]))
            x = input()
            if x.split(';') and not [x for x in x.split(';')
                                     if not x.isdigit()] and \
                        len(x.split(';')) == 2:
                try:
                    if bl(self.map.val(*[int(a) for a in x.split(';')])):
                        self.map.pop(*x.split(';'))
                    else:
                        self.map.mark(*x.split(';'))
                except IndexError:
                    print(f'Cannot access cell {x.split(";")}')
                finally:
                    pass
            elif x == 'gen':
                self.map.generate()
            elif x == 'frames':
                for x in range(len(self.map.frames)):
                    print(f'\n = {x} =')
                    [print(' '.join(x)) for x in self.map.frames[x]]
            elif x == 'glider':
                [self.map.mark(*x) for x in self.glider]
            elif x == 'save':
                self.map.save()
            elif x == 'cls':
                self.cls = False if self.cls else True
                print('CLS:', self.cls)
            elif x == 'speed':
                self.speed = self.speedlist[(self.speedlist.index(self.speed)
                                             + 1) % len(self.speedlist)]
                print('Speed:', self.speed)
            elif x == "allow_repeat":
                self.allow_repeat = False if self.allow_repeat else True
            elif x == '':
                break
            else:
                print('unexpected input')

    def apply_cord(self, matrix):
        mtx = matrix.copy()
        return [[' '] + [str(x) for x in range(self.width)]] + \
               [[str(x)] + mtx[x] for x in range(self.height)]


class Map():
    def __init__(self, height, width):
        self.h, self.w = height, width
        self.field = [['□' for x in range(width)] for y in range(height)]
        self.frames = []
        self.save()

    def generate(self):
        stk = FrameStreak(self.field)
        field = self.lastframe()
        cell = stk.next()
        while cell:
            c, n = bl(self.val(*cell)), len([x for x in stk.near()
                                             if bl(self.val(*x))])
            if c:
                if n < 2 or n > 3:
                    field[cell[0]][cell[1]] = '□'
            else:
                if n == 3:
                    field[cell[0]][cell[1]] = '■'
            cell = stk.next()
        self.field = copy.deepcopy(field)

    def mark(self, x, y):
        self.field[int(x)][int(y)] = '■'

    def pop(self, x, y):
        self.field[int(x)][int(y)] = '□'

    def save(self):
        self.frames.append(copy.deepcopy(self.field))

    def val(self, y, x):
        return self.field[y][x]

    def lastframe(self):
        return copy.deepcopy(self.field)


class FrameStreak():
    def __init__(self, frame):
        self.frame = copy.deepcopy(frame)
        self.x, self.y = -1, 0
        self.height, self.width = len(self.frame), len(self.frame[0])

    def next(self):
        if self.x + 1 == self.width:
            if self.y + 1 == self.height:
                return None
            else:
                self.x = 0
                self.y += 1
        else:
            self.x += 1
        return (self.y, self.x)

    def near(self):
        return [((self.y + 1) % self.height, self.x),
                ((self.y + 1) % self.height, (self.x + 1) % self.width),
                ((self.y - 1) % self.height, (self.x + 1) % self.width),
                ((self.y - 1) % self.height, (self.x - 1) % self.width),
                ((self.y + 1) % self.height, (self.x - 1) % self.width),
                (self.y, (self.x + 1) % self.width),
                ((self.y - 1) % self.height, self.x),
                (self.y, (self.x - 1) % self.width)]


def bl(obj):
    return True if obj == '■' else False


print('Height: (10 by default)')
h = input()
print('Width: (10 by default)')
w = input()
life = TheLife()
life.setup(height=int(h)) if h.isdigit() else None
life.setup(width=int(w)) if w.isdigit() else None
life.run()
input()
