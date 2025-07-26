class Calc:
    def add(self, a, b):
        return a + b
    def sub(self, a, b):
        return a - b
    def mul(self, a, b):
        return a * b
    def div(self, a, b):
        return a / b

c = Calc()
print(c.add('1', 2))
print(c.sub(5, '3'))
print(c.mul(2, None))
print(c.div(10, 0))
