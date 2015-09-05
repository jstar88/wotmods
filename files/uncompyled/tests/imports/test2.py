# 2015.09.05 18:13:45 ora legale Europa occidentale
# Embedded file name: test2.py
import __builtin__

def my_import(module_name, func_names = [], cache = False):
    if module_name in globals() and cache:
        return True
    try:
        m = __import__(module_name, globals(), locals(), func_names, -1)
        if func_names:
            for func_name in func_names:
                globals()[func_name] = getattr(m, func_name)

        else:
            globals()[module_name] = m
        return True
    except ImportError:
        return False


def my_imports(modules):
    for module in modules:
        if type(module) is tuple:
            name = module[0]
            funcs = module[1]
        else:
            name = module
            funcs = []
        if not my_import(name, funcs):
            return module

    return ''


def checkPluginsImports(plugin, modules):
    c = my_imports(modules)
    if c:
        print plugin + " has errors!: module '" + c + "' not found"
    else:
        __builtin__.modules = globals()


def d():
    checkPluginsImports('demoPlugin', [('test', ['x'])])
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\imports\test2.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:45 ora legale Europa occidentale
