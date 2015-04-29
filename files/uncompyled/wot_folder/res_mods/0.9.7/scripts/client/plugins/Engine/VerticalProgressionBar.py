from HorizontalProgressionBar import HorizontalProgressionBar

class VerticalProgressionBar(HorizontalProgressionBar):
    def __init__(self,leftTexture = '',rightTexture = ''):
        super(VerticalProgressionBar, self).__init__(leftTexture,rightTexture)
    
    def setPercentage(self,p):
        self.a.setWidth(self.width)
        self.b.setWidth(self.width)
        
        self.a.setPosition(self.position)
        self.b.setPosition((self.position[0],self.position[1]+self.height * p,self.position[2]))
        
        self.a.setHeight(self.height* p)
        self.b.setHeight(self.height* (1-p))
        
        
    