import sqlite3

class Database(object):
    
    def __init__(self, dbname):
        self.dbname = dbname
        
    def execute(self,query,fields = None):
        dbcon = sqlite3.connect(self.dbname)
        dbcon.row_factory = dict_factory
        c = dbcon.cursor()
        if fields is None:
            c.execute(query)
        else:
            c.execute(query,fields)
        dbcon.commit()
        dbcon.close()
        return True
        
    def executeFetchOne(self,query,fields = None):
        dbcon = sqlite3.connect(self.dbname)
        dbcon.row_factory = dict_factory
        c = dbcon.cursor()
        if fields is None:
            c.execute(query)
        else:
            c.execute(query,fields)
        dbcon.commit()
        tmp =  c.fetchone()
        dbcon.close()
        return tmp
        
    def executeFetchAll(self,query,fields = None):
        dbcon = sqlite3.connect(self.dbname)
        dbcon.row_factory = dict_factory
        c = dbcon.cursor()
        if fields is None:
            c.execute(query)
        else:
            c.execute(query,fields)
        dbcon.commit()
        tmp = c.fetchall()
        dbcon.close()
        return tmp
    
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d