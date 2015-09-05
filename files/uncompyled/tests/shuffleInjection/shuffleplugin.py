# 2015.09.05 18:13:46 ora legale Europa occidentale
# Embedded file name: shuffleplugin.py
import f
from g import Some

class A:

    @staticmethod
    def newApple():
        return 'green ' + oldApple()

    @staticmethod
    def newSome(self):
        return oldSome(self) + 'thing'

    def inject(self):
        inj()


def inj():
    global oldSome
    global oldApple
    if 'oldApple' in globals() or 'oldSome' in globals():
        raise Exception('global vars already definied')
    oldApple = f.apple
    oldSome = Some.some
    f.apple = A.newApple
    Some.some = A.newSome


A().inject()
print Some().some()
print f.apple()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\shuffleInjection\shuffleplugin.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:46 ora legale Europa occidentale
