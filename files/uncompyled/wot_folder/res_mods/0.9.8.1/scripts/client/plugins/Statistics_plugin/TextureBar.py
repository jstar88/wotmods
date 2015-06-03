import GUI
class TextureBar(object):
    def __init__(self, texture=''):
        self.pb = GUI.Simple(texture)

    def add(self):
        GUI.addRoot(self.pb)
    def delete(self):
        GUI.delRoot(self.pb)

    def setWidthMode(self,mode = 'PIXEL'):
        self.pb.widthMode = mode
    def setHeightMode(self,mode = 'PIXEL'):
        self.pb.heightMode = mode

    def setVerticalPositionMode(self,mode = 'PIXEL'):
        self.pb.verticalPositionMode = mode
    def setHorizontalPositionMode(self,mode = 'PIXEL'):
        self.pb.horizontalPositionMode = mode

    def setHorizontalAnchor(self,anchor = 'RIGHT'):
        self.pb.horizontalAnchor = anchor
    def setVerticalAnchor(self,anchor = 'TOP'):
        self.pb.verticalAnchor = anchor

    def setColor(self,color):
        self.pb.colour = color

    def setHeight(self,height):
        self.pb.height = height
    def setWidth(self,width):
        self.pb.width = width

    def setVisible(self,visible):
        self.pb.visible = visible

    def setPosition(self,position):
        self.pb.position = position