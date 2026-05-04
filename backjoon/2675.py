t = int(input())

lst = []

for i in range(t):
    a,b = input().split()
    lst.append((int(a),b))
# print(lst)

for k,v in lst:
    result = ""
    for ch in v:
        result = result + ch*k
    print(result)



# while True:
#     try:
#         a , b = input().split()
#         r = int(a)
#         result = ""

#         for ch in b:
#             result += ch*r

#         print(result)
    
#     except EOFError:
#         break