#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gzip
import shutil
from gziplogs import gzip_logs, _suffix_number
import unittest
from unittest import TestCase
from testfixtures import TempDirectory


class SuffixNumberTest(TestCase):
    filename = 'file'
    
    def test_add_suffix(self):
        filenames = []
        filename_suffix = _suffix_number(self.filename, filenames)
        self.assertEqual(filename_suffix,'file.0')

    def test_skip_num(self):
        filenames = ['file.0.gz']
        filename_suffix = _suffix_number(self.filename, filenames)
        self.assertEqual(filename_suffix, 'file.1')

    def test_skip_two_nums(self):
        filenames = ['file.0.gz', 'file.1.gz']
        filename_suffix = _suffix_number(self.filename, filenames)
        self.assertEqual(filename_suffix, 'file.2')

    def test_num_between(self):
        filenames = ['file.0.gz', 'file.2.gz']
        filename_suffix = _suffix_number(self.filename, filenames)
        self.assertEqual(filename_suffix, 'file.1')

    def test_occupied_suffix(self):
        filename = 'file.0'
        filenames = ['file.0.gz']
        filename_suffix = _suffix_number(filename, filenames)
        self.assertEqual(filename_suffix, 'file.1')

    def test_double_suffix(self):
        filename = 'file.1.0'
        filenames = ['file.1.0.gz']
        filename_suffix = _suffix_number(filename, filenames)
        self.assertEqual(filename_suffix, 'file.1.1')


def read_gzip(gzip_path):
    with gzip.open(gzip_path, 'rb') as f:
        file_content = f.read()
    return file_content

def get_td_zipped_twice():
    '''Zip the same filenames twice
       with different content
    '''
    td = TempDirectory()
    td.write('file.1', b'1')
    td.write('file.2', b'2')
    gzip_logs(td.path)
    td.write('file.1', b'3')
    td.write('file.2', b'4')
    gzip_logs(td.path)
    return td


class ZipLogsTest(TestCase):
    empty = b''

    def test_zip_file(self):
        with TempDirectory() as td:
            td.write('file', self.empty)
            gzip_logs(td.path)
            td.compare(['file.0.gz'])

    def test_zip_subfolder(self):
        with TempDirectory() as td:
            td.makedir('log')
            td.write('log/test', self.empty)

            gzip_logs(td.path)
            td.compare([
                'log/test.0.gz'
                ], files_only=True)

    def test_multiple_renames(self):
        with TempDirectory() as td:
            td.write('test', self.empty)
            td.write('test.0.gz', self.empty)
            td.write('test.1.gz', self.empty)

            gzip_logs(td.path)
            td.compare([
                'test.0.gz',
                'test.1.gz',
                'test.2.gz'
                ], files_only=True)

    def test_zips_in_different_folders(self):
        with TempDirectory() as td:
            td.write('test', self.empty)
            td.write('log/test', self.empty)
            gzip_logs(td.path)
            td.compare([
                'test.0.gz',
                'log/test.0.gz'
                ], files_only=True)

    def test_consecutive_zips(self):
        with TempDirectory() as td:
            td.write('file', self.empty)
            gzip_logs(td.path)
            td.write('file', self.empty)
            gzip_logs(td.path)
            td.compare([
                'file.0.gz',
                'file.1.gz'
                ], files_only=True)

    def test_non_recursive(self):
        with TempDirectory() as td:
            td.write('log/file', self.empty)
            td.write('file', self.empty)
            gzip_logs(td.path, non_recursive=True)
            td.compare([
                'log/file',
                'file.0.gz'
                ], files_only=True)

    def test_sorted_files(self):
        td = get_td_zipped_twice()

        td.compare([
            'file.1.gz',
            'file.2.gz',
            'file.3.gz',
            'file.4.gz'
            ], files_only=True)

        td.cleanup()
            

    def test_sorted_files_content(self):
        td = get_td_zipped_twice()

        gz1_cont = read_gzip(os.path.join(td.path, 'file.1.gz'))
        gz2_cont = read_gzip(os.path.join(td.path, 'file.2.gz'))
        gz3_cont = read_gzip(os.path.join(td.path, 'file.3.gz'))
        gz4_cont = read_gzip(os.path.join(td.path, 'file.4.gz'))

        td.cleanup()

        self.assertEqual(gz1_cont, b'1')
        self.assertEqual(gz2_cont, b'2')
        self.assertEqual(gz3_cont, b'3')
        self.assertEqual(gz4_cont, b'4')

if __name__ == '__main__':
    unittest.main()