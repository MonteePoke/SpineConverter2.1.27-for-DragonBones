import sys, os

from spBinaryReader import spBinaryReader
from spJsonReader import spJsonReader
from spBinaryWriter import spBinaryWriter
from spJsonWriter import spJsonWriter
from settings import SpineConverterSettings
import traceback

try:
    settings = SpineConverterSettings()
    if (len(sys.argv) >= 2):
        fileName = sys.argv[1]
        if (fileName.endswith(".skel")): 
            print("Converting " + fileName.split("\\")[-1] + " into .json.")

            binaryReader = spBinaryReader()
            jsonWriter = spJsonWriter()

            skeletonData = binaryReader.readSkeletonDataFile(fileName)
            jsonWriter.writeSkeletonDataFile(skeletonData, fileName.replace(".skel", ".json"))
        elif (fileName.endswith(".json")):
            print("Converting " + fileName.split("\\")[-1] + " into .skel.")

            jsonReader = spJsonReader()
            binaryWriter = spBinaryWriter()

            skeletonData = jsonReader.readSkeletonDataFile(fileName, settings)

            if settings.isAutoRenameOn(): # DragonBones
                try:
                    extensions = [".json", ".png", ".atlas"]
                    oldName = os.path.basename(fileName).strip(".json")
                    newName = oldName.replace("sprite", ".sprite.")
                    folderPath = os.path.dirname(fileName)
                    fileName = fileName.replace("sprite", ".sprite.")
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
                    pass

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
