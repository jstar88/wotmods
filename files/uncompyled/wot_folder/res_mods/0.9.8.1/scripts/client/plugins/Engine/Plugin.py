from ModUtils import FileUtils
class Plugin(object):
    def __init__(self):
        self.pluginEnable = True
        self.pluginName = self.__class__.__name__
    
    def run(self):
        pass
    
    def readConfig(self):
        value = FileUtils.readConfig(self.pluginName, getattr(self.__class__, 'myConf'))
        setattr(self.__class__,'myConf',value)
        if value.has_key('pluginEnable'):
            self.pluginEnable = value['pluginEnable']
        else:
            self.pluginEnable = True