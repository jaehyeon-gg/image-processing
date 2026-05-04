n=[]

for i in range(10):
    a = int(input())
    n.append(a)

b =[]

for i in n:
    b.append(i%42)

print(len(set(b)))
