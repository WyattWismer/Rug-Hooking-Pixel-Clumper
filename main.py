from collections import OrderedDict as OD
from sys import argv
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from pprint import pprint as pp
from math import sqrt

class color:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    def tup(self):
        return (self.r,self.g,self.b)
    def __eq__(self, oth):
        if not oth: return False
        return self.r == oth.r and self.g == oth.g and self.b == oth.b
    def __repr__(self):
        return str(self.tup())
    def __key(self):
        return (self.r, self.g, self.b)
    def __hash__(self):
        return hash(self.__key())
    def dist(self,oth):
        return sqrt(pow(self.r - oth.r,2) + pow(self.g - oth.g,2) + pow(self.b - oth.b,2))

def hexToInt(hx):
    def f(h):
        if ord('A') <= ord(h) <= ord('Z'):
            return ord(h)-ord('A')+10
        return int(h)
    return f(hx[0])*16 + f(hx[1])

def hexToColor(hx):
    hx = hx.upper()
    r,g,b = hexToInt(hx[0:2]), hexToInt(hx[2:4]), hexToInt(hx[4:6])
    c = color(r,g,b)
    return c

def load_colors(fname):
    colors = []
    for line in open(fname):
        if len(line.strip()) == 0: continue
        c = hexToColor(line)
        colors.append(c)
    return colors

def stats(im, colors, ignore):
    im = im.convert(mode='RGB')
    cnt = OD()
    for c in colors:
        if c not in ignore:
            cnt[c] = 0
    n = im.width
    m = im.height
    num_pixels = 0
    for i in range(n):
        for j in range(m):
            r,g,b = im.getpixel((i,j))
            nw = color(r,g,b)
            best = None
            for c in colors:
                if best == None or nw.dist(c) < nw.dist(best):
                    best = c
            if best not in ignore:
                cnt[best] += 1
                num_pixels += 1
    pairs = [(cnt[key]/num_pixels*100,key) for key in cnt]
    pairs.sort(reverse=True)
    res = OD()
    for p,k in pairs:
        res[k] = round(p,2)
    return res

def display(stats):
    WINDOW_SIZE=(500,1000) # width, height
    WINDOW_COLOR=(200,200,200)
    bar_height = WINDOW_SIZE[1]//len(stats)
    drawn = Image.new('RGB', WINDOW_SIZE, WINDOW_COLOR)
    d = ImageDraw.Draw(drawn)
    mper = max(stats.values())
    for i,c in enumerate(stats):
        per = stats[c]
        d.rectangle(((0,bar_height*i),(WINDOW_SIZE[0]*per/mper,bar_height*(i+1)-1)),c.tup())
    drawn.show()

def load_image(path):
    im = Image.open(path)
    return im

if __name__ == "__main__":
    if len(argv) < 3 or len(argv) > 4:
        print("Wrong number of arguments!\n")
        print("Usage:")
        print("         python main.py IMAGE COLORS {BLACKLIST}\n")
        print("Example:")
        print("         python main.py example.png colors.txt")
        print("Or:")
        print("         python main.py turtle2.jpg colors.txt blacklist.txt")
        exit()
    fname = argv[1]
    color_fname = argv[2]
    ignore = None
    if len(argv) == 4:
        ignore = load_colors(argv[3])
    im = load_image(fname)
    colors = load_colors(color_fname)
    im.show()
    st = stats(im, colors, ignore)
    display(st)
    pp(st)
