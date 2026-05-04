""" def twice(array,index=0):
    if index >= len(array):
        return array
    else :
        array[index] = array[index]*2
        return twice(array,index +1)

lst = [1,2,3,4]

#print(twice(lst))
 """
""" 
def sum(array):
    if len(array) == 1:
        return array[0]
    return array[0] + sum(array[1:len(array)])

print(sum([1,2,3,4,5,6])) """
""" 
def reverse(chr):
    if len(chr) == 1:
        return chr[0]
    return reverse(chr[1:len(chr)])+chr[0]

print(reverse("bbbaaa"))
 """
""" 
def count_x(chr):
    if len(chr) == 0:
        return 0
    if chr[0] == 'x':
        return count_x(chr[1:len(chr)]) + 1
    else :
        return count_x(chr[1:len(chr)]) 

print(count_x("axbxcxde"))
     """
""" 
def num_of_path(n):
    if n < 0 :
        return 0
    elif n == 1 or n == 0:
        return 1
    else :
        return num_of_path(n-1) + num_of_path(n-2) + num_of_path(n-3)

print(num_of_path(5))
 """
""" 
def anagram_of(chr):
    result = []
    for word in anagram_of(chr[1:len(chr)]):
        for i in range(len(chr)+1):
            result.insert(i,) """


def max(array):
    if len(array) == 1:
        return array[0]
    max_of_reminder = max(array[1:len(array)])
    if array[0] > max_of_reminder:
        return array[0]
    else :
        return max_of_reminder