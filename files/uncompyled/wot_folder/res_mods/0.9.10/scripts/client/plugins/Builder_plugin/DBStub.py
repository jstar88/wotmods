# 2015.09.05 18:13:47 ora legale Europa occidentale
# Embedded file name: DBStub.py


class DBStub:

    def __init__(self, f, dbname = 'example.db', tableName = 'objects', callback = None):
        self.constructor = {'module': 'Database',
         'class': 'Database',
         'instance_args': [dbname]}
        self.f = f
        self.tableName = tableName
        self.__createTable(tableName, ['id INTEGER PRIMARY KEY   AUTOINCREMENT',
         'x real',
         'y real',
         'z real',
         'yaw real',
         'path text'], callback)

    def __send(self, request, callback = None):
        self.constructor.update(request)
        self.f.write(self.constructor, callback)

    def __createTable(self, tableName, fields, callback = None):
        query = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' (' + ','.join(fields) + ')'
        request = {'method': 'execute',
         'args': [query]}
        self.__send(request, callback)

    def addObject(self, position, yaw, path, callback = None):
        x = position[0]
        y = position[1]
        z = position[2]
        query = 'INSERT INTO ' + self.tableName + ' VALUES (?,?,?,?,?,?)'
        request = {'method': 'execute',
         'args': [query, (None,
                   x,
                   y,
                   z,
                   yaw,
                   path)]}
        self.__send(request, callback)
        return

    def removeObject(self, dbId, callback = None):
        query = 'DELETE FROM ' + self.tableName + ' WHERE id=?'
        request = {'method': 'execute',
         'args': [query, dbId]}
        self.__send(request, callback)

    def clean(self, callback = None):
        query = 'DELETE FROM ' + self.tableName
        request = {'method': 'execute',
         'args': [query]}
        self.__send(request, callback)

    def getObject(self, dbId, callback):
        query = 'SELECT * FROM ' + self.tableName + ' WHERE id=?'
        request = {'method': 'executeFetchOne',
         'args': [query, dbId]}
        self.__send(request, callback)

    def getAllObjects(self, callback):
        query = 'SELECT * FROM ' + self.tableName + ' ORDER BY id'
        request = {'method': 'executeFetchAll',
         'args': [query]}
        self.__send(request, callback)

    def getNearObjects(self, position, callback):
        x = position[0]
        y = position[1]
        z = position[2]
        query = 'SELECT * FROM ' + self.tableName + ' WHERE x<? AND y<? AND z<? ORDER BY id'
        request = {'method': 'executeFetchAll',
         'args': [query, (x, y, z)]}
        self.__send(request, callback)

    def getLastId(self, callback):
        query = 'SELECT IFNULL(MAX(id), 0) FROM ' + self.tableName
        request = {'method': 'executeFetchOne',
         'args': [query]}
        self.__send(request, callback)
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Builder_plugin\DBStub.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:47 ora legale Europa occidentale
