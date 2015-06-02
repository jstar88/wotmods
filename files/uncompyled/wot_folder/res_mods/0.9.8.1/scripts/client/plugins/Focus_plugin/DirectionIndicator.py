from gui.Scaleform.Flash import Flash
from IDirectionIndicator import IDirectionIndicator
from gui import DEPTH_OF_Aim

class DirectionIndicator(Flash, IDirectionIndicator):

    def __init__(self,config):
        self.config = config
        Flash.__init__(self, config["swf_file_name"], config["flash_class"], [config["flash_mc_name"]], config["swf_path"])
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_Aim
        self.movie.backgroundAlpha = config["backgroundAlpha"]
        self.movie.scaleMode = config["scaleMode"]
        self.component.focus = config["focus"]
        self.component.moveFocus = config["moveFocus"]
        self.component.heightMode = config["heightMode"]
        self.component.widthMode = config["widthMode"]
        self.flashSize = config["flash_size"]
        self.component.relativeRadius = config["relativeRadius"]
        self.__dObject = getattr(self.movie, config["flash_mc_name"], None)

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
        
    def setVName(self,value):
        if self.__dObject and self.config['setVName']:
            self.__dObject.setVName(value)