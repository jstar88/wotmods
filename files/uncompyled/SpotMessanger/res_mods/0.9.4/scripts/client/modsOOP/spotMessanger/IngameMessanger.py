# -*- coding: utf-8 -*-

# @author: BirrettaMalefica EU
from messenger.proto import getBattleCommandFactory
from messenger.gui.Scaleform.channels.bw_chat2.factories import BattleControllersFactory
from messenger.gui.Scaleform.channels.bw_chat2.battle_controllers import *
from gui.WindowsManager import g_windowsManager
from chat_shared import CHAT_COMMANDS

class IngameMessanger:
    def __init__(self):
        self.commandFactory = getBattleCommandFactory()
        self.commonChannelController = None
        self.teamChannelController = None
        self.squadChannelController = None
        self.initied = False
    
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
        
    def sendCommand(self,controller,command):
        controller.sendCommand(command) 
    def sendText(self,controller,text):
        controller._broadcast(text)
                  
    def doPing(self,controller,cellIdx):            
        command = self.commandFactory.createByCellIdx(cellIdx)
        self.sendCommand(controller,command) 
    def callHelp(self,controller):
        command = self.commandFactory.createByName(CHAT_COMMANDS.HELPME.name())
        self.sendCommand(controller,command) 