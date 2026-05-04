a,b = map(int,input().split())
A =[]
for i in range(a):
    row = list(map(int,input().split()))
    A.append(row)

B =[]
for i in range(a):
    row = list(map(int,input().split()))
    B.append(row)

C =[[0]*b for i in range(a)]
# print(C)
for i in range(a):
    for j in range(b):
        C[i][j] = A[i][j]+B[i][j]
for row in C:
    print(*row)
#print(C[i][j] , end = "" for i in range(a) for j in range(b) )
