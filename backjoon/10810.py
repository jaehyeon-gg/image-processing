n = [int(i) for i in range(1,31)]

chk = []

for i in range(28):
    a = int(input())
    chk.append(a)

result = [x for x in n if x not in chk]
print(result[0])
print(result[1])