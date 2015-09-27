from gui.battle_control.battle_feedback import BattleFeedbackAdaptor,BattleFeedbackPlayer
from constants import BATTLE_EVENT_TYPE as _SET
from gui.battle_control import g_sessionProvider
from gui.battle_control.battlesessionprovider import BattleSessionProvider
#from gui.Scaleform.daapi.view.battle.markers import _VehicleMarker, MarkersManager
from plugins.Engine.ModUtils import BattleUtils, MinimapUtils, FileUtils, HotKeysUtils, DecorateUtils
from plugins.Engine.Plugin import Plugin
import Math
import BigWorld
from copy import deepcopy
from functools import partial
from gui.shared.utils.sound import Sound
from gui.app_loader import g_appLoader
from gui.shared import g_eventBus, events
from gui.app_loader.settings import APP_NAME_SPACE as _SPACE


class Marker(object):

    def __init__(self, position, distance, idM, time=None):
        self.idM = idM
        if time is None:
            self.time = BigWorld.time()
        else:
            self.time = time
        self.position = position
        self.distance = distance
        self.handle = None
    
    def remove(self):
        battle = g_appLoader.getDefBattleApp()
        if battle:
            markersManager = battle.markersManager
            if self.handle and markersManager:
                markersManager._MarkersManager__ownUI.delMarker(self.handle)
        
    def show(self):
        matrixProve = Math.Matrix()
        matrixProve.translation = self.position + (0, SpotExtended.myConf['markerHeight'], 0)
        battle = g_appLoader.getDefBattleApp()
        if battle:
            markersManager = battle.markersManager
            vehiclePoint = markersManager._MarkersManager__ownUI.addMarker(matrixProve, 'StaticObjectMarker')
            markersManager._MarkersManager__ownUI.markerInvoke(vehiclePoint, ('init', [SpotExtended.myConf['markerType'], 40, 40 + 1, self.distance]))
            self.handle = vehiclePoint
        
        

class MarkerManager(object):
    def __init__(self):
        self.procStarted = False
        self.markers = {}
        self.waiting = []
        
    def __add(self, marker):
        self.markers[marker.idM] = marker
        marker.show()
    
    def __remove(self, idM):
        if self.markers.has_key(idM):
            self.markers[idM].remove()
            del self.markers[idM]
        
    def __set(self, marker):
        if self.markers.has_key(marker.idM):
            self.__remove(marker.idM)
        self.__add(marker)
        
    def enqueue(self, marker):
        self.waiting.append(marker)
        
    def clean(self):
        for k, v in self.markers.iteritems():
            v.remove()
        self.markers = {}
        self.waiting = []
        
    def updateMarkers(self):
        if not Utils.inBattle:
            return
        for marker in self.waiting:
            self.__set(marker)
        self.waiting = []
        player = BigWorld.player()
        
        for k, v in deepcopy(self.markers).iteritems(): 
            if BigWorld.entities.has_key(k) and BigWorld.entities[k].isAlive() and BigWorld.time() - v.time < SpotExtended.myConf['markerTime']:
                if SpotExtended.myConf['markerMove']:
                    pos = BigWorld.entities[k].position
                    distance = (player.position - pos).length
                    marker = Marker(pos, distance, k, v.time)
                    self.__set(marker)
            else:
                self.__remove(k)
        BigWorld.callback(SpotExtended.myConf['markerUpdateTime'], self.updateMarkers) 
        
    # add a 3D marker above spotted tank    
    def addMarker(self, idV, player, position):
        distance = (player.position - position).length
        self.enqueue(Marker(position, distance, idV))
        if not self.procStarted:
            self.updateMarkers()
            self.procStarted = True   

class MessageManager():
    def __init__(self, vehiclesIDs):
        self.message = ''
        self.vehiclesIDs = {}
        for vehicleID in vehiclesIDs:
            vehicleID = fixId(vehicleID)
            self.vehiclesIDs[vehicleID] = vehicleID
    
    def add(self, idV, player, arena, position):
        del self.vehiclesIDs[idV]
        entryVehicle = arena.vehicles[idV]
        vehicleType = entryVehicle['vehicleType'].type
        iconPath = g_sessionProvider.getArenaDP().getVehicleInfo(idV).vehicleType.iconPath
        width, height = SpotExtended.myConf['iconSize']
        icon = '<img src="img://%s" width="%s" height="%s" />' % (iconPath.replace('..', 'gui'), width, height)
        fullPlayerName = g_sessionProvider.getCtx().getFullPlayerName(vID=idV)
        distance = round((player.position - position).length)
        infos = {'clanAbbrev': entryVehicle['clanAbbrev'],
                 'playerName':entryVehicle['name'],
                 'shortTankName': vehicleType.shortUserString,
                 'fullTankName': vehicleType.name,
                 'fullPlayerName': fullPlayerName,
                 'icon': icon,
                 'distance':distance
                 }           
        self.message += SpotExtended.myConf['message'].format(**infos)
        if not SpotExtended.myConf['inline'] or len(self.vehiclesIDs) == 0:
            self.flush()
    
    # Show message on specified panel: VehicleErrorsPanel, VehicleMessagesPanel, PlayerMessagesPanel
    def flush(self):
        panel = SpotExtended.myConf['panel']
        color = SpotExtended.myConf['color']
        index = 0
        battle = g_appLoader.getDefBattleApp()
        if battle and panel in ('VehicleErrorsPanel', 'VehicleMessagesPanel', 'PlayerMessagesPanel'):
            battle.call('battle.' + panel + '.ShowMessage', [index, self.message, color])
        self.clean()
        
    def clean(self):
        self.message = ''
    
class Utils(object):
    inBattle = False
    
    @staticmethod
    def waitForPosition(idV, arena, function):
        vehicle = BigWorld.entities.get(idV)   
        if vehicle is not None:
            position = BigWorld.entities[idV].position
        elif arena.positions.has_key(idV):
            position = arena.positions[idV]
        else:
            BigWorld.callback(0.5, partial(Utils.waitForPosition, idV, arena, function))
            return 
        if position is not None:
            function(position)
            
    @staticmethod
    def minimapPulse(vehicleID):
        battle = g_appLoader.getDefBattleApp()
        if battle:
            minimap = battle.minimap
            if minimap:
                minimap.showActionMarker(vehicleID,SpotExtended.myConf['minimapEffect'])

class SpotExtended(Plugin):
    # default config
    myConf = {'pluginEnable' : True,
              'reloadConfigKey': 'KEY_NUMPAD3',
              'panel':'PlayerMessagesPanel',
              'color': 'gold',
              'showMessage':True,
              'showMarker':True,
              'markerType': 'eye',
              'markerHeight': 9,
              'markerTime': 9.0,
              'markerMove': True,
              'markerUpdateTime': 0.1,
              'message':'{name}{tank}',
              'iconSize': (70, 24),
              'inline': True,
              'playSound': False,
              'sound': '/GUI/notifications_FX/enemy_sighted_for_team',
              'showMinimapEffect':True,
              'minimapEffect':'firstEnemy'
              }
        
    # plugin function, called at wot start
    @classmethod
    def run(cls):
        super(SpotExtended, SpotExtended).run()
        cls.addEventHandler(SpotExtended.myConf['reloadConfigKey'],cls.reloadConfig)
        saveOldFuncs()
        add = g_eventBus.addListener
        appEvent = events.AppLifeCycleEvent
        add(appEvent.INITIALIZING, SpotExtended.start)
        add(appEvent.DESTROYED, SpotExtended.stop)
        BattleFeedbackAdaptor.setPlayerAssistResult = SpotExtended.setPlayerAssistResult
        BattleFeedbackPlayer.setPlayerAssistResult = SpotExtended.setPlayerAssistResult
    
    @staticmethod
    def stop(event):
        if event.ns == _SPACE.SF_BATTLE:
            Utils.inBattle = False
            mm.clean()
    
    @staticmethod
    def start(event):
        if event.ns == _SPACE.SF_BATTLE:
            Utils.inBattle = True
            mm.clean()
    
    # injected, called when client receive events
    @staticmethod
    def setPlayerAssistResult(self, assistType, vehiclesIDs):
        old__start(self, assistType, vehiclesIDs)
        if assistType == _SET.SPOTTED:
            player = BigWorld.player()
            arena = player.arena
            msgm = MessageManager(vehiclesIDs)
            for idV in vehiclesIDs:
                idV = fixId(idV)
                if SpotExtended.myConf['showMarker']:
                    Utils.waitForPosition(idV, arena, partial(mm.addMarker, idV, player)) 
                if SpotExtended.myConf['showMessage']:
                    Utils.waitForPosition(idV, arena, partial(msgm.add, idV, player, arena))
                if SpotExtended.myConf['showMinimapEffect']:
                    Utils.minimapPulse(idV)
            if SpotExtended.myConf['playSound']:
                Sound(SpotExtended.myConf['sound']).play()
   
    
def saveOldFuncs():
    global old__start
    DecorateUtils.ensureGlobalVarNotExist('old__start')
    old__start = BattleFeedbackAdaptor.setPlayerAssistResult
    
# thanks Spoter_ru for this fix
def fixId(i):
    if i >> 32 & 4294967295L > 0: 
        i = i >> 32 & 4294967295L
    else: 
        i &= 4294967295L
    return i
    
mm = MarkerManager()
