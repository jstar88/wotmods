from BarTable import BarTable
import BigWorld
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from gui.shared.gui_items.Vehicle import VEHICLE_TYPES_ORDER
from gui.battle_control import g_sessionProvider
from plugins.Engine.ModUtils import BattleUtils
import re
from StarsBar import StarsBar
import GUI

class BattleLoadingBarTable(BarTable):
    def __init__(self,texture=''):
        super(BattleLoadingBarTable,self).__init__(texture)
        
    
    def getColor(self,code):
        return '\\c' + re.sub('[^A-Za-z0-9]+', '', code) + 'FF;'
    
    def addBars(self,config):
        amounts,tiers,currentTier = self.getVehicleTypeAmount()
        for vehicleType,amount in amounts.iteritems():
            if amount['enemy'] == 0:
                perc = 1
            else:
                perc = amount['ally']*1.0 /(amount['ally'] + amount['enemy'])
            config['percentage'] = perc
            if config['show_label']:
                config['label'] = config[vehicleType]
            else:
                config['label'] = ''
            amount['ally_color'] = self.getColor('#00ff00')
            amount['enemy_color'] = self.getColor('#ff0000')
            amount['sep_color'] = self.getColor('#ffffff')
            amount['tank_type'] = config[vehicleType]
            if config['show_perc']:
                config['percentage_text'] = config['table_bars_label'].format(**amount)
            else:
                config['percentage_text'] = ''
            self.addBar(config)
        config['texture'] = ''
        config['percentage_text'] = ''
        config['label'] = ''
        self.addBar(config)
        self.addStars(tiers,currentTier)
    
    def addStars(self,tiers,currentTier):
        from Statistics import Statistics
        if not Statistics.myConf['stars_enable']:
            return
        x, y = GUI.screenResolution()
        n = 5
        maxTierDiff = 2
        startPosition = eval(Statistics.myConf['stars_position'])
        delta = Statistics.myConf['stars_delta']
        size = Statistics.myConf['stars_size']
        activePath = Statistics.myConf['stars_activePath']
        inactivePath = Statistics.myConf['stars_inactivePath']
        st = StarsBar(n,startPosition,delta,size,activePath,inactivePath)
        averageTier = sum(tiers) / float(len(tiers))
        starsAmount = round(currentTier-averageTier) + n - maxTierDiff
        st.add(starsAmount)
        self.bars.append(st)
    
    def getVehicleTypeAmount(self):
        from Statistics import Statistics
        player = BigWorld.player()
        vehicles = player.arena.vehicles
        if player.playerVehicleID not in vehicles:
            return
        curVeh = vehicles[player.playerVehicleID]
        Statistics.getInfos(curVeh['accountDBID'])
        vehicles[player.playerVehicleID]['team']
        amounts = {VEHICLE_CLASS_NAME.HEAVY_TANK:{'ally':0,'enemy':0},
                VEHICLE_CLASS_NAME.MEDIUM_TANK:{'ally':0,'enemy':0},
                VEHICLE_CLASS_NAME.LIGHT_TANK:{'ally':0,'enemy':0},
                VEHICLE_CLASS_NAME.AT_SPG:{'ally':0,'enemy':0},
                VEHICLE_CLASS_NAME.SPG:{'ally':0,'enemy':0}}
        tiers = []
        for accountDBID,entityObj in Statistics.getEmo().getAll().iteritems():
            vID = g_sessionProvider.getCtx().getVehIDByAccDBID(accountDBID)
            if vID in vehicles:
                v_info = vehicles[vID]
                tiers.append(v_info['vehicleType'].level)
                if not BattleUtils.isMyTeam(v_info['team']):
                    tag = 'enemy'
                else:
                    tag = 'ally'
                for vehicleType in VEHICLE_TYPES_ORDER:
                    if vehicleType in v_info['vehicleType'].type.tags:
                        amounts[vehicleType][tag] += 1 
        currentTier = curVeh['vehicleType'].level       
        return (amounts,tiers,currentTier)