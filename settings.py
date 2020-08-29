import json


class SpineConverterSettings:
    def __init__(self):
        try:
            file = open('settings.json', 'r')
            text = file.read()
            file.close()
            self.settings = json.loads(text)
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
