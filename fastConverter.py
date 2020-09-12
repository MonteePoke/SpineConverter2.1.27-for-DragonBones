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

if len(args) == 0:
    args = [settings.getFilePath()]
    if args[0] == "" or not os.path.isfile(args[0]):
        print("File path empty or file doesn't exist\n"+
              "Edit \"filepath\" line in settings.json to choose a file\n"+
              "To copy file path:\n"+
              "Windows: right click on file while holding shift, press \"Copy as File\""+
              "Mac: while in right click menu holw down Option key, press \"Copy X as Pathname\"")
        input("Press enter to close")
        args = []

for arg in args:
    try:
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
    except Exception:
        traceback.print_exc()
        input("Press enter to close")
