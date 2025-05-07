class Tester():
    state: str = 'Initial'

    def __init__(self):
        print('--', Tester.state, '--')
        return
    
    @staticmethod
    def test(toustand):
        Tester.state = toustand


print(Tester.state)
a = Tester()
b = Tester()

a.test('x')
print(a.state)
print(b.state)

b.test('y')
print(a.state)
print(b.state)
