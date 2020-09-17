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
    '''Class that compresses files using zip_logs method
       at given location (default is DEFAULT_LOG_DIR)
       Compressed files are then deleted to free up space
    '''
    _zip_ext = ".gz"

    def __init__(self, args=None):
        if args == None:
            self._non_recursive = False
            self._stats = False
            self._log_dir = DEFAULT_LOG_DIR
        else:
            self._non_recursive = args.non_recursive
            self._stats = args.stats
            self._log_dir = args.log_dir


    def _suffix_number(self, filename, filenames):
        suffix_reg = r'(?<=.)\d+$'
        is_suffix = False
        num = 0
        filename_suffix = filename

        match = re.search(suffix_reg, filename)
        if match != None:
            num = int(match.group(0))
            is_suffix = True

        # suffix ordinal number to files
        # increment it if new zip name is already in the directory
        while True:
            if is_suffix:
                # increment the suffix number
                filename_suffix = re.sub(suffix_reg, str(num), filename_suffix)
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


    def run(self, log_dir=DEFAULT_LOG_DIR, stats=False, non_recursive=False):
        '''Compress log files in the _log_dir directory tree

        '''

        self._non_recursive = non_recursive
        self._stats = stats
        self._log_dir = log_dir

        zipped_cnt = 0
        if not os.path.isdir(self._log_dir):
            print("No directory at '" + self._log_dir + "' found")
            return

        # Repeats for every subdirectory (dirpath),
        # so filenames can be the same in different subdirectories
        for dirpath, dirnames, filenames in os.walk(self._log_dir):
            for filename in filenames:
                filepath= os.path.join(dirpath, filename)
                # skip symlinks
                if os.path.islink(filepath):
                    continue
                
                if self._is_regular_file(filepath):
                    if not os.path.isfile(filepath):
                        continue

                    new_file_name = self._suffix_number(filename, filenames)
                    # rename file to match the new zipped file name
                    new_filepath = os.path.join(dirpath, new_file_name)
                    new_filepath = self._rename_file(filepath, new_filepath)

                    # compress the file
                    zip_path = new_filepath + self._zip_ext
                    self._gzip_file(new_filepath, zip_path)
                    zipped_cnt += 1

            if self._non_recursive:
                break


        if self._stats:
            self._print_stats(zipped_cnt)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dir', dest='log_dir', default=DEFAULT_LOG_DIR,
        help='log files directory path')

    parser.add_argument('-s', '--stats', action='store_true',
        default=False, help='print statistics to stdout')

    parser.add_argument('-nr', '--non_recursive', action='store_true',
        default=False, help='do not compress files in subdirectories')

    args = parser.parse_args()
    logZipper(args).run()