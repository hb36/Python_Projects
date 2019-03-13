from random import choice
list = []
for i in range(4):
    for j in range(4):
        if i + j == 3:
        # (i,j) = choice([i,j])
# (i, j) = choice([i, j] for i in range(4) for j in range(4) )
            print((i,j))
            list.append(list(i,j))
print(choice(list))