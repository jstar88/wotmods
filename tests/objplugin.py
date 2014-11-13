
class B():
    def hello(self):
        return "hello"
    def some(self):
        print 'X '

class A():
    def __init__(self,objo):
        self.obj = objo

    def newHello(self):
        self.obj.some()
        return self.oldHello() + ' world'


b =B()
a = A(b)

a.oldHello = b.hello
b.hello = a.newHello
print b.hello()