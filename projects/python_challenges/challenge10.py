# -*-encoding='utf-8'-*-
strings = ['1', '11']

for i in range(1, 31):
    j = 0
    temp = ''
    while j < len(strings[i]):
        count = 1
        while j < len(strings[i]) - 1 and strings[i][j] == strings[i][j + 1]:
            j += 1
            count += 1
        temp = '%s%d%c' % (temp, count, strings[i][j])
        j += 1

    strings.append(temp)
print(len(strings[30]))
