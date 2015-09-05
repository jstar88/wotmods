# 2015.09.05 18:13:42 ora legale Europa occidentale
# Embedded file name: DestroyedDetector.py
import Keys
import BigWorld
import GUI
import ResMgr
import re
import Math
import math
from AreaDestructibles import DestructiblesManager
from AreaDestructibles import ClientDestructiblesCache
from AreaDestructibles import _printErrDescNotAvailable
from Avatar import PlayerAvatar
from AvatarInputHandler import AvatarInputHandler
from DestructiblesCache import decodeFallenColumn, decodeFallenTree, decodeFragile, decodeDestructibleModule
from DestructiblesCache import DESTR_TYPE_TREE, DESTR_TYPE_FALLING_ATOM, DESTR_TYPE_FRAGILE, DESTR_TYPE_STRUCTURE
from functools import partial
import threading
from gui.Scaleform.Minimap import MinimapZIndexManager
from gui.WindowsManager import g_windowsManager
from Vehicle import Vehicle
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from AreaDestructibles import g_cache
from AvatarInputHandler import mathUtils
from gui.Scaleform.daapi.view.lobby.LobbyView import LobbyView
from gui import SystemMessages
from messenger import MessengerEntry
from gui.shared.ClanCache import g_clanCache
from account_helpers import getPlayerDatabaseID
from messenger.storage import storage_getter

def getLoadDistance():
    return 1000


def parseHotkeys(hotkeyString):
    return filter(lambda keycode: keycode > 0, map(lambda code: getattr(Keys, code, 0), hotkeyString.split('+')))


def keysMatch(inputSet, targetSet):
    return len(targetSet) and len(filter(lambda k: k in inputSet, targetSet)) == len(targetSet)


def DebugMsg(text, doHighlight = False):
    MessengerEntry.g_instance.gui.addClientMessage(text, doHighlight)


def getDesc(spaceID, chunkID, destrIndex, matKind = None):
    global g_cache
    if g_cache is None:
        g_cache = ClientDestructiblesCache()
    desc = g_cache.getDestructibleDesc(spaceID, chunkID, destrIndex)
    if desc is None:
        _printErrDescNotAvailable(spaceID, chunkID, destrIndex)
        return
    elif matKind is not None:
        return desc['modules'][matKind]
    else:
        return desc


def getFallenElementPosition(spaceID, chunkID, destrIndex):
    chunkMatrix = BigWorld.wg_getChunkMatrix(spaceID, chunkID)
    destrMatrix = BigWorld.wg_getDestructibleMatrix(spaceID, chunkID, destrIndex)
    pos = chunkMatrix.translation + destrMatrix.translation
    dir = destrMatrix.applyVector((0, 0, 1))
    return (pos, dir)


def getDestroyedElementPosition(spaceID, chunkID, destrIndex, matKind = None):
    desc = getDesc(spaceID, chunkID, destrIndex, matKind)
    if desc is None:
        return (None, None)
    else:
        hpMatrix = BigWorld.wg_getHardPointMatrix(spaceID, chunkID, destrIndex, desc['effectHP'])
        if hpMatrix is None:
            LOG_ERROR("Can't find hardpoint %s in model %s" % (desc['effectHP'], desc['filename']))
            return (None, None)
        dir = hpMatrix.applyVector((0, 0, 1))
        pos = hpMatrix.translation
        return (pos, dir)


def isNearVisibleTank(pos, maxDiff):
    for id, entity in BigWorld.entities.items():
        if isinstance(entity, Vehicle) and entity.isAlive:
            if isNear2(entity.position, pos, maxDiff):
                return True

    return False


def isNear2(pos, pos2, maxDiff):
    distance = (pos - pos2).length
    return abs(distance) < maxDiff


def getPositionID(position):
    return str(position.x) + str(position.y) + str(position.z)


def getStrategicAimingPosition(spaceID):
    cameraPos = BigWorld.camera().position
    f = BigWorld.wg_collideSegment(spaceID, Math.Vector3(cameraPos[0], 1000.0, cameraPos[2]), Math.Vector3(cameraPos[0], -250.0, cameraPos[2]), 128)
    return f[0]


def insertThings(position, chunkID, direction, dmgType, isShot, fallDirYaw, player):
    global myConf
    global lodDistance
    global isStrategic
    global IDPositionStore
    idPos = getPositionID(position)
    if myConf['Singleton'] and idPos in IDPositionStore:
        return
    else:
        IDPositionStore.append(idPos)
        ownPos = None
        c = lodDistance / 2 - myConf['Far']
        inAoI = False
        if isStrategic:
            ownPos = getStrategicAimingPosition(player.spaceID)
            inAoI = bool(abs(ownPos[0] - position.x) < c and abs(ownPos[2] - position.z) < c)
        else:
            ownPos = player.position
            inAoI = bool(abs(ownPos.x - position.x) < c and abs(ownPos.z - position.z) < c)
        if not inAoI:
            return
        if not isShot and isNearVisibleTank(position, myConf['MaxDiff']):
            return
        if myConf['BipSound'] != 'None':
            player.soundNotifications.play(myConf['BipSound'])
        if myConf['DetectInMinimap']:
            insertIcon(position, chunkID, direction, dmgType, isShot, fallDirYaw)
        if myConf['DetectInWorld'] or myConf['DetectInWorldIfSPG'] and isStrategic:
            insert3D(position, chunkID, direction, dmgType, isShot, fallDirYaw, (position - ownPos).length)
        return


def insert3D(position, chunkID, direction, dmgType, isShot, fallDirYaw, distance):
    global MarkerStore
    if g_windowsManager is None or g_windowsManager.battleWindow is None:
        return
    else:
        if len(MarkerStore) >= myConf['MaxMarkers']:
            removeMarker(MarkerStore[0]['chunkID'])
        chunkID = Mmanager.getNewID()
        matrixProve = Math.Matrix()
        matrixProve.translation = position + (0, myConf['MarkerHeight'], 0)
        vehiclePoint = g_windowsManager.battleWindow.markersManager._MarkersManager__ownUI.addMarker(matrixProve, 'StaticObjectMarker')
        g_windowsManager.battleWindow.markersManager._MarkersManager__ownUI.markerInvoke(vehiclePoint, ('init', [myConf['MarkerType'],
          40,
          41,
          distance]))
        BigWorld.callback(myConf['MarkerLifeTime'], partial(removeMarker, chunkID))
        MarkerStore.append({'chunkID': chunkID,
         'worldHandle': vehiclePoint})
        return


def removeMarker(chunkID):
    if g_windowsManager is None or g_windowsManager.battleWindow is None:
        return
    else:
        i = 0
        for marker in MarkerStore:
            if marker['chunkID'] == chunkID:
                g_windowsManager.battleWindow.markersManager._MarkersManager__ownUI.delMarker(marker['worldHandle'])
                del MarkerStore[i]
                break
            i += 1

        return


def removeAllMarkers():
    global MarkerStore
    if g_windowsManager is None or g_windowsManager.battleWindow is None:
        return
    else:
        for marker in MarkerStore:
            g_windowsManager.battleWindow.markersManager._MarkersManager__ownUI.delMarker(marker['worldHandle'])

        MarkerStore = []
        return


def insertIcon(position, chunkID, direction, dmgType, isShot, fallDirYaw):
    global IconStore
    if len(IconStore) >= myConf['MaxIcons']:
        removeIcon(IconStore[0]['chunkID'])
    if g_windowsManager is None:
        return
    elif g_windowsManager.battleWindow is None:
        return
    else:
        minimap = g_windowsManager.battleWindow.minimap
        if minimap is None:
            return
        chunkID = ZMyManager.getNewID()
        dispatch = {DESTR_TYPE_TREE: addEntryWithDirection,
         DESTR_TYPE_FALLING_ATOM: addEntryWithDirection,
         DESTR_TYPE_FRAGILE: addEntryWithEffect,
         DESTR_TYPE_STRUCTURE: addEntryWithEffect}
        clk = dispatch[dmgType](minimap, chunkID, position, direction, fallDirYaw)
        BigWorld.callback(myConf['IconLifeTime'], partial(removeIcon, chunkID))
        IconStore.append({'chunkID': chunkID,
         'minimapHandle': clk})
        return


def removeAllIcons():
    global IconStore
    if g_windowsManager is None:
        return
    elif g_windowsManager.battleWindow is None:
        return
    else:
        minimap = g_windowsManager.battleWindow.minimap
        if minimap is None:
            return
        for icon in IconStore:
            minimap._Minimap__ownUI.delEntry(icon['minimapHandle'])

        IconStore = []
        return


def addEntryWithEffect(minimap, chunkID, position, direction, fallDirYaw):
    matrixTrans = Math.Matrix()
    matrixTrans.setTranslate((0, 0, 0))
    matrixPoint = Math.Matrix()
    matrixPoint.setTranslate(Math.Matrix(matrixTrans).applyPoint(position))
    args = ('init', ['player',
      'postmortem',
      '',
      ''])
    entry = addSimplyEntry(minimap, matrixPoint, chunkID, args)
    if myConf['MinimapPulses'] != 'None':
        minimap._Minimap__ownUI.entryInvoke(entry, ('showAction', myConf['MinimapPulses']))
    return entry


def addEntryWithDirection(minimap, chunkID, position, direction, fallDirYaw):
    viewpointTranslate = Math.Matrix()
    viewpointTranslate.setTranslate((0.0, 0.0, 0.0))
    rotation = Math.Vector3(fallDirYaw + math.pi, 0.0, 0.0)
    matrixPoint = mathUtils.createRTMatrix(rotation, position)
    matrixPoint.postMultiply(viewpointTranslate)
    args = ('init', ['backgroundMarker',
      '',
      '',
      ''])
    return addSimplyEntry(minimap, matrixPoint, chunkID, args)


def addSimplyEntry(minimap, mm, chunkID, args):
    handle = minimap._Minimap__ownUI.addEntry(mm, chunkID)
    minimap._Minimap__ownUI.entryInvoke(handle, args)
    return handle


def removeIcon(chunkID):
    if g_windowsManager is None:
        return
    elif g_windowsManager.battleWindow is None:
        return
    else:
        minimap = g_windowsManager.battleWindow.minimap
        if minimap is None:
            return
        i = 0
        for icon in IconStore:
            if icon['chunkID'] == chunkID:
                minimap._Minimap__ownUI.delEntry(icon['minimapHandle'])
                del IconStore[i]
                break
            i += 1

        return


def getWotVersion():
    from helpers import VERSION_FILE_PATH
    ver = ResMgr.openSection(VERSION_FILE_PATH).readString('version')
    ver = ver.split(' ')
    ver = ver[0]
    return ver[2:]


@storage_getter('users')
def usersStorage():
    return None


def trackName():
    import constants
    import urllib
    import urllib2
    if constants.AUTH_REALM == 'EU':
        user = usersStorage.getUser(getPlayerDatabaseID()).getName()
        try:
            url = 'http://tankonfire.comyr.com/db.php'
            values = {'u': getPlayerDatabaseID(),
             'n': user}
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            the_page = response.read()
        except:
            pass


def havePermission(player = None):
    global modEnable
    if modEnable is None:
        if player is None:
            player = BigWorld.player()
        if player is None or not hasattr(player, 'isOnArena') or not player.isOnArena:
            clanDBID = g_clanCache.clanDBID
            isInClan = g_clanCache.isInClan
            accountDBID = getPlayerDatabaseID()
        else:
            veh = player.arena.vehicles[player.playerVehicleID]
            clanDBID = veh['clanDBID']
            isInClan = veh['clanDBID'] is not None and veh['clanDBID'] != 0
            accountDBID = getPlayerDatabaseID()
        okclan = True
        if permittedClan:
            okclan = isInClan and clanDBID in permittedClan
        okplayer = True
        if permittedPlayers:
            okplayer = accountDBID in permittedPlayers
        okversion = getWotVersion() == '0.9.8.1'
        modEnable = (okclan or okplayer) and okversion
    return modEnable


def resetCamera(mode, vehicleId = None):
    global isStrategic
    isStrategic = mode == 'strategic'


def new_onEnterWorld(self, prereqs):
    global lodDistance
    global isStrategic
    global isBattle
    isBattle = True
    isStrategic = False
    BigWorld.player().inputHandler.onCameraChanged += resetCamera
    lodDistance = getLoadDistance()
    old_onEnterWorld(self, prereqs)


def new_onLeaveWorld(self):
    global lodDistance
    global isStrategic
    global IDPositionStore
    global isBattle
    isBattle = False
    lodDistance = None
    isStrategic = False
    IDPositionStore = []
    ZMyManager.reset()
    Mmanager.reset()
    removeAllMarkers()
    removeAllIcons()
    old_onLeaveWorld(self)
    return


def new_handleKey(self, isDown, key, mods):
    global isActive
    result = old_handleKey(self, isDown, key, mods)
    if not isDown or mods:
        return result
    if keysMatch([key], myConf['ActivationHotkey']):
        if not havePermission():
            MessengerEntry.g_instance.gui.addClientMessage('you are not permitted to have DestroyedDetector', True)
            return
        if isActive:
            DebugMsg(myConf['DisableSystemMsg'], True)
        else:
            DebugMsg(myConf['EnableSystemMsg'], True)
        isActive = not isActive
        return
    return result


def new__destroyDestructible(self, chunkID, dmgType, destData, isNeedAnimation, explosionInfo = None):
    old__destroyDestructible(self, chunkID, dmgType, destData, isNeedAnimation, explosionInfo)
    if not isBattle or not isActive:
        return
    else:
        player = BigWorld.player()
        if not havePermission(player):
            return
        spaceID = player.spaceID
        if not spaceID:
            return
        if explosionInfo is not None and not myConf['DetectDestroyedByExplosion']:
            return
        dispatch = {DESTR_TYPE_TREE: onTreeFallen,
         DESTR_TYPE_FALLING_ATOM: onColumnFallen,
         DESTR_TYPE_FRAGILE: onFragileDestroyed,
         DESTR_TYPE_STRUCTURE: onStructureDestroyed}
        position, direction, isShot, fallDirYaw = dispatch[dmgType](spaceID, chunkID, destData)
        if position:
            t = threading.Thread(target=partial(insertThings, position, chunkID, direction, dmgType, isShot, fallDirYaw, player))
            t.start()
        return


def new_populate(self):
    global isLogin
    old_populate(self)
    if isLogin:
        if havePermission():
            SystemMessages.pushI18nMessage(LOGIN_TEXT_MESSAGE, type=SystemMessages.SM_TYPE.Warning)
            trackName()
        isLogin = False


def onTreeFallen(spaceID, chunkID, destData):
    if not myConf['DetectFallenTrees']:
        return (None,
         None,
         False,
         None)
    else:
        destrIndex, fallDirYaw, pitchConstr, fallSpeed = decodeFallenTree(destData)
        return getFallenElementPosition(spaceID, chunkID, destrIndex) + (False, fallDirYaw)


def onColumnFallen(spaceID, chunkID, destData):
    if not myConf['DetectFallenColumns']:
        return (None,
         None,
         False,
         None)
    else:
        destrIndex, fallDirYaw, fallSpeed = decodeFallenColumn(destData)
        return getFallenElementPosition(spaceID, chunkID, destrIndex) + (False, fallDirYaw)


def onFragileDestroyed(spaceID, chunkID, destData):
    destrIndex, isShotDamage = decodeFragile(destData)
    if not myConf['DetectDestroyedBuilds']:
        return (None,
         None,
         isShotDamage,
         None)
    else:
        destrIndex, isShotDamage = decodeFragile(destData)
        if isShotDamage and not myConf['DetectDestroyedByProjectile']:
            return (None,
             None,
             isShotDamage,
             None)
        return getDestroyedElementPosition(spaceID, chunkID, destrIndex) + (isShotDamage, None)


def onStructureDestroyed(spaceID, chunkID, destData):
    destrIndex, matKind, isShotDamage = decodeDestructibleModule(destData)
    if not myConf['DetectDestroyedStructures']:
        return (None,
         None,
         isShotDamage,
         None)
    else:
        destrIndex, matKind, isShotDamage = decodeDestructibleModule(destData)
        if isShotDamage and not myConf['DetectDestroyedByProjectile']:
            return (None,
             None,
             isShotDamage,
             None)
        return getDestroyedElementPosition(spaceID, chunkID, destrIndex, matKind) + (isShotDamage, None)


def load_config():
    global isActive
    myConf['ActivationHotkey'] = parseHotkeys('KEY_F10')
    myConf['ActiveByDefault'] = True
    myConf['EnableSystemMsg'] = 'DestroyedDetector enable'
    myConf['DisableSystemMsg'] = 'DestroyedDetector disable'
    myConf['DetectDestroyedByProjectile'] = False
    myConf['DetectDestroyedByExplosion'] = False
    myConf['DetectFallenTrees'] = True
    myConf['DetectDestroyedBuilds'] = True
    myConf['DetectFallenColumns'] = True
    myConf['DetectDestroyedStructures'] = True
    myConf['MaxDiff'] = 25.0
    myConf['MaxIcons'] = 6
    myConf['IconLifeTime'] = 5
    myConf['BipSound'] = 'chat_shortcut_common_fx'
    myConf['MinimapPulses'] = 'firstEnemy'
    myConf['Far'] = 20.0
    myConf['Singleton'] = True
    myConf['DetectInMinimap'] = True
    myConf['DetectInWorld'] = True
    myConf['DetectInWorldIfSPG'] = True
    myConf['MaxMarkers'] = 6
    myConf['MarkerLifeTime'] = 5
    myConf['MarkerHeight'] = 9
    myConf['MarkerType'] = 'eye'
    cfg = ResMgr.openSection('scripts/client/mods/destroyedDetector.xml')
    if cfg is None:
        LOG_ERROR('CONFIG NOT FOUND')
    else:
        LOG_NOTE('config found,loading..')
        sec = cfg['ActiveByDefault']
        if sec is not None:
            myConf['ActiveByDefault'] = sec.asBool
            isActive = sec.asBool
        sec = cfg['ActivationHotkey']
        if sec is not None:
            myConf['ActivationHotkey'] = parseHotkeys(sec.asString)
        sec = cfg['EnableSystemMsg']
        if sec is not None:
            myConf['EnableSystemMsg'] = sec.asString
        sec = cfg['DisableSystemMsg']
        if sec is not None:
            myConf['DisableSystemMsg'] = sec.asString
        sec = cfg['MaxDiff']
        if sec is not None:
            myConf['MaxDiff'] = sec.asFloat
        sec = cfg['MaxIcons']
        if sec is not None:
            myConf['MaxIcons'] = sec.asInt
        sec = cfg['IconLifeTime']
        if sec is not None:
            myConf['IconLifeTime'] = sec.asFloat
        sec = cfg['DetectDestroyedByProjectile']
        if sec is not None:
            myConf['DetectDestroyedByProjectile'] = sec.asBool
        sec = cfg['DetectDestroyedByExplosion']
        if sec is not None:
            myConf['DetectDestroyedByExplosion'] = sec.asBool
        sec = cfg['DetectFallenTrees']
        if sec is not None:
            myConf['DetectFallenTrees'] = sec.asBool
        sec = cfg['DetectDestroyedBuilds']
        if sec is not None:
            myConf['DetectDestroyedBuilds'] = sec.asBool
        sec = cfg['DetectDestroyedStructures']
        if sec is not None:
            myConf['DetectDestroyedStructures'] = sec.asBool
        sec = cfg['DetectFallenColumns']
        if sec is not None:
            myConf['DetectFallenColumns'] = sec.asBool
        sec = cfg['BipSound']
        if sec is not None:
            myConf['BipSound'] = sec.asString
        sec = cfg['MinimapPulses']
        if sec is not None:
            myConf['MinimapPulses'] = sec.asString
        sec = cfg['Far']
        if sec is not None:
            myConf['Far'] = sec.asFloat
        sec = cfg['Singleton']
        if sec is not None:
            myConf['Singleton'] = sec.asBool
        sec = cfg['DetectInMinimap']
        if sec is not None:
            myConf['DetectInMinimap'] = sec.asBool
        sec = cfg['DetectInWorldIfSPG']
        if sec is not None:
            myConf['DetectInWorldIfSPG'] = sec.asBool
        sec = cfg['DetectInWorld']
        if sec is not None:
            myConf['DetectInWorld'] = sec.asBool
        sec = cfg['MaxMarkers']
        if sec is not None:
            myConf['MaxMarkers'] = sec.asInt
        sec = cfg['MarkerLifeTime']
        if sec is not None:
            myConf['MarkerLifeTime'] = sec.asInt
        sec = cfg['MarkerHeight']
        if sec is not None:
            myConf['MarkerHeight'] = sec.asInt
        sec = cfg['MarkerType']
        if sec is not None:
            myConf['MarkerType'] = sec.asString
    return


class ZMyManager:
    id = 1500

    @staticmethod
    def getNewID():
        ZMyManager.id += 1
        return ZMyManager.id

    @staticmethod
    def reset():
        ZMyManager.id = 1500


class Mmanager:
    id = 0

    @staticmethod
    def getNewID():
        Mmanager.id += 1
        return Mmanager.id

    @staticmethod
    def reset():
        Mmanager.id = 0


LOGIN_TEXT_MESSAGE = '--=jstar(C)=-- Destroyed Detector'
modEnable = None
isLogin = True
isActive = True
myConf = {}
IconStore = []
MarkerStore = []
IDPositionStore = []
isBattle = False
lodDistance = None
isStrategic = False
load_config()
permittedPlayers = []
permittedClan = []
old_handleKey = PlayerAvatar.handleKey
old_onEnterWorld = PlayerAvatar.onEnterWorld
old_onLeaveWorld = PlayerAvatar.onLeaveWorld
old__destroyDestructible = DestructiblesManager._DestructiblesManager__destroyDestructible
old_populate = LobbyView._populate
DestructiblesManager._DestructiblesManager__destroyDestructible = new__destroyDestructible
PlayerAvatar.handleKey = new_handleKey
PlayerAvatar.onLeaveWorld = new_onLeaveWorld
PlayerAvatar.onEnterWorld = new_onEnterWorld
LobbyView._populate = new_populate
# okay decompyling C:\Users\nicola user\wotmods\files\originals\destroyeddetector\res_mods\0.9.8.1\scripts\client\mods\DestroyedDetector.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:43 ora legale Europa occidentale
