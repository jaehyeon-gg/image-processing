n = [i for i in input().upper()]
#print(n)

d = {}
for i in n:
    d[i] = d.get(i,0)+1
#print(d)

#print(d)
max_value = max(d.values())
max_b = [k for k,v in d.items() if v == max_value]
#print(max_b)
if len(max_b) == 1:
    print(max_b[0])
else :
    print("?")

# d = {"a":3}
# print(d.get("b",0))
# print(d)