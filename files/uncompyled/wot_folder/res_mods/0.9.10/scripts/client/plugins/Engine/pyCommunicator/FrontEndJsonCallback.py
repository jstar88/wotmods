# 2015.09.05 18:13:49 ora legale Europa occidentale
# Embedded file name: FrontEndJsonCallback.py
from FrontEnd import FrontEnd
import json

class FrontEndJsonCallback(FrontEnd):

    class Queue:

        def __init__(self):
            self.items = []

        def enqueue(self, item):
            self.items.insert(0, item)

        def dequeue(self):
            return self.items.pop()

        def top(self):
            return self.items[self.size() - 1]

        def size(self):
            return len(self.items)

        def isEmpty(self):
            if self.items:
                return False
            return True

    def __init__(self, service):
        super(FrontEndJsonCallback, self).__init__(service)
        self.callbacks = FrontEndJsonCallback.Queue()

    def write(self, data, callback = None):
        self.callbacks.enqueue(callback)
        data = self.__wrapData(data)
        return FrontEnd.write(self, data)

    def on_read(self, data):
        hasCallback, data = self.__splitData(data)
        data = self.__unwrapData(data)
        if hasCallback == 'True' and not self.callbacks.isEmpty():
            callback = self.callbacks.dequeue()
            if callback is not None:
                callback(data)
        return FrontEnd.on_read(self, data)

    def __wrapData(self, data):
        return json.dumps(data)

    def __unwrapData(self, data):
        return json.loads(data, object_hook=_decode_dict)

    def __splitData(self, data):
        return tuple(data.split('----'))


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)

    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value

    return rv
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Engine\pyCommunicator\FrontEndJsonCallback.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:49 ora legale Europa occidentale
