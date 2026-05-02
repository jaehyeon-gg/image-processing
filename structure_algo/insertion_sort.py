""" def insertion_sort(array): 
    for index in range(1,len(array)):
        temp_value = array[index]
        position = index-1

        while position >= 0:
            if array[position] > temp_value:
                array[position +1] =array[position]
                position -=1
            else :
                break
        array[position+1] = temp_value
    return array

print(insertion_sort([4,2,7,1,3]))
 """
def insertion_sort(A: list) -> None:
    """제자리(in-place) 삽입 정렬. O(n²)"""
    # TODO: A[i]를 new_item에 꺼낸 뒤, 앞쪽 정렬된 구간(loc = i-1부터)을
    #       오른쪽으로 한 칸씩 밀면서 new_item이 들어갈 자리를 찾아 삽입하라.
    for i in range(1,len(A)):
        new_item = A[i]
        loc = i-1
        while loc >= 0 :
            if A[loc] > new_item:
                A[loc+1]=A[loc]
                loc = loc -1
            else :
                break
        A[loc+1]=new_item
    return A

print(insertion_sort([4,2,7,1,3]))
