#! /usr/bin/env python3.2

# This test should only be run as an executable.
if __name__ == '__main__':
    import unittest
    import sys
    import subprocess
    import os

    class Test_getPossibleDirInSubprocess(unittest.TestCase):

        __ThisScriptsDir = sys.argv[1]
        __TestRunnerName = 'runtest.sh'
        __TestRunnerPath = os.path.sep.join([__ThisScriptsDir, __TestRunnerName])
        __PythonExe = 'python3.2'
        __SubprocessScriptName = 'getPossibleDir_PyUnit.py'

        def setup(self):
            pass

        def test_scriptInCurrentDir(self):
            cls = self.__class__

            subprocScriptDir = cls.__ThisScriptsDir
            subprocScriptPath = \
              os.path.sep.join([subprocScriptDir, cls.__SubprocessScriptName])

            cmdBldr = [cls.__TestRunnerPath, cls.__PythonExe, subprocScriptPath]
            subprocRetCode = subprocess.call(cmdBldr)
            self.assertEqual(0, subprocRetCode)

    unittest.main(argv=[ sys.argv[0] ])