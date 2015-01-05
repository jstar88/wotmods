import BigWorld
import weakref

class VehicleMarkers():
    def __init__(self, vehicleID, minimap, period, dIndicator = None):
        self.__vehicleID = vehicleID
        self.__minimapRef = weakref.ref(minimap)
        self.__period = period
        self.__nextTime = BigWorld.time()
        self.__dIndicator = dIndicator

    def update(self):
        if self.__dIndicator is not None:
            vPosition = None
            vehicle = BigWorld.entities.get(self.__vehicleID)
            player = BigWorld.player()
            if vehicle is not None:
                vPosition = vehicle.position
            else:
                vPosition = player.arena.positions[self.__vehicleID]
            vector = vPosition - player.getOwnVehiclePosition()
            self.__dIndicator.update(vector.length, vPosition)
            #minimap marker adding
            #if self.__nextTime <= BigWorld.time():
            #    minimap = self.__minimapRef()
            #    if minimap is not None:
            #        minimap.showActionMarker(self.__vehicleID, 'attack')
            #    self.__nextTime = BigWorld.time() + self.__period

    def clear(self):
        if self.__dIndicator is not None:
            self.__dIndicator.clear()
        self.__dIndicator = None
        self.__vehicleID = -1
        self.__minimapRef = None
        self.__period = -1