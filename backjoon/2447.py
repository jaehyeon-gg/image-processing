import sys
sys.setrecursionlimit(10**7)

def star(n):
    # 기본 패턴 (가장 작은 단위)
    if n == 1:
        return ["*"]
    
    prev = star(n // 3)
    result = []

    for i in range(3):
        for line in prev:
            if i == 1:
                # 가운데 블록은 공백
                result.append(line + " " * (n // 3) + line)
            else:
                result.append(line * 3)

    return result


# 입력 받기 (3의 거듭제곱)
N = int(sys.stdin.readline().strip())

pattern = star(N)
print("\n".join(pattern))