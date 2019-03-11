from PIL import Image

ascii_char = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")


def get_char(r, g, b, alpha):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


img = Image.open('E:\Python36\projects\picture_to_ascii\dlam.png').convert('RGBA')
width = img.size[0]
height = img.size[1]
txt = ''
for w in range(width):
    for h in range(height):
        pixel = img.getpixel((w, h))
        txt += get_char(*pixel)
    txt += '\n'
print(txt)
