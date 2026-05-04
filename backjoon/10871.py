n , x = map(int,input().split())
lst = [int(i) for i in input().split()]

b=[]
for i in lst:
    if i < x:
        b.append(i)
    else :
        continue
print(*b)
