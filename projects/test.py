import os
from PIL import Image

img = Image.open('E:\Python36\projects\mosaic_img\\test-data\set1\img-6.png')

print(img.size)
img.thumbnail((20, 20))
print(img.size)
img.thumbnail((20, 15))
print(img.size)
img.thumbnail((15, 20))
print(img.size)
