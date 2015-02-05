from test2 import checkPluginsImports
import __builtin__

checkPluginsImports('demoPlugin',[('test',['x'])])

for k,v in  __builtin__.modules.iteritems():
    if not k.startswith("_"):
        globals()[k] = v



x()