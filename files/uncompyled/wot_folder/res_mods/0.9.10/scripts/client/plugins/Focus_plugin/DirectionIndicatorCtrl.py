# 2015.09.05 18:13:50 ora legale Europa occidentale
# Embedded file name: DirectionIndicatorCtrl.py
import BigWorld
from ProjectileMover import collideEntities

class DirectionIndicatorCtrl:

    def __init__(self, indicator, config, enemyVehicle):
        self.__shapes = config['colors']
        self.__indicator = indicator
        self.__indicator.setVName(enemyVehicle.typeDescriptor.type.shortUserString)
        self.curvehicle = enemyVehicle
        if self.directionCollid(enemyVehicle.position):
            self.__indicator.setShape(self.__shapes[0])
        else:
            self.__indicator.setShape(self.__shapes[1])
        self.__indicator.track(enemyVehicle.position)

    def update(self, distance, position):
        self.__indicator.setDistance(distance)
        if position is not None:
            self.__indicator.setPosition(position)
            if self.directionCollid(position):
                self.__indicator.setShape(self.__shapes[0])
            else:
                self.__indicator.setShape(self.__shapes[1])
        return

    def clear(self):
        if self.__indicator is not None:
            self.__indicator.remove()
        self.__indicator = None
        return

    def directionCollid(self, endPos):
        endPos = self.curvehicle.position
        p = BigWorld.player()
        spaceId = p.spaceID
        playerVehicleID = p.playerVehicleID
        startPos = BigWorld.entities.get(playerVehicleID).appearance.modelsDesc['gun']['model'].position
        if collideEntities(startPos, endPos, [self.curvehicle]) is not None:
            return True
        else:
            return False
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Focus_plugin\DirectionIndicatorCtrl.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:50 ora legale Europa occidentale
