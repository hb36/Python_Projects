# -*-encoding = 'utf-8'-*-
from urllib import request
import requests
import pickle

# save the file
# url = 'http://labfile.oss.aliyuncs.com/courses/408/banner.p'
# # data = request.urlopen(url).read().decode('utf-8')
# response = requests.get(url)
# data = response.text
# db = pickle.dumps(data)
# print(db)
# with open('text1_5.p', 'wb')as fw:
#     fw.write(db)



data_file = open('banner.p', 'rb')
data = pickle.load(data_file)
# print(data)
for line in data:
    print(''.join(i[0] * i[1] for i in line))
