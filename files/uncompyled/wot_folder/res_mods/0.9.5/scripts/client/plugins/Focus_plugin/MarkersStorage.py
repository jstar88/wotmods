class MarkersStorage(object):
    __markers = {}

    @classmethod
    def addMarker(cls, markerID, marker):
        cls.__markers[markerID] = marker

    @classmethod
    def removeMarker(cls, markerID = None):
        if markerID is None:
            while len(cls.__markers):
                _, marker = cls.__markers.popitem()
                marker.clear()
        else:
            marker = cls.__markers.pop(markerID, None)
            if marker is not None:
                marker.clear()

    @classmethod
    def hasMarker(cls, markerID):
        return markerID in cls.__markers

    @classmethod
    def hasMarkers(cls):
        return len(cls.__markers)

    @classmethod
    def updateMarkers(cls):
        for id,marker in cls.__markers.iteritems():
            vehicle = BigWorld.entities.get(id)
            if vehicle is None or not vehicle.isAlive():
                self.removeMarker(id)
            else:
                marker.update()

    @classmethod
    def clear(self):
        self.removeMarker()