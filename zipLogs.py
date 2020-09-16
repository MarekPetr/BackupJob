#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import mimetypes
import re
import gzip
import shutil
from pathlib import Path


def zipLogs(logDir="/var/log"):
    '''Compress log files to Zip in their directory

    '''
    if not os.path.isdir(logDir):
        print("No " + logDir + " directory found")
        return

    zipExt = ".gz"

    # Repeats for every subdirectory (dirPath)
    # So filenames can be the same in different subdirectories
    for dirPath, dirNames, fileNames in os.walk(logDir):
        for file in fileNames:
            # skip symlinks
            if os.path.islink(os.path.join(dirPath, file)):
                continue

            # check for regular file (not compressed)
            mime = mimetypes.guess_type(file,strict=False)
            if str(mime[1]) == "None":                

                filePath= os.path.join(dirPath, file)
                if not os.path.isfile(filePath):
                    continue

                futZipName = file + zipExt
                futFileName = file
                isSuffixNum = False
                num = 0
               
                # suffix ordinal number to files
                # increment it if future zip name is already in the directory
                while True:
                    if isSuffixNum:
                        futFileName = re.sub(r'\d+$',str(num), futFileName)
                    else:
                        futFileName += "." + str(num)
                        isSuffixNum = True

                    futZipName = futFileName + zipExt
                    if futZipName not in fileNames:
                        break

                    num += 1

                # rename file to match Zipped file name
                futFilePath = os.path.join(dirPath, futFileName)
                if filePath != futFilePath:
                    os.replace(filePath, futFilePath) # rename file
                    filePath = futFilePath

                # compress the file
                futZipPath = os.path.join(dirPath, futZipName)
                with open(filePath, 'rb') as f_in:
                    with gzip.open(futZipPath, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # remove it to make space for another version
                os.remove(filePath)


if __name__ == '__main__':
    zipLogs()