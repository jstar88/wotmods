#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original mod by Monstrofil(ru)
# Fully rewrote,improved,fixed and optimized by BirrettaMalefica(eu)
 
import BigWorld
import threading
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
from avatar import PlayerAvatar
from messenger.formatters.chat_message import _BattleMessageBuilder,CommonMessageBuilder
from gui.battle_control import g_sessionProvider
from items.vehicles import VEHICLE_CLASS_TAGS
from gui import GUI_SETTINGS    
from gui.Scaleform import VoiceChatInterface
from gui.battle_control.arena_info.arena_vos import VehicleActions
from gui.Scaleform.daapi.view.battle.markers import _VehicleMarker, MarkersManager
from gui.Scaleform.daapi.view.BattleLoading import BattleLoading
from gui.battle_control.battle_arena_ctrl import BattleArenaController
from gui.shared.utils.functions import getBattleSubTypeWinText
from gui.battle_control.arena_info import getClientArena, getArenaTypeID
from gui.WindowsManager import g_windowsManager
from EntityManagerOnline import EntityManagerOnline
from plugins.Engine.ModUtils import BattleUtils,MinimapUtils,FileUtils,HotKeysUtils,DecorateUtils
from gui.Scaleform.Battle import Battle

class Statistics(object):
    
    emo = None
    t = None
    lastime = 0 
    config = {
              'pluginEnable': False,
              
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
              
              'panels_enable' : True,
              'left' : "<font color='#{color_pr}'>{lang}</font>  {player_name}<br/>",
              'right' : "<font color='#{color_pr}'>{lang}</font>  {player_name}<br/>",
              'left_c' : "<font size='17' color='#{color_pr}'>«</font><font color='#{color_pr}'>{lang}</font><font size='17' color='#{color_pr}'>»</font>  {player_name}<br/>",
              'right_c' : "<font size='17' color='#{color_pr}'>«</font><font color='#{color_pr}'>{lang}</font><font size='17' color='#{color_pr}'>»</font>  {player_name}<br/>",
              
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
              'tab_left_c': '«{lang}»|{wr}%|{pr}  ',
              'tab_right_c': '  «{lang}»|{wr}%|{pr}',
              
              'win_chance_enable': True,
              'win_chance_text': "( Chance for win: <font color='{color}'>{win_chance}%</font> )",
              
              'colors_pr':[{'min':0,'color':'FE0E00'},
                        {'min':2020,'color':'FE7903'},
                        {'min':4185,'color':'F8F400'},
                        {'min':6340,'color':'60FF00'},
                        {'min':8525,'color':'02C9B3'},
                        {'min':9930,'color':'D042F3'},
                        {'min':11000,'color':'490A59'}],
              
              'colors_wr':[{'min':0,'color':'FE0E00'},
                        {'min':40,'color':'FE7903'},
                        {'min':48,'color':'F8F400'},
                        {'min':53,'color':'60FF00'},
                        {'min':55,'color':'02C9B3'},
                        {'min':58,'color':'D042F3'},
                        {'min':61,'color':'490A59'}],
              
              'colors_bt':[{'min':0,'color':'FE0E00'},
                        {'min':2000,'color':'FE7903'},
                        {'min':8000,'color':'F8F400'},
                        {'min':15000,'color':'60FF00'},
                        {'min':22000,'color':'02C9B3'},
                        {'min':26000,'color':'D042F3'},
                        {'min':32000,'color':'490A59'}],
              
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
    
    def __init__(self):
        self.pluginEnable = False
        
    def readConfig(self):
        Statistics.config = FileUtils.readConfig('scripts/client/plugins/Statistics_plugin/config.xml',Statistics.config,'Statistics')
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
    def hex_to_rgb(value):
        #value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    @staticmethod
    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb
    
    @staticmethod
    def hsl_to_rgb(c):
       import colorsys
       return colorsys.hls_to_rgb(c[0],c[1],c[2])

    @staticmethod
    def rgb_to_hsl(c):
        import colorsys
        return colorsys.rgb_to_hls(c[0],c[1],c[2])
    
    
    
    @staticmethod
    def changeLightness(hes,lum):
        LOG_NOTE(hes)
        rgb = Statistics.hex_to_rgb(hes)
        LOG_NOTE(rgb)
        hsl = Statistics.rgb_to_hsl(rgb)
        LOG_NOTE(hsl)
        hsl = (hsl[0],hsl[1],hsl[2]*lum)
        LOG_NOTE(hsl)
        rgb = Statistics.hsl_to_rgb(hsl)
        LOG_NOTE(rgb)
        hes = Statistics.rgb_to_hex(rgb)
        LOG_NOTE(hes)
        return hes
        
    
    
    
    @staticmethod
    def getColor(PR,type='pr'):
        if not PR:
            return ''
        levels = Statistics.config['colors_'+type]
        last = levels[0]['color']
        for level in levels:
            if PR < level['min']:
                return last
            last = level['color']
        return last
    
    @staticmethod
    def prettyNumber(number,type):
        divisor = Statistics.config[type+'_divisor']
        decimals = Statistics.config[type+'_decimals']
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
    def getFormat(type,pr,wr,bt,lang,player_name='',tank_name='',isAlive=True):
       formatz = {'player_name':player_name, 'lang':lang, 'tank_name':tank_name}
       couple = {'pr':pr,'wr':wr,'bt':bt}
       formatz = Statistics.updateWithColorDict(formatz, couple, isAlive)
       formatz = Statistics.updateWithNumbersDict(formatz, couple,type) 
       return formatz
    
    @staticmethod
    def updateWithColorDict(orig,couples, isAlive=True):
        colorDict={}
        for name,value in couples.iteritems():
            color = Statistics.getColor(value, name)
            #if not isAlive:
            #    color = Statistics.changeLightness(color, 0.8)
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
    
    #("<font color='#ffffff'>some</font><br/>", "<font color='#ffffff'> </font><br/>", "<font color='#ffffff'>M41 Bulldog</font><br/>")
    @staticmethod
    def new__getFormattedStrings(self, vInfoVO, vStatsVO, ctx, fullPlayerName):
        if not Statistics.okCw() or not Statistics.config['panels_enable']:
            return old__getFormattedStrings(self, vInfoVO, vStatsVO, ctx, fullPlayerName)
        player = BigWorld.player()
        uid = vInfoVO.player.accountDBID
        pr,lang,wr,bt = Statistics.getInfos(uid)
        player_name = fullPlayerName
        tank_name = vInfoVO.vehicleType.shortName
        fullPlayerName, fragsString, shortName =  old__getFormattedStrings(self, vInfoVO, vStatsVO, ctx, fullPlayerName)
        if BattleUtils.isMyTeam(vInfoVO.team):
            if Statistics.isMyCompatriot(uid,player):
                fullPlayerName = str(Statistics.config['left_c'])
            else:
                fullPlayerName = str(Statistics.config['left'])
        else:
            if Statistics.isMyCompatriot(uid,player):
                fullPlayerName = str(Statistics.config['right_c'])
            else:
                fullPlayerName = str(Statistics.config['right'])
        
        
        formatz= Statistics.getFormat('panels',pr, wr, bt, lang, player_name, tank_name,vInfoVO.isAlive())
        fullPlayerName = fullPlayerName.format(**formatz)
        return (fullPlayerName, fragsString, shortName)
     
    @staticmethod
    def new__setName(self, dbID, pName = None):
        old__setName(self, dbID, pName)
        if Statistics.config['chat_enable'] and Statistics.okCw():
            pr,lang,wr,bt = Statistics.getInfos(dbID)
            formatz= Statistics.getFormat('chat',pr, wr, bt, lang,self._ctx['playerName'])
            self._ctx['playerName'] = Statistics.config['chat'].format(**formatz)
        return self
    @staticmethod
    def new__setNameCommon(self, dbID, pName = None):
        old__setNameCommon(self, dbID, pName)
        if Statistics.config['chat_enable'] and Statistics.okCw():
            pr,lang,wr,bt = Statistics.getInfos(dbID)
            formatz= Statistics.getFormat('chat',pr, wr, bt, lang,self._ctx['playerName'])
            self._ctx['playerName'] = Statistics.config['chat'].format(**formatz)
        return self
    
    @staticmethod
    def new__createMarker(self, vProxy):
        if not Statistics.config['marker_enable'] or BattleUtils.isCw():
            return old_createMarker(self, vProxy)
        
        player = BigWorld.player()
        
        #----------- original code ------------------
        vInfo = dict(vProxy.publicInfo)
        battleCtx = g_sessionProvider.getCtx()
        if battleCtx.isObserver(vProxy.id):
            return -1
        isFriend = vInfo['team'] == player.team
        vehID = vProxy.id
        vInfoEx = g_sessionProvider.getArenaDP().getVehicleInfo(vehID)
        vTypeDescr = vProxy.typeDescriptor
        maxHealth = vTypeDescr.maxHealth
        mProv = vProxy.model.node('HP_gui')
        tags = set(vTypeDescr.type.tags & VEHICLE_CLASS_TAGS)
        vClass = tags.pop() if len(tags) > 0 else ''
        entityName = battleCtx.getPlayerEntityName(vehID, vInfoEx.team)
        entityType = 'ally' if player.team == vInfoEx.team else 'enemy'
        speaking = False
        if GUI_SETTINGS.voiceChat:
            speaking = VoiceChatInterface.g_instance.isPlayerSpeaking(vInfoEx.player.accountDBID)
        hunting = VehicleActions.isHunting(vInfoEx.events)
        handle = self._MarkersManager__ownUI.addMarker(mProv, 'VehicleMarkerAlly' if isFriend else 'VehicleMarkerEnemy')
        self._MarkersManager__markers[handle] = _VehicleMarker(vProxy, self._MarkersManager__ownUIProxy(), handle)
        fullName, pName, clanAbbrev, regionCode, vehShortName = battleCtx.getFullPlayerNameWithParts(vProxy.id)
        #----- end -------
        
        PR = ''
        curVeh = player.arena.vehicles[vProxy.id]
        if curVeh is not None:
            curID = curVeh['accountDBID']
            pr,lang,wr,bt = Statistics.getInfos(curID)
            formatz= Statistics.getFormat('marker',pr, wr, bt, lang,pName,vehShortName)
            PR = Statistics.config['marker'].format(**formatz)
            pName = PR
        
        #----------- original code ------------------
        self.invokeMarker(handle, 'init', [vClass,
         vInfoEx.vehicleType.iconPath,
         vehShortName,
         vInfoEx.vehicleType.level,
         fullName,
         pName,
         clanAbbrev,
         regionCode,
         vProxy.health,
         maxHealth,
         entityName.name(),
         speaking,
         hunting,
         entityType,
         self.isVehicleFlagbearer(vehID)])
        return handle
        #----------- end -----------------
    
    @staticmethod
    def new_makeItem(self, vInfoVO, userGetter, isSpeaking, actionGetter, regionGetter, playerTeam, isEnemy):
        old_return = old_makeItem(self, vInfoVO, userGetter, isSpeaking, actionGetter, regionGetter, playerTeam,isEnemy)
        if Statistics.config['battle_loading_enable'] and Statistics.okCw():
            pr,lang,wr,bt = Statistics.getInfos(vInfoVO.player.accountDBID)
            userName = old_return['playerName']
            region = old_return['region']
            clan = old_return['clanAbbrev']
            if clan:
                userName += '['+clan+']'
            if region:
                userName += region
            formatz= Statistics.getFormat('battle_loading',pr, wr, bt, lang, userName)
            if BattleUtils.isMyTeam(vInfoVO.team):
                old_return['playerName'] = Statistics.config['battle_loading_string_left'].format(**formatz)
            else:
                old_return['playerName'] = Statistics.config['battle_loading_string_right'].format(**formatz)
        old_return['region'] = ''
        old_return['clanAbbrev'] = ''
        return old_return
    
    @staticmethod
    def new_makeHash(self, index, playerFullName, vInfoVO, vStatsVO, viStatsVO, ctx, userGetter, isSpeaking, isMenuEnabled, regionGetter, playerAccountID, inviteSendingProhibited, invitesReceivingProhibited):
        tmp = old_makeHash(self, index, playerFullName, vInfoVO, vStatsVO, viStatsVO, ctx, userGetter, isSpeaking, isMenuEnabled, regionGetter, playerAccountID, inviteSendingProhibited, invitesReceivingProhibited)
        if not Statistics.config['tab_enable'] or not Statistics.okCw():
            return tmp

        dbID = vInfoVO.player.accountDBID
        userName = vInfoVO.player.getPlayerLabel()
        region = regionGetter(dbID)
        player = BigWorld.player()
        if region is None:
            region = ''
        if tmp['clanAbbrev']:
            userName +='['+tmp['clanAbbrev']+']'+region
        pr,lang,wr,bt = Statistics.getInfos(dbID)
        if BattleUtils.isMyTeam(vInfoVO.team):
            if Statistics.isMyCompatriot(dbID,player):
                f = Statistics.config['tab_left_c']
            else:
                f =Statistics.config['tab_left']
        else:
            if Statistics.isMyCompatriot(dbID,player):
                f = Statistics.config['tab_right_c']
            else:
                f = Statistics.config['tab_right']
        
        formatz= Statistics.getFormat('tab',pr, wr, bt, lang, userName)
        userName = f.format(**formatz)
    
        tmp['region'] = ''
        tmp['userName'] = userName
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
    global old__onBecomePlayer,old_createMarker,old__getFormattedStrings,old_makeItem,old_makeHash,old_addArenaExtraData,old__setName,old__setNameCommon
    DecorateUtils.ensureGlobalVarNotExist('old__onBecomePlayer')
    DecorateUtils.ensureGlobalVarNotExist('old_createMarker')
    DecorateUtils.ensureGlobalVarNotExist('old__setName')
    DecorateUtils.ensureGlobalVarNotExist('old__setNameCommon')
    DecorateUtils.ensureGlobalVarNotExist('old__getFormattedStrings')
    DecorateUtils.ensureGlobalVarNotExist('old_makeItem')
    DecorateUtils.ensureGlobalVarNotExist('old_makeHash')
    DecorateUtils.ensureGlobalVarNotExist('old_addArenaExtraData')
        
    old__onBecomePlayer = PlayerAvatar.onBecomePlayer
    old_createMarker = MarkersManager.createMarker
    old__setName = _BattleMessageBuilder.setName
    old__setNameCommon = CommonMessageBuilder.setName
    old__getFormattedStrings = Battle.getFormattedStrings
    old_makeItem = BattleLoading._BattleLoading__makeItem
    old_makeHash = BattleArenaController._BattleArenaController__makeHash
    old_addArenaExtraData = BattleLoading._BattleLoading__addArenaExtraData
        
def injectNewFuncs():
    
    #tab
    BattleArenaController._BattleArenaController__makeHash = Statistics.new_makeHash
    
    #player panels
    Battle.getFormattedStrings = Statistics.new__getFormattedStrings
    
    #marker
    MarkersManager.createMarker = Statistics.new__createMarker
    
    #chat
    _BattleMessageBuilder.setName= Statistics.new__setName
    CommonMessageBuilder.setName= Statistics.new__setNameCommon
    
    #winchance
    BattleLoading._BattleLoading__addArenaExtraData = Statistics.new_addArenaExtraData
    
    #battleloading
    BattleLoading._BattleLoading__makeItem = Statistics.new_makeItem
    
    g_windowsManager.onDestroyBattleGUI += Statistics.stopBattle