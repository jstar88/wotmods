# -*- coding: utf-8 -*-

# @author: BirrettaMalefica EU
from messenger.proto import getBattleCommandFactory
from messenger.gui.Scaleform.channels.bw_chat2.factories import BattleControllersFactory
from messenger.gui.Scaleform.channels.bw_chat2.battle_controllers import *
from chat_shared import CHAT_COMMANDS
import BigWorld
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from functools import partial
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
import time




class IngameMessanger:
    myconfig = {"TextDelay":0.5,"CommandDelay":5}
    cooldDown = 0
    def __init__(self):
        self.commandFactory = getBattleCommandFactory()
        self.commonChannelController = None
        self.teamChannelController = None
        self.squadChannelController = None
        self.initied = False
        self.pluginEnable = True
    
    # retrive channel controllers only when in battle!
    def checkInit(self):
        if self.initied:
            return
        self.initied = True
        controllers = BattleControllersFactory().init()
        for controller in controllers:
            if isinstance(controller, TeamChannelController):
                self.teamChannelController = controller
            elif isinstance(controller, CommonChannelController):
                self.commonChannelController = controller
            else:
                self.squadChannelController = controller
    
    def hasTeamChannelController(self):
        self.checkInit()
        return self.teamChannelController is not None
    def hasCommonChannelController(self):
        self.checkInit()
        return self.commonChannelController is not None
    def hasSquadChannelController(self):
        self.checkInit()
        return self.squadChannelController is not None
    
    def getTeamChannelController(self):
        self.checkInit()
        return self.teamChannelController
    def getCommonChannelController(self):
        self.checkInit()
        return self.commonChannelController
    def getSquadChannelController(self):
        self.checkInit()
        return self.squadChannelController
        
                  
    def doPing(self,controller,cellIdx):  
        command = self.commandFactory.createByCellIdx(cellIdx)
        self.sendCommand(controller,command) 
    def callHelp(self,controller):
        command = self.commandFactory.createByName(CHAT_COMMANDS.HELPME.name())
        self.sendCommand(controller,command)
        
    def sendCommand(self,controller,command):
        diff = IngameMessanger.cooldDown - BigWorld.time()
        if diff < 0:
            diff = 0
            IngameMessanger.cooldDown = BigWorld.time()
        IngameMessanger.cooldDown += IngameMessanger.myconfig['CommandDelay']
        BigWorld.callback(diff, partial(controller.sendCommand,command)) 
    def sendText(self,controller,text):
        diff = IngameMessanger.cooldDown - BigWorld.time()
        if diff < 0:
            diff = 0
            IngameMessanger.cooldDown = BigWorld.time()
        IngameMessanger.cooldDown += IngameMessanger.myconfig['TextDelay']
        BigWorld.callback(diff,partial(controller._broadcast,text))

    def readConfig(self):
        IngameMessanger.myconfig = FileUtils.readXml('scripts/client/plugins/IngameMessanger_plugin/config.xml',IngameMessanger.myconfig)     
        
    def run(self):
        pass


     