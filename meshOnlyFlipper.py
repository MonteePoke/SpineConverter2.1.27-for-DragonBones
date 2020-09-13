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

        for skinName in jsonData["skins"]["default"]:
            skinSubName = next(iter(jsonData["skins"]["default"][skinName]))
            skin = jsonData["skins"]["default"][skinName][skinSubName]

            if "type" in skin:
                if skin["type"] == "mesh":
                    vertices = skin["vertices"]
                    for i in range(0, len(vertices), 2):
                        # vertices[i] = vertices[i]*-1
                        vertices[i + 1] = vertices[i + 1] * -1

        file = open(arg, 'w')
        file.write(json.dumps(jsonData, indent=2, separators=(",", ": ")))
        file.close()
    except Exception:
        traceback.print_exc()
        input("Press enter to close")