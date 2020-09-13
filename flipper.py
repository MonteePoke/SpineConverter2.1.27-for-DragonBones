import sys
import json
import traceback

args = sys.argv[1:]

for arg in args:
    try:
        file = open(arg, 'r')
        text = file.read()
        jsonData = json.loads(text)
        file.close()

        file = open(arg.replace(".json", "_not_flipped.json"), 'w')
        file.write(text)
        file.close()

        for skinName in jsonData["skins"]["default"]:
            skinSubName = next(iter(jsonData["skins"]["default"][skinName]))
            skin = jsonData["skins"]["default"][skinName][skinSubName]
            # if "type" in skin:
            #     if skin["type"] == "skinnedmesh":
            #         continue
            if "scaleX" in skin.keys():
                skin["scaleX"] = skin["scaleX"] * -1
            else:
                skin["scaleX"] = -1

            rotation = 0
            if "rotation" in skin.keys():
                rotation = skin["rotation"]

            if rotation == 0:
                skin["rotation"] = 180
            else:
                if rotation > 0:
                    rotation = 180 - rotation
                else:
                    rotation = -180 - rotation
                skin["rotation"] = rotation

            if "y" in skin.keys():
                skin["y"] = skin["y"] * -1

            if "type" in skin:
                if skin["type"] == "skinnedmesh":
                    vertices = skin["vertices"]
                    i = 0
                    length = len(vertices)
                    while i < length:
                        boneCount = vertices[i]
                        i = i + 2
                        for j in range(0, boneCount):
                            # vertices[i] = vertices[i]*-1
                            vertices[i+1] = vertices[i+1]*-1
                            i = i + 4
                        i -= 1
                # if skin["type"] == "mesh":
                #     vertices = skin["vertices"]
                #     for i in range(0, len(vertices), 2):
                #         # vertices[i] = vertices[i]*-1
                #         vertices[i + 1] = vertices[i + 1] * -1


        for bone in jsonData["bones"]:
            if bone["name"] == "root":
                bone["rotation"] = 180
                continue

            if "y" in bone.keys():
                bone["y"] = bone["y"] * -1

            if "rotation" in bone.keys():
                bone["rotation"] = bone["rotation"] * -1
                if bone["rotation"] == 0:
                    bone["rotation"] = 180

        if "animations" in jsonData:
            for animation in jsonData["animations"].items():
                for bone in animation[1]["bones"].items():
                    if "translate" in bone[1]:
                        for i in bone[1]["translate"]:
                            if "y" in i:
                                i["y"] = i["y"] * -1
                            else:
                                i["y"] = 0
                    if "rotate" in bone[1]:
                        for i in bone[1]["rotate"]:
                            if "angle" in i:
                                i["angle"] = i["angle"] * -1

        file = open(arg, 'w')
        file.write(json.dumps(jsonData, indent=2, separators=(",", ": ")))
        file.close()
    except Exception:
        traceback.print_exc()
        input("Press enter to close")