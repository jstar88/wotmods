import f
from g import Some

class A():
    @staticmethod
    def newApple():
        return 'green '+oldApple()
    
    @staticmethod
    def newSome(self):
        return oldSome(self)+'thing'

    def inject(self):
        # since procedural code is hard to override from inside class
        inj()


def inj():
    global oldApple,oldSome
    if 'oldApple' in globals() or 'oldSome' in globals():
        raise Exception( 'global vars already definied' )
    oldApple = f.apple
    oldSome = Some.some
    f.apple = A.newApple
    Some.some = A.newSome


A().inject()
print Some().some()
print f.apple()