import os

url = 'https://www.shiyanlou.com/courses/1126/Source.zip'

while True:
    data = input(">>>")
    if 10 < len(data):
        print("over index")
        break
    else:
        print(data)
