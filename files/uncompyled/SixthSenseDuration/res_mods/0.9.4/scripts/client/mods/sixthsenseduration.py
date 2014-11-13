from game import *
autoFlushPythonLog()
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
            
# --------------- audio ------------- #
def playSound(sound,i):
    if i < 1:
        sequenceEnd()
        return
    sound.stop()
    sound.play()
    i -= 1
    BigWorld.callback(myConf['AudioTick']/1000, partial(playSound,sound,i))
    
def sequenceEnd():
    SoundGroups.g_instance.setVolume(myConf['VolumeType'],backupVolume)
    
def new_showSixthSenseIndicator(self, isShow):
    global backupVolume
    old_showSixthSenseIndicator(self, isShow)
    startGuiCountDown()
    sound = SoundGroups.g_instance.FMODgetSound(myConf['AudioPath'])
    #sound.stop()
    i = myConf['AudioRange'] / myConf['AudioTick']
    backupVolume = SoundGroups.g_instance.getVolume(myConf['VolumeType'])
    SoundGroups.g_instance.setVolume(myConf['VolumeType'],myConf['Volume'])
    playSound(sound,i)
    
    
old_showSixthSenseIndicator = Battle.showSixthSenseIndicator
Battle.showSixthSenseIndicator = new_showSixthSenseIndicator

# --------------- icon ------------- #
def new_spaceDone(self):
    old_spaceDone(self)
    GUI_SETTINGS._GuiSettings__settings['sixthSenseDuration'] = myConf['IconRange']

old_spaceDone = _HangarSpace._HangarSpace__spaceDone
_HangarSpace._HangarSpace__spaceDone = new_spaceDone

# --------------- countdown ------------- #


def initGuiCountDown():
    global guiCountDown
    if guiCountDown is not None:
        return
    guiCountDown = GUI.Text('')
    GUI.addRoot(guiCountDown)
    guiCountDown.widthMode = 'PIXEL'
    guiCountDown.heightMode = 'PIXEL'
    guiCountDown.verticalPositionMode = 'PIXEL'
    guiCountDown.horizontalPositionMode = 'PIXEL'
    guiCountDown.horizontalAnchor = 'LEFT'
    guiCountDown.colourFormatting = True
    guiCountDown.font = myConf['TimerFont']
    guiCountDown.visible = False
    x, y = GUI.screenResolution()
    guiCountDown.position = eval(myConf['TimerPosition'])

def startGuiCountDown():
    global guiCountDown
    if myConf['TimerRange'] == 0:
        return
    if guiCountDown is None:
        initGuiCountDown()
    guiCountDown.visible = True
    max = myConf['TimerRange'] / 1000
    min = - 1
    diff = - myConf['TimerTick'] / 1000
    for i in xrange(max,min,diff):
        BigWorld.callback(i, partial(tickGuiCountDown,max-i))
    
def endGuiCountDown():
    global guiCountDown
    if guiCountDown is not None:
        guiCountDown.visible = False
        
def tickGuiCountDown(i):
    global guiCountDown
    color = myConf['TimerColor']
    color = '\\c' + re.sub('[^A-Za-z0-9]+', '', color) + 'FF;'
    guiCountDown.text = color + myConf['TimerText'] % (str(i))
    if i == 0:
        BigWorld.callback(myConf['TimerZeroDelay']/1000,endGuiCountDown )
        
g_windowsManager.onInitBattleGUI += initGuiCountDown
g_windowsManager.onDestroyBattleGUI += endGuiCountDown

# --------------- config ------------- #
guiCountDown = None
backupVolume = None
myConf= {}
myConf['AudioPath'] = '/GUI/notifications_FX/cybersport_timer'
myConf['AudioRange'] = 9000
myConf['AudioTick'] = 1000
myConf['IconRange'] = 2000
myConf['Volume'] = 1.0
myConf['VolumeType'] = "gui"
myConf['TimerColor'] = "#FF8000"
myConf['TimerFont'] = 'verdana_medium.font'
myConf['TimerPosition'] = "(round(x / 2) + 120, round(y / 6) + 20, 0.7)"
myConf['TimerRange'] = 9000
myConf['TimerTick'] = 1000
myConf['TimerZeroDelay'] = 200
myConf['TimerText'] = "%s"


cfg = ResMgr.openSection('scripts/client/mods/sixthsenseduration.xml')
if cfg is None:
    LOG_ERROR('CONFIG NOT FOUND')
else:
    sec = cfg['AudioPath']
    if sec is not None:
        myConf['AudioPath'] = sec.asString
        
    sec = cfg['AudioRange']
    if sec is not None:
        myConf['AudioRange'] = sec.asFloat
        
    sec = cfg['AudioTick']
    if sec is not None:
        myConf['AudioTick'] = sec.asFloat
            
    sec = cfg['IconRange']
    if sec is not None:
        myConf['IconRange'] = sec.asFloat
        
    sec = cfg['Volume']
    if sec is not None:
        myConf['Volume'] = sec.asFloat
    
    sec = cfg['VolumeType']
    if sec is not None:
        myConf['VolumeType'] = sec.asString
        
    sec = cfg['TimerRange']
    if sec is not None:
        myConf['TimerRange'] = sec.asInt
            
    sec = cfg['TimerTick']
    if sec is not None:
        myConf['TimerTick'] = sec.asInt
        
    sec = cfg['TimerZeroDelay']
    if sec is not None:
        myConf['TimerZeroDelay'] = sec.asFloat
        
    sec = cfg['TimerColor']
    if sec is not None:
        myConf['TimerColor'] = sec.asString
        
    sec = cfg['TimerFont']
    if sec is not None:
        myConf['TimerFont'] = sec.asString
        
    sec = cfg['TimerPosition']
    if sec is not None:
        myConf['TimerPosition'] = sec.asString
        
    sec = cfg['TimerText']
    if sec is not None:
        myConf['TimerText'] = sec.asString
            