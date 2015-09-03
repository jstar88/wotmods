# -*- coding: utf-8 -*-

# @author: BirrettaMalefica EU
from game import *
#autoFlushPythonLog()
import constants
from gui.Scaleform.Battle import Battle
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from plugins.IngameMessanger_plugin.IngameMessanger import IngameMessanger
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from plugins.Engine.Plugin import Plugin

class SpotMessanger(Plugin):
    isActive = True
    myConf = {
        'ActiveByDefault':True,
        'ActivationHotkey':'KEY_F11',
        'ReloadConfigKey':'KEY_NUMPAD4',
        'DoPing':False,
        'CallHelp':False,
        'ImSpotted':'I\'m spotted at {pos}',
        'EnableSystemMsg':'enabled',
        'DisableSystemMsg':'disabled',
        'TryPlatoonMes':False,
        'AvoidRandomMes':True,
        'AvoidTrainingMes':False,
        'AvoidCompanyMes':False,
        'AvoidCyberSportMes':False,
        'AvoidClanWarMes':False,
        'AvoidHistoricalMes':False,
        'AvoidFortificationsMes':False,
        'OnTD':True,
        'OnMD':True,
        'OnHT':True,
        'OnLT':True,
        'OnSPG':True,
        'MaxTeamAmountOnRandom':0,
        'MaxTeamAmountOnTraining':0,
        'MaxTeamAmountOnCompany':0,
        'MaxTeamAmountOnCyberSport':0,
        'MaxTeamAmountOnHistorical':0,
        'MaxTeamAmountOnFortifications':0,
        'MaxTeamAmountOnClanWar':0,
        'pluginEnable' : True
        } 
    
    @staticmethod
    def getController(player):
    
        #battle type checks
        battleType = player.arena.guiType
        controller = None
        battleTypeName = ''
        if battleType == constants.ARENA_GUI_TYPE.RANDOM:
            battleTypeName = 'Random'
            if SpotMessanger.myConf['TryPlatoonMes']:
                if IngameMessanger().hasSquadChannelController():
                    controller = IngameMessanger().getSquadChannelController()
                elif SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                    return None
                else:
                    controller = IngameMessanger().getTeamChannelController()
            elif SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                return None
            else:
                controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.TRAINING:
            battleTypeName = 'Training'
            if SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.COMPANY:
            battleTypeName = 'Company'
            if SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.CYBERSPORT:
            battleTypeName = 'CyberSport'
            if SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.HISTORICAL:
            battleTypeName = 'Historical'
            if SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.SORTIE:
            battleTypeName = 'Fortifications'
            if SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        else:
            battleTypeName = 'ClanWar'
            if not SpotMessanger.myConf['Avoid'+battleTypeName+'Mes']:
                controller = IngameMessanger().getTeamChannelController()
            else:
                return None
        
        #vehicle type checks
        vehicleType = BattleUtils.getVehicleType(BattleUtils.getCurrentVehicleDesc(player))
        if vehicleType == VEHICLE_CLASS_NAME.SPG and not SpotMessanger.myConf['OnSPG']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.LIGHT_TANK and not SpotMessanger.myConf['OnLT']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.MEDIUM_TANK and not SpotMessanger.myConf['OnMD']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.HEAVY_TANK and not SpotMessanger.myConf['OnHT']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.AT_SPG and not SpotMessanger.myConf['OnTD']:
            return None
        
        #team amount checks
        maxTeamAmount = SpotMessanger.myConf['MaxTeamAmountOn'+battleTypeName]
        if maxTeamAmount > 0:
            if maxTeamAmount < BattleUtils.getTeamAmount(player):
                return None
        return controller

    @staticmethod
    def myDoPing(controller,position):
        if controller and SpotMessanger.myConf['DoPing']:
            IngameMessanger().doPing(controller,MinimapUtils.name2cell(position))
            
    @staticmethod
    def myCallHelp(controller):
        if controller and SpotMessanger.myConf['CallHelp']:
            IngameMessanger().callHelp(controller)
    
    @staticmethod
    def mySendMessage(controller,text):
        if text != "None" and text and controller:
            IngameMessanger().sendText(controller,text)
    
    #------ injected methods --------
    @staticmethod
    def showSixthSenseIndicator(self, isShow):
        if isShow and SpotMessanger.isActive:
            player = BattleUtils.getPlayer()
            position = MinimapUtils.getOwnPos(player)
            text = SpotMessanger.myConf['ImSpotted']
            controller = SpotMessanger.getController(player)
            SpotMessanger.mySendMessage(controller,text.replace("{pos}", position+""))
            SpotMessanger.myDoPing(controller,position)
            SpotMessanger.myCallHelp(controller)                
        return oldShowSixthSenseIndicatorFromSpotMessanger(self,isShow)
    
    
    @staticmethod
    def handleActivationHotkey():
        if SpotMessanger.isActive:
            BattleUtils.DebugMsg(SpotMessanger.myConf['DisableSystemMsg'], True)
        else:
            BattleUtils.DebugMsg(SpotMessanger.myConf['EnableSystemMsg'], True)
        SpotMessanger.isActive = not SpotMessanger.isActive
        
    #--------- end ---------
    @classmethod
    def run(cls):
        super(SpotMessanger, SpotMessanger).run()
        cls.addEventHandler(SpotMessanger.myConf['ReloadConfigKey'],cls.reloadConfig)
        cls.addEventHandler(SpotMessanger.myConf['ActivationHotkey'],SpotMessanger.handleActivationHotkey)
        saveOldFuncs()
        injectNewFuncs()
        
    @classmethod
    def readConfig(cls):
        super(SpotMessanger, SpotMessanger).readConfig()
        SpotMessanger.isActive = SpotMessanger.myConf['ActiveByDefault']
        
def saveOldFuncs():
    global oldShowSixthSenseIndicatorFromSpotMessanger
    DecorateUtils.ensureGlobalVarNotExist('oldShowSixthSenseIndicatorFromSpotMessanger')
    oldShowSixthSenseIndicatorFromSpotMessanger = Battle._showSixthSenseIndicator
    
def injectNewFuncs():
    Battle._showSixthSenseIndicator = SpotMessanger.showSixthSenseIndicator
    
    
