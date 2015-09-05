# 2015.09.05 18:13:46 ora legale Europa occidentale
# Embedded file name: objplugin.py


class B:

    def hello(self):
        return 'hello'

    def some(self):
        print 'X '


class A:

    def __init__(self, objo):
        self.obj = objo

    def newHello(self):
        self.obj.some()
        return self.oldHello() + ' world'


b = B()
a = A(b)
a.oldHello = b.hello
b.hello = a.newHello
print b.hello()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\objectInjection\objplugin.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:46 ora legale Europa occidentale
