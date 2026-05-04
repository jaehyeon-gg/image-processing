class SortableArray:
    def __init__(self,array):
        self.array = array
    def partition(self,left_pointer,right_pointer):
        #pivot은 항상 오른쪽 끝
        pivot_index = right_pointer
        pivot = self.array[pivot_index]

        #right pointer 는 pivot 바로 왼쪽부터 시작
        right_pointer -=1

        while True:
            #left pointer 이동(pivot 보다 작을 때)
            while self.array[left_pointer] < pivot:
                left_pointer +=1
            
            #right pointer 이동(pivot보다 클 때)
            while self.array[right_pointer] > pivot:
                right_pointer -= 1
            
            #교차 여부 확인.
            if left_pointer >= right_pointer :
                break
            else :
                # swap
                self.array[right_pointer],self.array[left_pointer] = self.array[left_pointer],self.array[right_pointer]

                # 왼쪽 pointer 이동
                left_pointer +=1
        
        self.array[left_pointer],self.array[pivot_index] = self.array[pivot_index],self.array[left_pointer]

        return left_pointer
    
    def quicksort(self,left_index,right_index):
        
        #base case
        if right_index - left_index <= 0:
            return
        
        #partition 수행 해서 pivot_index 반환
        pivot_index = self.partition(left_index,right_index)

        # left 정렬
        self.quicksort(left_index , pivot_index -1)

        # right 정렬
        self.quicksort(pivot_index +1, right_index)