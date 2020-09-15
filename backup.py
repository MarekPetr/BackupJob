#!/usr/bin/env python3

import os, tarfile, mimetypes
from pathlib import Path

# TODO: Ordinal number for fileName.gz files when the same log file appears again
# - do not overwrite it, create new fileName[i].gz file
def tardir():
    dest = "test/log"

    for root, dirs, files in os.walk(dest):
        for file in files:
            mime = mimetypes.guess_type(file,strict=False)

            if (str(mime[1]) == "None"):
                filePath= os.path.join(root, file)
                fileName = file + ".gz"

                if fileName not in files:
                    #with tarfile.open(filePath + ".gz", "w:gz") as tar_handle:
                        print(filePath)
                        #tar_handle.add(filePath, recursive=False)

tardir()