import FMOD
import SoundGroups
import BigWorld
import ResMgr
import GUI
from gui.Scaleform.Battle import Battle
from gui.WindowsManager import g_windowsManager
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from functools import partial
from gui.shared.utils.HangarSpace import _HangarSpace
from gui import GUI_SETTINGS
import re
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils

class SixthSenseDuration:
    myConf = {
              'AudioPath': '/GUI/notifications_FX/cybersport_timer',
              'AudioRange': 9000,
              'AudioTick': 1000,
              'IconRange': 2000,
              'Volume': 1.0,
              'VolumeType': "gui",
              'TimerColor': "#FF8000",
              'TimerFont': 'verdana_medium.font',
              'TimerPosition': "(round(x / 2) + 120, round(y / 6) + 20, 0.7)",
              'TimerRange': 9000,
              'TimerTick': 1000,
              'TimerZeroDelay': 200,
              'TimerText': "%s",
              'pluginEnable' : True
    }
    guiCountDown = None
    backupVolume = None 
    
    
    def __init__(self):
        self.pluginEnable = False
    
    # --------------- audio ------------- #
    @staticmethod
    def playSound(sound,i):
        if i < 1:
            SixthSenseDuration.sequenceEnd()
            return
        sound.stop()
        sound.play()
        i -= 1
        BigWorld.callback(SixthSenseDuration.myConf['AudioTick']/1000, partial(SixthSenseDuration.playSound,sound,i))
    
    @staticmethod
    def sequenceEnd():
        SoundGroups.g_instance.setVolume(SixthSenseDuration.myConf['VolumeType'],SixthSenseDuration.backupVolume)
    
    @staticmethod
    def new_showSixthSenseIndicator(self, isShow):
        old_showSixthSenseIndicatorFromSixthSenseDuration(self, isShow)
        SixthSenseDuration.startGuiCountDown()
        sound = SoundGroups.g_instance.FMODgetSound(SixthSenseDuration.myConf['AudioPath'])
        #sound.stop()
        i = SixthSenseDuration.myConf['AudioRange'] / SixthSenseDuration.myConf['AudioTick']
        SixthSenseDuration.backupVolume = SoundGroups.g_instance.getVolume(SixthSenseDuration.myConf['VolumeType'])
        SoundGroups.g_instance.setVolume(SixthSenseDuration.myConf['VolumeType'],SixthSenseDuration.myConf['Volume'])
        SixthSenseDuration.playSound(sound,i)

    # --------------- icon ------------- #
    @staticmethod
    def new_spaceDone(self):
        old_spaceDoneFromSixthSenseDuration(self)
        GUI_SETTINGS._GuiSettings__settings['sixthSenseDuration'] = SixthSenseDuration.myConf['IconRange']


    # --------------- countdown ------------- #
    @staticmethod
    def initGuiCountDown():
        if SixthSenseDuration.guiCountDown is not None:
            return
        SixthSenseDuration.guiCountDown = GUI.Text('')
        GUI.addRoot(SixthSenseDuration.guiCountDown)
        SixthSenseDuration.guiCountDown.widthMode = 'PIXEL'
        SixthSenseDuration.guiCountDown.heightMode = 'PIXEL'
        SixthSenseDuration.guiCountDown.verticalPositionMode = 'PIXEL'
        SixthSenseDuration.guiCountDown.horizontalPositionMode = 'PIXEL'
        SixthSenseDuration.guiCountDown.horizontalAnchor = 'LEFT'
        SixthSenseDuration.guiCountDown.colourFormatting = True
        SixthSenseDuration.guiCountDown.font = SixthSenseDuration.myConf['TimerFont']
        SixthSenseDuration.guiCountDown.visible = False
        x, y = GUI.screenResolution()
        SixthSenseDuration.guiCountDown.position = eval(SixthSenseDuration.myConf['TimerPosition'])
    
    @staticmethod
    def startGuiCountDown():
        if SixthSenseDuration.myConf['TimerRange'] == 0:
            return
        if SixthSenseDuration.guiCountDown is None:
            SixthSenseDuration.initGuiCountDown()
        SixthSenseDuration.guiCountDown.visible = True
        max = SixthSenseDuration.myConf['TimerRange'] / 1000
        min = - 1
        diff = - SixthSenseDuration.myConf['TimerTick'] / 1000
        for i in xrange(max,min,diff):
            BigWorld.callback(i, partial(SixthSenseDuration.tickGuiCountDown,max-i))
    
    @staticmethod
    def endGuiCountDown():
        if SixthSenseDuration.guiCountDown is not None:
            SixthSenseDuration.guiCountDown.visible = False
    
    @staticmethod    
    def tickGuiCountDown(i):
        color = SixthSenseDuration.myConf['TimerColor']
        color = '\\c' + re.sub('[^A-Za-z0-9]+', '', color) + 'FF;'
        SixthSenseDuration.guiCountDown.text = color + SixthSenseDuration.myConf['TimerText'] % (str(i))
        if i == 0:
            BigWorld.callback(SixthSenseDuration.myConf['TimerZeroDelay']/1000,SixthSenseDuration.endGuiCountDown )

    def readConfig(self):
        SixthSenseDuration.myConf = FileUtils.readConfig('scripts/client/plugins/SixthSenseDuration_plugin/config.xml',SixthSenseDuration.myConf,"SixthSenseDuration")
        self.pluginEnable =  SixthSenseDuration.myConf['pluginEnable']
    
    def run(self):
        saveOldFuncs()
        injectNewFuncs()
        
def saveOldFuncs():
    global old_showSixthSenseIndicatorFromSixthSenseDuration,old_spaceDoneFromSixthSenseDuration
    DecorateUtils.ensureGlobalVarNotExist('old_showSixthSenseIndicatorFromSixthSenseDuration')
    DecorateUtils.ensureGlobalVarNotExist('old_spaceDoneFromSixthSenseDuration')
    old_showSixthSenseIndicatorFromSixthSenseDuration = Battle.showSixthSenseIndicator
    old_spaceDoneFromSixthSenseDuration = _HangarSpace._HangarSpace__spaceDone
    
def injectNewFuncs():
    Battle.showSixthSenseIndicator = SixthSenseDuration.new_showSixthSenseIndicator
    _HangarSpace._HangarSpace__spaceDone = SixthSenseDuration.new_spaceDone    
    g_windowsManager.onInitBattleGUI += SixthSenseDuration.initGuiCountDown
    g_windowsManager.onDestroyBattleGUI += SixthSenseDuration.endGuiCountDown
