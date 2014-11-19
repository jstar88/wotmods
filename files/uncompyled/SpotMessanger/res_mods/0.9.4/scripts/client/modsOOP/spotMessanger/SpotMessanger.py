# -*- coding: utf-8 -*-

# @author: BirrettaMalefica EU
from game import *
autoFlushPythonLog()
import game
import constants
from gui.Scaleform.Battle import Battle
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from modsOOP.spotMessanger.IngameMessanger import IngameMessanger
from modsOOP.spotMessanger.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from functools import partial
import BigWorld

class SpotMessanger:
    isActive = True
    myconfig = {
        'ActiveByDefault':True,
        'ActivationHotkey':'KEY_F11',
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
        'Delay': 0.120
        }
    
    def __init__(self):
        SpotMessanger.myconfig = FileUtils.readXml('scripts/client/modsOOP/spotMessanger/config.xml',SpotMessanger.myconfig)
        #LOG_NOTE(SpotMessanger.myconfig)
        SpotMessanger.myconfig['ActivationHotkey'] = HotKeysUtils.parseHotkeys(SpotMessanger.myconfig['ActivationHotkey'])
        SpotMessanger.isActive = SpotMessanger.myconfig['ActiveByDefault']
        
            
    
    
    @staticmethod
    def getController(player):
    
        #battle type checks
        battleType = player.arena.guiType
        controller = None
        battleTypeName = ''
        if battleType == constants.ARENA_GUI_TYPE.RANDOM:
            battleTypeName = 'Random'
            if SpotMessanger.myconfig['TryPlatoonMes']:
                if IngameMessanger().hasSquadChannelController():
                    controller = IngameMessanger().getSquadChannelController()
                elif SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                    return None
                else:
                    controller = IngameMessanger().getTeamChannelController()
            elif SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            else:
                controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.TRAINING:
            battleTypeName = 'Training'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.COMPANY:
            battleTypeName = 'Company'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.CYBERSPORT:
            battleTypeName = 'CyberSport'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.HISTORICAL:
            battleTypeName = 'Historical'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.SORTIE:
            battleTypeName = 'Fortifications'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = IngameMessanger().getTeamChannelController()
        else:
            battleTypeName = 'ClanWar'
            if not SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                controller = IngameMessanger().getTeamChannelController()
            else:
                return None
        
        #vehicle type checks
        vehicleType = BattleUtils.getVehicleType(BattleUtils.getCurrentVehicleDesc(player))
        if vehicleType == VEHICLE_CLASS_NAME.SPG and not SpotMessanger.myconfig['OnSPG']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.LIGHT_TANK and not SpotMessanger.myconfig['OnLT']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.MEDIUM_TANK and not SpotMessanger.myconfig['OnMD']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.HEAVY_TANK and not SpotMessanger.myconfig['OnHT']:
            return None
        elif vehicleType == VEHICLE_CLASS_NAME.AT_SPG and not SpotMessanger.myconfig['OnTD']:
            return None
        
        #team amount checks
        maxTeamAmount = SpotMessanger.myconfig['MaxTeamAmountOn'+battleTypeName]
        if maxTeamAmount > 0:
            if maxTeamAmount < BattleUtils.getTeamAmount(player):
                return None
        return controller

    @staticmethod
    def myDoPing(controller,position):
        if controller and SpotMessanger.myconfig['DoPing']:
            IngameMessanger().doPing(controller,MinimapUtils.name2cell(position))
            
    @staticmethod
    def myCallHelp(controller):
        if controller and SpotMessanger.myconfig['CallHelp']:
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
            text = SpotMessanger.myconfig['ImSpotted']
            controller = SpotMessanger.getController(player)
            SpotMessanger.mySendMessage(controller,text.replace("{pos}", position+""))
            BigWorld.callback(SpotMessanger.myconfig['Delay'],partial(SpotMessanger.myDoPing,controller,position))
            BigWorld.callback(SpotMessanger.myconfig['Delay'],partial(SpotMessanger.myCallHelp,controller))                
        return oldShowSixthSenseIndicatorFromSpotMessanger(self,isShow)
    
    
    @staticmethod
    def handleKeyEvent(event):
        try:
            isDown, key, mods, isRepeat = game.convertKeyEvent(event)
            if not isRepeat and isDown and HotKeysUtils.keysMatch([key],SpotMessanger.myconfig['ActivationHotkey']):
                if SpotMessanger.isActive:
                    BattleUtils.DebugMsg(SpotMessanger.myconfig['DisableSystemMsg'], True)
                else:
                    BattleUtils.DebugMsg(SpotMessanger.myconfig['EnableSystemMsg'], True)
                SpotMessanger.isActive = not SpotMessanger.isActive
                return
        except Exception as e:
            LOG_CURRENT_EXCEPTION()
        finally:
            return oldHandleKeyEventFromSpotMessanger(event)
        
    #--------- end ---------
    def inject(self):
        saveOldFuncs()
        injectNewFuncs()
        
def saveOldFuncs():
    global oldShowSixthSenseIndicatorFromSpotMessanger,oldHandleKeyEventFromSpotMessanger
    DecorateUtils.ensureGlobalVarNotExist('oldShowSixthSenseIndicatorFromSpotMessanger')
    DecorateUtils.ensureGlobalVarNotExist('oldHandleKeyEventFromSpotMessanger')
    oldShowSixthSenseIndicatorFromSpotMessanger = Battle.showSixthSenseIndicator
    oldHandleKeyEventFromSpotMessanger = game.handleKeyEvent
    
def injectNewFuncs():
    Battle.showSixthSenseIndicator = SpotMessanger.showSixthSenseIndicator
    game.handleKeyEvent = SpotMessanger.handleKeyEvent
