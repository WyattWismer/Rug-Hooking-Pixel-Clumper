from PIL import Image
from so import f
im = Image.open('turtle.jpg')
im.convert('HSV')
