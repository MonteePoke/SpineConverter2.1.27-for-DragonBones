import re
import spUtils
from spAtlas import *


def addEmptyAnimations(skeletonData, fileName):
    type = re.search("sprite\.?(.*).json", fileName).group(1)
    types = [type]
    if type == "defend":
        types.push("death")

    for j in types:
        hasAnimation = False
        for i in skeletonData["animations"]:
            if i["name"] == type:
                hasAnimation = True
        if hasAnimation == False:
            skeletonData["animations"].append(
                {"name": j, "slots": list(), "bones": list(), "ik": list(), "ffd": list(), "drawOrder": list(),
                 "events": list()})


def fixMeshes(skeletonData, fileName):
    try:
        atlas = readAtlasFile(fileName.replace(".skel", ".atlas"))
        atlasSections = atlas[0]["regionSections"]
    except:
        print("Coulnd't find assosiated .atlas file")

    for slot in skeletonData["skins"][0]["slots"]:
        for attachment in slot["attachments"]:
            if attachment["attachmentType"] == spUtils.SP_ATTACHMENT_SKINNED_MESH or attachment["attachmentType"] == spUtils.SP_ATTACHMENT_MESH:
                verticesCount = attachment["hullLength"]

                atlasRegion = next(item for item in atlasSections if item["name"] == attachment["placeholderName"])
                attachment["width"] = atlasRegion["width"]
                attachment["height"] = atlasRegion["height"]

                attachment["edges"].append(0)
                attachment["edges"].append(verticesCount - 1)
                for i in range (0, verticesCount - 1):
                    attachment["edges"].append(i)
                    attachment["edges"].append(i+1)
                for i in range (0, len(attachment["edges"])):
                    attachment["edges"][i] = attachment["edges"][i]*2

def _areNeighbors_(a, b, size) -> bool:
    return abs(a - b) == 1 or abs(a - b) == size - 1

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