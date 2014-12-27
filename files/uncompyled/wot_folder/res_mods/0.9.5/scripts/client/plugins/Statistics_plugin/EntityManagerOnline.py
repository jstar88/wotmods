from EntityManager import EntityManager
from DownloaderWG import DownloaderWG

class EntityManagerOnline(EntityManager):
    def __init__(self, config ):
        super(EntityManagerOnline, self).__init__()
        self.firstTime = True
        self.config = config
    def updateList(self,players):
        tmp = []
        for id in players:
            if not self.existEntity(id):
                tmp.append(id)
            if len(tmp)==self.config['maxentries'] and not self.firstTime and BigWorld.player().arena.guiType == 0:
                break
            firstTime = False
        if not tmp:
            return
        xs = DownloaderWG(self.config).getEntities(tmp)
        for ent in xs:
            self.setEntity(ent)