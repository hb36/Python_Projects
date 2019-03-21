import zipfile

path = 'E:\Python36\projects\python_challenges\channel\\'
file_name = '90052'

zip = zipfile.ZipFile('E:\Python36\projects\python_challenges\channel\channel.zip', 'r')

print(zip.getinfo('90052.txt').comment.decode())
