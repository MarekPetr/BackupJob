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
GZIP_EXT = ".gz"

def _sort_nicely(l):
    """ Sort the given list in the way that humans expect.
        Source: https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )


def _suffix_number(filename, filenames):
    '''Return a non colliding 'filename with suffix .(int)'
       with zipped filenames
       e.g. for filenames ['file', 'file.0.gz'] and filename 'file'
            Return 'file.1'
    '''
    suffix_reg = r'(?<=\.)\d+$'
    is_suffix = False
    num = 0
    filename_suffix = filename

    # look for an existing suffix number
    match = re.search(suffix_reg, filename)
    if match != None:
        num = int(match.group(0))
        is_suffix = True

    # suffix ordinal number to files
    # increment it if new gzip name is already in the directory
    while True:
        if is_suffix:
            gzipNameSuffix = filename_suffix + GZIP_EXT
            if gzipNameSuffix not in filenames:
                break
            else:
                # increment the suffix number
                filename_suffix = re.sub(suffix_reg, str(num), filename_suffix)
                num += 1
        else:
            filename_suffix += "." + str(num)
            is_suffix = True

    return filename_suffix

def _rename_file(filepath, new_filepath):
    if filepath != new_filepath:
        os.replace(filepath, new_filepath) # rename file
    return new_filepath

def _gzip_file(filepath, gzip_path):
    with open(filepath, 'rb') as f_in:
        with gzip.open(gzip_path, 'wb') as f_out:
           shutil.copyfileobj(f_in, f_out)

    # remove it to make space for another version
    if os.path.isfile(filepath):
        os.remove(filepath)

def _is_compressed_file(filepath):
    if os.path.islink(filepath):
        return False
    if not os.path.isfile(filepath):
        return False
    # guess filetype based on file extension
    # other means have to be installed -> inconvenient
    mime = mimetypes.guess_type(filepath,strict=False)
    if str(mime[1]) == "None":
        return False
    return True

def _print_stats(gzipped_cnt):
    if gzipped_cnt == 1:
        print("1 file compressed")
    else:
        print(str(gzipped_cnt) + " files compressed")

def gzip_logs(log_dir=DEFAULT_LOG_DIR, stats=False, non_recursive=False):
    '''Compress log files in the log_dir directory tree
    '''
    gzipped_cnt = 0
    if not os.path.isdir(log_dir):
        print("No directory at '" + log_dir + "' found")
        return

    # Repeats for every subdirectory (dirpath),
    # so filenames can be the same in different subdirectories
    for dirpath, dirnames, filenames in os.walk(log_dir):
        _sort_nicely(filenames)
        for filename in filenames:
            filepath= os.path.join(dirpath, filename)            
            if _is_compressed_file(filepath):
                continue
            new_file_name = _suffix_number(filename, filenames)
            # rename file to match the new gzipped file name
            new_filepath = os.path.join(dirpath, new_file_name)
            new_filepath = _rename_file(filepath, new_filepath)

            # compress the file
            gzip_path = new_filepath + GZIP_EXT
            _gzip_file(new_filepath, gzip_path)
            filenames.append(new_file_name + GZIP_EXT)
            gzipped_cnt += 1

        if non_recursive:
            break

    if stats:
        _print_stats(gzipped_cnt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dir', dest='log_dir', default=DEFAULT_LOG_DIR,
        help='directory path of log files')
    parser.add_argument('-s', '--stats', action='store_true',
        default=False, help='print statistics to stdout')
    parser.add_argument('-nr', '--non_recursive', action='store_true',
        default=False, help='do not compress files in subdirectories')
    args = parser.parse_args()

    gzip_logs(args.log_dir, args.stats, args.non_recursive)