# 2015.09.05 18:13:49 ora legale Europa occidentale
# Embedded file name: BackEndJsonCallback.py
from BackEnd import BackEnd
import json

class BackEndJsonCallback(BackEnd):

    def on_read(self, data):
        data = self.__unwrapData(data)
        return BackEnd.on_read(self, data)

    def write(self, data, hasCallback = 'False'):
        data = self.__wrapData(data)
        data = self.__joinData(data, hasCallback)
        return BackEnd.write(self, data)

    def reply(self, data):
        return self.write(data, 'True')

    def __wrapData(self, data):
        return json.dumps(data)

    def __unwrapData(self, data):
        return json.loads(data, object_hook=_decode_dict)

    def __joinData(self, data, hasCallback):
        return hasCallback + '----' + data


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
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Engine\pyCommunicator\BackEndJsonCallback.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:49 ora legale Europa occidentale
