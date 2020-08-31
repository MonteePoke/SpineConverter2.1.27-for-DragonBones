import re
import spUtils
import json
import os
from spAtlas import *

class DragonBonesFixer:
    def __init__(self, settings):
        self.settings = settings

    def fixDragonBonesJson(self, fileName):
        file = open(fileName, 'r')
        jsonData = json.loads(file.read())
        file.close()

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

        file = open( fileName, 'w' )
        file.write( json.dumps(jsonData) )
        file.close()

        return fileName

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

    def replaceDeformToFFD(self, jsonData):
        for animation in jsonData["animations"].items():
            if "deform" in animation[1]:
                animation[1]["ffd"] = animation[1].pop("deform")

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

    def rename(self, fileName):
        try:
            extensions = [".json", ".png", ".atlas"]
            oldName = os.path.basename(fileName)[:-5]
            newName = re.sub('_\d*$', '', oldName)
            if oldName.find(".sprite.") == -1:
                newName = newName.replace("sprite", ".sprite.")
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

    def addEmptyAnimations(self, jsonData, fileName):
        type = re.search("sprite\.?(.*).json", fileName).group(1)
        types = [type]
        if type == "defend":
            types.append("death")

        for j in types:
            if j not in jsonData["animations"].keys():
                jsonData["animations"][j] = {};


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

                    atlasRegion = next(item for item in atlasSections if item["name"] == skinName)
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

    def removeShear(self, jsonData):
        for animation in jsonData["animations"].items():
            if "bones" in animation[1].keys():
                for bone in animation[1]["bones"].items():
                    if "shear" in bone[1].keys():
                        bone[1].pop("shear")

# def _areNeighbors_(a, b, size) -> bool:
#     return abs(a - b) == 1 or abs(a - b) == size - 1
    # types = [
    #     {"name": "afflicted",
    #      "animations": ["afflicted"]},
    #     {"name": "camp",
    #      "animations": ["camp"]},
    #     {"name": "combat",
    #      "animations": ["combat"]},
    #     {"name": "defend",
    #      "animations": ["death", "defend"]},
    #     {"name": "heroic",
    #      "animations": ["heroic"]},
    #     {"name": "idle",
    #      "animations": ["idle"]},
    #     {"name": "investigate",
    #      "animations": ["investigate"]},
    #     {"name": "walk",
    #      "animations": ["walk"]}
    # ]

    ### Useless code ###
    # triangleCount = len(attachment["triangles"])
    # pairs = set()
    # for triangle in range(0, triangleCount, 3):
    #     vertex1 = attachment["triangles"][triangle]
    #     vertex2 = attachment["triangles"][triangle + 1]
    #     vertex3 = attachment["triangles"][triangle + 2]
    #     if not _areNeighbors_(vertex1, vertex2, verticesCount):
    #         pairs.add((vertex1*2, vertex2*2))
    #     if not _areNeighbors_(vertex2, vertex3, verticesCount):
    #         pairs.add((vertex2*2, vertex3*2))
    #     if not _areNeighbors_(vertex1, vertex3, verticesCount):
    #         pairs.add((vertex1*2, vertex3*2))
    # if attachment["placeholderName"] == "feather03":
    #     print("ya")
    # # remove reverse duplicate pairs
    # pairs = {tuple(sorted(item)) for item in pairs}
    # # sort set of tuples
    # pairs = sorted(pairs, key=lambda tup: (tup[0], tup[1]))
    # # set of tuples to list
    # attachment["edges"] = [item for t in pairs for item in t]

# DragonBones start
# if "edges" in mesh.keys():
#     if ( len( mesh["edges"] ) > 0 ):
#         jsonAttachment[placeholderName]["edges"] = mesh["edges"]
# if "width" in mesh.keys():
#     if ( mesh["width"] > 0 ):
#         jsonAttachment[placeholderName]["width"] = mesh["width"]
# if "height" in mesh.keys():
#     if ( mesh["height"] > 0 ):
#         jsonAttachment[placeholderName]["height"] = mesh["height"]
# DragonBones end