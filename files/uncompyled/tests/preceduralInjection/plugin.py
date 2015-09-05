# 2015.09.05 18:13:46 ora legale Europa occidentale
# Embedded file name: plugin.py


class B:

    def hello(self):
        return 'hello'

    def some(self):
        print 'X '


def newHello(self):
    self.some()
    return oldHello(self) + ' world'


oldHello = B.hello
B.hello = newHello
print B().hello()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\preceduralInjection\plugin.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:46 ora legale Europa occidentale
