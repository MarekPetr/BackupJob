#!/usr/bin/env python3

import os, tarfile, mimetypes
from pathlib import Path

# Gets a directory path
# e.g. filePath /var/log/file returns /var/log dirPath
def getDirPath(filePath):
    path = Path(filePath)
    dirPathTuple = path.parts[:-1] # get a tuple of a dir path
    dirPath = os.path.join(*dirPathTuple) #join paths to string
    return dirPath

def isDuplicitArchive(futureArchivName, filePath):    
    fileDir = getDirPath(filePath)
    files = [f for f in os.listdir(fileDir)]

    #TODO rewrite to filter: filtered_numbers = [num for num in nums if num < 3]
    #archiveFiles = [file for file in files if mimetypes.guess_type(file,strict=False)[1] == 'None']
    print(files)
    #print(archiveFiles)
    #print(os.listdir(fileDir))
    for file in files:
        fileName = file + ".gz"
        #if futureArchivName == fileName:
            #print(futureArchivName + "==" + fileName)


# TODO: Ordinal number for fileName.gz files when the same log file appears again
# - do not overwrite it, create new fileName[i].gz file
def tardir():
    dest = "test/log"

    for root, dirs, files in os.walk(dest):
        for file in files:
            mime = mimetypes.guess_type(file,strict=False)
            if str(mime[1]) == "None":
                filePath= os.path.join(root, file)
                futureArchivName = file + ".gz"
                isDuplicitArchive(futureArchivName, filePath)

                #with tarfile.open(filePath + ".gz", "w:gz") as tar_handle:
                    #print(filePath)
                    #print(fileName)
                    
                    #tar_handle.add(filePath, recursive=False)

tardir()