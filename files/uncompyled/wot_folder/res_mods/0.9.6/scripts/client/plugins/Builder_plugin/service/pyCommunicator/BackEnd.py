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
        
    def write(self,data):
        print data
        sys.stdout.flush()
        
    def on_read(self,data):
        return self.onRead(data)