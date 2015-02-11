import urllib2
import json
from Entity import Entity
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE


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
        ens = safe_list_get(json.loads(urllib2.urlopen(self.url.format(**self.formatz), timeout=30).read()),'data',None)
        if ens is None:
            LOG_NOTE('players is None')
        else:
            for id,info in ens.iteritems():
                if info is not None:
                    pr = int(getNestedElement(info,self.formatz['pr_index']))
                    bt = int(getNestedElement(info,self.formatz['battles_index']))
                    wr = int(getNestedElement(info,self.formatz['wr_index']))
                    if not bt:
                        wr = 0.0
                    else:
                        wr = wr * 100.0 / bt
                    id = int(id)
                    lang = getNestedElement(info,self.formatz['lang_index'])
                    entity = Entity(id, pr,lang, wr,bt)
                    tmp.append(entity)
        return tmp
    
def getNestedElement(v,path):
    indexes = path.split('.')
    for index in indexes:
        v = v[index]
    return v

def safe_list_get (l, idx, default):
    if l is None:
        LOG_NOTE("got None list")
        return default
    try:
        return l[idx]
    except:
        LOG_NOTE("index: "+ str(idx)+ " not in list")
    return default