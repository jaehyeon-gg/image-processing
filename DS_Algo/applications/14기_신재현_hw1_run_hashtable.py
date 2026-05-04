import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from hashTable.hashtable import HashTable

ht = HashTable()



#문제 input
exam = ("123 50 224 30 123 25 24 25 123 40 224 77 S 123 25 D 123 25 D 123 40 D 224 100 ")
#exam1 = "1 10 1 20 1 30 D 1 20 "
#exam2 = "123 50 224 30 123 25 24 25 123 40 224 77 S 123 25 D 123 25 D 123 40 D 224 100 S 224 30 "
tokens = exam.split()

i=0

while i < len(tokens) :
    if tokens[i] == 'S':
        print(ht.search(int(tokens[i+1]),tokens[i+2]),end=' ')
        i = i+3
    elif tokens[i] == 'D' :
        print(ht.delete(int(tokens[i+1]),tokens[i+2]),end=' ')
        i = i+3
    else :
        ht.insert(int(tokens[i]),tokens[i+1])
        i = i+2



