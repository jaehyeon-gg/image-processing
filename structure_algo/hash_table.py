#1
""" lst1=[1,2,3,4,5]
lst2=[0,2,4,6,8]
dic={}
for i in lst1:
    dic[i] = True


result =[]

for i in lst2:
    if i in dic:
        result.append(i)
print(result)
 """

#2
lst1 = ['a','b','c','d','c','e','d']
dic = {}
""" for i in lst1:
    dic[i] = lst1.count(i)
    if dic[i] >= 2:
        print(i)
        break """

""" for i in lst1:
    if i in dic:
        print(i)
        break
    dic[i] = True

 """
#3-1

""" import string

sentence = "the quick brown box jumps over a lazy dog"
dic ={}

for i in string.ascii_lowercase:
    dic[i] = 0

for i in dic:
    if i in sentence:
        continue
    else :
        print(i)
        break
#3-2
lst = list(map(chr,range(97,123)))
sentence = "the quick brown box jumps over a lazy dog"

sentence ="".join(sentence.split())
dic ={}
for s in sentence:
    dic[s] = True
for s in lst:
    if s not in dic:
        print(s)
 """

#4
chr = "minimum"
dic = {}

for i in chr:
    if i not in dic:
        dic[i] = 1
    else :
        dic[i] +=1

for i in dic:
    if dic[i] < 2:
        print(i)
        break