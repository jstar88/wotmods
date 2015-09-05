# 2015.09.05 18:13:49 ora legale Europa occidentale
# Embedded file name: BackEnd.py
import threading
import sys
from libs.Event import Event as EVNT

class BackEnd(object):
    onRead = EVNT()

    def __init__(self):
        pass

    def run(self):

        def rund():
            while True:
                self.on_read(raw_input())

        t = threading.Thread(target=rund)
        t.start()

    def write(self, data):
        print data
        sys.stdout.flush()

    def on_read(self, data):
        return self.onRead(data)
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Engine\pyCommunicator\BackEnd.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:49 ora legale Europa occidentale
