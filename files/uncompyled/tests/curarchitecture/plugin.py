# 2015.09.05 18:13:45 ora legale Europa occidentale
# Embedded file name: plugin.py
from util import *
modules = [('orig', ['Orig'])]

def errf(module):
    print "module '" + str(module) + "' not found"


exec getCodeForImports(modules, errf)

class A:

    @staticmethod
    def newtest(self):
        print 'world'


c = Orig()
old = override(Orig, 'test', A.newtest)
c.test()
override(Orig, 'test', old)
c.test()
print ''
c = Orig()
old = override(c, 'test', A.newtest)
c.test()
Orig().test()
print ''
c = Orig()
override(c, 'test2', A.newtest)
print hasattr(Orig, 'test2')
print hasattr(c, 'test2')
c.test2()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\curarchitecture\plugin.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:45 ora legale Europa occidentale
