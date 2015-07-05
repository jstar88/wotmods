from gui.battle_control.battle_feedback import BattleFeedbackAdaptor
from constants import BATTLE_EVENT_TYPE as _SET
from gui.battle_control import g_sessionProvider
from gui.battle_control.battlesessionprovider import BattleSessionProvider
from gui.WindowsManager import g_windowsManager
import BigWorld
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from plugins.Engine.Plugin import Plugin

class SpotExtended(Plugin):
    myConf = {'pluginEnable' : True,
              'panel':'PlayerMessagesPanel',
              'color': 'gold'
              }
        
    def run(self):
        saveOldFuncs()
        g_windowsManager.onInitBattleGUI += SpotExtended.start
        BattleFeedbackAdaptor.setPlayerAssistResult = SpotExtended.setPlayerAssistResult
    
    
    #Show message on specified panel: VehicleErrorsPanel, VehicleMessagesPanel, PlayerMessagesPanel
    @staticmethod
    def showMessageOnPanel(panel, msgText, color, index = 0):
        if g_windowsManager.battleWindow is not None and panel in ('VehicleErrorsPanel', 'VehicleMessagesPanel', 'PlayerMessagesPanel'):
            g_windowsManager.battleWindow.call('battle.' + panel + '.ShowMessage', [index, msgText, color])

    @staticmethod
    def start():
        if g_sessionProvider is not None and g_sessionProvider.getFeedback() is not None:
            g_sessionProvider._BattleSessionProvider__feedback.stop()
            g_sessionProvider._BattleSessionProvider__feedback = BattleFeedbackAdaptor()
            g_sessionProvider._BattleSessionProvider__feedback.start(g_sessionProvider._BattleSessionProvider__arenaDP)

    @staticmethod
    def setPlayerAssistResult(self, assistType, vehiclesIDs):
        old__start(self, assistType, vehiclesIDs)
        if assistType == _SET.SPOTTED:
            arena = BigWorld.player().arena
            for idV in vehiclesIDs:
                entryVehicle = arena.vehicles[idV]
                vehicleDescr = entryVehicle['vehicleType']
                vehicleType = vehicleDescr.type
                shortName = vehicleType.shortUserString
                SpotExtended.showMessageOnPanel(SpotExtended.myConf['panel'],shortName,SpotExtended.myConf['color'])
        
def saveOldFuncs():
    global old__start
    old__start = BattleFeedbackAdaptor.setPlayerAssistResult