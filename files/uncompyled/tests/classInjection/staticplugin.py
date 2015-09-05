# 2015.09.05 18:13:44 ora legale Europa occidentale
# Embedded file name: staticplugin.py


class B:

    def hello(self):
        return 'hello'

    def some(self):
        print 'X '


class A:

    @staticmethod
    def newHello(self):
        self.some()
        return A.oldHello(self) + ' world'

    def inject(self):
        A.oldHello = B.hello
        B.hello = A.newHello


A().inject()
print B().hello()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\classInjection\staticplugin.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:44 ora legale Europa occidentale
