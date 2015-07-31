import urllib2
import traceback
from StringIO import StringIO
import gzip
import json
import zlib
from Entity import Entity
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE, LOG_WARNING


class DownloaderWG(object):
    def __init__(self, config):
        self.url = config['url']
        self.formatz = {
                        'application_id':config['application_id'], 
                        'region':config['region'], 
                        'pr_index':config['pr_index'], 
                        'lang_index':config['lang_index'], 
                        'wr_index':config['wr_index'], 
                        'battles_index':config['battles_index']
                        }
    def getEntities(self,ids):
        self.formatz['id'] = ','.join(map(str,ids))
        tmp = []
        try:
            url = self.url.format(**self.formatz)
            data = fetchUrl(url)
            ens = json.loads(data)['data']
        except:
            #traceback.print_exc()
            for id in ids:
                tmp.append(Entity(id, 0,'', 0.0,0))
            return tmp
        if ens is None:
            LOG_NOTE('players are None')
        else:
            for id,info in ens.iteritems():
                id = int(id)
                if info is not None:
                    pr = int(getNestedElement(info,self.formatz['pr_index']))
                    bt = int(getNestedElement(info,self.formatz['battles_index']))
                    wr = int(getNestedElement(info,self.formatz['wr_index']))
                    if not bt:
                        wr = 0.0
                    else:
                        wr = wr * 100.0 / bt
                    lang = getNestedElement(info,self.formatz['lang_index'])
                    entity = Entity(id, pr,lang, wr,bt)
                    tmp.append(entity)
                else:
                    tmp.append(Entity(id, 0,'', 0.0,0))
        return tmp
    

def decode (page):
    encoding = page.info().get("Content-Encoding") 
    content = page.read()   
    if encoding in ('gzip', 'x-gzip', 'deflate'):
        if encoding == 'deflate':
            data = StringIO(zlib.decompress(content))
        else:
            data = gzip.GzipFile('', 'rb', 9, StringIO(content))
        content = data.read()
    return content


def fetchUrl(url,tryGzip=True,timeout=10):
    opener = urllib2.build_opener()
    if tryGzip:
        opener.addheaders = [('Accept-encoding', 'gzip,deflate')]
    response = opener.open(url)    
    return decode(response)

def getNestedElement(v,path):
    indexes = path.split('.')
    for index in indexes:
        v = v[index]
    return v