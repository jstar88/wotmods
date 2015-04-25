# this is a file in another distribution

import marshal
import sys

def reply(data):
    print marshal.dumps(data)
    
def retriveData():
    return marshal.loads(sys.stdin.readline())


# just an echo example
reply(retriveData())