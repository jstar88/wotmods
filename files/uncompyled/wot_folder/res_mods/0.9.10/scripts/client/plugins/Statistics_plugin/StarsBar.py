import GUI
class StarsBar:
    def __init__(self,n,startPosition,delta,size,activePath,inactivePath):
        self.delta = delta
        self.n = n
        self.size = size
        self.startPosition = startPosition
        self.activePath = activePath
        self.inactivePath = inactivePath
        self.stars = []
    
    def add(self,activeAmount):
        i = 0
        while(i < activeAmount):
            self.stars.append(self.createStar(True))
            i+=1
        
        while(i < self.n):
            self.stars.append(self.createStar(False))
            i+=1
    
    def createStar(self, active):
        if active:
            path = self.activePath
        else:
            path = self.inactivePath
        newPos = (self.startPosition[0]+self.delta*len(self.stars),self.startPosition[1],self.startPosition[2])
        item = GUI.Simple(path)
        GUI.addRoot(item)
        item.widthMode = item.heightMode = item.verticalPositionMode = item.horizontalPositionMode = 'PIXEL'
        item.horizontalAnchor = 'LEFT'
        item.verticalAnchor = 'TOP'
        item.size = self.size
        item.position = newPos
        item.visible = True
        return item
    
    def delete(self):
        for item in self.stars:
            GUI.delRoot(item)
        self.stars = []
        
        