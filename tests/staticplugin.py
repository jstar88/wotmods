
#1
class B():
    def hello(self):
        return "hello"
    def some(self):
        print 'X '

class A():
    @staticmethod
    def newHello(self):
        self.some()
        return A.oldHello(self) + ' world'

    def inject(self):
        A.oldHello = B.hello
        B.hello = A.newHello

A().inject()
print B().hello()