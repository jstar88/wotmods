import BigWorld
class MarkersStorage(object):
    __markers = []

    @classmethod
    def addMarker(cls, markerID, marker,maxCount = 3):
        if len(cls.__markers) == maxCount:
            MarkersStorage.removeOldest()
        cls.__markers.append({"time": BigWorld.time(),"marker":marker,"id":markerID})

    @classmethod
    def removeMarker(cls, markerID = None):
        if markerID is None:
            for data in cls.__markers:
                marker = data['marker']
                marker.clear() 
            cls.__markers = []   
        else:
            i = 0
            for data in cls.__markers:
                i += 1
                if data['id'] == markerID:
                    marker = data['marker']
                    marker.clear()
                    del cls.__markers[i]

    @classmethod
    def hasMarker(cls, markerID):
        for data in cls.__markers:
            if data['id'] == markerID:
                return True
        return False

    @classmethod
    def hasMarkers(cls):
        return len(cls.__markers)
    
    
    @classmethod
    def removeOldest(cls):
        data = cls.__markers[0]
        marker = data['marker']
        marker.clear()
        del cls.__markers[0]

    @classmethod
    def updateMarkers(cls,maxTime = 900):
        for data in cls.__markers:
            id = data["id"]
            vehicle = BigWorld.entities.get(id)
            elapsed = BigWorld.time() - data["time"]
            if (vehicle is None and not BigWorld.player().arena.positions.has_key(id)) or not vehicle.isAlive() or not vehicle.isStarted or elapsed > maxTime:
                self.removeMarker(id)
            else:
                marker.update()

    @classmethod
    def clear(self):
        self.removeMarker()