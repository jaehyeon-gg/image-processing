n , m = map(int,input().split())
lst = [int(i) for i in range(1,n+1)]

for i in range(m):
    a,b = map(int,input().split())
    lst[a-1:b] = lst[a-1:b][::-1]
print(*lst)
    
