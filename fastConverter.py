import sys, os

from spBinaryReader import spBinaryReader
from spJsonReader import spJsonReader
from spBinaryWriter import spBinaryWriter
from spJsonWriter import spJsonWriter
import json
import logging

logger = logging.getLogger('ftpuploader')

try:
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

            skeletonData = jsonReader.readSkeletonDataFile(fileName)
            binaryWriter.writeSkeletonDataFile(skeletonData, fileName.replace(".json", ".skel"))
        else:
            print("Invalid file type.")    
    else:
        print("Required arguments not found.")
except Exception as e:
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
    logger.error('Failed to upload to ftp: '+ str(e))
    input("Press enter to close")