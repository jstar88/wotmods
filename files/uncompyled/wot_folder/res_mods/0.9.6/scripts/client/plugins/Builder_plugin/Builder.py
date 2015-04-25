import sys
import os
from plugins.Engine.ModUtils import BattleUtils, MinimapUtils, FileUtils, HotKeysUtils, DecorateUtils
from PathManager import PathManager
from MyModel import MyModel
from ModelManager import ModelManager
from gui.WindowsManager import g_windowsManager
import game
import BigWorld
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from constants import SERVER_TICK_LENGTH
import constants
import BattleReplay

class Builder:
    pm = None
    mm = None
    currentPath = ''
    currentPreview = None
    moving = False
    inBattle = False
    blockMove = False
    
    myconfig = {
        'pluginEnable': False,
        'NextModel':'KEY_ADD',
        'PrevModel': 'KEY_MINUS',
        'SaveModel': 'KEY_NUMPADENTER',
        'BlockMoving': 'KEY_NUMPAD5',
        'RotateLeft':'KEY_NUMPAD4',
        'RotateRight':'KEY_NUMPAD6',
        'IncreaseAltitude':'KEY_NUMPAD8',
        'DecreaseAltitude':'KEY_NUMPAD2',
        'RotationTick': 0.2,
        'AltitudeTick':0.5
        }
    
    def __init__(self):
        self.pluginEnable = False
        
    def readConfig(self):
        Builder.myconfig = FileUtils.readConfig('scripts/client/plugins/Builder_plugin/config.xml',Builder.myconfig,"Builder")
        self.pluginEnable =  Builder.myconfig['pluginEnable']
        
    def run(self):
        saveOldFuncs()
        injectNewFuncs()
        Builder.pm = PathManager()
    
    @staticmethod
    def handleKeyEvent(event):
        if not hasattr(BigWorld.player(),'arena') or ( not Builder.isTraining() and not Builder.isReply()):
            return oldHandleKeyEventFromBuilder(event)
        try:
            isDown, key, mods, isRepeat = game.convertKeyEvent(event)
            if not isRepeat and isDown:
                if HotKeysUtils.keyMatch(key, Builder.myconfig['NextModel']):
                    Builder.blockMove = False
                    Builder.inBattle = True
                    Builder.currentPath = Builder.pm.getNextPath()
                    position = BigWorld.player().inputHandler.getDesiredShotPoint()
                    if Builder.currentPreview is not None:
                        Builder.currentPreview.remove()
                    Builder.currentPreview = MyModel(-1, position, 0, Builder.currentPath)
                    if not Builder.moving:
                        BigWorld.callback(SERVER_TICK_LENGTH, Builder.previewMove)
                        Builder.moving = True
                        
                if HotKeysUtils.keyMatch(key, Builder.myconfig['PrevModel']):
                    Builder.blockMove = False
                    Builder.inBattle = True
                    Builder.currentPath = Builder.pm.getNextPath()
                    position = BigWorld.player().inputHandler.getDesiredShotPoint()
                    if Builder.currentPreview is not None:
                        Builder.currentPreview.remove()
                    Builder.currentPreview = MyModel(-1, position, 0, Builder.currentPath)
                    if not Builder.moving:
                        BigWorld.callback(SERVER_TICK_LENGTH, Builder.previewMove)
                        Builder.moving = True
                    
                if HotKeysUtils.keyMatch(key,  Builder.myconfig['SaveModel']):
                    position = BigWorld.player().inputHandler.getDesiredShotPoint()
                    yaw = 0
                    if Builder.currentPreview is not None:
                        yaw = Builder.currentPreview.getYaw()
                        position = Builder.currentPreview.getPosition()
                    Builder.mm.addModel(position, yaw, Builder.currentPath)
                    Builder.blockMove = False
                    
                if HotKeysUtils.keyMatch(key, Builder.myconfig['BlockMoving']):
                     Builder.blockMove = not Builder.blockMove
                    
                if HotKeysUtils.keyMatch(key, Builder.myconfig['RotateLeft']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseRotation(Builder.myconfig['RotationTick'])
                    
                if HotKeysUtils.keyMatch(key, Builder.myconfig['RotateRight']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseRotation(-Builder.myconfig['RotationTick'])
                
                if HotKeysUtils.keyMatch(key, Builder.myconfig['IncreaseAltitude']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseAltitude(Builder.myconfig['AltitudeTick'])
                
                if HotKeysUtils.keyMatch(key, Builder.myconfig['DecreaseAltitude']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseAltitude(-Builder.myconfig['AltitudeTick'])
                    
        except Exception as e:
            LOG_CURRENT_EXCEPTION()
        finally:
            return oldHandleKeyEventFromBuilder(event)
    
    
    @staticmethod
    def previewMove():
        if not Builder.inBattle or Builder.currentPreview is None:
            Builder.moving = False
            return
        
        if not Builder.blockMove:
            position = BigWorld.player().inputHandler.getDesiredShotPoint()
            Builder.currentPreview.move(position)
        BigWorld.callback(SERVER_TICK_LENGTH, Builder.previewMove)
        
    
    @staticmethod
    def initGui():
        if not Builder.isTraining() and not Builder.isReply():
            return
        Builder.mm = ModelManager(Builder.getMapName())
        Builder.currentPath = Builder.pm.getNextPath()
        Builder.inBattle = True
        Builder.moving = False
        Builder.blockMove = False
    
    @staticmethod
    def endGui():
        Builder.mm.clean()
        Builder.pm.resetPointer()
        Builder.inBattle = False
        
        
    @staticmethod
    def isTraining():
        return BigWorld.player().arena.guiType == constants.ARENA_GUI_TYPE.TRAINING
    
    @staticmethod
    def getMapName():
        return BigWorld.player().arena.arenaType.name
    
    @staticmethod
    def isReply():
        return BattleReplay.g_replayCtrl.isPlaying
        
        
def saveOldFuncs():
    global oldHandleKeyEventFromBuilder
    DecorateUtils.ensureGlobalVarNotExist('oldHandleKeyEventFromBuilder')
    oldHandleKeyEventFromBuilder = game.handleKeyEvent
    
def injectNewFuncs():
    game.handleKeyEvent = Builder.handleKeyEvent
    g_windowsManager.onInitBattleGUI += Builder.initGui
    g_windowsManager.onDestroyBattleGUI += Builder.endGui
