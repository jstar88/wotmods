from gui.battle_control.battle_feedback import BattleFeedbackAdaptor
from constants import BATTLE_EVENT_TYPE as _SET
from gui.battle_control import g_sessionProvider
from gui.battle_control.battlesessionprovider import BattleSessionProvider
from gui.WindowsManager import g_windowsManager
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from plugins.Engine.Plugin import Plugin
import Math
import BigWorld
from copy import deepcopy
from functools import partial



class Marker(object):

    def __init__(self,position,distance,idM,time = None):
        self.idM = idM
        if time is None:
            self.time = BigWorld.time()
        else:
            self.time = time
        self.position = position
        self.distance = distance
        self.handle = None
    
    def remove(self):
        if self.handle is not None and g_windowsManager.battleWindow is not None:
            g_windowsManager.battleWindow.markersManager._MarkersManager__ownUI.delMarker(self.handle)
        
    def show(self):
        matrixProve = Math.Matrix()
        matrixProve.translation = self.position + (0, SpotExtended.myConf['markerHeight'], 0)
        vehiclePoint = g_windowsManager.battleWindow.markersManager._MarkersManager__ownUI.addMarker(matrixProve, 'StaticObjectMarker')
        g_windowsManager.battleWindow.markersManager._MarkersManager__ownUI.markerInvoke(vehiclePoint, ('init', [SpotExtended.myConf['markerType'], 40, 40 + 1, self.distance]))
        self.handle = vehiclePoint
        
        

class MarkerManager(object):
    def __init__(self):
        self.markers = {}
        self.waiting = []
        
    def __add(self,marker):
        self.markers[marker.idM] = marker
        marker.show()
    
    def __remove(self,idM):
        if self.markers.has_key(idM):
            self.markers[idM].remove()
            del self.markers[idM]
        
    def __set(self,marker):
        if self.markers.has_key(marker.idM):
            self.__remove(marker.idM)
        self.__add(marker)
        
    def enqueue(self,marker):
        self.waiting.append(marker)
        
    def clean(self):
        for k,v in self.markers.iteritems():
            v.remove()
        self.markers = {}
        self.waiting = []
        
    def updateMarkers(self):
        if not inBattle:
            return
        for marker in self.waiting:
            self.__set(marker)
        self.waiting = []
        player = BigWorld.player()
        
        for k,v in deepcopy(self.markers).iteritems(): 
            if BigWorld.entities.has_key(k) and BigWorld.entities[k].isAlive() and BigWorld.time()-v.time < SpotExtended.myConf['markerTime']:
                if SpotExtended.myConf['markerMove']:
                    pos = BigWorld.entities[k].position
                    distance = (player.position-pos).length
                    marker = Marker(pos, distance, k, v.time)
                    self.__set(marker)
            else:
                self.__remove(k)
        BigWorld.callback(SpotExtended.myConf['markerUpdateTime'], self.updateMarkers)    

        
    

mm = MarkerManager()
inBattle = False
procStarted = False

class SpotExtended(Plugin):
    # default config
    myConf = {'pluginEnable' : True,
              'panel':'PlayerMessagesPanel',
              'color': 'gold',
              'showMessage':True,
              'showMarker':True,
              'markerType': 'eye',
              'markerHeight': 9,
              'markerTime': 9.0,
              'markerMove': True,
              'markerUpdateTime': 0.1,
              'message':'{name}{tank}'
              }
        
    #plugin function, called at wot start
    def run(self):
        saveOldFuncs()
        g_windowsManager.onInitBattleGUI += SpotExtended.start
        g_windowsManager.onDestroyBattleGUI +=  SpotExtended.stop
        BattleFeedbackAdaptor.setPlayerAssistResult = SpotExtended.setPlayerAssistResult
    
    # injected, called when battle stop
    @staticmethod
    def stop():
        global inBattle
        inBattle = False
        mm.clean()
    
    # injected, called when battle start
    @staticmethod
    def start():
        global inBattle
        inBattle = True
        mm.clean()
        if g_sessionProvider is not None and g_sessionProvider.getFeedback() is not None:
            g_sessionProvider._BattleSessionProvider__feedback.stop()
            g_sessionProvider._BattleSessionProvider__feedback = BattleFeedbackAdaptor()
            g_sessionProvider._BattleSessionProvider__feedback.start(g_sessionProvider._BattleSessionProvider__arenaDP)

    # injected, called when client receive events
    @staticmethod
    def setPlayerAssistResult(self, assistType, vehiclesIDs):
        old__start(self, assistType, vehiclesIDs)
        if assistType == _SET.SPOTTED:
            player = BigWorld.player()
            arena = player.arena
            for idV in vehiclesIDs:
                if SpotExtended.myConf['showMarker']: 
                    SpotExtended.addMarker(idV, arena, player)
                if SpotExtended.myConf['showMessage']:
                    SpotExtended.addMessage(idV, arena)

    # add a 3D marker above spotted tank    
    @staticmethod
    def addMarker(idV, arena, player):
        global procStarted
        vehicle = BigWorld.entities.get(idV)
        
        if vehicle is not None:
            position =  BigWorld.entities[idV].position
        elif arena.positions.has_key(idV):
            position = arena.positions[idV]
        else:
            BigWorld.callback(0.5,partial(SpotExtended.addMarker,idV, arena, player))
            return
        if position is not None:   
            distance = (player.position-position).length
            mm.enqueue(Marker(position,distance,idV))
            if not procStarted:
                mm.updateMarkers()
                procStarted = True
    
    # format the message and show it
    @staticmethod
    def addMessage(idV, arena):
        entryVehicle = arena.vehicles[idV]
        vehicleType = entryVehicle['vehicleType'].type
        infos = {'clanAbbrev': entryVehicle['clanAbbrev'],
                 'playerName':entryVehicle['name'],
                 'shortTankName': vehicleType.shortUserString,
                 'fullTankName': vehicleType.name}
                
        msg = SpotExtended.myConf['message'].format(**infos)
        SpotExtended.showMessageOnPanel(SpotExtended.myConf['panel'],msg,SpotExtended.myConf['color'])
        
    #Show message on specified panel: VehicleErrorsPanel, VehicleMessagesPanel, PlayerMessagesPanel
    @staticmethod
    def showMessageOnPanel(panel, msgText, color, index = 0):
        if g_windowsManager.battleWindow is not None and panel in ('VehicleErrorsPanel', 'VehicleMessagesPanel', 'PlayerMessagesPanel'):
            g_windowsManager.battleWindow.call('battle.' + panel + '.ShowMessage', [index, msgText, color])
    
def saveOldFuncs():
    global old__start
    old__start = BattleFeedbackAdaptor.setPlayerAssistResult