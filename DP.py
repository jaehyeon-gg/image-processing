# A는 r x c 행렬
def solve(A) :
    # 누적값을 저장할 dp 행렬 생성
    dp =[[0 for j in range(len(A[0]))] for i in range(len(A))]
    
    # dp의 초기값 설정
    dp[0][0] = A[0][0]
    
    # dp의 초기 각 끝 행/열 값 설정
    for i in range(1, len(A)) : #행
        dp[i][0] = dp[i-1][0] + A[i][0]
    for j in range(1,len(A[0])): #열
        dp[0][j] = dp[0][j-1] + A[0][j]
    
    for i in range(1,len(A)):
        for j in range(1,len(A[0])):
            dp[i][j] = max(dp[i-1][j],dp[i][j-1]) + A[i][j]
    
    return dp[len(A)-1][len(A[0])-1]

A = [
    [5, 1, 3, 2],
    [2, 8, 1, 4],
    [1, 2, 9, 1]
]

print(solve(A))