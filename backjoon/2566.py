lst = []
for i in range(9):
    row = [int(a) for a in input().split()]
    lst.append(row)
#print(lst)
m = 0
for i in range(9):
    for j in range(9):
        if m <= lst[i][j]:
            m = lst[i][j]
            a ,b = i+1, j+1

print(m)
print("{} {}".format(a,b))