from MarkersStorage import MarkersStorage
from DirectionIndicator import DirectionIndicator
from DirectionIndicatorCtrl import DirectionIndicatorCtrl
from VehicleMarkers import VehicleMarkers
from gui.app_loader import g_appLoader
import BigWorld
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE

def showMarker(enemyID,config):
    if enemyID is None or MarkersStorage.hasMarker(enemyID):
        return
    battle = g_appLoader.getDefBattleApp()
    if battle is None:
        return
    minimap = battle.minimap
    enemyVehicle = BigWorld.entities.get(enemyID)
    if enemyVehicle is None:
        return
    if not enemyVehicle.isAlive():
        return
    indicator = DirectionIndicator(config)
    if indicator is None:
        return
    indicatorCtrl = DirectionIndicatorCtrl(indicator, config, enemyVehicle)
    VehicleMarker = VehicleMarkers(enemyID, minimap, 5, indicatorCtrl)
    if VehicleMarker is not None:
        MarkersStorage.addMarker(enemyID, VehicleMarker, config)