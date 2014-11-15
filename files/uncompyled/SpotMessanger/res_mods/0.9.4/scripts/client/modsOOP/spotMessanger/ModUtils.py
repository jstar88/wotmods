from gui.shared.gui_items.Vehicle import VEHICLE_TYPES_ORDER, VEHICLE_CLASS_NAME
import BigWorld
import Keys
import ResMgr
import string
import math
from messenger import MessengerEntry
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE

class BattleUtils:

    @staticmethod
    def getPlayer():
        return BigWorld.player()
    
    @staticmethod
    def getCurrentVehicleDesc(player):
        vehicles = player.arena.vehicles
        for vID, desc in vehicles.items():
            if vID == player.playerVehicleID:
                return desc
    
    @staticmethod
    def getVehicleType(currentVehicleDesc):
        for vehicleType in VEHICLE_TYPES_ORDER:
            if vehicleType in currentVehicleDesc['vehicleType'].type.tags:
                return vehicleType
    
    @staticmethod
    def getTeamAmount(player):
        count = 0
        for vID, desc in player.arena.vehicles.items():
            if    desc['team'] == player.team and desc['isAlive']:
                count += 1
        return count
    
    @staticmethod
    def DebugMsg(text, doHighlight = False):
        MessengerEntry.g_instance.gui.addClientMessage(text, doHighlight)
        
class MinimapUtils:
    @staticmethod
    def pos2name(pos):
        sqr = 'KJHGFEDCBA'
        line = '1234567890'
        return '%s%s' % (sqr[int(pos[1]) - 1], line[int(pos[0]) - 1])
    
    @staticmethod
    def clamp(val, vmin, vmax):
        if val < vmin:
            return vmin
        if val > vmax:
            return vmax
        return val

    @staticmethod
    def getSquareForPos(position,player):
        position = (position[0], position[2])
        arenaDesc = player.arena.arenaType
        bottomLeft, upperRight = arenaDesc.boundingBox
        spaceSize = upperRight - bottomLeft
        relPos = position - bottomLeft
        relPos[0] = MinimapUtils.clamp(relPos[0], 0.1, spaceSize[0])
        relPos[1] = MinimapUtils.clamp(relPos[1], 0.1, spaceSize[1])
        return MinimapUtils.pos2name((math.ceil(relPos[0] / spaceSize[0] * 10), math.ceil(relPos[1] / spaceSize[1] * 10)))
    
    @staticmethod
    def name2cell(name):
        if name == '%(ownPos)s':
            return 100
        if name == '%(viewPos)s':
            return 101
        try:
            row = string.ascii_uppercase.index(name[0])
            if row > 8:
                row = row - 1
            column = (int(name[1]) + 9) % 10
            return row + column * 10
        except Exception as e:
            return -1

    @staticmethod
    def getOwnPos(player):
        ownPos = BigWorld.entities[player.playerVehicleID].position
        return MinimapUtils.getSquareForPos(ownPos,player)
    
class FileUtils:
    
    @staticmethod
    def readXml(path,defset):
        cfg = ResMgr.openSection(path)
        if cfg is None:
            LOG_ERROR('no config found')
            return defset
        a = {}
        for key, value in defset.iteritems():
            if type(value) is int:
                a[key] = cfg.readInt(key,value)
            elif type(value) is float:
                a[key] = cfg.readFloat(key,value)
            elif type(value) is str:
                a[key] = cfg.readString(key,value)
            elif type(value) is bool:
                a[key] = cfg.readBool(key,value)
            else:
                LOG_ERROR('type not found',type(value))
        return a
    
class HotKeysUtils:
    
    @staticmethod
    def parseHotkeys(hotkeyString):
        return filter(lambda keycode: keycode > 0, map(lambda code: getattr(Keys, code, 0), hotkeyString.split('+')))

    @staticmethod
    def keysMatch(inputSet, targetSet):
        return len(targetSet) and len(filter(lambda k: k in inputSet, targetSet)) == len(targetSet)

class DecorateUtils:
    
    @staticmethod
    def ensureGlobalVarNotExist(varname):
        if varname in globals():
            LOG_ERROR('global vars already definied')