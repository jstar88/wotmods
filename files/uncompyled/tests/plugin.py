class B():
    def hello(self):
        return "hello"
    def some(self):
        print 'X '
        
def newHello(self):
    self.some()
    return oldHello(self) + ' world'
oldHello = B.hello
B.hello = newHello

print B().hello()