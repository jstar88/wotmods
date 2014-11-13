from messenger.proto import getBattleCommandFactory
from messenger.gui.Scaleform.channels.bw_chat2.factories import BattleControllersFactory
from messenger.gui.Scaleform.channels.bw_chat2.battle_controllers import *
from gui.WindowsManager import g_windowsManager

class IngameMessanger:
	def __init__(self):
		self.commandFactory = None
		self.commonChannelController = None
		self.teamChannelController = None
		self.squadChannelController = None
		self.init()
	
	def init(self):
		self.commandFactory = getBattleCommandFactory()
		controllers = BattleControllersFactory().init()
		for controller in controllers:
			if isinstance(controller, TeamChannelController):
				self.teamChannelController = controller
			elif isinstance(controller, CommonChannelController):
				self.commonChannelController = controller
			else:
				self.squadChannelController = controller
	
	def hasTeamChannelController(self):
		return self.teamChannelController is not None
	def hasCommonChannelController(self):
		return self.commonChannelController is not None
	def hasSquadChannelController(self):
		return self.squadChannelController is not None
	
	def getTeamChannelController(self):
		return self.teamChannelController
	def getCommonChannelController(self):
		return self.commonChannelController
	def getSquadChannelController(self):
		return self.squadChannelController
		
	def sendCommand(self,controller,command):
		controller.sendCommand(command)
				
	def doPing(self,controller,cellIdx):			
		command = self.commandFactory.createByCellIdx(cellIdx)
		self.sendCommand(controller,command)
	
	def callHelp(self,controller):
		command = self.commandFactory.createByName(CHAT_COMMANDS.HELPME.name())
		self.sendCommand(controller,command)
	
	def sendText(self,controller,text):
		controller._broadcast(text)

def new_enable():
	global g_ingameMessanger
	g_ingameMessanger = IngameMessanger()
g_ingameMessanger	= None
g_windowsManager.onInitBattleGUI += new_enable