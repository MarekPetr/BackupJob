#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import zipLogs
import os
from ziplogs import zip_logs
import unittest
from unittest import TestCase
from testfixtures import TempDirectory



zipper = logZipper()


class SuffixNumberTest(TestCase):
    filename = 'file'
    
    def test_add_suffix(self):
        filenames = ['file.1.gz']
        filename_suffix = zipper._suffix_number(self.filename, filenames)
        assert(filename_suffix == 'file.0')

    def test_skip_num(self):
        filenames = ['file.0.gz']
        filename_suffix = zipper._suffix_number(self.filename, filenames)
        assert(filename_suffix == 'file.1')

    def test_skip_two_nums(self):
        filenames = ['file.0.gz', 'file.1.gz']
        filename_suffix = zipper._suffix_number(self.filename, filenames)
        assert(filename_suffix == 'file.2')

    def test_num_between(self):
        filenames = ['file.0.gz', 'file.2.gz']
        filename_suffix = zipper._suffix_number(self.filename, filenames)
        assert(filename_suffix == 'file.1')

    def test_double_suffix(self):
        filename = 'file.0'
        filenames = ['file.0.gz']
        filename_suffix = zipper._suffix_number(filename, filenames)
        assert(filename_suffix == 'file.0.0')


class ZipLogsTest(TestCase):
    def test_zip_file(self):
        with TempDirectory() as td:
            td.write('test.log', b'some foo thing')
            zipper.zip_logs(td.path, True)
            td.compare(['test.log.0.gz'])

    def test_zip_subfolder(self):
        with TempDirectory() as td:
            td.makedir('log')
            td.write('log/test.log', b'some foo thing')

            zipper.zip_logs(td.path, True)
            td.compare([
                'log/test.log.0.gz'
                ], files_only=True)

    def test_multiple_renames(self):
        with TempDirectory() as td:
            td.write('log/test.log', b'some foo thing')

if __name__ == '__main__':
    unittest.main()