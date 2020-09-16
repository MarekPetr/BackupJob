#!/usr/bin/env python3

import os, tarfile, mimetypes, re, gzip, shutil
from pathlib import Path


def gzipLogs(logDir="/var/log"):
    if not os.path.isdir(logDir):
        print("No " + logDir + " directory found")
        return

    archExtens = ".gz"

    # Repeats for every subdirectory (dirPath)
    # So filenames can be the same in different subdirectories
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
               
                firstRun = True
                 # add number if neccessary or increment it
                # if future archive name is already in the directory
                while futArchName in fileNames:
                    if isSuffixNum:
                        futFileName = re.sub(r'\d+$',str(num), futFileName)
                    elif not firstRun:
                        futFileName += "." + str(num)
                        isSuffixNum = True

                    futArchName = futFileName + archExtens                    

                    if isSuffixNum:
                        num += 1
                    firstRun = False

                #rename archived file if the archive will be renamed
                futFilePath = os.path.join(dirPath, futFileName)                
                if filePath != futFilePath:
                    os.replace(filePath, futFilePath) # rename file
                    filePath = futFilePath

                #compress the file
                futArchPath = os.path.join(dirPath, futArchName)
                with open(filePath, 'rb') as f_in:
                    with gzip.open(futArchPath, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                #remove it to make space for another version
                os.remove(filePath)

#TODO delete test/log
gzipLogs("test/log")