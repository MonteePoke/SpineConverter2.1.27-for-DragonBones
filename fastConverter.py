import sys, os

from spBinaryReader import spBinaryReader
from spJsonReader import spJsonReader
from spBinaryWriter import spBinaryWriter
from spJsonWriter import spJsonWriter
from settings import SpineConverterSettings
import scriptUtils
import re
import traceback

settings = SpineConverterSettings()
args = sys.argv[1:]

for arg in args:
    try:
        if (len(sys.argv) >= 2):
            fileName = arg
            if (fileName.endswith(".skel")):
                print("Converting " + fileName.split("\\")[-1] + " into .json.")

                binaryReader = spBinaryReader()
                jsonWriter = spJsonWriter()

                skeletonData = binaryReader.readSkeletonDataFile(fileName)

                if settings.isFixMeshes():
                    scriptUtils.fixMeshes(skeletonData, fileName)

                jsonWriter.writeSkeletonDataFile(skeletonData, fileName.replace(".skel", ".json"))
            elif (fileName.endswith(".json")):
                print("Converting " + fileName.split("\\")[-1] + " into .skel.")

                jsonReader = spJsonReader()
                binaryWriter = spBinaryWriter()

                skeletonData = jsonReader.readSkeletonDataFile(fileName, settings)

                if settings.isAutoRenameOn(): # DragonBones
                    try:
                        extensions = [".json", ".png", ".atlas"]
                        oldName =  os.path.basename(fileName)[:-5]
                        newName = re.sub('_\d*$', '', oldName.replace("sprite", ".sprite."))
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
                                os.rename(folderPath + os.path.sep + foundName, folderPath + os.path.sep + newName + foundFileExtension)
                    except Exception:
                        print("Error while trying to rename file, consider turning it of in settings.json")
                        raise

                if (settings.isAddEmptyAnimationsOn()): # DragonBones
                    scriptUtils.addEmptyAnimations(skeletonData, fileName)

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
