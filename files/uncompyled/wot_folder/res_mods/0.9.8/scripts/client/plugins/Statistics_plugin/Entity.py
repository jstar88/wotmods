class Entity(object):
    def __init__(self,id,pr,lang,wr,battles):
        self.id = id
        self.pr = pr
        self.lang = lang
        self.wr = wr
        self.battles = battles
    def getPersonalRating(self):
        return self.pr
    def getClientLang(self):
        return self.lang
    def getId(self):
        return self.id
    def getBattlesAmount(self):
        return self.battles
    def getWinRate(self):
        return self.wr