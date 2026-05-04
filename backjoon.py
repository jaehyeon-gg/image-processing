#문제 두 정수 a,b, 가 주어졌을 때 a,b를 비교하는 프로그램
a, b = map(int,input().split())
#print(a,b)

if a < b :
    print('<')
elif a > b:
    print('>')
else :
    print("==")

#입력 : 시험점수
score = int(input("시험점수 : "))


