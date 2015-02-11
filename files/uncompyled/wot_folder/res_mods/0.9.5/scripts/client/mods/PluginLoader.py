import os
import imp
import sys
import importlib
import traceback
from plugins.Engine.ModUtils import FileUtils
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_NOTE,LOG_WARNING

wotFolder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PluginFolder = os.path.join(wotFolder,'res_mods')
PluginFolder = os.path.join(PluginFolder,FileUtils.getWotVersion())
PluginFolder = os.path.join(PluginFolder,'scripts')
PluginFolder = os.path.join(PluginFolder,'client')
PluginFolder = os.path.join(PluginFolder,'plugins')

def getPlugins():
    plugins = []
    sys.path.append(PluginFolder)
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or i == "Engine":
            continue
        plugins.append(i)
    return plugins

def loadPlugin(i):
    try:
        module = __import__(i)
        my_class = getattr(module, i.replace("_plugin",""))
        plugin = my_class()
        plugin.readConfig()
        if plugin.pluginEnable:
            print "---> Loading "+i
            plugin.run()
    except:
        LOG_ERROR('plugin "'+i+'" contains errors!')
        traceback.print_exc()
        

map(loadPlugin, getPlugins())