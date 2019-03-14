# -*- coding=utf-8 -*-
from MyQR import myqr
import os


def qr(input_file, output_file):
    url = 'https://github.com/hb36'
    myqr.run(
        words=url,
        picture=input_file,
        colorized=True,
        save_name=output_file,
        save_dir='E:\Python36\projects\qr_code\img'
    )


def main():
    path = 'E:\Python36\projects\qr_code\Sources'
    for root, dirs, files in os.walk(path):
        for file in files:
            input_file = path + '\\' + file
            if file.split('.')[1] == 'jpg':
                output_file = 'qr_' + file.split('.')[0] + '.png'
            else:
                output_file = 'qr_' + file
            qr(input_file, output_file)


if __name__ == '__main__':
    main()
