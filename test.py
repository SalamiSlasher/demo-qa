class A:
    def __init__(self, a):
        self.x = a

    def f(self):
        return self.x


if __name__ == '__main__':
    func = A.f

    a = A(2)

    print(func(a))
