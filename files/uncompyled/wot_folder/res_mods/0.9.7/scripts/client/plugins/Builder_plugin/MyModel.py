import BigWorld
import Math
from plugins.Engine.ModUtils import FileUtils
import os

class MyModel:
    def __init__(self, dbID, pos, yaw, modelPath):
        self.model = None
        self.modelPath = modelPath
        self.motor = None
        self.pos = pos
        self.yaw = yaw
        self.dbID = dbID
        self.create()
    
    def create(self):
        m = Math.Matrix()  
        m.setRotateYPR(Math.Vector3(self.yaw,0,0))
        m.translation = self.pos
        
        self.motor = BigWorld.Servo(m)
        self.model = BigWorld.Model(self.modelPath)
        self.model.addMotor(self.motor)
        
        BigWorld.addModel(self.model)
        self.model.visible = True
        return self.model
        
    def move(self, pos):
        if pos is None:
            return
        self.model.motors = ()
        self.model.position = pos
        self.pos = pos
        
    def rotate(self, yaw):
        self.model.motors = ()
        self.model.yaw = yaw
        self.yaw = yaw
        
    def increaseRotation(self,r):
        self.rotate(self.yaw + r)
        
    def increaseAltitude(self,y):
        pos = self.getPosition()
        newPos= Math.Vector3((pos[0],pos[1]+y,pos[2]))
        self.move(newPos)
    
    def remove(self):
        if self.motor and self.motor in self.model.motors:
            self.model.delMotor(self.motor)
        BigWorld.delModel(self.model)
    
    def action(self, name):
        self.model.action(name)
        
    def getDBId(self):
        return self.dbID
    
    def getPosition(self):
        return self.pos

    def getYaw(self):
        return self.yaw
    
    def getPath(self):
        return self.modelPath
    
    def setDBId(self,dbID):
        self.dbID = dbID
        
    
