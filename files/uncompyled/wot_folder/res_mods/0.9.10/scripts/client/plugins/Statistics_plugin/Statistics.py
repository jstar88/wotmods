#!/usr/bin/env python
# -*- coding: utf-8 -*-

# by BirrettaMalefica(eu)
 
import BigWorld
import threading
from debug_utils import LOG_ERROR
from messenger.formatters.chat_message import _BattleMessageBuilder,CommonMessageBuilder
from gui.battle_control import g_sessionProvider,arena_info
from gui import GUI_SETTINGS    
from gui.Scaleform import VoiceChatInterface
from gui.battle_control.arena_info.arena_vos import VehicleActions
from gui.Scaleform.daapi.view.battle.markers import _VehicleMarker, MarkersManager
from gui.Scaleform.daapi.view.battle_loading import BattleLoading
from gui.battle_control.battle_arena_ctrl import BattleArenaController
from gui.shared import g_eventBus, events#, EVENT_BUS_SCOPE
from EntityManagerOnline import EntityManagerOnline
from plugins.Engine.ModUtils import BattleUtils,DecorateUtils
from plugins.Engine.Plugin import Plugin
import PowerBar
import re
from gui.Scaleform.daapi.view.battle.stats_form import _StatsForm
from CTFManager import g_ctfManager
from messenger.gui.Scaleform.BattleEntry import BattleEntry
from gui.battle_control.arena_info import getClientArena, getArenaTypeID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from gui.battle_control.arena_info import hasResourcePoints, hasFlags
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.daapi.view.fallout_info_panel_helper import getHelpTextAsDicts
from gui.LobbyContext import g_lobbyContext
from helpers import tips
from gui.shared.formatters import text_styles
import constants
import GUI
from BattleLoadingBarTable import BattleLoadingBarTable
from gui.app_loader import g_appLoader
from gui.app_loader.settings import GUI_GLOBAL_SPACE_ID
import math
from gui.app_loader.settings import APP_NAME_SPACE as _SPACE

class Statistics(Plugin):
    
    emo = None
    t = None
    cache = {}
    lastime = 0 
    table = None
    myConf = {
              'pluginEnable': True,
              'reloadConfigKey': 'KEY_NUMPAD5',
              'delay' : 1,
              'maxentries' : 3,
              'cw' : False,
              'region' : 'eu',
              'pr_index': 'global_rating',
              'lang_index': 'client_language',
              'wr_index': 'statistics.all.wins',
              'battles_index': 'statistics.all.battles',
              'application_id': 'demo',
              'url': 'http://api.worldoftanks.{region}/wot/account/info/?application_id={application_id}&fields={pr_index},{lang_index},{wr_index},{battles_index}&account_id={id}',
              
              'flags_folder':'scripts/client/plugins/Statistics_plugin/flags',
              'rating_folder':'scripts/client/plugins/Statistics_plugin/ratings',
              
              'death_font_color':'#2B2323',
              'compatriot_font_color':'#2B2323',
              
              'powerbar_enable': True,
              'powerbar_texture':'system/maps/col_white.dds',
              'powerbar_width': 400,
              'powerbar_height': 5,
              'powerbar_position': '(x/2-200,y/10 - 50,0.7)',
              'powerbar_colors': ['(100, 255, 0, 100)','(255, 50, 50, 100)'],
              'powerbar_materialFX':'ADD',
              'powerbar_font':'default_small.font',
              
              'panels_enable' : True,
              'left' : "<font color='#{color_pr}'>{lang}</font>  {player_name}<br/>",
              'right' : "<font color='#{color_pr}'>{lang}</font>  {player_name}<br/>",
              
              'left_2' : "<font color='#{color_pr}'>{tank_name}</font><br/>",
              'right_2' : "<font color='#{color_pr}'>{tank_name}</font><br/>",
              
              'marker_enable' : True,
              'marker' : '{player_name} {pr}',
              
              'chat_enable' : True,
              'chat':'{player_name}|{pr}',
              
              'battle_loading_enable' : True,
              'battle_loading_string_left' : '  {lang}|{wr}%|{pr}',
              'battle_loading_string_right' : '{lang}|{wr}%|{pr}  ',
              
              'tab_enable': True,
              'tab_left': '{lang}|{wr}%|{pr}  ',
              'tab_right': '  {lang}|{wr}%|{pr}',
              
              'tab_left_2' : "<font color='#{color_pr}'>{tank_name}</font><br/>",
              'tab_right_2' : "<font color='#{color_pr}'>{tank_name}</font><br/>",
              
              'win_chance_enable': True,
              'win_chance_text': "( Chance for win: <font color='{color}'>{win_chance}%</font> )",
              'win_chance_formula':'math.tan(1.5 * ally_balance_weight/enemy_balance_weight - 1.5 )/4 + 0.5',
              
              'table_enable': True,               
              'table_texture':'scripts/client/plugins/Statistics_plugin/bg.dds',
              'table_width':500,
              'table_height':475,
              'table_position':'(x/2-250, y/2-250, 1)',
              'table_materialFX':'SOLID',
              'table_color':'(255, 255, 255, 255)',
              'table_bars_texture':'system/maps/col_white.dds',
              'table_bars_width':200,
              'table_bars_height':5,
              'table_bars_position':'(x/2-100,y/2-160,0)',
              'table_bars_delta':40,
              'table_bars_font':'default_small.font',
              'table_bars_materialFX':'ADD',
              'table_bars_color':['(100, 255, 0, 100)','(255, 50, 50, 100)'],
               VEHICLE_CLASS_NAME.LIGHT_TANK:'LT',
               VEHICLE_CLASS_NAME.MEDIUM_TANK:'MT',
               VEHICLE_CLASS_NAME.HEAVY_TANK:'HT',
               VEHICLE_CLASS_NAME.SPG:'SPG',
               VEHICLE_CLASS_NAME.AT_SPG:'TD',
               'table_bars_label':'{ally_color}{ally}{sep_color}/{enemy_color}{enemy}',
               'table_bars_label_pos':'top',
               'table_bars_tankType_show':True,
               'table_bars_label_show':True,
               'table_bars_align':'vertical',
               
               'stars_enable': True,
               'stars_position':'(x/2-100,y/2+160,0)',
               'stars_delta':40,
               'stars_size':(128,128),
               'stars_activePath':'scripts/client/plugins/Statistics_plugin/stars/active.png',
               'stars_inactivePath':'scripts/client/plugins/Statistics_plugin/stars/inactive.png',   
              
              
              'colors_pr':[{'min':0,'color':'FE0E00','image':'1'},
                        {'min':2020,'color':'FE7903','image':'2'},
                        {'min':4185,'color':'F8F400','image':'3'},
                        {'min':6340,'color':'60FF00','image':'4'},
                        {'min':8525,'color':'02C9B3','image':'5'},
                        {'min':9930,'color':'D042F3','image':'6'},
                        {'min':11000,'color':'490A59','image':'7'}],
              
              'colors_wr':[{'min':0,'color':'FE0E00','image':'1'},
                        {'min':40,'color':'FE7903','image':'2'},
                        {'min':48,'color':'F8F400','image':'3'},
                        {'min':53,'color':'60FF00','image':'4'},
                        {'min':55,'color':'02C9B3','image':'5'},
                        {'min':58,'color':'D042F3','image':'6'},
                        {'min':61,'color':'490A59','image':'7'}],
              
              'colors_bt':[{'min':0,'color':'FE0E00','image':'1'},
                        {'min':2000,'color':'FE7903','image':'2'},
                        {'min':8000,'color':'F8F400','image':'3'},
                        {'min':15000,'color':'60FF00','image':'4'},
                        {'min':22000,'color':'02C9B3','image':'5'},
                        {'min':26000,'color':'D042F3','image':'6'},
                        {'min':32000,'color':'490A59','image':'7'}],
              
              'panels_bt_divisor':1000,
              'panels_bt_decimals':0,
              'panels_pr_divisor':1000,
              'panels_pr_decimals':0,
              'panels_wr_decimals':0,
              'panels_wr_divisor':1,
              
              'chat_bt_divisor':1000,
              'chat_bt_decimals':0,
              'chat_pr_divisor':1000,
              'chat_pr_decimals':0,
              'chat_wr_decimals':0,
              'chat_wr_divisor':1,
              
              'marker_bt_divisor':1000,
              'marker_bt_decimals':0,
              'marker_pr_divisor':1000,
              'marker_pr_decimals':0,
              'marker_wr_decimals':0,
              'marker_wr_divisor':1,
              
              'battle_loading_bt_divisor':1000,
              'battle_loading_bt_decimals':0,
              'battle_loading_pr_divisor':1000,
              'battle_loading_pr_decimals':0,
              'battle_loading_wr_decimals':0,
              'battle_loading_wr_divisor':1,
              
              'tab_bt_divisor':1000,
              'tab_bt_decimals':0,
              'tab_pr_divisor':1000,
              'tab_pr_decimals':0,
              'tab_wr_decimals':0,
              'tab_wr_divisor':1
              
              }
        
    @staticmethod
    def okCw():
        return not BattleUtils.isCw() or Statistics.myConf['cw']
    
    @staticmethod
    def getEmo():
        if Statistics.emo is None:
            Statistics.emo = EntityManagerOnline(Statistics.myConf)
        return Statistics.emo

    @staticmethod
    def updateStats():
        arena = getClientArena()
        if arena != None:
            players = []
            for pl in arena.vehicles.values():
                players.append(pl['accountDBID'])
            Statistics.getEmo().updateList(players)        
        else:
            Statistics.emo = None

    @staticmethod   
    def getInfos(uid):
        if BattleUtils.isCw():
            curtime = BigWorld.time()
            if (Statistics.t is None or not Statistics.t.isAlive()) and (Statistics.lastime + Statistics.myConf['delay'] < curtime ):
                Statistics.t = threading.Thread(target=Statistics.updateStats)
                Statistics.t.start()
                Statistics.lastime = curtime
        else:
            Statistics.updateStats()
        wins = ''
        lang = ''
        wr = 0
        battles = 0
        if Statistics.getEmo().existEntity(uid):
            player = Statistics.getEmo().getEntity(uid)
            wins = player.getPersonalRating()
            lang = player.getClientLang()
            wr = player.getWinRate()
            battles = player.getBattlesAmount()
        return (wins,lang,wr,battles)
    
    
    @staticmethod
    def hex_to_rgb(value):
        #value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    @staticmethod
    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb    
    
    
    @staticmethod
    def getColor(PR,type='pr'):
        if not PR:
            return ('','')
        levels = Statistics.myConf['colors_'+type]
        last = levels[0]
        for level in levels:
            if PR < level['min']:
                return (last['color'],last['image'])
            last = level
        return (last['color'],last['image'])
    
    @staticmethod
    def prettyNumber(number,type):
        divisor = Statistics.myConf[type+'_divisor']
        decimals = Statistics.myConf[type+'_decimals']
        if number == "":
            number = 0.0
        else:
            number = float(number)
        divisor = float(divisor)
        value = number / divisor 
        if decimals == 0:
            return int(round(value))
        return round(value,decimals)
    
    @staticmethod
    def updateWithNumbersDict(orig,couples,group):
        numberDict={}
        for name,value in couples.iteritems():
            numberDict[name]= Statistics.prettyNumber(value,group+'_'+name)
        orig.update(numberDict)
        return orig
    
    @staticmethod
    def getFormat(type,pr,wr,bt,lang,player_name='',tank_name='',clan_name='', isAlive= True, isCompatriot = False):
        if clan_name:
            clan_name = "["+clan_name+"]"
        formatz = {'player_name':player_name, 'lang':lang, 'tank_name':tank_name, 'clan_name':clan_name}
        couple = {'pr':pr,'wr':wr,'bt':bt }
        formatz = Statistics.updateWithColorDict(formatz, couple)
        formatz = Statistics.updateWithNumbersDict(formatz, couple,type)
        formatz['flag_url'] = 'img://'+Statistics.myConf['flags_folder']+'/'+lang+'.png'
        if isAlive:
            formatz['ifdeath_color_begin'] = ''
            formatz['ifdeath_color_end'] = ''
        else:
            formatz['ifdeath_color_begin'] = '<font color="'+Statistics.myConf['death_font_color']+'">'
            formatz['ifdeath_color_end'] = '</font>'
            
        if not isCompatriot:
            formatz['ifcompatriot_color_begin'] = ''
            formatz['ifcompatriot_color_end'] = ''
        else:
            formatz['ifcompatriot_color_begin'] = '<font color="'+Statistics.myConf['compatriot_font_color']+'">'
            formatz['ifcompatriot_color_end'] = '</font>'
        return formatz
    
    @staticmethod
    def updateWithColorDict(orig,couples):
        colorDict={}
        for name,value in couples.iteritems():
            color,image = Statistics.getColor(value, name)
            colorDict['rating_url_'+name] = 'img://'+Statistics.myConf['rating_folder']+'/'+image
            colorDict['color_'+name]= color
        orig.update(colorDict)
        return orig
    
    @staticmethod        
    def isMyCompatriot(tid,player):
        curVeh = player.arena.vehicles[player.playerVehicleID]
        id = curVeh['accountDBID']
        if id == tid :
            return False
        if not Statistics.getEmo().existEntity(id) or not Statistics.getEmo().existEntity(tid):
            return False
        return Statistics.getEmo().getEntity(id).getClientLang() == Statistics.getEmo().getEntity(tid).getClientLang()
    
    @staticmethod
    def updatePowerBar():
       if Statistics.okCw() and Statistics.myConf['powerbar_enable']:
            win_chance = Statistics.getWinChance()
            if win_chance:
                color = '#ff0000'
                if win_chance < 49:
                    color = '#ff0000'
                elif win_chance >= 49 and win_chance <= 51:
                    color = '#ffff00'
                elif win_chance > 51:
                    color = '#00ff00'
                color = '\\c' + re.sub('[^A-Za-z0-9]+', '', color) + 'FF;'
                PowerBar.updateWinRate(win_chance*1.0/100,color+str(win_chance)+'%',Statistics.myConf)
    
    
    @staticmethod
    def new__getFormattedStrings(self, vInfoVO, vStatsVO, viStatsVO, ctx, player_name):
        Statistics.updatePowerBar()
        tmp =  old__getFormattedStrings(self, vInfoVO, vStatsVO, viStatsVO, ctx, player_name)
        tmp = list(tmp)
        if not Statistics.okCw() or not Statistics.myConf['panels_enable']:
            return tuple(tmp)
        uid = vInfoVO.player.accountDBID
        isAlive = vInfoVO.isAlive()
        cacheId = str(uid) + str(isAlive)
        if Statistics.cache.has_key('panels') and Statistics.cache['panels'].has_key(cacheId):
            fullPlayerName_built, shortName_built = Statistics.cache['panels'][cacheId]
        else:
            player = BigWorld.player()
            pr, lang, wr, bt = Statistics.getInfos(uid)
            tank_name = vInfoVO.vehicleType.shortName
            clan_name = vInfoVO.player.clanAbbrev
            player_name = vInfoVO.player.name
            isCompatriot = Statistics.isMyCompatriot(uid,player);
            if BattleUtils.isMyTeam(vInfoVO.team):
                fullPlayerName_template = Statistics.myConf['left']
                shortName_template = Statistics.myConf['left_2']
            else:
                fullPlayerName_template = Statistics.myConf['right']
                shortName_template = Statistics.myConf['right_2']
            formatz= Statistics.getFormat('panels',pr, wr, bt, lang, player_name, tank_name, clan_name, isAlive,isCompatriot)
            fullPlayerName_built = fullPlayerName_template.format(**formatz)
            shortName_built = shortName_template.format(**formatz)
            if not Statistics.cache.has_key('panels'):
                Statistics.cache['panels'] = {}
            Statistics.cache['panels'][cacheId] = (fullPlayerName_built, shortName_built)
        
        tmp[0] = fullPlayerName_built
        tmp[2] = shortName_built
        return tuple(tmp)
     
    @staticmethod
    def new__setName(self, dbID, pName = None):
        old__setName(self, dbID, pName)
        if not Statistics.myConf['chat_enable'] or not Statistics.okCw():
            return self
        arenaDP = g_sessionProvider.getArenaDP()
        vID = arenaDP.getVehIDByAccDBID(dbID)
        vInfo = arenaDP.getVehicleInfo(vID)
        isAlive = vInfo.isAlive()
        cacheId = str(uid) + str(isAlive)
        if Statistics.cache.has_key('chat') and Statistics.cache['chat'].has_key(cacheId):
            self._ctx['playerName'] = Statistics.cache['chat'][cacheId]
        else:
            pr, lang, wr, bt = Statistics.getInfos(dbID)
            player_name = self._ctx['playerName']
            tank_name = vInfo.vehicleType.shortName
            clan_name = vInfo.player.clanAbbrev
            isCompatriot = Statistics.isMyCompatriot(dbID,BigWorld.player());
            formatz= Statistics.getFormat('chat',pr, wr, bt, lang, player_name, tank_name, clan_name, isAlive,isCompatriot)
            self._ctx['playerName'] = Statistics.myConf['chat'].format(**formatz)
            if not Statistics.cache.has_key('chat'):
                Statistics.cache['chat'] = {}
            Statistics.cache['chat'][cacheId] = self._ctx['playerName']
        return self
    @staticmethod
    def new__setNameCommon(self, dbID, pName = None):
        old__setNameCommon(self, dbID, pName)
        Statistics.new__setName(self, dbID, pName);
        return self
    
    @staticmethod
    def new_addVehicleMarker(self, vProxy, vInfo, guiProps):
        if not Statistics.myConf['marker_enable'] or BattleUtils.isCw():
            return old_addVehicleMarker(self, vProxy, vInfo, guiProps)
        
        #----------- original code ------------------
        vTypeDescr = vProxy.typeDescriptor
        maxHealth = vTypeDescr.maxHealth
        mProv = vProxy.model.node('HP_gui')
        isAlly = guiProps.isFriend
        speaking = False
        if GUI_SETTINGS.voiceChat:
            speaking = VoiceChatInterface.g_instance.isPlayerSpeaking(vInfo.player.accountDBID)
        hunting = VehicleActions.isHunting(vInfo.events)
        markerID = self._MarkersManager__ownUI.addMarker(mProv, 'VehicleMarkerAlly' if isAlly else 'VehicleMarkerEnemy')
        self._MarkersManager__markers[vInfo.vehicleID] = _VehicleMarker(markerID, vProxy, self._MarkersManager__ownUIProxy)
        battleCtx = g_sessionProvider.getCtx()
        fullName, pName, clanAbbrev, regionCode, vehShortName = battleCtx.getFullPlayerNameWithParts(vProxy.id)
        vType = vInfo.vehicleType
        squadIcon = ''
        if arena_info.getIsMultiteam() and vInfo.isSquadMan():
            teamIdx = g_sessionProvider.getArenaDP().getMultiTeamsIndexes()[vInfo.team]
            squadIconTemplate = '%s%d'
            if guiProps.name() == 'squadman':
                squadTeam = 'my'
            elif isAlly:
                squadTeam = 'ally'
            else:
                squadTeam = 'enemy'
            squadIcon = squadIconTemplate % (squadTeam, teamIdx)
        #----- end -------
        isAlive = vInfo.isAlive()
        curID = vInfo.player.accountDBID
        cacheId = str(curID) + str(isAlive)
        if Statistics.cache.has_key('marker') and Statistics.cache['marker'].has_key(cacheId):
            pName_built = Statistics.cache['marker'][cacheId]
        else:
            pr, lang, wr, bt = Statistics.getInfos(curID)
            player_name = pName
            tank_name = vehShortName
            clan_name = clanAbbrev
            isCompatriot = Statistics.isMyCompatriot(dbID,BigWorld.player());
            formatz= Statistics.getFormat('marker',pr, wr, bt, lang, player_name, tank_name, clan_name, isAlive, isCompatriot)
            pName_built = Statistics.myConf['marker'].format(**formatz)
            if not Statistics.cache.has_key('marker'):
                Statistics.cache['marker'] = {}
            Statistics.cache['marker'][cacheId] = pName_built
        
        #----------- original code ------------------
        self.invokeMarker(markerID, 'init', [vType.classTag,
         vType.iconPath,
         vehShortName,
         vType.level,
         fullName,
         pName_built,
         clanAbbrev,
         regionCode,
         vProxy.health,
         maxHealth,
         guiProps.name(),
         speaking,
         hunting,
         guiProps.base,
         g_ctfManager.isFlagBearer(vInfo.vehicleID),
         squadIcon])
        return markerID
        #----------- end -----------------
    
    @staticmethod
    def new_makeItem(self, vInfoVO, viStatsVO, userGetter, isSpeaking, actionGetter, regionGetter, playerTeam, isEnemy, squadIdx, isFallout = False):
        tmp = old_makeItem(self, vInfoVO, viStatsVO, userGetter, isSpeaking, actionGetter, regionGetter, playerTeam, isEnemy, squadIdx, isFallout)
        if Statistics.myConf['battle_loading_enable'] and Statistics.okCw():
            dbID = vInfoVO.player.accountDBID
            pr, lang, wr, bt = Statistics.getInfos(dbID)
            player_name = tmp['playerName']
            tank_name = tmp['vehicleName']
            region = tmp['region']
            clan_name = tmp['clanAbbrev']
            if region:
                player_name += " "+region
            isAlive = vInfoVO.isAlive()
            player = BigWorld.player();
            isCompatriot = Statistics.isMyCompatriot(dbID,player);
            formatz= Statistics.getFormat('battle_loading',pr, wr, bt, lang, player_name, tank_name, clan_name, isAlive, isCompatriot)
            if BattleUtils.isMyTeam(vInfoVO.team):
                playerName_template = Statistics.myConf['battle_loading_string_left']
            else:
                playerName_template = Statistics.myConf['battle_loading_string_right']
            playerName_built = playerName_template.format(**formatz)
            tmp['playerName'] = playerName_built
            tmp['region'] = ''
            tmp['clanAbbrev'] = ''
        return tmp
    
    @staticmethod
    def new_makeHash(self, index, playerFullName, vInfoVO, vStatsVO, viStatsVO, ctx, playerAccountID, inviteSendingProhibited, invitesReceivingProhibited, isEnemy):
        tmp = old_makeHash(self, index, playerFullName, vInfoVO, vStatsVO, viStatsVO, ctx, playerAccountID, inviteSendingProhibited, invitesReceivingProhibited, isEnemy)
        if not Statistics.myConf['tab_enable'] or not Statistics.okCw():
            return tmp
        dbID = tmp['uid']
        player_name = tmp['userName']
        tank_name = tmp['vehicle']
        region = tmp['region']
        clan_name = tmp['clanAbbrev']
        isAlive = vInfoVO.isAlive()
        cacheId = str(dbID) + str(isAlive)
        if Statistics.cache.has_key('tab') and Statistics.cache['tab'].has_key(cacheId):
            userName_built,vehicle_built = Statistics.cache['tab'][cacheId]
        else:
            player = BigWorld.player()       
            if region:
                player_name +=' '+region
            isCompatriot = Statistics.isMyCompatriot(dbID,player);
            pr, lang, wr, bt = Statistics.getInfos(dbID)
            if BattleUtils.isMyTeam(vInfoVO.team):
                userName_template =Statistics.myConf['tab_left']
                vehicle_template = Statistics.myConf['tab_left_2']
            else:
                userName_template = Statistics.myConf['tab_right'] 
                vehicle_template = Statistics.myConf['tab_right_2']       
            formatz= Statistics.getFormat('battle_loading',pr, wr, bt, lang, player_name, tank_name, clan_name, isAlive,isCompatriot)
            userName_built = userName_template.format(**formatz)
            vehicle_built = vehicle_template.format(**formatz)
            if not Statistics.cache.has_key('tab'):
                Statistics.cache['tab'] = {}
            Statistics.cache['tab'][cacheId] = (userName_built,vehicle_built)
    
        tmp['region'] = ''
        tmp['userName'] = userName_built
        tmp['vehicle'] = vehicle_built
        tmp['clanAbbrev'] = ''
        return tmp
    
    @staticmethod
    def getBalanceWeight(v_info,entityObj):
        v_balance_weight = v_info['vehicleType'].balanceWeight
        v_balance_level = v_info['vehicleType'].level
        p_balance_weight = entityObj.getPersonalRating() / 1000 * v_balance_level
        return v_balance_weight + p_balance_weight

    @staticmethod
    def getWinChance():
        player = BigWorld.player()
        vehicles = player.arena.vehicles
        if player.playerVehicleID not in vehicles:
            return
        curVeh = vehicles[player.playerVehicleID]
        Statistics.getInfos(curVeh['accountDBID'])
        vehicles[player.playerVehicleID]['team']
        ally_balance_weight = 0
        enemy_balance_weight = 0
        for accountDBID,entityObj in Statistics.getEmo().getAll().iteritems():
            vID = g_sessionProvider.getCtx().getVehIDByAccDBID(accountDBID)
            if vID in vehicles:
                v_info = vehicles[vID]
                if v_info['isAlive']:
                    if not BattleUtils.isMyTeam(v_info['team']):
                        enemy_balance_weight += Statistics.getBalanceWeight(v_info,entityObj)
                    else:
                        ally_balance_weight += Statistics.getBalanceWeight(v_info,entityObj)
        if enemy_balance_weight == 0 or enemy_balance_weight == 0:
            return
        f = eval(Statistics.myConf['win_chance_formula'])
        f= int(round(f*100))
        return max(0,min(f,100))
        #return max(0, min(100, int(round(ally_balance_weight / enemy_balance_weight * 50))))        

#     @staticmethod    
#     def new_setArenaInfo(self, arenaDP):
#         if Statistics.myConf['win_chance_enable'] and Statistics.okCw():
#             win_chance = Statistics.getWinChance()
#             if win_chance:
#                 arenaTypeID = getArenaTypeID()
#                 colour = '#ff0000'
#                 if win_chance < 49:
#                     colour = '#ff0000'
#                 elif win_chance >= 49 and win_chance <= 51:
#                     colour = '#ffff00'
#                 elif win_chance > 51:
#                     colour = '#00ff00'
#                 formatz = {'win_chance':win_chance,'color':colour}
#                 text = Statistics.myConf['win_chance_text'].format(**formatz)
#                 arenaDP['winText'] += text
#         old_setArenaInfo(self, arenaDP)
    
 
    @staticmethod
    def new_setTipsInfo(self):
        DEFAULT_BATTLES_COUNT = 100
        
        arena = getClientArena()
        isFallout = arena.guiType == constants.ARENA_GUI_TYPE.EVENT_BATTLES
        arenaDP = self._battleCtx.getArenaDP()
        if hasResourcePoints():
            bgUrl = RES_ICONS.MAPS_ICONS_EVENTINFOPANEL_FALLOUTRESOURCEPOINTSEVENT
        elif hasFlags():
            bgUrl = RES_ICONS.MAPS_ICONS_EVENTINFOPANEL_FALLOUTFLAGSEVENT
        else:
            bgUrl = ''
        if isFallout:
            self.as_setEventInfoPanelDataS({'bgUrl': bgUrl,
             'items': getHelpTextAsDicts(arena.arenaType)})
        if not self._BattleLoading__isTipInited:
            battlesCount = DEFAULT_BATTLES_COUNT
            if g_lobbyContext.getBattlesCount() is not None:
                battlesCount = g_lobbyContext.getBattlesCount()
            vType, vLvl, nation = arenaDP.getVehicleInfo().getTypeInfo()
            tipsIterator = tips.getTipsIterator(arena.guiType, battlesCount, vType, nation, vLvl)
            statusStr, tipStr = ('', '')
            if tipsIterator is not None:
                statusStr, tipStr = next(tipsIterator)
            else:
                LOG_ERROR('No required tips found')
            self.as_setTipTitleS(text_styles.highTitle(statusStr))
            
            #------win chance----
            content = text_styles.playerOnline(tipStr) 
            if Statistics.myConf['win_chance_enable'] and Statistics.okCw():
                win_chance = Statistics.getWinChance()
                if win_chance:
                    arenaTypeID = getArenaTypeID()
                    colour = '#ff0000'
                    if win_chance < 49:
                        colour = '#ff0000'
                    elif win_chance >= 49 and win_chance <= 51:
                        colour = '#ffff00'
                    elif win_chance > 51:
                        colour = '#00ff00'
                    formatz = {'win_chance':win_chance,'color':colour}
                    content += Statistics.myConf['win_chance_text'].format(**formatz)
            self.as_setTipS(content)
            #---------------------
                
            #----- table ----------
            if Statistics.myConf['table_enable'] and Statistics.okCw():
                x, y = GUI.screenResolution()      
                Statistics.table = BattleLoadingBarTable(Statistics.myConf['table_texture'])
                Statistics.table.setWidthMode('PIXEL')
                Statistics.table.setHeightMode('PIXEL')
                Statistics.table.setVerticalPositionMode('PIXEL')
                Statistics.table.setHorizontalPositionMode('PIXEL')
                Statistics.table.setHorizontalAnchor('LEFT')
                Statistics.table.setVerticalAnchor('TOP')
                Statistics.table.setWidth(Statistics.myConf['table_width'])#400
                Statistics.table.setHeight(Statistics.myConf['table_height'])#5
                Statistics.table.setPosition(eval(Statistics.myConf['table_position']))
                Statistics.table.setMaterialFx(Statistics.myConf['table_materialFX'])
                Statistics.table.setColor(eval(Statistics.myConf['table_color']))
                Statistics.table.setVisible(True)
                Statistics.table.add()
                config = {}
                config['texture'] = Statistics.myConf['table_bars_texture']
                config['width'] = Statistics.myConf['table_bars_width']
                config['height'] = Statistics.myConf['table_bars_height']
                config['position'] = eval(Statistics.myConf['table_bars_position'])
                config['delta'] = Statistics.myConf['table_bars_delta']
                config['font'] = Statistics.myConf['table_bars_font']
                config['materialFX'] = Statistics.myConf['table_bars_materialFX']
                config['color'] = (eval(Statistics.myConf['table_bars_color'][0]),eval(Statistics.myConf['table_bars_color'][1]))
                config[VEHICLE_CLASS_NAME.LIGHT_TANK] = Statistics.myConf[VEHICLE_CLASS_NAME.LIGHT_TANK]
                config[VEHICLE_CLASS_NAME.MEDIUM_TANK] = Statistics.myConf[VEHICLE_CLASS_NAME.MEDIUM_TANK]
                config[VEHICLE_CLASS_NAME.HEAVY_TANK] = Statistics.myConf[VEHICLE_CLASS_NAME.HEAVY_TANK]
                config[VEHICLE_CLASS_NAME.SPG] = Statistics.myConf[VEHICLE_CLASS_NAME.SPG]
                config[VEHICLE_CLASS_NAME.AT_SPG] = Statistics.myConf[VEHICLE_CLASS_NAME.AT_SPG]     
                config['table_bars_label'] = Statistics.myConf['table_bars_label']
                config['table_bars_odd_pos'] = Statistics.myConf['table_bars_label_pos']
                config['show_label'] = Statistics.myConf['table_bars_tankType_show']
                config['show_perc'] = Statistics.myConf['table_bars_label_show']
                config['align'] = Statistics.myConf['table_bars_align']
                Statistics.table.addBars(config)
            #---------------------
            
            self._BattleLoading__isTipInited = True
        return
    
    @staticmethod
    def onGUISpaceChanged(spaceID):
        if spaceID == GUI_GLOBAL_SPACE_ID.BATTLE:
            if Statistics.table:
                Statistics.table.delete()
        
        
    @staticmethod
    def getFullName(uid):
        vID = g_sessionProvider.getCtx().getVehIDByAccDBID(uid)
        entryVehicle = BigWorld.player().arena.vehicles[vID]
        return entryVehicle['name']
    
    @staticmethod
    def new__onAddToIgnored(self, _, uid, userName):
        old__onAddToIgnored(self, _, uid, Statistics.getFullName(uid))
    
    @staticmethod
    def new__onAddToFriends(self, _, uid, userName):
        old__onAddToFriends(self, _, uid, Statistics.getFullName(uid))
    
    @staticmethod    
    def stopBattle(event):
        if event.ns == _SPACE.SF_BATTLE:
            PowerBar.battleEnd()
            Statistics.t = None
            Statistics.lastime = 0
            Statistics.emo = None
            Statistics.cache = {}
    
    @classmethod    
    def run(cls):
        super(cls, cls).run()
        cls.addEventHandler(cls.myConf['reloadConfigKey'],cls.reloadConfig)
        saveOldFuncs()
        injectNewFuncs()
        
    @classmethod
    def reloadConfig(cls):
        cls.readConfig()
        cls.cache = {}
        
def saveOldFuncs():
    global old_addVehicleMarker,old__getFormattedStrings,old_makeItem,old_makeHash,old_setArenaInfo,old__setName,old__setNameCommon,old__onAddToIgnored,old__onAddToFriends
    DecorateUtils.ensureGlobalVarNotExist('old_addVehicleMarker')
    DecorateUtils.ensureGlobalVarNotExist('old__setName')
    DecorateUtils.ensureGlobalVarNotExist('old__setNameCommon')
    DecorateUtils.ensureGlobalVarNotExist('old__getFormattedStrings')
    DecorateUtils.ensureGlobalVarNotExist('old_makeItem')
    DecorateUtils.ensureGlobalVarNotExist('old_makeHash')
    DecorateUtils.ensureGlobalVarNotExist('old_setArenaInfo')
    DecorateUtils.ensureGlobalVarNotExist('old__onAddToIgnored')
        
    old_addVehicleMarker = MarkersManager.addVehicleMarker
    old__setName = _BattleMessageBuilder.setName
    old__setNameCommon = CommonMessageBuilder.setName
    old__getFormattedStrings = _StatsForm.getFormattedStrings
    old_makeItem = BattleLoading._makeItem
    old_makeHash = BattleArenaController._makeHash
    old_setArenaInfo = BattleLoading._setArenaInfo
    old__onAddToIgnored = BattleEntry._BattleEntry__onAddToIgnored
    old__onAddToFriends = BattleEntry._BattleEntry__onAddToFriends
        
def injectNewFuncs():
    
    #tab
    BattleArenaController._makeHash = Statistics.new_makeHash
    
    #player panels + powerbar
    _StatsForm.getFormattedStrings = Statistics.new__getFormattedStrings
    
    #marker
    MarkersManager.addVehicleMarker = Statistics.new_addVehicleMarker
    
    #chat
    _BattleMessageBuilder.setName= Statistics.new__setName
    CommonMessageBuilder.setName= Statistics.new__setNameCommon
    
    #winchance
    #BattleLoading._setArenaInfo = Statistics.new_setArenaInfo
    
    #battleloading
    BattleLoading._makeItem = Statistics.new_makeItem
    BattleLoading._setTipsInfo = Statistics.new_setTipsInfo
    g_appLoader.onGUISpaceChanged += Statistics.onGUISpaceChanged
    
    g_eventBus.addListener(events.AppLifeCycleEvent.DESTROYED, Statistics.stopBattle)#, scope=EVENT_BUS_SCOPE.BATTLE)
    
    #fixing panel actions
    BattleEntry._BattleEntry__onAddToIgnored = Statistics.new__onAddToIgnored
    BattleEntry._BattleEntry__onAddToFriends = Statistics.new__onAddToFriends