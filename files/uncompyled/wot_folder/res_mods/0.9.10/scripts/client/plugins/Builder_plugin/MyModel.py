# 2015.09.05 18:13:47 ora legale Europa occidentale
# Embedded file name: MyModel.py
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
        return

    def create(self):
        m = Math.Matrix()
        m.setRotateYPR(Math.Vector3(self.yaw, 0, 0))
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
        else:
            self.model.motors = ()
            self.model.position = pos
            self.pos = pos
            return

    def rotate(self, yaw):
        self.model.motors = ()
        self.model.yaw = yaw
        self.yaw = yaw

    def increaseRotation(self, r):
        self.rotate(self.yaw + r)

    def increaseAltitude(self, y):
        pos = self.getPosition()
        newPos = Math.Vector3((pos[0], pos[1] + y, pos[2]))
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

    def setDBId(self, dbID):
        self.dbID = dbID
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Builder_plugin\MyModel.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:47 ora legale Europa occidentale
