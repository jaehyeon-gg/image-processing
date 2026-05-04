def p(n):
    if n == 1 :
        return 1
    if n == 0:
        return 0 
    return p(n-1) + p(n-2)


a = int(input())
print(p(a))

