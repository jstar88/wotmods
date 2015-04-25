from PyPyCommunicator import PyPyCommunicator


def callback(obj):
    print obj

com = PyPyCommunicator()
for i in xrange(0,5):
    com.addRequest(['python','ext_service.py'], ['Hello','World',i], callback)