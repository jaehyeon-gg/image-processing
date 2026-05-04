n = int(input())

def hanoi(n,start, mid, end):

    if n==1:
        print(start,end)
        return
    

    #1단계 : n-1 개를 start -> mid
    hanoi(n-1,start,end,mid)

    #2단계 : 가장 큰 원판 이동
    print(start,end)
    
    #3단계 : n-1개를 mid -> end
    hanoi(n-1,mid,start,end)

print(2**n -1)
hanoi(n,1,2,3)

