class EntityManager(object):
    def __init__(self):
        self.entities = {}    
    def existEntity(self,id):
        return id in self.entities
    def getEntity(self,id):
        return self.entities[id]
    def setEntity(self,entity):
        self.entities[entity.getId()] = entity
    def getAll(self):
        return self.entities