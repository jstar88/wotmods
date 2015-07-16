import types
import game

class A:
    @classmethod
    def p(cls):
        global old
        old = game.k
        game.k = cls.f
        
    @classmethod
    def f(claz):
        old()
        print 'hi'
        
class B(A):
    pass
A.p()
#B.p()

game.k()