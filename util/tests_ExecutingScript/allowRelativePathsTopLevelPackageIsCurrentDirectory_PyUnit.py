#! /usr/bin/env python3.2

# This test should only be run as an executable.
if __name__ == '__main__':
    from ExecutingScript import *
    ExecutingScript.allowRelativePaths('.')

    from .DummyModuleForImportTest_1 import *

    import unittest

    class Test_allowRelativePaths(unittest.TestCase):
        def test(self):
            pass

    if __name__ == '__main__':
        import sys
        unittest.main(argv=[sys.argv[0]])