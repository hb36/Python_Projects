import string

with open('./text2.txt', 'r', encoding='utf-8')as fr:
    text = fr.readlines()
text_str = ''
for line in text:
    l = line.rstrip()
    text_str  += l
dict = {}
for char in text_str:
    dict[char] = dict.get(char,0) + 1
avg = len(text_str) / len(dict)
real_text = ''
for char in text_str:
    if dict[char] < avg:
        real_text += char
# real_text = ''.join([char for char in text_str if dict[char] < avg])
# real_text = list(filter(lambda x: x in string.ascii_letters,text))
print(real_text)

