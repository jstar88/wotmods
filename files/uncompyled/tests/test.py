# 2015.09.05 18:13:43 ora legale Europa occidentale
# Embedded file name: test.py
import types

class A:

    def test(self):
        print 'A'


class B:

    @classmethod
    def ciao(place, self):
        self.test()

    def test(self):
        print 'B'


a = A()
a.ciao = types.MethodType(B.ciao, a)
a.ciao()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\test.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:43 ora legale Europa occidentale
