import re
import string

# method_1

text = open('./text3.txt', 'r', encoding='utf-8').read()
text_list = re.findall('[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]', text)
print("".join(text_list))



# method_2

# text = open('./text3.txt', 'r', encoding='utf-8').read()
# lows = string.ascii_lowercase
# ups = string.ascii_uppercase
# text_list = ""
# for i in range(len(text) - 9):
#     if text[i] in lows and text[i + 1] in ups and text[i + 2] in ups \
#             and text[i + 3] in ups and text[i + 4] in lows and text[i + 5] in ups \
#             and text[i + 6] in ups and text[i + 7] in ups and text[i + 8] in lows:
#         text_list += text[i + 4]
#
# n = len(text) - 8
# if text[n] in lows and text[n + 1] in ups and text[n + 2] in ups \
#             and text[n + 3] in ups and text[n + 4] in lows and text[n + 5] in ups \
#             and text[n + 6] in ups and text[n + 7] in ups:
#     text_list += text[n + 4]
# print(text_list)



# method_3

# def is_capital(list, index):
#     flag = False
#     for n in range(3):
#         if 65 <= ord(list[index + n]) and 90 >= ord(list[index + n]):
#             flag = True
#         else:
#             return False
#     return flag
#
#
# if __name__ == '__main__':
#     with open('./text3.txt', 'r', encoding='utf-8')as fr:
#         text = fr.readlines()
#
#     lower_letters = ''
#     for line in text:
#         linelist = list(line.strip())
#         # print(linelist)
#         i = 0
#         while i < len(linelist) - 7:
#             if 97 <= ord(linelist[i]) <= 122 and is_capital(linelist, i + 1)\
#                 and 97 <= ord(linelist[i + 4]) <= 122 and is_capital(linelist, i + 5)\
#                     and 97 <= ord(linelist[i + 8]) <= 122:
#                 # print(linelist[i + 4])
#                 lower_letters += linelist[i + 4]
#             i += 1
#     print(lower_letters)
