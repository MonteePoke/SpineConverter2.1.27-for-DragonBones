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
        return False


    def hasSeveralAnimations(self) -> bool:
        if "severalAnimations" in self.settings.keys():
            return self.settings["severalAnimations"]
        return False
