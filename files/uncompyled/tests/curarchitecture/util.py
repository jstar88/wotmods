# 2015.09.05 18:13:45 ora legale Europa occidentale
# Embedded file name: util.py
import types

def override(t, name, newFunc):
    if type(newFunc) != types.FunctionType and type(newFunc) != types.MethodType:
        raise Exception('third arg must be a function')
    if type(name) is not str:
        raise Exception('second arg must be a string func name')
    tmp = None
    if hasattr(t, name):
        tmp = getattr(t, name)
    if not isinstance(t, type):
        setattr(t, name, lambda : newFunc(t))
    else:
        setattr(t, name, newFunc)
    return tmp


class ModulesManager(object):

    def __init__(self, modules = {}):
        self.modules = {}
        self.loads(modules, True)

    def load(self, module, cache = True):
        if type(module) is tuple:
            module_name = module[0]
            func_names = module[1]
        else:
            module_name = module
            func_names = []
        if module_name in self.modules and cache:
            return True
        try:
            m = __import__(module_name, globals(), locals(), func_names, -1)
            if func_names:
                for func_name in func_names:
                    self.modules[func_name] = getattr(m, func_name)

            else:
                self.modules[module_name] = m
            return True
        except ImportError:
            return False

    def loads(self, modules, cache = True):
        for module in modules:
            if not self.load(module, cache):
                self.errfunc(module)
                return

    def getGlobals(self):
        return self.modules

    def errfunc(self, module):
        raise ImportError("module '" + str(module) + "' not found")


def getCodeForImports(modules, errfunc = None):
    if errfunc is not None:
        ModulesManager.errfunc = lambda a, b: errfunc(b)
    return 'map(lambda v: globals().__setitem__(v[0],v[1]) , ModulesManager(' + str(modules) + ').getGlobals().items())'
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\curarchitecture\util.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:45 ora legale Europa occidentale
