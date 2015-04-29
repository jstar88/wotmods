from DBStub import DBStub
from MyModel import MyModel
from functools import partial
from pyCommunicator.FrontEndJsonCallback import FrontEndJsonCallback
from plugins.Engine.ModUtils import FileUtils
import os
from Math import Vector3
import BigWorld
from debug_utils import LOG_NOTE



class ModelManager:
    def __init__(self, mapName):
        self.data = {}
        self.tmpdata = None
        path = FileUtils.getRealPluginPath('Builder_plugin')
        path = os.path.join(path, 'service')
        path = os.path.join(path, 'dist')
        path = os.path.join(path, 'generic_instance_manager.exe')
        f = FrontEndJsonCallback([path])
        f.run()
        
        path = FileUtils.getRealPluginPath('Builder_plugin')
        path = os.path.join(path, 'maps')
        path = os.path.join(path, mapName + '.db')
        LOG_NOTE('Loading: '+path)
        self.db = DBStub(f, path, 'models', self.__onInited)
    
    def __onInited(self, state):
        self.loadFromDB()
    
    
    def addModel(self, position, yaw, modelPath, callback=None):
        model = MyModel(-1 , position, yaw, modelPath)
        self.db.addObject(position, yaw, modelPath, partial(self.onAdded, model, callback))
        
    def onAdded(self, model, callback, state):
        self.db.getLastId(partial(self.onGotID, model, callback))
    
    def onGotID(self, model, callback, dbID):
        dbID = dbID.values()[0]
        model.setDBId(dbID)
        self.data[dbID] = model
        if callback is not None:
            callback()
        
    
        
    def getModel(self, dbID):
        return self.data[dbID]
    
    def removeModel(self, dbID, callback=None):
        model = self.data[dbID]
        model.remove()
        del self.data[dbID]
        self.db.removeObject(dbID, callback)
    
    def clean(self, callback=None):
        for k, v in self.data.iteritems():
            v.remove()
        self.data = {}
        
    
    
    def loadFromDB(self):
        self.db.getAllObjects(self.__onLoadedFromDB)
        self.checkCreate()
    
    def checkCreate(self):
        if self.tmpdata is None:
            BigWorld.callback(1,self.checkCreate)
            return
        for model in self.tmpdata:
            yaw = model['yaw']
            path = model['path']
            bid = model['id']
            pos = Vector3((model['x'], model['y'], model['z']))
            self.data[bid] = MyModel(bid, pos, yaw, path)
        
    def __onLoadedFromDB(self, models):
        self.tmpdata = models
