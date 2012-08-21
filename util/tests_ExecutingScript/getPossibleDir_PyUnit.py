#! /usr/bin/env python3.2

# This test should only be run as an executable.
if __name__ == '__main__':

    def scriptBroadcaster(scriptListner):
        scriptListner()

    from ExecutingScript import *
    ExecutingScript.init('getPossibleDir_PyUnit')

    import unittest
    import sys

    class Test_getPossibleDir(unittest.TestCase):
        def test(self):
            expectedExecutingScriptDir = sys.argv[1]
            self.assertEqual(
              expectedExecutingScriptDir,
              ExecutingScript.getPossibleDir())

    unittest.main(argv=[ sys.argv[0] ])