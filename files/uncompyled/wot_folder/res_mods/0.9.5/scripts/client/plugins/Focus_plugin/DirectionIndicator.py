from gui.Scaleform.Flash import Flash
from IDirectionIndicator import IDirectionIndicator
from gui import DEPTH_OF_Aim

class DirectionIndicator(Flash, IDirectionIndicator):
    __SWF_FILE_NAME = 'DirectionIndicator.swf'
    __FLASH_CLASS = 'WGDirectionIndicatorFlash'
    __FLASH_MC_NAME = 'directionalIndicatorMc'
    __FLASH_SIZE = (680, 680)

    def __init__(self):
        Flash.__init__(self, self.__SWF_FILE_NAME, self.__FLASH_CLASS, [self.__FLASH_MC_NAME])
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_Aim
        self.movie.backgroundAlpha = 0.0
        self.movie.scaleMode = 'NoScale'
        self.component.focus = False
        self.component.moveFocus = False
        self.component.heightMode = 'PIXEL'
        self.component.widthMode = 'PIXEL'
        self.flashSize = self.__FLASH_SIZE
        self.component.relativeRadius = 0.5
        self.__dObject = getattr(self.movie, self.__FLASH_MC_NAME, None)

    def __del__(self):
        pass

    def setShape(self, shape):
        if self.__dObject:
            self.__dObject.setShape(shape)

    def setDistance(self, distance):
        if self.__dObject:
            self.__dObject.setDistance(distance)

    def setPosition(self, position):
        self.component.position3D = position

    def track(self, position):
        self.active(True)
        self.component.visible = True
        self.component.position3D = position

    def remove(self):
        self.__dObject = None
        self.close()