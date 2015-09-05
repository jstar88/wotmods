# 2015.09.05 18:13:43 ora legale Europa occidentale
# Embedded file name: test2.py
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
game.k()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\test2.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:43 ora legale Europa occidentale
