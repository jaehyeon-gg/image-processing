n = int(input())
lst = [int(x) for x in input().split()]

max_lst = max(lst)

for i in range(n):
    lst[i] = (lst[i]/max_lst)*100

print(round(sum(lst)/len(lst),2))