# -*-encoding = 'utf-8'-*-
import re
import zipfile

path = 'E:\Python36\projects\python_challenges\channel\\'
file_name = '90052'
comments = []
zip = zipfile.ZipFile(path + "channel.zip", 'r')

while True:
    comments.append(zip.getinfo(file_name + '.txt').comment.decode())
    data = open(path + file_name + '.txt', 'r', encoding='utf-8').read()
    find_name = re.search(r"(Next nothing is )([0-9]+)", data)
    if find_name:
        file_name = find_name.group(2)
    else:
        # print(data)
        break

print("".join(comments))
