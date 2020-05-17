from collections import defaultdict as dd
from sys import argv
from PIL import Image
from PIL import ImageFilter
from pprint import pprint as pp

#im = Image.open

def load_image(path):
    im = Image.open(path)
    return im

def normalize_brightness(im):
    im = im.convert('HSV')
    for i in range(im.width):
        for j in range(im.height):
            h,s,v = im.getpixel((i,j))
            im.putpixel((i,j),(h,s,100))
    return im

def blur(im,radius):
    im = im.convert(mode='RGB')
    return im.filter(ImageFilter.GaussianBlur(radius))

def quantize(im, num_colors):
    im = im.convert(mode='RGB')
    im = im.quantize(colors=num_colors)
    return im

def stats(im):
    im = im.convert(mode='RGB')
    cnt = dd(int)
    n = im.width
    m = im.height
    for i in range(n):
        for j in range(m):
            cnt[im.getpixel((i,j))] += 1
    num_pixels = n*m
    res = {}
    for key in cnt:
        res[key] = round(cnt[key]/num_pixels*100,2)
    return res

if __name__ == "__main__":
    if len(argv) < 3:
        print("Wrong number of arguments!\n")
        print("Usage:")
        print("Example:")
        print("         python main.py example.png 6")
        print("OR:")
        print("         python main.py example.png 6")
        exit()
    fname = argv[1]
    num_colors = int(argv[2])
    im = load_image(fname)
    im.show()
    """
    im = normalize_brightness(im)
    im.show()
    im = blur(im,1)
    im.show()
    """
    im = quantize(im, num_colors)
    im.show()
    st = stats(im)
    pp(st)

