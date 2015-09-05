# 2015.09.05 18:13:44 ora legale Europa occidentale
# Embedded file name: main.py
from PyPyCommunicator import PyPyCommunicator

def callback(obj):
    print obj


com = PyPyCommunicator()
for i in xrange(0, 5):
    com.addRequest(['python', 'ext_service.py'], ['Hello', 'World', i], callback)
# okay decompyling C:\Users\nicola user\wotmods\files\originals\tests\communication\main.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:44 ora legale Europa occidentale
