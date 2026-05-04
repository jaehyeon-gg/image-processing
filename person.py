class Person : 

    def __init__(self,name,age): #생성자를 사용할 때도 첫번쨰 parameter는 무조건 self
        self.name = name
        self.age = age
    def hello(self): #self를 먼저 해줘야하는 이유는?
        print(f"Hello. I'm {self.name}!")
    def update_age(self,age):
        if age < 0:
            raise ValueError('나이는 음수일 수 없습니다.')
        else:
            self.age = age
            print(f"Now I'm {self.age} years old.")

if __name__ =='__main__' :
    man = Person("John",30)
    man.hello() #man 안에 있는 객체를 가져올 수 있음.
    man.update_age(-1)

#객체 지향 4대 주요 개념
#1. 상속 : 클래스 상속
## 기존 클래스(부모)- 범위 넓은 거에서 좁은 클래스(자식)으로 대물림.
### super(). -> 부모클래스가 정의한 것을 자식 클래스에서 가져올때
####부모클래스에서 정의된 걸 자식 클래스에서도 메소드를 재정의해서 사용 가능.


    
