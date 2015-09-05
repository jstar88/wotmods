# 2015.09.05 18:13:47 ora legale Europa occidentale
# Embedded file name: Builder.py
import sys
import os
from plugins.Engine.ModUtils import FileUtils, HotKeysUtils, DecorateUtils
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
from plugins.Engine.Plugin import Plugin

class Builder(Plugin):
    pm = None
    mm = None
    currentPath = ''
    currentPreview = None
    moving = False
    inBattle = False
    blockMove = False
    myConf = {'pluginEnable': True,
     'NextModel': 'KEY_ADD',
     'PrevModel': 'KEY_MINUS',
     'SaveModel': 'KEY_NUMPADENTER',
     'BlockMoving': 'KEY_NUMPAD5',
     'RotateLeft': 'KEY_NUMPAD4',
     'RotateRight': 'KEY_NUMPAD6',
     'IncreaseAltitude': 'KEY_NUMPAD8',
     'DecreaseAltitude': 'KEY_NUMPAD2',
     'RotationTick': 0.2,
     'AltitudeTick': 0.5}

    @classmethod
    def run(cls):
        super(Builder, Builder).run()
        saveOldFuncs()
        injectNewFuncs()
        Builder.pm = PathManager()

    @staticmethod
    def handleKeyEvent(event):
        if not hasattr(BigWorld.player(), 'arena') or not Builder.isTraining() and not Builder.isReply():
            return oldHandleKeyEventFromBuilder(event)
        try:
            isDown, key, mods, isRepeat = game.convertKeyEvent(event)
            if not isRepeat and isDown:
                if HotKeysUtils.keyMatch(key, Builder.myConf['NextModel']):
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
                if HotKeysUtils.keyMatch(key, Builder.myConf['PrevModel']):
                    Builder.blockMove = False
                    Builder.inBattle = True
                    Builder.currentPath = Builder.pm.getPrevPath()
                    position = BigWorld.player().inputHandler.getDesiredShotPoint()
                    if Builder.currentPreview is not None:
                        Builder.currentPreview.remove()
                    Builder.currentPreview = MyModel(-1, position, 0, Builder.currentPath)
                    if not Builder.moving:
                        BigWorld.callback(SERVER_TICK_LENGTH, Builder.previewMove)
                        Builder.moving = True
                if HotKeysUtils.keyMatch(key, Builder.myConf['SaveModel']):
                    position = BigWorld.player().inputHandler.getDesiredShotPoint()
                    yaw = 0
                    if Builder.currentPreview is not None:
                        yaw = Builder.currentPreview.getYaw()
                        position = Builder.currentPreview.getPosition()
                    Builder.mm.addModel(position, yaw, Builder.currentPath)
                    Builder.blockMove = False
                if HotKeysUtils.keyMatch(key, Builder.myConf['BlockMoving']):
                    Builder.blockMove = not Builder.blockMove
                if HotKeysUtils.keyMatch(key, Builder.myConf['RotateLeft']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseRotation(Builder.myConf['RotationTick'])
                if HotKeysUtils.keyMatch(key, Builder.myConf['RotateRight']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseRotation(-Builder.myConf['RotationTick'])
                if HotKeysUtils.keyMatch(key, Builder.myConf['IncreaseAltitude']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseAltitude(Builder.myConf['AltitudeTick'])
                if HotKeysUtils.keyMatch(key, Builder.myConf['DecreaseAltitude']):
                    if Builder.currentPreview is None:
                        return
                    Builder.currentPreview.increaseAltitude(-Builder.myConf['AltitudeTick'])
        except Exception as e:
            LOG_CURRENT_EXCEPTION()
        finally:
            return oldHandleKeyEventFromBuilder(event)

    @staticmethod
    def previewMove():
        if not Builder.inBattle or Builder.currentPreview is None:
            Builder.moving = False
            return
        else:
            if not Builder.blockMove:
                position = BigWorld.player().inputHandler.getDesiredShotPoint()
                Builder.currentPreview.move(position)
            BigWorld.callback(SERVER_TICK_LENGTH, Builder.previewMove)
            return

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
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Builder_plugin\Builder.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:47 ora legale Europa occidentale
