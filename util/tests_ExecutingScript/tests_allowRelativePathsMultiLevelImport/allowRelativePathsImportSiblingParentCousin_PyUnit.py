#! /usr/bin/env python3.2

from ExecutingScript import *
ExecutingScript.allowRelativePaths('..')

from .DummyModuleForImportTest_1 import *
from ..DummyModuleForImportTest_1 import *
from ..DummyPackageForImportTest_1 import *
from ..DummyPackageForImportTest_1.DummyModuleForImportTest_1 import *

import unittest

class Test_allowRelativePaths(unittest.TestCase):
    def test(self):
        pass

if __name__ == '__main__':
    import sys
    unittest.main(argv=[sys.argv[0]])