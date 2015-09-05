# 2015.09.05 18:13:45 ora legale Europa occidentale
# Embedded file name: f.py
modules = [('test', ['x'])]
from test3 import ModulesManager
map(lambda v: globals().__setitem__(v[0], v[1]), ModulesManager(modules).getGlobals().items())
x()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\imports\f.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:45 ora legale Europa occidentale
