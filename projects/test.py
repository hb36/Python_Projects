import os

url = 'https://www.shiyanlou.com/courses/1126/Source.zip'

path = 'E:\Python36\projects\qr_code\Sources'
for root, dir, file in os.walk(path):
    for f in file:
        print('qr_' + f)
        print(path + '\\' + f)
