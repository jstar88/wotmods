# 2015.09.05 18:13:47 ora legale Europa occidentale
# Embedded file name: PathManager.py
import os
import zipfile
from glob import glob
from zipfile import ZipFile
from plugins.Engine.ModUtils import FileUtils

class PathManager:

    def __init__(self, zipName = 'res/packages/shared_content.pkg', extPath = None):
        self.data = {}
        paths = self.__getModelPaths(zipName, extPath)
        for path in paths:
            self.data[os.path.basename(path)] = path

        self.basenames = self.data.keys()
        self.basenamesPointer = -1

    def __getModelPaths(self, zipName, extPath):
        if not os.path.isfile(zipName):
            raise Exception('Invalid zip models path')
        zip = zipfile.ZipFile(zipName)
        names = zip.namelist()
        dirname = ''
        ext = '.model'.lower()
        paths = []
        for name in names:
            if name.lower().endswith(ext):
                paths.append(os.path.join(dirname, name))

        if extPath is not None:
            if not os.path.isdir(extPath):
                raise Exception('Invalid external models path')
            result = [ y for x in os.walk(extPath) for y in glob(os.path.join(x[0], '*.model')) ]
            paths.extend(result)
        return sorted(paths)

    def getBaseNames(self):
        return self.basenames

    def getPathFromBaseName(self, name):
        return self.data[name]

    def getNextBaseName(self):
        self.basenamesPointer += 1
        if self.basenamesPointer == len(self.basenames):
            self.basenamesPointer = -1
            return self.basenames[0]
        return self.basenames[self.basenamesPointer]

    def getPrevBaseName(self):
        self.basenamesPointer -= 1
        if self.basenamesPointer < 0:
            self.basenamesPointer = len(self.basenames) - 1
        return self.basenames[self.basenamesPointer]

    def getNextPath(self):
        return self.getPathFromBaseName(self.getNextBaseName())

    def getPrevPath(self):
        return self.getPathFromBaseName(self.getPrevBaseName())

    def resetPointer(self):
        self.basenamesPointer = -1

    def extract(self, zip_path = 'res/packages/shared_content.pkg', path = 'content/Railway/rw012_MechSemafor/', output = 'models'):
        temp_dir = os.path.join(FileUtils.getRealPluginPath('Builder_plugin'), output)
        with ZipFile(zip_path, 'r') as zip_file:
            members = zip_file.namelist()
            members_to_extract = [ m for m in members if m.startswith(path) ]
            zip_file.extractall(temp_dir, members_to_extract)

    def clean(self, output):
        pass
# okay decompyling C:\Users\nicola user\wotmods\files\originals\wot_folder\res_mods\0.9.10\scripts\client\plugins\Builder_plugin\PathManager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.09.05 18:13:48 ora legale Europa occidentale
