#!/usr/bin/env python
#
# tests.py

import sys
import unittest

import conda_api

from utils import get_root_prefix

def print_basic_info():
    print('sys.version: {}'.format(sys.version.replace('\n', ' ')))
    print('sys.executable: {}\n'.format(sys.executable))

class UtilsTestCase(unittest.TestCase):

    def test_get_root_prefix_returns_correct_value(self):
        self.assertEqual(get_root_prefix(), '/home/josh/miniconda')
        
    def test_ROOT_PREFIX_gets_set_correctly(self):
        conda_api.set_root_prefix(get_root_prefix())
        self.assertEqual(conda_api.ROOT_PREFIX, '/home/josh/miniconda')

if __name__ == '__main__':
    print_basic_info()
    unittest.main(verbosity=2)
