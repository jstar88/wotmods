from pyCommunicator.BackEndJsonCallback import BackEndJsonCallback
import imports


def myHandler(data):
    global claz_objs,bjc
    idc = data['module']+data['class']+str(data['instance_args'])
    if idc in claz_objs:
        claz_obj = claz_objs[idc]
    else:
        module = __import__(data['module'])
        claz = getattr(module,data['class'])
        instance_args =data['instance_args']  
        claz_obj = claz(*instance_args)
        claz_objs[idc] = claz_obj
    
    methodToCall = getattr(claz_obj,data['method'])  
    bjc.reply(methodToCall(*data['args']))
    

bjc = BackEndJsonCallback()
claz_objs = {}
bjc.onRead += myHandler
bjc.run()