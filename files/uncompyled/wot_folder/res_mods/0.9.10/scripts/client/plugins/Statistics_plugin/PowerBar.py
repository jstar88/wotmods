from HorizontalProgressionBarWithText import HorizontalProgressionBarWithText
import GUI


powerBar = None

def battleInit(config):
    global powerBar  
    x, y = GUI.screenResolution()
    powerBar = HorizontalProgressionBarWithText(config['powerbar_texture'],config['powerbar_texture'])
    powerBar.add()
    powerBar.setWidthMode('PIXEL')
    powerBar.setHeightMode('PIXEL')
    powerBar.setVerticalPositionMode('PIXEL')
    powerBar.setHorizontalPositionMode('PIXEL')
    powerBar.setHorizontalAnchor('LEFT')
    powerBar.setVerticalAnchor('TOP')
    powerBar.setWidth(config['powerbar_width'])#400
    powerBar.setHeight(config['powerbar_height'])#5
    powerBar.setPosition(eval(config['powerbar_position']))#(pos_x/2-200,pos_y/10 - 50,0.7)
    powerBar.setColor(eval(config['powerbar_colors'][0]),eval(config['powerbar_colors'][1]))#(100, 255, 0, 100),(255, 50, 50, 100))
    powerBar.setMaterialFx(config['powerbar_materialFX'])
    powerBar.setFont(config['powerbar_font'])
    powerBar.setVisible(True)
    
def battleEnd():
    global powerBar
    if powerBar is not None:  
        powerBar.delete()
        powerBar = None
    
def updateWinRate(winrate=0.5,winratetext='50%',config = None):
    global powerBar
    if powerBar is None:
        battleInit(config)
    powerBar.setPercentageText(winrate,winratetext)
    