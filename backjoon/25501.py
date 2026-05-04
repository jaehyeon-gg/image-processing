t = int(input())
lst = []

for i in range(t):
    a = input()
    lst.append(a)


def recursion(s, l, r,cnt = 0):
    cnt = cnt +1

    if l >= r: 
        return 1 , cnt
    elif s[l] != s[r]: 
        return 0 , cnt 
    else: 
        res , cnt = recursion(s,l+1,r-1,cnt)
        return res, cnt 

def isPalindrome(s):
    return recursion(s, 0, len(s)-1)

for i in lst:
    result , cnt = isPalindrome(i)
    print("{} {}".format( result , cnt))

# print('ABBA:', isPalindrome('ABBA'))
# print('ABC:', isPalindrome('ABC'))

# def f(a, cnt=0):
#     a = a + 1
#     cnt = cnt + 1
#     return a, cnt

# print(f(1))
# print(f(2))
# print(f(3, 0))
# print(f(4))