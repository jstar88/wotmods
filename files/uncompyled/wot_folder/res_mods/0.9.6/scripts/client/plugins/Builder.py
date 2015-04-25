from ProjectileMover import collideDynamicAndStatic
from AvatarInputHandler import AimingSystems
import BigWorld
import Math
import GUI
import AvatarInputHandler
import Keys
import game
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE
import os
import zipfile

#preload2 = BigWorld.Model('characters/npc/flying_dragon/flying_dragon.model')

class MyModel:
	def __init__(self,modelPath = 'objects/red.model'):
		self.model = None
		self.motor = None
		self.modelPath = modelPath
	
	def create(self, pos):
		view = Math.Matrix()
		view.setTranslate((0, 0, 0))
		m = Math.Matrix()
		m.setTranslate(Math.Matrix(view).applyPoint(pos))
		self.motor = BigWorld.Servo(m)
		self.model = BigWorld.Model(self.modelPath)
		self.model.addMotor(self.motor)
		BigWorld.addModel(self.model)
		self.model.visible = True
		return self.model
		
	def move(self, pos):
		self.model.position = pos
	
	def remove(self):
		self.model.delMotor(self.motor)
		BigWorld.delModel(self.model)
	
	def action(self,name):
		self.model.action(name)
		


def handleKeyEvent(event):
	try:
		isDown, key, mods, isRepeat = game.convertKeyEvent(event)
		if not isRepeat and isDown:
			#MyModel('helpers/models/entity_arrow.model').create(BigWorld.player().inputHandler.getDesiredShotPoint())
			entity = BigWorld.createEntity('OfflineEntity', BigWorld.player().spaceID, 0, BigWorld.player().inputHandler.getDesiredShotPoint(), (0, 0, 0), dict())
			model = MyModel('content/Railway/rw012_MechSemafor/normal/lod0/rw012_MechSemafor.model').create(BigWorld.player().inputHandler.getDesiredShotPoint())
			
	except Exception as e:
		LOG_CURRENT_EXCEPTION
		print e
	finally:
		return oldFromPlatoonChatHandleKeyEvent(event)

oldFromPlatoonChatHandleKeyEvent = game.handleKeyEvent
game.handleKeyEvent = handleKeyEvent
		
def parseHotkeys(hotkeyString):
	return filter(lambda keycode: keycode > 0, map(lambda code: getattr(Keys, code, 0), hotkeyString.split('+')))
	

def keysMatch(inputSet, targetSet):
	return len(targetSet) and len(filter(lambda k: k in inputSet, targetSet)) == len(targetSet)
	

def getModels(zipName = 'shared_content'):
	zip=zipfile.ZipFile('res/packages/'+zipName+'.pkg')
	names = sorted(zip.namelist())
	dirname = ''
	ext = '.model'.lower()
	paths = []

	for name in names:
		if name.lower().endswith(ext):
			paths.append(os.path.join(dirname, name))
	return paths
	