from TextureBar import TextureBar

class HorizontalProgressionBar(object):
    def __init__(self,leftTexture = '',rightTexture = ''):
        self.a = TextureBar(leftTexture)
        self.b = TextureBar(rightTexture)
        self.width = 0
        self.position = (0,0,0)
        self.p = 0
        self.height = 0

    def add(self):
        self.a.add()
        self.b.add()
    def delete(self):
        self.a.delete()
        self.b.delete()

    def setWidthMode(self,mode = 'PIXEL'):
        self.a.setWidthMode(mode)
        self.b.setWidthMode(mode)
    def setHeightMode(self,mode = 'PIXEL'):
        self.a.setHeightMode(mode)
        self.b.setHeightMode(mode)

    def setVerticalPositionMode(self,mode = 'PIXEL'):
        self.a.setVerticalPositionMode(mode)
        self.b.setVerticalPositionMode(mode)
    def setHorizontalPositionMode(self,mode = 'PIXEL'):
        self.a.setHorizontalPositionMode(mode)
        self.b.setHorizontalPositionMode(mode)

    def setHorizontalAnchor(self,anchor = 'RIGHT'):
        self.a.setHorizontalAnchor(anchor)
        self.b.setHorizontalAnchor(anchor)
    def setVerticalAnchor(self,anchor = 'TOP'):
        self.a.setVerticalAnchor(anchor)
        self.b.setVerticalAnchor(anchor)

    def setColor(self,color1,color2):
        self.a.setColor(color1)
        self.b.setColor(color2)

    def setHeight(self,height):
        self.height = height
        self.setPercentage(self.p)
    def setWidth(self,width):
        self.width = width
        self.setPercentage(self.p)

    def setVisible(self,visible):
        self.a.setVisible(visible)
        self.b.setVisible(visible)

    def setPosition(self,position):
        self.position = position
        self.setPercentage(self.p)

    def setPercentage(self,p):
        self.a.setWidth(self.width * p)
        self.b.setWidth(self.width * (1-p))

        self.a.setPosition(self.position)
        self.b.setPosition((self.position[0]+self.width * p,self.position[1],self.position[2]))

        self.a.setHeight(self.height)
        self.b.setHeight(self.height)
    
    def setMaterialFx(self,type = 'ADD'):
        self.a.setMaterialFx(type)
        self.b.setMaterialFx(type)
        
    def attachTo(self,component):
        self.a.attachTo(component)
        self.b.attachTo(component)
    
    def detachFrom(self,component):
        self.a.detachFrom(component)
        self.b.detachFrom(component)