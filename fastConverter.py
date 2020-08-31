import sys, os

from spBinaryReader import spBinaryReader
from spJsonReader import spJsonReader
from spBinaryWriter import spBinaryWriter
from spJsonWriter import spJsonWriter
from settings import SpineConverterSettings
from dragonBonesFixer import DragonBonesFixer
import re
import traceback


settings = SpineConverterSettings()
args = sys.argv[1:]
dragonBonesFixer = DragonBonesFixer(settings)


for arg in args:
    try:
        if (len(sys.argv) >= 2):
            fileName = arg
            if (fileName.endswith(".skel")):
                print("Converting " + fileName.split("\\")[-1] + " into .json.")

                binaryReader = spBinaryReader()
                jsonWriter = spJsonWriter()

                skeletonData = binaryReader.readSkeletonDataFile(fileName)

                jsonWriter.writeSkeletonDataFile(skeletonData, fileName.replace(".skel", ".json"))

                dragonBonesFixer.fixSpineConverterJson(fileName.replace(".skel", ".json"))
            elif (fileName.endswith(".json")):
                print("Converting " + fileName.split("\\")[-1] + " into .skel.")

                jsonReader = spJsonReader()
                binaryWriter = spBinaryWriter()

                fileName = dragonBonesFixer.fixDragonBonesJson(fileName)

                skeletonData = jsonReader.readSkeletonDataFile(fileName)

                binaryWriter.writeSkeletonDataFile(skeletonData, fileName.replace(".json", ".skel"))
            else:
                print("Invalid file type.")
                input("Press enter to close")
        else:
            print("Required arguments not found")
            input("Press enter to close")
    except Exception:
        traceback.print_exc()
        input("Press enter to close")
