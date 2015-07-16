import types
def f ():
    print 'ciao'


class A():
    def __init__(self):
        print 'initied'

    def hello(self):
        print "hello1"
        self.some()
    def some(self):
        print ' A '

class B():
    
    @classmethod
    def newHello(clas,self):
        print 'hello2'
        Manager.getInstance(clas).some()
        Manager.getInstance(clas).oldHello()
        self.some()
    
    def some(self):
        print ' B '
    
    @classmethod
    def f(clas):
        Manager.getInstance(clas).some()
    
class Manager:
    instance = None
    @staticmethod
    def getInstance(clas):
        if Manager.instance is None:
            Manager.instance = clas()
        return Manager.instance

A = type('A',(object,),dict(A.__dict__))
o = A.__new__(A)


B.oldHello = types.MethodType(A.hello,o)
A.hello = types.MethodType(B.newHello,o)


a = A()
a.hello()   

# f = B.f
# f()