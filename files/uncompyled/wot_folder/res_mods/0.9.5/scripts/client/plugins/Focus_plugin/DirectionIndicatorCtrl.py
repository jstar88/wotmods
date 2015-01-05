import BigWorld

class DirectionIndicatorCtrl():
    def __init__(self, indicator, config, position):
        self.__shapes = config["colors"]
        self.__indicator = indicator
        if self.directionCollid(position):
            self.__indicator.setShape(self.__shapes[0])
        else:
            self.__indicator.setShape(self.__shapes[1])
        self.__indicator.track(position)

    def update(self, distance, position):
        self.__indicator.setDistance(distance)
        if position is not None:
            self.__indicator.setPosition(position)
            if self.directionCollid(position):
                self.__indicator.setShape(self.__shapes[0])
            else:
                self.__indicator.setShape(self.__shapes[1])

    def clear(self):
        if self.__indicator is not None:
            self.__indicator.remove()
        self.__indicator = None
        
    def directionCollid(self, endPos):
        p = BigWorld.player()
        spaceId = p.spaceID
        playerVehicleID = p.playerVehicleID
        startPos = BigWorld.entities.get(playerVehicleID).appearance.modelsDesc['gun']['model'].position
        if BigWorld.wg_collideSegment(spaceId, endPos, startPos, False) != None:
            return True
        return False