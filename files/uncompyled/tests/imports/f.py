modules = [('test',['x'])]


from test3 import ModulesManager

map(lambda v: globals().__setitem__(v[0],v[1]) , ModulesManager(modules).getGlobals().items())
'''
from test2 import checkPluginsImports
import __builtin__
checkPluginsImports('demoPlugin',modules)
for k,v in  __builtin__.modules.iteritems():
    if not k.startswith("_"):
        globals()[k] = v

'''

x()
