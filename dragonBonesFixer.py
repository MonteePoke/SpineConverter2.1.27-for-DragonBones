import re
import spUtils
import json
import os
from spAtlas import *

class DragonBonesFixer:
    def __init__(self, settings):
        self.settings = settings

    # fixes .json file from DragonBones editor
    def fixDragonBonesJson(self, fileName):
        file = open(fileName, 'r')
        jsonData = json.loads(file.read())
        file.close()

        hash1 = hash(json.dumps(jsonData, sort_keys=True))

        file = open(fileName.replace(".json", "_db.json"), 'w')
        file.write( json.dumps(jsonData) )
        file.close()

        # adds spine version
        jsonData["skeleton"]["spine"] = "2.1.27"

        if self.settings.isAutoRenameOn():
            fileName = self.rename(fileName)

        if "animations" not in jsonData.keys():
            jsonData["animations"] = dict()

        if (self.settings.isAddEmptyAnimationsOn()):
            self.addEmptyAnimations(jsonData, fileName)

        if (self.settings.hasSeveralAnimations()):
            self.fixSeveralAnimations(jsonData)

        self.removeShear(jsonData)

        if self.settings.isSkinnedMeshesExperimental():
            self.detectSkinnedMeshes(jsonData)

        self.replaceDeformToFFD(jsonData)

        hash2 = hash(json.dumps(jsonData, sort_keys=True))

        if hash1 != hash2:
            file = open( fileName, 'w' )
            file.write( json.dumps(jsonData) )
            file.close()

        return fileName

    # fixes .skel file from Spine editor
    def fixSpineConverterJson(self, fileName):
        file = open(fileName, 'r+')
        text = file.read()
        jsonData = json.loads(text)
        file.close()

        if self.settings.isFixMeshes():
            self.fixMeshes(jsonData, fileName)

        file = open( fileName, 'w' )
        file.write( json.dumps(jsonData) )
        file.close()

    # renames deform to ffd
    # looks like later Spine versions contain deform, not ffd
    def replaceDeformToFFD(self, jsonData):
        for animation in jsonData["animations"].items():
            if "deform" in animation[1]:
                animation[1]["ffd"] = animation[1].pop("deform")

    # changes mesh type to skinned mesh
    # DragonBones doesn't distinguish mesh and skinnedmesh
    # A mesh is skinned (weighted for later version?) if the number of vertices > number of UV
    def detectSkinnedMeshes(self, jsonData):
        if "skins" in jsonData:
            if "default" in jsonData["skins"]:
                for skinName in jsonData["skins"]["default"].keys():
                    skinSubName = next(iter(jsonData["skins"]["default"][skinName]))
                    skin = jsonData["skins"]["default"][skinName][skinSubName]
                    if "type" in skin:
                        if skin["type"] == "mesh":
                            uvsCount = len(skin["uvs"])
                            verticesCount = len(skin["vertices"])
                            if verticesCount > uvsCount:
                                skin["type"] = "skinnedmesh"

    # DragonBones only include skin color if it != FFFFFFFF (opaque)
    # Because of that animations only contain information on what to make transparent
    # Example why that's no good:
    # Abomination enters combat -> beast becomes transparent
    # You activate transformation -> human becomes transparent
    # But human does not appear, because animation doesn't know it should make human visible
    def fixSeveralAnimations(self, jsonData):
        slotsArray = dict()
        for i in jsonData["animations"].keys():
            if "slots" in jsonData["animations"][i]:
                for j in jsonData["animations"][i]["slots"]:
                    if j not in slotsArray.keys():
                        slotsArray[j] = {"color": [{"color": "FFFFFFFF", "time": 0}]}
        k = 0
        for i in jsonData["animations"].keys():
            for j in slotsArray.keys():
                if "slots" in jsonData["animations"][i].keys():
                    if j not in jsonData["animations"][i]["slots"].keys():
                        jsonData["animations"][i]["slots"][j] = slotsArray[j]
            k = k + 1

    # Adds commas around word "sprite" in json, png and atlas file names
    # Because DB doesn't support commas in project name
    def rename(self, fileName):
        try:
            extensions = [".json", ".png", ".atlas"]
            oldName = os.path.basename(fileName)[:-5]
            newName = re.sub('_\d*$', '', oldName)
            if oldName.find(".sprite.") == -1:
                newName = newName.replace("sprite", ".sprite.")
                if newName.startswith(".sprite."):
                    newName = "class" + newName
            folderPath = os.path.dirname(fileName)
            fileName = folderPath + os.path.sep + newName + ".json"
            for foundName in os.listdir(folderPath):
                foundFileName, foundFileExtension = os.path.splitext(foundName)
                if foundFileName == oldName and foundFileExtension in extensions:
                    if foundFileExtension == ".atlas":
                        file = open(folderPath + os.path.sep + foundName, "r+")
                        text = file.read()
                        text = text.replace(oldName, newName)
                        file.seek(0)
                        file.write(text)
                        file.truncate()
                        file.close()
                    os.rename(folderPath + os.path.sep + foundName,
                              folderPath + os.path.sep + newName + foundFileExtension)
        except Exception:
            print("Error while trying to rename file, consider turning it of in settings.json")
            raise
        return fileName

    # DragonBones doesn't include empty animations
    # (no translation, rotation, scaling, changing color)
    # adds animation based on fileName if the animation is missing
    def addEmptyAnimations(self, jsonData, fileName):
        searchResult = re.search("sprite\.?(.*).json", fileName)
        if searchResult == None:
            print("File is poorly named, name should look like \"%className%.sprite.%animationName%\"")
            return

        type = searchResult.group(1)
        types = [type]
        if type == "defend":
            types.append("death")

        for j in types:
            if j not in jsonData["animations"].keys():
                jsonData["animations"][j] = {};

    # Game's skel files doesn't contain edges, width and height information for meshes
    # Width and height can be retrieved from atlas file
    # Edges can easily be generated from hull size
    def fixMeshes(self, jsonData, fileName):
        try:
            atlas = readAtlasFile(fileName.replace(".json", ".atlas"))
            for i in range(0, len(atlas)):
                if "regionSections" in atlas[i].keys():
                    atlasSections = atlas[i]["regionSections"]
        except:
            print("Coulnd't find assosiated .atlas file")
            raise

        for skinName in jsonData["skins"]["default"]:
            skinSubName =  next(iter(jsonData["skins"]["default"][skinName]))
            skin = jsonData["skins"]["default"][skinName][skinSubName]
            if "type" in skin:
                if skin["type"] in ["skinnedmesh", "mesh"]:
                    verticesCount = skin["hull"]

                    atlasNameToFind = skinSubName
                    if "path" in skin:
                        atlasNameToFind = skin["path"]
                    print("Same skin is used for 2+ slots, use Replace Image button in DragonBones")

                    atlasRegion = next(item for item in atlasSections if item["name"] == atlasNameToFind)
                    skin["width"] = atlasRegion["width"]
                    skin["height"] = atlasRegion["height"]

                    skin["edges"] = list()
                    skin["edges"].append(0)
                    skin["edges"].append(verticesCount - 1)
                    for i in range (0, verticesCount - 1):
                        skin["edges"].append(i)
                        skin["edges"].append(i+1)
                    for i in range (0, len(skin["edges"])):
                        skin["edges"][i] = skin["edges"][i]*2

    # Shear isn't supported in original SpineConverter  (and Spine 2.1.27 too?)
    # So we just delete it, otherwise rotation breaks
    def removeShear(self, jsonData):
        for animation in jsonData["animations"].items():
            if "bones" in animation[1].keys():
                for bone in animation[1]["bones"].items():
                    if "shear" in bone[1].keys():
                        bone[1].pop("shear")