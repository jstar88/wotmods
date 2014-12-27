import types
class A:
    def test(self):
        print "A"

class B:
    @classmethod
    def ciao(place,self):
        self.test()
    
    def test(self):
        print "B"
        



a = A()      
a.ciao = types.MethodType(B.ciao,a)
a.ciao()