# -*-coding=utf-8-*-
# 将图片转化为字符画
from PIL import Image

ascii_char = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")


def get_char(r, g, b, alpha):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = (r * 30 + g * 59 + b * 11 + 50) / 100

    index = length / 256
    return ascii_char[int(gray * index)]


if __name__ == '__main__':
    img = Image.open('E:\Python36\projects\picture_to_ascii\dlam.png').convert('RGBA')
    width = img.size[0]
    height = img.size[1]
    txt = ''
    for h in range(height):
        for w in range(width):
            pixel = img.getpixel((w, h))
            txt += get_char(*pixel)
        txt += '\n'
    print(txt)
    with open('./dlam_2.txt', 'w', encoding='utf-8')as fw:
        fw.write(txt)