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

        def setup(self):
            pass

        def test_scriptInCurrentDir(self):
            cls = self.__class__

            subprocScriptDir = cls.__ThisScriptsDir
            subprocScriptName = 'getPossibleDir_PyUnit_NoAutoExecute.py'
            subprocScriptPath = \
              os.path.sep.join([subprocScriptDir, subprocScriptName])

            cmdBldr = [cls.__TestRunnerPath, cls.__PythonExe, subprocScriptPath]
            subprocRetCode = subprocess.call(cmdBldr)
            self.assertEqual(0, subprocRetCode)

        def test_scriptInSubDir(self):
            cls = self.__class__

            subprocScriptDirName = 'tests_getPossibleDirForSubprocessScript'
            subprocScriptDir = \
              os.path.sep.join([cls.__ThisScriptsDir, subprocScriptDirName])
            subprocScriptName = 'getPossibleDir_PyUnit_NoAutoExecute.py'
            subprocScriptPath = \
              os.path.sep.join([subprocScriptDir, subprocScriptName])

            cmdBldr = [cls.__TestRunnerPath, cls.__PythonExe, subprocScriptPath]
            subprocRetCode = subprocess.call(cmdBldr)
            self.assertEqual(0, subprocRetCode)

    unittest.main(argv=[ sys.argv[0] ])