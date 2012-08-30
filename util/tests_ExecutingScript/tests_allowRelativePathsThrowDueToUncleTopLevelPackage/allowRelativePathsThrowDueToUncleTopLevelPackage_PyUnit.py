#! /usr/bin/env python3.2

# This test should only be run as an executable.
if __name__ == '__main__':
    from ExecutingScript import *

    _Exception = None
    try:
        ExecutingScript.allowRelativePaths(
          '../DummyUncleTopLevelPackageForImportTest_1')
    except Exception as ex:
        _Exception = ex

    import unittest

    class Test_allowRelativePathsThrowDueToUncleTopLevelPackage(
      unittest.TestCase):

        def test(self):
            with self.assertRaises(ExecutingScript.InvalidTopLevelPackageError):
                if _Exception is not None:
                    raise _Exception

    import sys
    unittest.main(argv=[sys.argv[0]])