"""
Library to make asynchronous-statefull-bidirectional communication with external software.
"""

import subprocess
import threading
from functools import partial


class Communicator(object):
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
    
    def __init__(self):
        self.queue = Communicator.Queue()
        
    def __elaborate(self, callback, proc, message):
        stdout_value, stderr_value = proc.communicate(message)
        if stderr_value:
            print stderr_value
            raise Exception('Error returned from external communication') 
        callback(stdout_value)
            
    def __runTask(self):
        element = self.queue.top()
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        proc = subprocess.Popen(element[1],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        startupinfo=startupinfo
                        )
        t = threading.Thread(target=partial(self.__elaborate, element[0], proc, element[2]))
        t.start()
    
    def addRequest(self, command, message, callback):
        def signal(*args, **kwargs):
            callback(*args, **kwargs)
            self.queue.dequeue()
            if self.queue.size() > 0:
                self.__runTask()
        self.queue.enqueue([signal, command, message])
        if self.queue.size() == 1:
            self.__runTask()    
    
    def addFreeRequest(self, command, message, callback):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        proc = subprocess.Popen(command,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        startupinfo=startupinfo
                        )
        t = threading.Thread(target=partial(self.__elaborate, callback, proc, message))
        t.start()
        
        

#---------------- Example --------------------
def example():
    def callback(v):
        print '1)' + v
    
    def callback2(v):
        print '2)' + v
    
    def callback3(v):
        print '3)' + v

    communicator = Communicator()
    communicator.addRequest(['python', 'b.py'], 'hello world', callback)
    communicator.addRequest(['python', 'c.py'], 'hello world2', callback2)
    communicator.addFreeRequest(['python', 'c.py'], 'hello world3', callback3)
    print 'code is going to be free'


#example()
"""
code is going to be free
3)c.py
hello world3

1)b.py
hello world

2)c.py
hello world2
"""