#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original mod by Monstrofil(ru)
# Fully rewrote,improved,fixed and optimized by BirrettaMalefica(eu)
 
import BigWorld
import threading
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from avatar import PlayerAvatar
from gui.Scaleform.daapi.view.battle.PlayersPanel import PlayersPanel
from gui.battle_control.BattleContext import BattleContext
from gui.battle_control.arena_info import getClientArena
from gui.battle_control import g_sessionProvider
from items.vehicles import VEHICLE_CLASS_TAGS
from gui import GUI_SETTINGS    
from gui.Scaleform import VoiceChatInterface
from gui.battle_control.arena_info.arena_vos import VehicleActions
from gui.Scaleform.Battle import _VehicleMarker, VehicleMarkersManager
from gui.Scaleform.daapi.view.BattleLoading import BattleLoading
from gui.battle_control.battle_arena_ctrl import BattleArenaController
from account_helpers.settings_core.SettingsCore import g_settingsCore
from gui.shared.utils.functions import getBattleSubTypeWinText
from gui.battle_control.arena_info import getClientArena, getArenaTypeID
from gui.WindowsManager import g_windowsManager
from EntityManagerOnline import EntityManagerOnline
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils

class Statistics(object):
    
    emo = None
    t = None
    lastime = 0 
    config = {
              'pluginEnable': True,
              
              'delay' : 1,
              'maxentries' : 3,
              'cw' : False,
              'region' : 'eu',
              'pr_index': 'global_rating',
              'lang_index': 'client_language',
              'wr_index': 'Statisticss.all.wins',
              'battles_index': 'Statisticss.all.battles',
              'application_id': 'demo',
              'url': 'http://api.worldoftanks.{region}/wot/account/info/?application_id={application_id}&fields={pr_index},{lang_index},{wr_index},{battles_index}&account_id={id}',
              
              'panels_enable' : True,
              'left' : "<font color='#{color}'>{lang}</font>  {player_name}<br/>",
              'right' : "<font color='#{color}'>{lang}</font>  {player_name}<br/>",
              'left_c' : "<font size='17' color='#{color}'>«</font><font color='#{color}'>{lang}</font><font size='17' color='#{color}'>»</font>  {player_name}<br/>",
              'right_c' : "<font size='17' color='#{color}'>«</font><font color='#{color}'>{lang}</font><font size='17' color='#{color}'>»</font>  {player_name}<br/>",
              
              'marker_enable' : True,
              'marker' : ' {rating}',
              
              'chat_enable' : True,
              
              'battle_loading_enable' : True,
              'battle_loading_string_left' : '  {lang}|{win_rate}%|{rating}',
              'battle_loading_string_right' : '{lang}|{win_rate}%|{rating}  ',
              
              'tab_enable': True,
              'tab_left': '{lang}|{win_rate}%|{rating}  ',
              'tab_right': '  {lang}|{win_rate}%|{rating}',
              'tab_left_c': '«{lang}»|{win_rate}%|{rating}  ',
              'tab_right_c': '  «{lang}»|{win_rate}%|{rating}',
              
              'win_chance_enable': True,
              'win_chance_text': "( Chance for win: <font color='{color}'>{win_chance}%</font> )",
              
              'colors':[{'min':0,'color':'FE0E00'},
                        {'min':2020,'color':'FE7903'},
                        {'min':4185,'color':'F8F400'},
                        {'min':6340,'color':'60FF00'},
                        {'min':8525,'color':'02C9B3'},
                        {'min':9930,'color':'D042F3'},
                        {'min':11000,'color':'490A59'}]
              
              }
    
    def __init__(self):
        self.pluginEnable = False
        
    def readConfig(self):
        Statistics.config = FileUtils.readXml('scripts/client/plugins/Statistics_plugin/config.xml',Statistics.config,'Statistics')
        self.pluginEnable = Statistics.config['pluginEnable']
        
    @staticmethod
    def okCw():
        return not BattleUtils.isCw() or Statistics.config['cw']
    
    @staticmethod
    def getEmo():
        if Statistics.emo is None:
            Statistics.emo = EntityManagerOnline(Statistics.config)
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
            if (Statistics.t is None or not Statistics.t.isAlive()) and (Statistics.lastime + Statistics.config['delay'] < curtime ):
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
    def getColor(PR):
        if not PR:
            return ''
        last = None
        levels = Statistics.config['colors']
        for level in levels:
            if last is None:
                last = level['color']
            if PR < level['min']:
                return last
            last = level['color']
    
    @staticmethod        
    def isMyCompatriot(tid):
        curVeh = BigWorld.player().arena.vehicles[BigWorld.player().playerVehicleID]
        id = curVeh['accountDBID']
        if id == tid :
            return False
        if not Statistics.getEmo().existEntity(id) or not Statistics.getEmo().existEntity(tid):
            return False
        return Statistics.getEmo().getEntity(id).getClientLang() == Statistics.getEmo().getEntity(tid).getClientLang()
    
    @staticmethod
    def new__getFormattedStrings(self, vInfoVO, vStatsVO, ctx, fullPlayerName):
        if not Statistics.okCw() or not Statistics.config['panels_enable']:
            return old__getFormattedStrings(self, vInfoVO, vStatsVO, ctx, fullPlayerName)
        uid = vInfoVO.player.accountDBID
        wins,lang,wr,bt = Statistics.getInfos(uid)
        player_name = fullPlayerName
        tank_name = vInfoVO.vehicleType.shortName
        fullPlayerName, fragsString, shortName =  old__getFormattedStrings(self, vInfoVO, vStatsVO, ctx, fullPlayerName)
        color = Statistics.getColor(wins)
        if BattleUtils.isMyTeam(vInfoVO.team):
            if Statistics.isMyCompatriot(uid):
                fullPlayerName = str(Statistics.config['left_c'])
            else:
                fullPlayerName = str(Statistics.config['left'])
        else:
            if Statistics.isMyCompatriot(uid):
                fullPlayerName = str(Statistics.config['right_c'])
            else:
                fullPlayerName = str(Statistics.config['right'])
        bt = round(bt /1000)
        wr = round(wr,1)
        formatz = {'color':color, 'rating':wins, 'player_name':player_name, 'lang':lang, 'tank_name':tank_name, 'win_rate':wr, 'battle_amount':bt}
        fullPlayerName = fullPlayerName.format(**formatz)
        return (fullPlayerName, fragsString, shortName)
     
    @staticmethod
    def new__getFullPlayerNameWithParts(self, vID = None, accID = None, pName = None, showVehShortName = True, showClan = True, showRegion = True):
        fullName, pName, clanAbbrev, regionCode, vehShortName = old__getFullPlayerNameWithParts(self, vID, accID, pName, showVehShortName, showClan, showRegion)
        if accID is not None and Statistics.config['chat_enable'] and Statistics.okCw():
            wins,lang,wr,bt = Statistics.getInfos(accID)
            if wins:
                fullName = str(wins) + ' ' + fullName
                pName = str(wins) + ' ' + pName
        return (fullName,
            pName,
            clanAbbrev,
            regionCode,
            vehShortName)    
    
    @staticmethod
    def new__createMarker(self, vProxy):
        if not Statistics.config['marker_enable'] or BattleUtils.isCw():
            return old_createMarker(self, vProxy)
        vInfo = dict(vProxy.publicInfo)
        if g_sessionProvider.getCtx().isObserver(vProxy.id):
            return -1
        isFriend = BattleUtils.isMyTeam(vInfo['team'])
        vInfoEx = g_sessionProvider.getArenaDP().getVehicleInfo(vProxy.id)
        vTypeDescr = vProxy.typeDescriptor
        maxHealth = vTypeDescr.maxHealth
        mProv = vProxy.model.node('HP_gui')
        tags = set(vTypeDescr.type.tags & VEHICLE_CLASS_TAGS)
        vClass = tags.pop() if len(tags) > 0 else ''
        entityName = g_sessionProvider.getCtx().getPlayerEntityName(vProxy.id, vInfoEx.team)
        entityType = 'ally' if BigWorld.player().team == vInfoEx.team else 'enemy'
        speaking = False
        if GUI_SETTINGS.voiceChat:
            speaking = VoiceChatInterface.g_instance.isPlayerSpeaking(vInfoEx.player.accountDBID)
        hunting = VehicleActions.isHunting(vInfoEx.events)
        handle = self._VehicleMarkersManager__ownUI.addMarker(mProv, 'VehicleMarkerAlly' if isFriend else 'VehicleMarkerEnemy')
        self._VehicleMarkersManager__markers[handle] = _VehicleMarker(vProxy, self._VehicleMarkersManager__ownUIProxy, handle)
        fullName, pName, clanAbbrev, regionCode, vehShortName = g_sessionProvider.getCtx().getFullPlayerNameWithParts(vProxy.id)
        #new code
        PR = ''
        curVeh = BigWorld.player().arena.vehicles[vProxy.id]
        if curVeh is not None:
            curID = curVeh['accountDBID']
            wins,lang,wr,bt = Statistics.getInfos(curID)
            bt = round(bt /1000)
            wr = round(wr,1)
            formatz = {'rating':wins,'lang':lang,'battle_amount':bt,'win_rate':wr,'color':Statistics.getColor(wins)}
            PR = Statistics.config['marker'].format(**formatz)
        self.invokeMarker(handle, 'init', [vClass,
            vInfoEx.vehicleType.iconPath,
            vehShortName,
            vInfoEx.vehicleType.level,
            fullName,
            pName + PR,
            clanAbbrev,
            regionCode,
            vProxy.health,
            maxHealth,
            entityName.name(),
            speaking,
            hunting,
            entityType])
        self._VehicleMarkersManager__parentUI.call('minimap.entryInited', [])
        return handle
    
    @staticmethod
    def new_makeItem(self, vInfoVO, userGetter, isSpeaking, actionGetter, regionGetter, playerTeam):
        old_return = old_makeItem(self, vInfoVO, userGetter, isSpeaking, actionGetter, regionGetter, playerTeam)
        if Statistics.config['battle_loading_enable'] and Statistics.okCw():
            wins,lang,wr,bt = Statistics.getInfos(vInfoVO.player.accountDBID)
            bt = round(bt /1000)
            wr = round(wr,1)
            formatz = {'rating':wins,'lang':lang,'battle_amount':bt,'win_rate':wr,'color':Statistics.getColor(wins)}
            if BattleUtils.isMyTeam(vInfoVO.team):
                s = Statistics.config['battle_loading_string_left'].format(**formatz)
                old_return['playerName'] = s + old_return['playerName']
            else:
                s = Statistics.config['battle_loading_string_right'].format(**formatz)
                old_return['region'] = s
        return old_return
    
    @staticmethod
    def new_makeHash(self, index, playerFullName, vInfoVO, vStatsVO, ctx, userGetter, isSpeaking, isMenuEnabled, regionGetter):
        if not Statistics.config['tab_enable'] or not Statistics.okCw():
            return old_makeHash(self, index, playerFullName, vInfoVO, vStatsVO, ctx, userGetter, isSpeaking, isMenuEnabled, regionGetter)
        vehicleID = vInfoVO.vehicleID
        vTypeVO = vInfoVO.vehicleType
        playerVO = vInfoVO.player
        dbID = playerVO.accountDBID
        user = userGetter(dbID)
        if user:
            roster = user.getRoster()
            isMuted = user.isMuted()
        else:
            roster = 0
            isMuted = False
        
        userName = playerVO.getPlayerLabel()
        region = regionGetter(dbID)
        if region is None:
            region = ''
        wins,lang,wr,bt = Statistics.getInfos(dbID)
        color = Statistics.getColor(wins)
        if BattleUtils.isMyTeam(vInfoVO.team):
            if Statistics.isMyCompatriot(dbID):
                userName = str(Statistics.config['tab_left_c']) + userName
            else:
                userName = str(Statistics.config['tab_left']) + userName
        else:
            if Statistics.isMyCompatriot(dbID):
                region += str(Statistics.config['tab_right_c'])
            else:
                region += str(Statistics.config['tab_right'])
        bt = round(bt /1000)
        wr = round(wr,1)
        formatz = {'color':color, 'rating':wins, 'lang':lang, 'win_rate':wr, 'battle_amount':bt}
        userName = userName.format(**formatz)
        region = region.format(**formatz)
    
        return {
            'position': index + 1,
            'label': playerFullName,
            'userName': userName,
            'icon': vTypeVO.iconPath,
            'vehicle': vTypeVO.shortName,
            'vehicleState': vInfoVO.vehicleStatus,
            'frags': vStatsVO.frags,
            'squad': ctx.getSquadIndex(vInfoVO),
            'clanAbbrev': playerVO.clanAbbrev,
            'speaking': isSpeaking(dbID),
            'uid': dbID,
            'himself': ctx.isPlayerSelected(vInfoVO),
            'roster': roster,
            'muted': isMuted,
            'vipKilled': 0,
            'VIP': False,
            'teamKiller': ctx.isTeamKiller(vInfoVO),
            'denunciations': ctx.denunciationsLeft,
            'isPostmortemView': ctx.isPostmortemView(vInfoVO),
            'level': vTypeVO.level if g_settingsCore.getSetting('ppShowLevels') else 0,
            'vehAction': ctx.getAction(vInfoVO),
            'team': vInfoVO.team,
            'vehId': vehicleID,
            'isIGR': playerVO.isIGR(),
            'igrType': playerVO.igrType,
            'igrLabel': playerVO.getIGRLabel(),
            'isEnabledInRoaming': isMenuEnabled(dbID),
            'region': region}
    
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
        vehicles[BigWorld.player().playerVehicleID]['team']
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
        if ally_balance_weight == 0 or enemy_balance_weight == 0:
            return
        return max(0, min(100, int(round(ally_balance_weight / enemy_balance_weight * 50))))        

    @staticmethod    
    def new_addArenaExtraData(self, arenaDP):
        old_addArenaExtraData(self, arenaDP)
        if not Statistics.config['win_chance_enable'] or not Statistics.okCw():
            return
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
            text = Statistics.config['win_chance_text'].format(**formatz)
            self.as_setWinTextS(getBattleSubTypeWinText(arenaTypeID, 2) + text)
    
    @staticmethod    
    def stopBattle():
        Statistics.t = None
        Statistics.lastime = 0
        Statistics.emo = None
        
    def run(self):
        saveOldFuncs()
        injectNewFuncs()
        
def saveOldFuncs():
    global old__onBecomePlayer,old_createMarker,old__getFullPlayerNameWithParts,old__getFormattedStrings,old_makeItem,old_makeHash,old_addArenaExtraData
    DecorateUtils.ensureGlobalVarNotExist('old__onBecomePlayer')
    DecorateUtils.ensureGlobalVarNotExist('old_createMarker')
    DecorateUtils.ensureGlobalVarNotExist('old__getFullPlayerNameWithParts')
    DecorateUtils.ensureGlobalVarNotExist('old__getFormattedStrings')
    DecorateUtils.ensureGlobalVarNotExist('old_makeItem')
    DecorateUtils.ensureGlobalVarNotExist('old_makeHash')
    DecorateUtils.ensureGlobalVarNotExist('old_addArenaExtraData')
        
    old__onBecomePlayer = PlayerAvatar.onBecomePlayer
    old_createMarker = VehicleMarkersManager.createMarker
    old__getFullPlayerNameWithParts = BattleContext.getFullPlayerNameWithParts
    old__getFormattedStrings = PlayersPanel.getFormattedStrings
    old_makeItem = BattleLoading._BattleLoading__makeItem
    old_makeHash = BattleArenaController._BattleArenaController__makeHash
    old_addArenaExtraData = BattleLoading._BattleLoading__addArenaExtraData
        
def injectNewFuncs():
    BattleLoading._BattleLoading__addArenaExtraData = Statistics.new_addArenaExtraData
    BattleArenaController._BattleArenaController__makeHash = Statistics.new_makeHash
    PlayersPanel.getFormattedStrings = Statistics.new__getFormattedStrings
    VehicleMarkersManager.createMarker = Statistics.new__createMarker
    BattleContext.getFullPlayerNameWithParts = Statistics.new__getFullPlayerNameWithParts
    BattleLoading._BattleLoading__makeItem = Statistics.new_makeItem
    g_windowsManager.onDestroyBattleGUI += Statistics.stopBattle