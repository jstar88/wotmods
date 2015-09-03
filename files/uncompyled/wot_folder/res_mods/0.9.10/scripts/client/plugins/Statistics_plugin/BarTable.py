from TextureBar import TextureBar
from HorizontalProgressionBarWithText import HorizontalProgressionBarWithText

class BarTable(TextureBar):
    def __init__(self,texture=''):
        super(BarTable,self).__init__(texture)
        self.bars = [] 
        self.position = (0,0,0)

        
    def addBar(self,config):
        bar = self.createBar(config)
        self.bars.append(bar)
        
    def createBar(self,config):
        powerBar = HorizontalProgressionBarWithText(config['texture'],config['texture'])
        powerBar.setMaterialFx(config['materialFX'])
        powerBar.add()
        powerBar.setWidthMode('PIXEL')
        powerBar.setHeightMode('PIXEL')
        powerBar.setVerticalPositionMode('PIXEL')
        powerBar.setHorizontalPositionMode('PIXEL')
        powerBar.setHorizontalAnchor('LEFT')
        powerBar.setVerticalAnchor('TOP')
        powerBar.setWidth(config['width'])#400
        powerBar.setHeight(config['height'])#5
        v = config['position']
        if config['align'] == 'vertical':
            v =( v[0],v[1] + len(self.bars)*config['delta'],v[2] )
        else:
            v =( v[0]+ len(self.bars)*config['delta'],v[1],v[2] )
        powerBar.setPosition(v,config['table_bars_odd_pos'])#(pos_x/2-200,pos_y/10 - 50,0.7)
        powerBar.setColor(config['color'][0],config['color'][1])#(100, 255, 0, 100),(255, 50, 50, 100))
        powerBar.setFont(config['font'])
        powerBar.setPercentageText(config['percentage'],config['percentage_text'])
        powerBar.setLabelText(config['label'])
        powerBar.setVisible(True)
        #powerBar.attachTo(self.getComponent())
        return powerBar
    
    def delete(self):
        for bar in self.bars:
            bar.delete()
        self.bars = []
        super(BarTable, self).delete()
    
    def setPosition(self,position):
        self.position = position
        super(BarTable,self).setPosition(position)
        