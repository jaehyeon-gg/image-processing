import sys

def cantor(arr, start,size):
    if size == 1:
        return
    
    third = size // 3

    #가운데를 공백으로
    for i in range(start+third , start+2*third):
        arr[i] = ' '
    
    #왼쪽 오른쪽 재귀
    cantor(arr,start,third)
    cantor(arr,start+2*third, third)


for line in sys.stdin:
    line = line.strip()
    
    if not line:
        continue

    n = int(line)
    size = 3**n

    arr = ['-']*size
    cantor(arr,0,size)
    print(''.join(arr))