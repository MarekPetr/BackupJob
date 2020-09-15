#!/usr/bin/env python3

import os, tarfile, mimetypes, re
from pathlib import Path


def tardir(logDir="/var/log"):
    if not os.path.isfile(logDir):
        print("No " + logDir + " directory found")
        return

    archExtens = ".gz"

    for dirPath, dirNames, fileNames in os.walk(logDir):

        for file in fileNames:
            # skip symlinks
            if os.path.islink(os.path.join(dirPath, file)):
                continue

            mime = mimetypes.guess_type(file,strict=False)
            # Is not archive
            if str(mime[1]) == "None":                
                futArchName = file + archExtens
                filePath= os.path.join(dirPath, file)                
                futFileName = file
                isSuffixNum = False
                num = 0
                # add number if neccessary or increment it
                # if future archive name is already in the directory
                firstRun = True
                for x in range(1,10):
                    if isSuffixNum:
                        futFileName = re.sub(r'\d+$',str(num), futFileName)
                    elif not firstRun:
                        futFileName += "." + str(num)
                        isSuffixNum = True

                    futArchName = futFileName + archExtens
                    
                    if futArchName not in fileNames:
                        break

                    if isSuffixNum:
                        num += 1
                    firstRun = False
                print(os.path.join(dirPath,futArchName))

                with tarfile.open(os.path.join(dirPath,futArchName), "w:gz") as tar:
                    tar.add(filePath, recursive=False)
                    os.remove(filePath)

#TODO delete test/log
tardir("test/log")