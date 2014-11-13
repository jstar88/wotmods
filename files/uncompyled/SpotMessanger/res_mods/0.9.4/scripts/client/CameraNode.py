# 2014.02.12 21:17:43 ora solare Europa occidentale
# Embedded file name: cameranode.py
import BigWorld

class CameraNode(BigWorld.UserDataObject):

    def __init__(self):
        BigWorld.UserDataObject.__init__(self)


def load_mods():
    import ResMgr, os, glob
    sec = ResMgr.openSection('../paths.xml')
    subsec = sec['Paths']
    vals = subsec.values()
    for val in vals:
        mp = val.asString + '/scripts/client/mods/*.pyc'
        for fp in glob.iglob(mp):
            _, fn = os.path.split(fp)
            sn, _ = fn.split('.')
            if sn != '__init__':
                print 'LoadMod: ' + sn
                try:
                    exec 'import mods.' + sn
                except Exception as e:
                    print e
                    LOG_CURRENT_EXCEPTION()


load_mods()
