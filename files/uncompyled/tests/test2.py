
class FileUtils2:
    @staticmethod
    def readElement(value,defaultValue):
        if type(defaultValue) is list:
            tmp = []
            for k,v in enumerate(defaultValue[:]):
                if len(value) <= k:
                    print "missing list entry"+str(k+1)
                    tmp.append(v)
                else:
                    tmp.append(FileUtils2.readElement(value[k],v))
            return tmp
        if type(defaultValue) is dict:
            tmp = {}
            for k,v in defaultValue.iteritems():
                if k not in value:
                    k = str(k)
                    print "wrong dict key:"+k
                if k not in value:
                    print "missing dict key:"+k
                    tmp[k] = v
                else:
                    tmp[k]= FileUtils2.readElement(value[k],v)
            return tmp
        if type(defaultValue) is int:
            try:
                value = int(value)
            except Exception:
                print "wrong value"
                value = defaultValue
            return value
        if type(defaultValue) is float:
            return float(value)
        if type(defaultValue) is str:
            return value.tostring()
        if type(defaultValue) is bool: 
            return bool(value)
        print 'error'
        return None  

defs = {'a':1,
        2: 2,
        'c': [6,7,8]
        }
vals = {'a':'1',
        '2':0.2,
        'c':['6',7,8]
        }
    
print FileUtils2.readElement(vals,defs) 