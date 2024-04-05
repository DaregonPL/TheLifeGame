import shutil
import os
import base64
if not os.path.exists('game.py'):
    code = b'from random import randint\r\nimport time\r\nimport glob\r\nimport os\r\nimport copy\r\n\r\n\r\nclass TheLife():\r\n    glider = [(2, 0), (2, 1), (2, 2), (1, 2), (0, 1)]\r\n    speedlist = [0.5, 0.75, 1, 1.5, 2, 5, 10, 20]\r\n    bg = \'\xe2\x97\xa6\'\r\n    maxfill = 0.75\r\n    \r\n    def __init__(self):\r\n        self.height, self.width = 10, 10\r\n        self.f = \'\'\r\n        self.lastload = \'default\'\r\n        self.cls = False\r\n        self.speed = 5\r\n        self.allow_repeat = False\r\n\r\n    def setup(self, **kw):\r\n        for n, v in kw.items():\r\n            if n == \'height\':\r\n                self.height = v\r\n            elif n == \'width\':\r\n                self.width = v\r\n            elif n == \'lfc_startpath\':\r\n                self.f = v\r\n\r\n    def create_map(self):\r\n        self.map = Map(self.height, self.width)\r\n        with open(\'lfc/default.lfc\', \'w\') as deflfc:\r\n            deflfc.write(\'\\n\'.join([\'\'.join(y) for y in\r\n                                    [x for x in self.map.lastframe()]])\r\n                         .replace(\'\xe2\x96\xa0\', \'1\').replace(\'\xe2\x96\xa1\', \'0\'))\r\n\r\n    def run(self):\r\n        print(\'TheLifeGame CR: VovLer Games;\\nSettings:\')\r\n        print(f\' x:{self.width};\\n y:{self.height}\')\r\n        print(f\' speed{self.speed};\\n cls:{self.cls};\\n\' +\r\n              f\'allow_repeat: {self.allow_repeat}\')\r\n        self.set_marks()\r\n        print(\'Limit of generations: (do not type anything to skip)\')\r\n        limit = input()\r\n        if limit != \'0\':\r\n            limit = int(limit) if limit.isdigit() else None\r\n            self.generate(limit, self.allow_repeat)\r\n        print(\'Game Over! Results:\')\r\n        print(self.map.statistic)\r\n        print(f\'Generations: {len(self.map.frames)}\')\r\n        input()\r\n        self.run()\r\n\r\n    def generate(self, limit=None, repeat_ok=True):\r\n        framenum = 0\r\n        delay = 0.5 / self.speed\r\n        while 1:\r\n            framenum += 1\r\n            os.system(\'cls\') if self.cls else print(\'\\n\\n\\n\')\r\n            self.map.generate()\r\n            [print(\' \'.join(x).replace(\'\xe2\x96\xa1\', self.bg)) for x in\r\n                     self.map.lastframe()]\r\n            if limit and framenum == limit:\r\n                break\r\n            elif not repeat_ok and self.map.lastframe() in self.map.frames:\r\n                break\r\n            self.map.save() if not repeat_ok else None\r\n            time.sleep(delay)\r\n\r\n    def set_marks(self):\r\n        sepcol = \' \' * len(str(self.width - 1))\r\n        maxrow = len(str(len(self.map.lastframe()) - 1))\r\n        while True:\r\n            print(\'\\n= Setup: Enter {row};{column} to fill\' +\r\n                  \' a cell or nothin if you\\\'re done =\')\r\n            print(\'commands:\')\r\n            print(\'"glider" - create glider\')\r\n            print(\'"random" - fill random cells\')\r\n            print(\'"cls" - enable/disable cleaning console\')\r\n            print(\'"speed" - change speed\')\r\n            print(\'"clear" - clear the map\')\r\n            print(\'"bg" - switch background\')\r\n            print(\'"allow_repeat" - allow/prohibit repeating frames\')\r\n            print(\'"view" - preview of current configuration\')\r\n            print(\'"load" - load confifuration\')\r\n            print(\'"reload" - load last file\')\r\n            print(\'"save_lfc" - save configuration\')\r\n            print(\'\\nSettings:\')\r\n            print(f\' speed: {self.speed}x;\\n cls: {self.cls};\\n\' +\r\n                  f\' allow_repeat: {self.allow_repeat};\\n bg: "{self.bg}"\')\r\n            print(f\'CurrentFile: {self.lastload}.lfc\')\r\n            print(\'\')\r\n            field = self.apply_cord(self.map.lastframe())\r\n            for r in field:\r\n                r[0] = r[0] + \' \' * (maxrow - len(r[0]))\r\n            cols = \'\'\r\n            for x in field.pop(0):\r\n                if \' \' not in x:\r\n                    cols += x + \' \' * (len(sepcol) + 1 - len(x))\r\n                else:\r\n                    cols += \' \' * maxrow + sepcol\r\n            print(cols)\r\n            print(\'\\n\'.join([sepcol.join(x) for x in\r\n                             field]))\r\n            x = input()\r\n            if x.split(\';\') and not [x for x in x.split(\';\')\r\n                                     if not x.isdigit()] and \\\r\n                        len(x.split(\';\')) == 2:\r\n                try:\r\n                    if bl(self.map.val(*[int(a) for a in x.split(\';\')])):\r\n                        self.map.pop(*x.split(\';\'))\r\n                    else:\r\n                        self.map.mark(*x.split(\';\'))\r\n                except IndexError:\r\n                    print(f\'Cannot access cell {x.split(";")}\')\r\n                finally:\r\n                    pass\r\n            elif x == \'gen\':\r\n                self.map.generate()\r\n            elif x == \'frames\':\r\n                for x in range(len(self.map.frames)):\r\n                    print(f\'\\n = {x} =\')\r\n                    [print(\' \'.join(x)) for x in self.map.frames[x]]\r\n            elif x == \'glider\':\r\n                [self.map.mark(*x) for x in self.glider]\r\n            elif x == \'random\':\r\n                cells = randint(0, int(self.map.w * self.map.h * self.maxfill))\r\n                for x in range(cells):\r\n                    self.map.mark(randint(0, self.map.h - 1),\r\n                                   randint(0, self.map.w - 1))\r\n            elif x == \'clear\':\r\n                self.create_map()\r\n            elif x == \'save\':\r\n                self.map.save()\r\n            elif x == \'load\':\r\n                lfcs = [x[4:] for x in glob.glob(\'lfc/*.lfc\')]\r\n                f = self.f\r\n                while 1:\r\n                    opt = self.lfc_navigate(f, lfcs)\r\n                    print(f\'==== lfc/{f}\')\r\n                    pos = []\r\n                    if f:\r\n                        print(\'<< back\')\r\n                        pos.append(\'back\')\r\n                    for typ, var in opt.items():\r\n                        for x in var:\r\n                            fp = self.lfc_navigate(\'.\'.join([x for x in\r\n                                                             f.split(\'.\') if x]\r\n                                                            + [x]), lfcs)\r\n                            st = \'/\' if typ == \'group\' else \'|\' if typ == \'file\' else \':\'\r\n                            print(f\'{st}{x}{" " * (20 - len(x))}|{typ}\',\r\n                                  f\' {len(fp["group"])}g\',\r\n                                  f\'{len(fp["file"])}f {len(fp["size"])}s\')\r\n                            pos.append(x)\r\n                    if opt[\'size\'] == [\'default\']:\r\n                        break\r\n                    ans = input(\'>\')\r\n                    if ans in pos:\r\n                        if ans == \'back\':\r\n                            f = \'.\'.join(f.split(\'.\')[:-1])\r\n                            continue\r\n                        elif opt[\'size\']:\r\n                            if ans != \'default\':\r\n                                f += f\'-{ans}\'\r\n                            break\r\n                        f = \'.\'.join([x for x in f.split(\'.\') if x] + [ans])\r\n                    elif ans == \'-root\':\r\n                        f = \'\'\r\n                    elif not ans:\r\n                        break\r\n                if os.path.exists(f\'lfc/{f}.lfc\'):\r\n                    self.f = \'.\'.join(f.split(\'.\')[:-1])\r\n                    self.load(f)\r\n                    self.lastload = f\r\n                    self.run()\r\n                    break\r\n                else:\r\n                    print(\'not found\')\r\n            elif x == \'reload\':\r\n                if os.path.exists(f\'lfc/{self.lastload}.lfc\'):\r\n                    self.load(self.lastload)\r\n                    self.run()\r\n                    break\r\n                else:\r\n                    print(\'not found\')\r\n            elif x == \'view\':\r\n                pv = self.map.lastframe()\r\n                print(\'\\n\'.join([\' \'.join(x) for x in\r\n                                 pv]).replace(\'\xe2\x96\xa1\', self.bg))\r\n            elif x == \'save_lfc\':\r\n                print(\'Name format: {group}.{name}-{size}\')\r\n                print(\'name:\')\r\n                name = input(\'>|\')\r\n                if not name:\r\n                    continue\r\n                elif [x for x in name if not\r\n                      (x.isalnum() or x in [\'.\', \'-\'])] or \\\r\n                      name.count(\'-\') not in [0, 1]:\r\n                    print(\'name can consist alpha, numbers, "." and "-" only.\',\r\n                          \'Use one "-"\', sep=\'\\n\')\r\n                    continue\r\n                fld = self.map.lastframe()\r\n                fld = \'\\n\'.join([\'\'.join(y) for y in [x for x in fld]]) \\\r\n                      .replace(\'\xe2\x96\xa0\', \'1\').replace(\'\xe2\x96\xa1\', \'0\')\r\n                with open(f\'lfc/{name}.lfc\', \'w\') as fff:\r\n                    fff.write(fld)\r\n                self.lastload = name\r\n                print(\'saved\')\r\n            elif x == \'cls\':\r\n                self.cls = False if self.cls else True\r\n                print(\'CLS:\', self.cls)\r\n            elif x == \'speed\':\r\n                self.speed = self.speedlist[(self.speedlist.index(self.speed)\r\n                                             + 1) % len(self.speedlist)]\r\n                print(\'Speed:\', self.speed)\r\n            elif x == "allow_repeat":\r\n                self.allow_repeat = False if self.allow_repeat else True\r\n            elif x == \'bg\':\r\n                self.bg = \' \' if self.bg != \' \' else \'\xe2\x97\xa6\'\r\n            elif x == \'\':\r\n                break\r\n            else:\r\n                print(\'unexpected input\')\r\n\r\n    def load(self, name):\r\n        with open(f\'lfc/{name}.lfc\') as lfc:\r\n            data = lfc.read()\r\n        h = len(data.split(\'\\n\'))\r\n        w = max([len(x) for x in data.split(\'\\n\')])\r\n        self.map = Map(h, w)\r\n        data = data.split(\'\\n\')\r\n        self.height = h\r\n        self.width = w\r\n        self.create_map()\r\n        for x in range(h):\r\n            for y in range(len(data[x])):\r\n                self.map.mark(x, y) if data[x][y] == \'1\' else 0\r\n\r\n    def apply_cord(self, matrix):\r\n        mtx = matrix.copy()\r\n        return [[\' \'] + [str(x) for x in range(self.width)]] + \\\r\n               [[str(x)] + mtx[x] for x in range(self.height)]\r\n\r\n    def lfc_navigate(self, group, fileList):\r\n        a = [x for x in fileList if x.startswith(group)]\r\n        group = [x for x in group.split(\'.\') if x]\r\n        opts = {\'group\': [], \'file\': [], \'size\': []}\r\n        for x in a:\r\n            fulldata = x.split(\'.\')[:-1]\r\n            fit = fulldata[len(group):]\r\n            if len(fit) > 1 and fit[0] not in opts[\'group\']:\r\n                opts[\'group\'].append(fit[0])\r\n            elif len(fit) == 1 and fit[0].split(\'-\')[0] not in opts[\'file\']:\r\n                opts[\'file\'].append(fit[0].split(\'-\')[0])\r\n            elif len(fit) == 0 and \'-\' not in fulldata[-1]:\r\n                opts[\'size\'].append(\'default\')\r\n            elif len(fit) == 0 and fulldata[-1].split(\'-\')[1] not in opts[\'size\']:\r\n                opts[\'size\'].append(fulldata[-1].split(\'-\')[1])\r\n        return opts\r\n\r\n\r\nclass Map():\r\n    def __init__(self, height, width):\r\n        self.h, self.w = height, width\r\n        self.field = [[\'\xe2\x96\xa1\' for x in range(width)] for y in range(height)]\r\n        self.frames = []\r\n        self.statistic = {\'Died\': 0, \'Born\': 0}\r\n        self.save()\r\n\r\n    def generate(self):\r\n        stk = FrameStreak(self.field)\r\n        field = self.lastframe()\r\n        cell = stk.next()\r\n        while cell:\r\n            c, n = bl(self.val(*cell)), len([x for x in stk.near()\r\n                                             if bl(self.val(*x))])\r\n            if c:\r\n                if n < 2 or n > 3:\r\n                    field[cell[0]][cell[1]] = \'\xe2\x96\xa1\'\r\n                    self.statistic[\'Died\'] += 1\r\n            else:\r\n                if n == 3:\r\n                    field[cell[0]][cell[1]] = \'\xe2\x96\xa0\'\r\n                    self.statistic[\'Born\'] += 1\r\n            cell = stk.next()\r\n        self.field = copy.deepcopy(field)\r\n\r\n    def mark(self, x, y):\r\n        self.field[int(x)][int(y)] = \'\xe2\x96\xa0\'\r\n\r\n    def pop(self, x, y):\r\n        self.field[int(x)][int(y)] = \'\xe2\x96\xa1\'\r\n\r\n    def save(self):\r\n        self.frames.append(copy.deepcopy(self.field))\r\n\r\n    def val(self, y, x):\r\n        return self.field[y][x]\r\n\r\n    def lastframe(self):\r\n        return copy.deepcopy(self.field)\r\n\r\n\r\nclass FrameStreak():\r\n    def __init__(self, frame):\r\n        self.frame = copy.deepcopy(frame)\r\n        self.x, self.y = -1, 0\r\n        self.height, self.width = len(self.frame), len(self.frame[0])\r\n\r\n    def next(self):\r\n        if self.x + 1 == self.width:\r\n            if self.y + 1 == self.height:\r\n                return None\r\n            else:\r\n                self.x = 0\r\n                self.y += 1\r\n        else:\r\n            self.x += 1\r\n        return (self.y, self.x)\r\n\r\n    def near(self):\r\n        return [((self.y + 1) % self.height, self.x),\r\n                ((self.y + 1) % self.height, (self.x + 1) % self.width),\r\n                ((self.y - 1) % self.height, (self.x + 1) % self.width),\r\n                ((self.y - 1) % self.height, (self.x - 1) % self.width),\r\n                ((self.y + 1) % self.height, (self.x - 1) % self.width),\r\n                (self.y, (self.x + 1) % self.width),\r\n                ((self.y - 1) % self.height, self.x),\r\n                (self.y, (self.x - 1) % self.width)]\r\n\r\n\r\ndef bl(obj):\r\n    return True if obj == \'\xe2\x96\xa0\' else False\r\n\r\n\r\nprint(\'Height: (10 by default)\')\r\nh = input()\r\nprint(\'Width: (10 by default)\')\r\nw = input()\r\nlife = TheLife()\r\nlife.setup(height=int(h)) if h.isdigit() else None\r\nlife.setup(width=int(w)) if w.isdigit() else None\r\nlife.create_map()\r\nlife.run()\r\n'
    with open('game.py', 'wb') as codef:
        codef.write(code)
    print('game installed;')
if not os.path.exists('lfc'):
    lfc = base64.b64decode(b'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')
    with open('LFC.zip', 'wb') as lfcf:
        lfcf.write(lfc)
    shutil.unpack_archive('LFC.zip', 'lfc', 'zip')
    os.remove('LFC.zip')
    print('lfc installed;')
import game
