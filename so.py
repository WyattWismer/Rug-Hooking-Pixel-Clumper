from functools import reduce
import operator

def e(im):
    h = im.convert("L").histogram()
    lut = []
    for b in range(0, len(h), 256):
        # step size
        step = reduce(operator.add, h[b:b+256]) / 255
        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + h[i+b]
    # map image through lookup table
    return im.point(lut*im.layers)

def f(im):
    im = im.convert('HSV')
    for i in range(im.width):
        for j in range(im.height):
            h,s,v = im.getpixel((i,j))
            im.putpixel((i,j),(h,s,100))
    return im
