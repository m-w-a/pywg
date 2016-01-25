#! /usr/bin/env python3.2

import unittest
import sys
import os.path
import argparse

# import util.ExecutingScript
# top_level_dir=util.ExecutingScript.ExecutingScript.getPossibleDir()

_UnittestPattern="*_PyUnit.py"

class _CommandLine:
    def __init__(self):
        self.__parsedCmdLine = None
    
    @property
    def getParsedValueFor(self):
        """
        If parse was called then:
          1) returns the parsed command line obj, else
          2) None.
        
        The returned object will have the following attributes:
          verbosity <int>
          paths <string(s) denoting unittest files or directories.>
        """
        return self.__parsedCmdLine
    
    def parse(self) -> None:
        cmdLineParser = argparse.ArgumentParser(
          description="Discover and run unit tests.");

        def addVerbosityOptionArg() -> None:
            cmdLineParser.add_argument(
              '-v',
              '--verbosity',
              nargs='?',
              default=1,
              type=int,
              choices=[0, 1, 2],
              dest='verbosity',
              help='The verbosity level to run the unittest(s) with.')

        def addPathsPositionalArg() -> None:
            class Path:
                def __new__(cls, path : str):
                    if not os.path.exists(path):
                        msg = "{0} is not accessible".format(path)
                        raise argparse.ArgumentTypeError(msg)
                    
                    return path
            
            cmdLineParser.add_argument(
              dest='paths',
              metavar='unittest-or-directory',
              type=Path,
              nargs='+', 
              help=\
                "A unit test file or a directory in which to search for unit "
                "test files.")

        addVerbosityOptionArg()
        addPathsPositionalArg()
        
        self.__parsedCmdLine = cmdLineParser.parse_args()


def _runtestApp() -> None:
    def foreachPathCombineAndRunAllUnittests(
      verbosity : int, testpaths, topLevelPackageDir : str) -> None:
        for path in testpaths:
            def getTestSuite(
              path : str, topLevelPackageDir : str) -> unittest.TestSuite:
                startDir = None
                pattern = None
                if os.path.isdir(path):
                    startDir = os.path.abspath(path)
                    pattern = _UnittestPattern

                else:
                    filepath = os.path.abspath(path)
                    startDir = os.path.dirname(path)
                    pattern = os.path.basename(path)
                
                return \
                  unittest.defaultTestLoader.discover(
                    startDir, pattern, topLevelPackageDir)
            
            def runTestSuite(
              verbosity : int, testsuite : unittest.TestSuite) -> None:
                unittest.TextTestRunner(verbosity=verbosity).run(testsuite)
            
            runTestSuite(
              verbosity, 
              getTestSuite(path, topLevelPackageDir) )

    cmdLine = _CommandLine()
    cmdLine.parse()

    # Since this script is not intended to be run in interactive mode, this 
    # should return the correct value all the time.
    topLevelPackageDir=os.path.dirname(os.path.abspath(sys.argv[0]))

    foreachPathCombineAndRunAllUnittests(
      cmdLine.getParsedValueFor.verbosity, 
      cmdLine.getParsedValueFor.paths,
      topLevelPackageDir)

if __name__ == '__main__':
    _runtestApp()