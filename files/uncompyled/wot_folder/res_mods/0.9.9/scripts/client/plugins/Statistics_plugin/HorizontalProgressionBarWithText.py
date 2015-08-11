from HorizontalProgressionBar import HorizontalProgressionBar
import GUI

class HorizontalProgressionBarWithText(HorizontalProgressionBar):
    def __init__(self,leftTexture = '',rightTexture = ''):
        super(HorizontalProgressionBarWithText, self).__init__(leftTexture, rightTexture)
        self.text = GUI.Text('')
        GUI.addRoot(self.text)
        self.text.colourFormatting = True

    def setPercentageText(self,p,winratetext):
        self.text.text = winratetext
        super(HorizontalProgressionBarWithText, self).setPercentage(p)

    def setWidthMode(self,mode = 'PIXEL'):
        self.text.widthMode = mode
        super(HorizontalProgressionBarWithText, self).setWidthMode(mode)
    def setHeightMode(self,mode = 'PIXEL'):
        self.text.heightMode = mode
        super(HorizontalProgressionBarWithText, self).setHeightMode(mode)

    def setVerticalPositionMode(self,mode = 'PIXEL'):
        self.text.verticalPositionMode = mode
        super(HorizontalProgressionBarWithText, self).setVerticalPositionMode(mode)
    def setHorizontalPositionMode(self,mode = 'PIXEL'):
        self.text.horizontalPositionMode = mode
        super(HorizontalProgressionBarWithText, self).setHorizontalPositionMode(mode)

    def setHorizontalAnchor(self,anchor = 'RIGHT'):
        self.text.horizontalAnchor = anchor
        super(HorizontalProgressionBarWithText, self).setHorizontalAnchor(anchor)
    def setVerticalAnchor(self,anchor = 'TOP'):
        self.text.verticalAnchor = anchor
        super(HorizontalProgressionBarWithText, self).setVerticalAnchor(anchor)

    def setPosition(self,position):
        self.text.position = (position[0]+ self.width/2 -10,position[1]+10, position[2])
        super(HorizontalProgressionBarWithText, self).setPosition(position)
        
    def delete(self):
        GUI.delRoot(self.text)
        super(HorizontalProgressionBarWithText, self).delete()
        
    def setFont(self,type):
        self.text.font = type