import json
import os
import sys

class SpineConverterSettings:
    def __init__(self):
        try:
            path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'settings.json')
            file = open(path, 'r')
            text = file.read()
            text = text.replace("\\", "/")
            file.close()
            jsonData = json.loads(text)
            self.settings = jsonData
        except:
            print("Couldn't find settings.json")
            self.settings = dict()

    def isSkinnedMeshesExperimental(self) -> bool:
        if "skinnedMeshesExperimental" in self.settings.keys():
            return self.settings["skinnedMeshesExperimental"]
        return True


    def hasSeveralAnimations(self) -> bool:
        if "severalAnimations" in self.settings.keys():
            return self.settings["severalAnimations"]
        return True

    def isAutoRenameOn(self) -> bool:
        if "autoRename" in self.settings.keys():
            return self.settings["autoRename"]
        return True

    def isAddEmptyAnimationsOn(self) -> bool:
        if "addEmptyAnimations" in self.settings.keys():
            return self.settings["addEmptyAnimations"]
        return True

    def isFixMeshes(self) -> bool:
        if "fixMeshes" in self.settings.keys():
            return self.settings["fixMeshes"]
        return True

    def isDumpSkelData(self) -> bool:
        if "dumpSkelData" in self.settings.keys():
            return self.settings["dumpSkelData"]
        return False

    def isPreserveDBJson(self) -> bool:
        if "preserveDBJson" in self.settings.keys():
            return self.settings["preserveDBJson"]
        return False

    def isFixDataFromSkel(self) -> bool:
        if "fixDataFromSkel" in self.settings.keys():
            return self.settings["fixDataFromSkel"]
        return True

    def getFilePath(self) -> bool:
        if "filePath" in self.settings.keys():
            return self.settings["filePath"]
        return ""
