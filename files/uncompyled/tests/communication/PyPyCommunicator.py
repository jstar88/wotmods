# 2015.09.05 18:13:44 ora legale Europa occidentale
# Embedded file name: PyPyCommunicator.py
from base.Communicator import Communicator
import marshal

class PyPyCommunicator(Communicator):

    def __init__(self):
        super(PyPyCommunicator, self).__init__()

    def __wrapData(self, data):
        return marshal.dumps(data)

    def __unwrapData(self, data):
        return marshal.loads(data)

    def __unwrapArgs(self, args, kwargs):
        args = map(self.__unwrapData, args)
        kwargs = {k:self.__unwrapData(v) for k, v in kwargs.iteritems()}
        return (args, kwargs)

    def addFreeRequest(self, command, message, callback):

        def newCallback(*args, **kwargs):
            args, kwargs = self.__unwrapArgs(args, kwargs)
            return callback(*args, **kwargs)

        newMessage = self.__wrapData(message)
        super(PyPyCommunicator, self).addFreeRequest(command, newMessage, newCallback)

    def addRequest(self, command, message, callback):

        def newCallback(*args, **kwargs):
            args, kwargs = self.__unwrapArgs(args, kwargs)
            return callback(*args, **kwargs)

        newMessage = self.__wrapData(message)
        super(PyPyCommunicator, self).addRequest(command, newMessage, newCallback)
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\communication\PyPyCommunicator.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:44 ora legale Europa occidentale
