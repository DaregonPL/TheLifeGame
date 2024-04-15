from random import randint
import time
import glob
import os
import copy


class TheLife():
    glider = [(2, 0), (2, 1), (2, 2), (1, 2), (0, 1)]
    speedlist = [0.5, 0.75, 1, 1.5, 2, 5, 10, 20]
    bg = '◦'
    maxfill = 0.75

    def __init__(self):
        self.height, self.width = 10, 10
        self.f = ''
        self.lastload = 'default'
        self.cls = False
        self.speed = 5
        self.allow_repeat = False

    def setup(self, **kw):
        for n, v in kw.items():
            if n == 'height':
                self.height = v
            elif n == 'width':
                self.width = v
            elif n == 'lfc_startpath':
                self.f = v

    def create_map(self):
        self.map = Map(self.height, self.width)
        with open('lfc/default.lfc', 'w') as deflfc:
            deflfc.write('\n'.join([''.join(y) for y in
                                    [x for x in self.map.lastframe()]])
                         .replace('■', '1').replace('□', '0'))

    def run(self):
        print('TheLifeGame CR: VovLer Games;\nSettings:')
        print(f' x:{self.width};\n y:{self.height}')
        print(f' speed{self.speed};\n cls:{self.cls};\n' +
              f'allow_repeat: {self.allow_repeat}')
        self.set_marks()
        print('Limit of generations: (do not type anything to skip)')
        limit = input()
        if limit != '0':
            limit = int(limit) if limit.isdigit() else None
            self.generate(limit, self.allow_repeat)
        print('Game Over! Results:')
        print(self.map.statistic)
        print(f'Generations: {len(self.map.frames)}')
        input()
        self.run()

    def generate(self, limit=None, repeat_ok=True):
        framenum = 0
        delay = 0.5 / self.speed
        while 1:
            framenum += 1
            os.system('cls') if self.cls else print('\n\n\n')
            self.map.generate()
            [print(' '.join(x).replace('□', self.bg)) for x in
             self.map.lastframe()]
            if limit and framenum == limit:
                break
            elif not repeat_ok and self.map.lastframe() in self.map.frames:
                break
            self.map.save() if not repeat_ok else None
            time.sleep(delay)

    def set_marks(self):
        sepcol = ' ' * len(str(self.width - 1))
        maxrow = len(str(len(self.map.lastframe()) - 1))
        while True:
            print('\n= Setup: Enter {row};{column} to fill' +
                  ' a cell or nothin if you\'re done =')
            print('commands:')
            print('"glider" - create glider')
            print('"random" - fill random cells')
            print('"cls" - enable/disable cleaning console')
            print('"speed" - change speed')
            print('"clear" - clear the map')
            print('"bg" - switch background')
            print('"allow_repeat" - allow/prohibit repeating frames')
            print('"view" - preview of current configuration')
            print('"resize" - resize the map')
            print('"load" - load confifuration')
            print('"reload" - load last file')
            print('"save_lfc" - save configuration')
            print('\nSettings:')
            print(f' speed: {self.speed}x;\n cls: {self.cls};\n' +
                  f' allow_repeat: {self.allow_repeat};\n bg: "{self.bg}"')
            print(f'CurrentFile: {self.lastload}.lfc')
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
            elif x == 'random':
                cells = randint(0, int(self.map.w * self.map.h * self.maxfill))
                for x in range(cells):
                    self.map.mark(randint(0, self.map.h - 1),
                                  randint(0, self.map.w - 1))
            elif x == 'clear':
                self.create_map()
            elif x == 'save':
                self.map.save()
            elif x == 'resize':
                self.ask_size()
                self.run()
                break
            elif x == 'load':
                lfcs = [x[4:] for x in glob.glob('lfc/*.lfc')]
                f = self.f
                while 1:
                    opt = self.lfc_navigate(f, lfcs)
                    print(f'==== lfc/{f}')
                    pos = []
                    if f:
                        print('<< back')
                        pos.append('back')
                    for typ, var in opt.items():
                        for x in var:
                            fp = self.lfc_navigate('.'.join([x for x in
                                                             f.split('.') if x]
                                                            + [x]), lfcs)
                            st = '/' if typ == 'group' else '|' \
                                 if typ == 'file' else ':'
                            print(f'{st}{x}{" " * (20 - len(x))}|{typ}',
                                  f' {len(fp["group"])}g',
                                  f'{len(fp["file"])}f {len(fp["size"])}s')
                            pos.append(x)
                    if opt['size'] == ['default']:
                        break
                    ans = input('>')
                    if ans in pos:
                        if ans == 'back':
                            f = '.'.join(f.split('.')[:-1])
                            continue
                        elif opt['size']:
                            if ans != 'default':
                                f += f'-{ans}'
                            break
                        f = '.'.join([x for x in f.split('.') if x] + [ans])
                    elif ans == '-root':
                        f = ''
                    elif not ans:
                        break
                if os.path.exists(f'lfc/{f}.lfc'):
                    self.f = '.'.join(f.split('.')[:-1])
                    self.load(f)
                    self.lastload = f
                    self.run()
                    break
                else:
                    print('not found')
            elif x == 'reload':
                if os.path.exists(f'lfc/{self.lastload}.lfc'):
                    self.load(self.lastload)
                    self.run()
                    break
                else:
                    print('not found')
            elif x == 'view':
                pv = self.map.lastframe()
                print('\n'.join([' '.join(x) for x in
                                 pv]).replace('□', self.bg))
            elif x == 'save_lfc':
                print('Name format: {group}.{name}-{size}')
                print('name:')
                name = input('>|')
                if not name:
                    continue
                elif ([x for x in name if not
                      (x.isalnum() or x in ['.', '-'])] or
                      (name.count('-') not in [0, 1])):
                    print('name can consist alpha, numbers, "." and "-" only.',
                          'Use one "-"', sep='\n')
                    continue
                fld = self.map.lastframe()
                fld = '\n'.join([''.join(y) for y in [x for x in fld]]) \
                      .replace('■', '1').replace('□', '0')
                with open(f'lfc/{name}.lfc', 'w') as fff:
                    fff.write(fld)
                self.lastload = name
                print('saved')
            elif x == 'cls':
                self.cls = False if self.cls else True
                print('CLS:', self.cls)
            elif x == 'speed':
                self.speed = self.speedlist[(self.speedlist.index(self.speed)
                                             + 1) % len(self.speedlist)]
                print('Speed:', self.speed)
            elif x == "allow_repeat":
                self.allow_repeat = False if self.allow_repeat else True
            elif x == 'bg':
                self.bg = ' ' if self.bg != ' ' else '◦'
            elif x == '':
                break
            else:
                print('unexpected input')

    def load(self, name):
        with open(f'lfc/{name}.lfc') as lfc:
            data = lfc.read()
        h = len(data.split('\n'))
        w = max([len(x) for x in data.split('\n')])
        self.map = Map(h, w)
        data = data.split('\n')
        self.height = h
        self.width = w
        self.create_map()
        for x in range(h):
            for y in range(len(data[x])):
                self.map.mark(x, y) if data[x][y] == '1' else 0

    def apply_cord(self, matrix):
        mtx = matrix.copy()
        return [[' '] + [str(x) for x in range(self.width)]] + \
               [[str(x)] + mtx[x] for x in range(self.height)]

    def lfc_navigate(self, group, fileList):
        a = [x for x in fileList if x.startswith(group)]
        group = [x for x in group.split('.') if x]
        opts = {'group': [], 'file': [], 'size': []}
        for x in a:
            fulldata = x.split('.')[:-1]
            fit = fulldata[len(group):]
            if len(fit) > 1 and fit[0] not in opts['group']:
                opts['group'].append(fit[0])
            elif len(fit) == 1 and fit[0].split('-')[0] not in opts['file']:
                opts['file'].append(fit[0].split('-')[0])
            elif len(fit) == 0 and '-' not in fulldata[-1]:
                opts['size'].append('default')
            elif len(fit) == 0 and (fulldata[-1].split('-')[1]
                                    not in opts['size']):
                opts['size'].append(fulldata[-1].split('-')[1])
        return opts

    def ask_size(self):
        print('Height: (10 by default)')
        h = input()
        print('Width: (10 by default)')
        w = input()
        self.setup(height=int(h)) if h.isdigit() else None
        self.setup(width=int(w)) if w.isdigit() else None
        self.create_map()


class Map():
    def __init__(self, height, width):
        self.h, self.w = height, width
        self.field = [['□' for x in range(width)] for y in range(height)]
        self.frames = []
        self.statistic = {'Died': 0, 'Born': 0}
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
                    self.statistic['Died'] += 1
            else:
                if n == 3:
                    field[cell[0]][cell[1]] = '■'
                    self.statistic['Born'] += 1
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
