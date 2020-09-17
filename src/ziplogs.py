#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import mimetypes
import re
import gzip
import shutil
import argparse
from pathlib import Path

DEFAULT_LOG_DIR = "/var/log"

class logZipper:
    _zip_ext = ".gz"

    def _suffix_number(self, filename, filenames):
        is_suffix = False
        num = 0
        filename_suffix = filename
        # suffix ordinal number to files
        # increment it if new zip name is already in the directory
        while True:
            if is_suffix:
                # increment the suffix number
                filename_suffix = re.sub(r'\d+$',str(num), filename_suffix)
            else:
                filename_suffix += "." + str(num)
                is_suffix = True

            zipNameSuffix = filename_suffix + self._zip_ext
            if zipNameSuffix not in filenames:
                break

            num += 1

        return filename_suffix

    def _rename_file(self, filepath, new_filepath):    
        if filepath != new_filepath:
            os.replace(filepath, new_filepath) # rename file
        return new_filepath

    def _gzip_file(self, filepath, zip_path):
        with open(filepath, 'rb') as f_in:
            with gzip.open(zip_path, 'wb') as f_out:
               shutil.copyfileobj(f_in, f_out)

        # remove it to make space for another version
        if os.path.isfile(filepath):
            os.remove(filepath)

    def _is_regular_file(self, filepath):
        mime = mimetypes.guess_type(filepath,strict=False)
        if str(mime[1]) == "None":
            return True
        return False


    def _print_stats(self, zipped_cnt):
        if zipped_cnt == 1:
            print("1 file compressed")
        else:
            print(str(zipped_cnt) + " files compressed")


    def zip_logs(self, log_dir=DEFAULT_LOG_DIR, silent=False):
        '''Compress log files in the log_dir directory tree

        '''
        zipped_cnt = 0
        if not os.path.isdir(log_dir):
            print("No directory at '" + log_dir + "' found")
            return

        # Repeats for every subdirectory (dirpath),
        # so filenames can be the same in different subdirectories
        for dirpath, dirnames, filenames in os.walk(log_dir):
            for filename in filenames:
                filepath= os.path.join(dirpath, filename)
                # skip symlinks
                if os.path.islink(filepath):
                    continue
                
                if self._is_regular_file(filepath):
                    if not os.path.isfile(filepath):
                        continue

                    newFileName = self._suffix_number(filename, filenames)
                    # rename file to match the new zipped file name
                    new_filepath = os.path.join(dirpath, newFileName)
                    new_filepath = self._rename_file(filepath, new_filepath)

                    # compress the file
                    zip_path = new_filepath + self._zip_ext
                    self._gzip_file(new_filepath, zip_path)
                    zipped_cnt += 1

        if not silent:
            self._print_stats(zipped_cnt)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dir', dest='log_dir', default=DEFAULT_LOG_DIR,
        help='logs root directory')

    parser.add_argument('-s', '--silent', action='store_true',
        default=False, help='Display no output')

    args = parser.parse_args()

    log_zipper = logZipper()
    log_zipper.zip_logs(args.log_dir, args.silent)