#! /usr/bin/env python3.2

import unittest
from .. import *

class Test_noop(unittest.TestCase):
    def test_noopRuns(self):
        with noop() as obj:
            pass

if __name__ == '__main__':
    unittest.main()