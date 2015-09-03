from HorizontalProgressionBar import HorizontalProgressionBar
import GUI

class HorizontalProgressionBarWithText(HorizontalProgressionBar):
    def __init__(self,leftTexture = '',rightTexture = ''):
        super(HorizontalProgressionBarWithText, self).__init__(leftTexture, rightTexture)
        self.text = GUI.Text('')
        self.label = GUI.Text('')
        self.text.colourFormatting = True
        self.label.colourFormatting = True

    
    def add(self):
        super(HorizontalProgressionBarWithText,self).add()
        GUI.addRoot(self.text)
        GUI.addRoot(self.label)
    
    def setPercentageText(self,p,winratetext):
        self.text.text = winratetext
        super(HorizontalProgressionBarWithText, self).setPercentage(p)
    
    def setLabelText(self,text):
        self.label.text = text

    def setWidthMode(self,mode = 'PIXEL'):
        self.text.widthMode = mode
        self.label.widthMode = mode
        super(HorizontalProgressionBarWithText, self).setWidthMode(mode)
    def setHeightMode(self,mode = 'PIXEL'):
        self.text.heightMode = mode
        self.label.heightMode = mode
        super(HorizontalProgressionBarWithText, self).setHeightMode(mode)

    def setVerticalPositionMode(self,mode = 'PIXEL'):
        self.text.verticalPositionMode = mode
        self.label.verticalPositionMode = mode
        super(HorizontalProgressionBarWithText, self).setVerticalPositionMode(mode)
    def setHorizontalPositionMode(self,mode = 'PIXEL'):
        self.text.horizontalPositionMode = mode
        self.label.horizontalPositionMode = mode
        super(HorizontalProgressionBarWithText, self).setHorizontalPositionMode(mode)

    def setHorizontalAnchor(self,anchor = 'RIGHT'):
        self.text.horizontalAnchor = anchor
        self.label.horizontalAnchor = anchor
        super(HorizontalProgressionBarWithText, self).setHorizontalAnchor(anchor)
    def setVerticalAnchor(self,anchor = 'TOP'):
        self.text.verticalAnchor = anchor
        self.label.verticalAnchor = anchor
        super(HorizontalProgressionBarWithText, self).setVerticalAnchor(anchor)

    def setPosition(self,position,perPos = 'bottom'):
        barX = position[0]
        barY = position[1]
        barZ = position[2]
        barWidth = self.width
        barHeight = self.height
        
        if perPos == 'bottom':
            self.text.position = (barX+barWidth/2-10, barY+10, barZ)
        elif perPos == 'top':
            self.text.position = (barX+barWidth/2-10, barY-barHeight-10, barZ)
        elif perPos == 'right':
            self.text.position = (barX+barWidth+10, barY-barHeight, barZ)
        else:
            self.text.position = eval(perPos)
        self.label.position = (barX-40, barY-barHeight, barZ)
        
        super(HorizontalProgressionBarWithText, self).setPosition(position)
        
    def delete(self):
        GUI.delRoot(self.text)
        GUI.delRoot(self.label)
        super(HorizontalProgressionBarWithText, self).delete()
        
    def setFont(self,type):
        self.text.font = type
        self.label.font = type
        
    def setMaterialFx(self,type = 'ADD'):
        super(HorizontalProgressionBarWithText, self).setMaterialFx(type)