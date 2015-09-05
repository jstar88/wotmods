# 2015.09.05 18:13:46 ora legale Europa occidentale
# Embedded file name: CameraNode.py
import BigWorld
import os

class CameraNode(BigWorld.UserDataObject):

    def __init__(self):
        BigWorld.UserDataObject.__init__(self)


def fixPath(path):
    a = path.split('/')
    restore = False
    if not a[0]:
        a[0] = '_'
        restore = True
    path = os.path.join(*a)
    if restore:
        return path[1:]
    return path


def load_mods():
    import ResMgr, os, glob
    sec = ResMgr.openSection(fixPath('../paths.xml'))
    subsec = sec['Paths']
    vals = subsec.values()
    for val in vals:
        mp = val.asString + fixPath('/scripts/client/mods/*.pyc')
        for fp in glob.iglob(mp):
            _, fn = os.path.split(fp)
            sn, _ = fn.split('.')
            if sn != '__init__':
                print 'LoadMod: ' + sn
                try:
                    exec 'import mods.' + sn
                except Exception as e:
                    print e


load_mods()
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\CameraNode.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:46 ora legale Europa occidentale
