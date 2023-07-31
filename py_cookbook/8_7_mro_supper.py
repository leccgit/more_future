class A:
    def spam(self):
        print('A.spam')
        super().spam()  # 按 __mro__, 调用下一个继承的方法


class B:
    def spam(self):
        print('B.spam')


class C:
    def spam(self):
        print('C.spam')


class Do1(A, B):
    pass


class Do2(A, C):
    pass


if __name__ == '__main__':
    t_d1 = Do1()
    t_d1.spam()
    print(A.spam)
    print(B.spam)
    print('*' * 20)
    t_d2 = Do2()
    t_d2.spam()
    print(A.spam)
    print(C.spam)
