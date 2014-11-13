# -*- coding: utf-8 -*-

# @author: BirrettaMalefica EU
from game import *
autoFlushPythonLog()
import BigWorld
import game
import math
import Keys
import string
import ResMgr
import constants
from gui.Scaleform.Battle import Battle
from gui.WindowsManager import g_windowsManager
from messenger import MessengerEntry
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from gui.shared.gui_items.Vehicle import VEHICLE_TYPES_ORDER, VEHICLE_CLASS_NAME
from modsOOP.spotMessanger.IngameMessanger import g_ingameMessanger

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
        'MaxTeamAmountOnClanWar':0
        }
    
    def __init__(self):
        SpotMessanger.myconfig = SpotMessanger.readXml('scripts/client/modsOOP/spotMessanger/config.xml',SpotMessanger.myconfig)
        #LOG_NOTE(SpotMessanger.myconfig)
        SpotMessanger.myconfig['ActivationHotkey'] = SpotMessanger.parseHotkeys(SpotMessanger.myconfig['ActivationHotkey'])
        SpotMessanger.isActive = SpotMessanger.myconfig['ActiveByDefault']
        
            
    #------ usefull functions --------
    @staticmethod
    def readXml(path,defset):
        cfg = ResMgr.openSection(path)
        if cfg is None:
            LOG_ERROR('no config found')
            return defset
        a = {}
        for key, value in defset.iteritems():
            if type(value) is int:
                a[key] = cfg.readInt(key,value)
            elif type(value) is float:
                a[key] = cfg.readFloat(key,value)
            elif type(value) is str:
                a[key] = cfg.readString(key,value)
            elif type(value) is bool:
                a[key] = cfg.readBool(key,value)
            else:
                LOG_ERROR('type not found',type(value))
        return a
    
    @staticmethod
    def getPlayer():
        return BigWorld.player()
    
    @staticmethod
    def DebugMsg(text, doHighlight = False):
        MessengerEntry.g_instance.gui.addClientMessage(text, doHighlight)

    @staticmethod
    def clamp(val, vmin, vmax):
        if val < vmin:
            return vmin
        if val > vmax:
            return vmax
        return val

    @staticmethod
    def pos2name(pos):
        sqr = 'KJHGFEDCBA'
        line = '1234567890'
        return '%s%s' % (sqr[int(pos[1]) - 1], line[int(pos[0]) - 1])

    @staticmethod
    def getSquareForPos(position,player):
        position = (position[0], position[2])
        arenaDesc = player.arena.arenaType
        bottomLeft, upperRight = arenaDesc.boundingBox
        spaceSize = upperRight - bottomLeft
        relPos = position - bottomLeft
        relPos[0] = SpotMessanger.clamp(relPos[0], 0.1, spaceSize[0])
        relPos[1] = SpotMessanger.clamp(relPos[1], 0.1, spaceSize[1])
        return SpotMessanger.pos2name((math.ceil(relPos[0] / spaceSize[0] * 10), math.ceil(relPos[1] / spaceSize[1] * 10)))

    @staticmethod
    def name2cell(name):
        if name == '%(ownPos)s':
            return 100
        if name == '%(viewPos)s':
            return 101
        try:
            row = string.ascii_uppercase.index(name[0])
            if row > 8:
                row = row - 1
            column = (int(name[1]) + 9) % 10
            return row + column * 10
        except Exception as e:
            return -1

    @staticmethod
    def getOwnPos(player):
        ownPos = BigWorld.entities[player.playerVehicleID].position
        return SpotMessanger.getSquareForPos(ownPos,player)

    @staticmethod
    def parseHotkeys(hotkeyString):
        return filter(lambda keycode: keycode > 0, map(lambda code: getattr(Keys, code, 0), hotkeyString.split('+')))

    @staticmethod
    def keysMatch(inputSet, targetSet):
        return len(targetSet) and len(filter(lambda k: k in inputSet, targetSet)) == len(targetSet)

    @staticmethod
    def getCurrentVehicleDesc(player):
        vehicles = player.arena.vehicles
        for vID, desc in vehicles.items():
            if vID == player.playerVehicleID:
                return desc
    
    @staticmethod
    def getVehicleType(currentVehicleDesc):
        for vehicleType in VEHICLE_TYPES_ORDER:
            if vehicleType in currentVehicleDesc['vehicleType'].type.tags:
                return vehicleType
    
    @staticmethod
    def getTeamAmount(player):
        count = 0
        for vID, desc in player.arena.vehicles.items():
            if    desc['team'] == player.team and desc['isAlive']:
                count += 1
        return count
    
    #--------- end ---------
    
    @staticmethod
    def getController(player):
    
        #battle type checks
        battleType = player.arena.guiType
        controller = None
        battleTypeName = ''
        if battleType == constants.ARENA_GUI_TYPE.RANDOM:
            battleTypeName = 'Random'
            if SpotMessanger.myconfig['TryPlatoonMes']:
                if g_ingameMessanger.hasSquadChannelController():
                    controller = g_ingameMessanger.getSquadChannelController()
                elif SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                    return None
                else:
                    controller = g_ingameMessanger.getTeamChannelController()
            elif SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            else:
                controller = g_ingameMessanger.getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.TRAINING:
            battleTypeName = 'Training'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = g_ingameMessanger.getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.COMPANY:
            battleTypeName = 'Company'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = g_ingameMessanger.getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.CYBERSPORT:
            battleTypeName = 'CyberSport'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = g_ingameMessanger.getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.HISTORICAL:
            battleTypeName = 'Historical'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = g_ingameMessanger.getTeamChannelController()
        elif battleType == constants.ARENA_GUI_TYPE.SORTIE:
            battleTypeName = 'Fortifications'
            if SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                return None
            controller = g_ingameMessanger.getTeamChannelController()
        else:
            battleTypeName = 'ClanWar'
            if not SpotMessanger.myconfig['Avoid'+battleTypeName+'Mes']:
                controller = g_ingameMessanger.getTeamChannelController()
            else:
                return None
        
        #vehicle type checks
        vehicleType = SpotMessanger.getVehicleType(SpotMessanger.getCurrentVehicleDesc(player))
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
            if maxTeamAmount < SpotMessanger.getTeamAmount(player):
                return None
        return controller

    @staticmethod
    def myDoPing(controller,position):
        if controller and SpotMessanger.myconfig['DoPing']:
            g_ingameMessanger.doPing(controller,SpotMessanger.name2cell(position))
            
    @staticmethod
    def myCallHelp(controller):
        if controller and SpotMessanger.myconfig['CallHelp']:
            g_ingameMessanger.callHelp(controller)
    
    @staticmethod
    def mySendMessage(controller,text):
        if text != "None" and text:
            g_ingameMessanger.sendText(controller,text)
    
    #------ injected methods --------
    @staticmethod
    def showSixthSenseIndicator(self, isShow):
        if isShow and SpotMessanger.isActive:
            player = SpotMessanger.getPlayer()
            position = SpotMessanger.getOwnPos(player)
            text = SpotMessanger.myconfig['ImSpotted']
            controller = SpotMessanger.getController(player)
            SpotMessanger.mySendMessage(controller,text.replace("{pos}", position+""))
            SpotMessanger.myDoPing(controller,position)
            SpotMessanger.myCallHelp(controller)                
        return Battle.oldShowSixthSenseIndicator(self,isShow)
    
    
    @staticmethod
    def handleKeyEvent(event):
        try:
            isDown, key, mods, isRepeat = game.convertKeyEvent(event)
            if not isRepeat and isDown and SpotMessanger.keysMatch([key],SpotMessanger.myconfig['ActivationHotkey']):
                if SpotMessanger.isActive:
                    SpotMessanger.DebugMsg(SpotMessanger.myconfig['DisableSystemMsg'], True)
                else:
                    SpotMessanger.DebugMsg(SpotMessanger.myconfig['EnableSystemMsg'], True)
                SpotMessanger.isActive = not SpotMessanger.isActive
                return
        except Exception as e:
            LOG_CURRENT_EXCEPTION()
        finally:
            return game.oldHandleKeyEvent(event)
        
    #--------- end ---------
    def inject(self):
        Battle.oldShowSixthSenseIndicator = Battle.showSixthSenseIndicator
        Battle.showSixthSenseIndicator = SpotMessanger.showSixthSenseIndicator
        
        game.oldHandleKeyEvent = game.handleKeyEvent
        game.handleKeyEvent = SpotMessanger.handleKeyEvent
