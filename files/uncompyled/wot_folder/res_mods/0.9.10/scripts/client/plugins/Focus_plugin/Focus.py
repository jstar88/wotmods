from gui.battle_control.ChatCommandsController import ChatCommandsController
from Avatar import PlayerAvatar
from MarkersStorage import MarkersStorage
from markersUtils import showMarker
import BigWorld
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from warnings import catch_warnings
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from chat_shared import CHAT_COMMANDS
from plugins.Engine.Plugin import Plugin
from gui.app_loader import g_appLoader
from gui.shared import g_eventBus, events
from gui.app_loader.settings import APP_NAME_SPACE as _SPACE

class Focus(Plugin):

    lastCallback = None
    inBattle = False
    myConf = {
                'reloadConfigKey': 'KEY_NUMPAD1',
                "pluginEnable":False,
                "setVName":False,
                "swf_path":"gui/scaleform",
                "maxArrows":3,
                "maxArrowTime":60,
                "delIfUnspotted":True,
                "delIfNotVisible":False,
                "delIfDeath":True,
                "colors":("red", "purple"),
                "swf_file_name":"DirectionIndicator.swf",
                "flash_class":"WGDirectionIndicatorFlash",
                "flash_mc_name":"directionalIndicatorMc",
                "flash_size":(680,680),
                "heightMode":"PIXEL",
                "widthMode":"PIXEL",
                "relativeRadius":0.5,
                "moveFocus":False,
                "focus":False,
                "scaleMode":"NoScale",
                "backgroundAlpha":0.0
                } 
        
    @classmethod
    def run(cls):
        super(Focus, Focus).run()
        cls.addEventHandler(Focus.myConf['reloadConfigKey'],cls.reloadConfig)
        saveOldFuncs()
        injectNewFuncs()
               
    @staticmethod 
    def stopBattle():
        if event.ns == _SPACE.SF_BATTLE:
            Focus.inBattle = False
            MarkersStorage.clear()
            if Focus.lastCallback is not None:
                try:
                    BigWorld.cancelCallback(Focus.lastCallback)
                except:
                    pass
                Focus.lastCallback = None   
        
    @staticmethod
    def check():
        if not Focus.inBattle:
            return
        MarkersStorage.updateMarkers(Focus.myConf)
        Focus.lastCallback = BigWorld.callback(0.7,Focus.check)

    @staticmethod
    def new_handlePublicCommand(self, cmd):
        old_handlePublicCommand(self, cmd)
        if not Focus.inBattle:
            Focus.inBattle = True
            Focus.check()
        receiverID = cmd.getFirstTargetID()
        if receiverID and cmd.showMarkerForReceiver():
            showMarker(receiverID,Focus.myConf)
        
def saveOldFuncs():
    global old_handlePublicCommand
    DecorateUtils.ensureGlobalVarNotExist('old_handlePublicCommand')
    old_handlePublicCommand = ChatCommandsController._ChatCommandsController__handlePublicCommand

def injectNewFuncs():
    ChatCommandsController._ChatCommandsController__handlePublicCommand = Focus.new_handlePublicCommand
    add = g_eventBus.addListener
    appEvent = events.AppLifeCycleEvent
    add(appEvent.INITIALIZING, Focus.stopBattle)