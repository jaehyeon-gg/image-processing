a = [15,4,3,67,5]
for i in range(len(a)-1):
    if a[i] < a[i+1]:
        max = a[i+1]

print(max)