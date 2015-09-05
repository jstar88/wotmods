# 2015.09.05 18:13:48 ora legale Europa occidentale
# Embedded file name: ModUtils.py
from gui.shared.gui_items.Vehicle import VEHICLE_TYPES_ORDER, VEHICLE_CLASS_NAME
import BigWorld
import Keys
import ResMgr
import string
import math
from messenger import MessengerEntry
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE, LOG_WARNING
from helpers import VERSION_FILE_PATH
import json
import codecs
import os
from functools import partial

class BattleUtils:

    @staticmethod
    def getPlayer():
        return BigWorld.player()

    @staticmethod
    def getCurrentVehicleDesc(player = None):
        if player is None:
            player = BigWorld.player()
        return player.arena.vehicles[player.playerVehicleID]

    @staticmethod
    def getVehicleType(currentVehicleDesc):
        for vehicleType in VEHICLE_TYPES_ORDER:
            if vehicleType in currentVehicleDesc['vehicleType'].type.tags:
                return vehicleType

    @staticmethod
    def isMyTeam(team, player = None):
        if player is None:
            player = BigWorld.player()
        return team == player.team

    @staticmethod
    def isCw(player = None):
        if player is None:
            player = BigWorld.player()
        return player.arena.guiType == 0

    @staticmethod
    def getTeamAmount(player = None):
        if player is None:
            player = BigWorld.player()
        count = 0
        for vID, desc in player.arena.vehicles.items():
            if BattleUtils.isMyTeam(desc['team'], player) and desc['isAlive']:
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
    def getSquareForPos(position, player):
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
        return MinimapUtils.getSquareForPos(ownPos, player)


class FileUtils:

    @staticmethod
    def readElement(value, defaultValue, filename = '', ke = ''):
        if type(defaultValue) is list:
            value = value.values()
            tmp = []
            tipe = None
            i = 0
            lenNew = len(value)
            lenDefault = len(defaultValue)
            while i < lenDefault:
                if i < lenNew:
                    tmp.append(FileUtils.readElement(value[i], defaultValue[i], filename, i))
                    tipe = defaultValue[i]
                i += 1

            while i < lenNew:
                tmp.append(FileUtils.readElement(value[i], tipe, filename, i))
                i += 1

            return tmp
        elif type(defaultValue) is tuple:
            values = filter(None, value.asString.split(' '))
            tmp = ()
            for k, v in enumerate(defaultValue[:]):
                if len(values) <= k:
                    LOG_WARNING(filename + ': missing tuple entry', k + 1)
                    tmp += v
                else:
                    miniTuple = (FileUtils.readElement(values[k], v, filename, k),)
                    tmp += miniTuple

            return tmp
        elif type(defaultValue) is dict:
            confkeys = value.keys()
            tmp = {}
            for k, v in defaultValue.iteritems():
                if k not in confkeys:
                    k = str(k)
                    if k in confkeys:
                        LOG_WARNING(filename + ': wrong dict key', k)
                if k not in confkeys:
                    LOG_WARNING(filename + ': missing dict key', k)
                    tmp[k] = v
                else:
                    tmp[k] = FileUtils.readElement(value[k], v, filename, k)

            return tmp
        elif type(defaultValue) is int:
            if type(value) is not str:
                value = value.asString
            try:
                value = int(value)
            except Exception:
                LOG_WARNING(filename + " in key '" + ke + "': wrong value type", value)
                value = defaultValue

            return value
        elif type(defaultValue) is float:
            if type(value) is not str:
                value = value.asString
            try:
                value = float(value)
            except Exception:
                LOG_WARNING(filename + " in key '" + ke + "': wrong value type", value)
                value = defaultValue

            return value
        elif type(defaultValue) is bool:
            if type(value) is not str:
                value = value.asString
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            else:
                LOG_WARNING(filename + " in key '" + ke + "': wrong value type", value)
                value = defaultValue
            return value
        elif type(defaultValue) is str:
            if type(value) is str:
                return value
            return value.asString
        else:
            LOG_ERROR(filename + ": type not found in key '" + ke + "'", type(defaultValue))
            return

    @staticmethod
    def readXml(path, defset, filename = ''):
        cfg = ResMgr.openSection(path)
        if cfg is None:
            LOG_WARNING('no config found')
            return defset
        else:
            return FileUtils.readElement(cfg, defset, filename, 'root')

    @staticmethod
    def readConfig(pluginName, defset, configName = 'config'):
        realPath = FileUtils.getRealPluginPath(pluginName)
        virtualPath = FileUtils.getVirtualPluginPath(pluginName)
        xmlVirtualPath = os.path.join(virtualPath, configName + '.xml')
        jsonVirtualPath = os.path.join(virtualPath, configName + '.json')
        xmlRealPath = os.path.join(realPath, configName + '.xml')
        jsonRealPath = os.path.join(realPath, configName + '.json')
        d = {xmlRealPath: partial(FileUtils.readXml, xmlVirtualPath, defset, pluginName),
         jsonRealPath: partial(FileUtils.readJson, jsonVirtualPath, defset, pluginName)}
        for s, f in d.iteritems():
            if os.path.isfile(s):
                return f()

        LOG_WARNING(path + " can't be read, unknow format")
        return defset

    @staticmethod
    def getWotVersion():
        ver = ResMgr.openSection(VERSION_FILE_PATH).readString('version')
        ver = ver.split('#')
        ver = ver[0]
        return ver[2:-1]

    @staticmethod
    def readJson(path, defset, filename = ''):
        fullPath = os.path.join('res_mods', FileUtils.getWotVersion())
        fullPath = os.path.join(fullPath, path)
        if not os.path.exists(fullPath):
            return defset
        json1_file = codecs.open(fullPath, 'r', 'utf-8-sig')
        return json.loads(json1_file.read(), object_hook=_decode_dict)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def my_imports(modules):
        for module in modules:
            if type(module) is tuple:
                name = module[0]
                funcs = module[1]
            else:
                name = module
                funcs = []
            if not FileUtils.my_import(name, funcs):
                return module

        return ''

    @staticmethod
    def checkPluginsImports(plugin, modules):
        c = FileUtils.my_imports(modules)
        if c:
            LOG_ERROR(plugin + " has errors!: module '" + c + "' not found")

    @staticmethod
    def getWotPluginsPath():
        wotFolder = os.path.dirname(os.path.abspath(__file__))
        wotFolder = os.path.dirname(wotFolder)
        return wotFolder

    @staticmethod
    def getWotRoot():
        path = FileUtils.getWotPluginsPath()
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        return os.path.dirname(path)

    @staticmethod
    def getWotResPath():
        return os.path.join(FileUtils.getWotRoot(), 'res')

    @staticmethod
    def getRealPluginsPath():
        wotFolder = FileUtils.getWotPluginsPath()
        p = wotFolder.split('scripts')
        p[0] += os.path.join(os.path.join('res_mods', FileUtils.getWotVersion()), 'scripts')
        return p[0] + p[1]

    @staticmethod
    def getRealPluginPath(pluginName):
        return os.path.join(FileUtils.getRealPluginsPath(), pluginName + '_plugin')

    @staticmethod
    def getVirtualPluginPath(pluginName):
        return os.path.join('scripts', 'client', 'plugins', pluginName + '_plugin')


class HotKeysUtils:

    @staticmethod
    def parseHotkeys(hotkeyString):
        return filter(lambda keycode: keycode > 0, map(lambda code: getattr(Keys, code, 0), hotkeyString.split('+')))

    @staticmethod
    def keysMatch(inputSet, targetSet):
        return len(targetSet) and len(filter(lambda k: k in inputSet, targetSet)) == len(targetSet)

    @staticmethod
    def keyMatch(a, b):
        return a == getattr(Keys, b)


class DecorateUtils:

    @staticmethod
    def ensureGlobalVarNotExist(varname):
        if varname in globals():
            LOG_ERROR('global vars already definied')
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Engine\ModUtils.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:48 ora legale Europa occidentale
