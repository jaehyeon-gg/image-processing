#1927 최소 heap 구현
''' x 자연수면 insert
x= 0이면 꺼내기. min
 '''

class MinHeap:
    def __init__(self):
        self.A=[]

    def insert(self,x):
        self.A.append(x) #끝에 x를 추가
        i = len(self.A)-1
        self.percolateUp(i)


    def percolateUp(self,k):
        parent = (k-1)//2 #k == 0 루트일경우에는 부모 없음.
        if k>0 and self.A[parent] > self.A[k]:
            self.A[k],self.A[parent] =self.A[parent],self.A[k]
            self.percolateUp(parent)
    
    def popmin(self):
        if len(self.A) == 0:
            return 0
        else :
            if len(self.A) == 1:
                min = self.A.pop()
            else :
                min = self.A[0] #pop은 오래걸리거같음.
                self.A[0] = self.A.pop()
                self.percolateDown(0)
        return min

    def percolateDown(self,i):
        child = 2*i+1
        right = 2*i+2
        if child < len(self.A):
            if right <len(self.A) and self.A[child] > self.A[right]:
                child = right #더 작은 값이 child
            if self.A[i] > self.A[child]:
                self.A[i] ,self.A[child] = self.A[child],self.A[i]
                self.percolateDown(child)




import sys
input = sys.stdin.readline

mh = MinHeap()

result = []

for _ in range(int(input().strip())):
    x = int(input().strip())
    if x == 0:
        result.append(str(mh.popmin()))
    else :
        mh.insert(x)

print('\n'.join(result))
