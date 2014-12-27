from gui.battle_control.ChatCommandsController import ChatCommandsController
from Avatar import PlayerAvatar
from MarkersStorage import MarkersStorage
from markersUtils import showMarker
import BigWorld
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from warnings import catch_warnings
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE

class Focus:

    lastCallback = None
    myconfig = {"pluginEnable":False} 
    
    def __init__(self):
        self.pluginEnable = False
        
    def readConfig(self):
        Focus.myconfig = FileUtils.readXml('scripts/client/plugins/Focus_plugin/config.xml',Focus.myconfig)
        self.pluginEnable = Focus.myconfig["pluginEnable"]
        
    def run(self):
        saveOldFuncs()
        injectNewFuncs()
               
    @staticmethod 
    def new_onLeaveWorld(self):
        MarkersStorage.clear()
        if Focus.lastCallback is not None:
            try:
                BigWorld.cancelCallback(Focus.lastCallback)
            except:
                pass
            Focus.lastCallback = None
        old_onLeaveWorld(self)
    
    @staticmethod
    def new_onEnterWorld(self, prereqs):
        old_onEnterWorld(self, prereqs)
        
    @staticmethod
    def check():
        MarkersStorage.updateMarkers()
        Focus.lastCallback = BigWorld.callback(0.7,Focus.check)

    @staticmethod
    def new_handlePublicCommand(self, cmd):
        old_handlePublicCommand(self, cmd)
        receiverID = cmd.getFirstTargetID()
        #vehicle = BigWorld.player().arena.vehicles[receiverID]
        #distance = (BigWorld.player().getOwnVehiclePosition() - vehicle.position).length
        if receiverID:
            showMarker(receiverID)
        
def saveOldFuncs():
    global old_onLeaveWorld,old_onEnterWorld,old_handlePublicCommand
    DecorateUtils.ensureGlobalVarNotExist('old_onLeaveWorld')
    DecorateUtils.ensureGlobalVarNotExist('old_onEnterWorld')
    DecorateUtils.ensureGlobalVarNotExist('old_handlePublicCommand')

    old_onLeaveWorld = PlayerAvatar.onLeaveWorld
    old_onEnterWorld = PlayerAvatar.onEnterWorld
    old_handlePublicCommand = ChatCommandsController._ChatCommandsController__handlePublicCommand

def injectNewFuncs():
    PlayerAvatar.onLeaveWorld = Focus.new_onLeaveWorld
    PlayerAvatar.onEnterWorld = Focus.new_onEnterWorld
    ChatCommandsController._ChatCommandsController__handlePublicCommand = Focus.new_handlePublicCommand