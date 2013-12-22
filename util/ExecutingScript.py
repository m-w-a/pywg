#! /usr/bin/env python3.2

import sys
import os
import builtins
import types
import functools as ft

class _OnImport:
    __Initors = []

    @classmethod
    def addInitor(cls, initor) -> None:
        cls.__Initors.append(initor)
        return None

    @classmethod
    def initAll(cls) -> None:
        for initor in cls.__Initors:
            initor()

        return None

class ExecutingScript:
    """
    Utility class to aid the use of the currently executing python script.

    Use of this script requires the executing script to:
      1) To import this module before any other modules and before executing
         any other lines of code.
    """

    class InvalidTopLevelPackageError(Exception): pass

    @classmethod
    def getPossibleDir(cls) -> str or None:
        """
        Try getting the script directory, taking into account all corner cases.

        Returns:
          None if unable to get the executing scripts directory, else
          An absolute path that may or may NOT be the scripts directory (for the
          reasons why, consult "The Algorithm" section below).

        The Algorithm:
        --------------
        If frozen, then script filepath can only be reliably obtained via 
          sys.executable.
        Else, try obtaining script filepath via the call stack if the call stack
          is available (that's because all other methods are less reliable, 
          see other methods for more info).
        Else, try obtaining script filepath via sys.argv[0]. 
          Note, this may fail since in interactive mode sys.argv[0] will return 
          an empty string for any script run from the prompt.
        Else, try the executing script's __file__.
          Note, this may fail since in interactive mode the __file__ will not
          exist for the script run from the prompt.
          Note, this may return a false path in Windows if os.chdir() was
          executed before this class was initialized.

        Note:
          sys.path[0] is not a robust solution.  It will fail for t2.py that
          was spawned off as a subprocess of t1.py, giving the directory of
          t1.py regardless of where t2.py resides.
        """

        return cls.__Impl.getPossibleDir()

    @classmethod
    def allowRelativePaths(cls, topLevelPkgDir : str) -> None:
        """
        Allows relative imports in the executing python script.

        Requirements:
          All directories that will be relatively imported from need to be
          designated as packages by having a possibly empty __init__.py file.

          Must be called before any relative imports take place.

        topLevelPkgDir:
          Relative ancestor path to the executing script, or the current
          directory designated by '.', indicating the directory
          of the top level package that relative imports in the executing script
          should be referenced to.

        Throws:
          InvalidTopLevelPackageError
            If topLevelPkgDir is not the same directory as nor an ancestor path
            of the executing script directory, then above exception is raised.
        """
        return cls.__Impl.allowRelativePaths(topLevelPkgDir)

    class __Impl:

        __ExecutingScriptModule = None
        __PossibleScriptDir = None

        @classmethod
        def init(cls) -> None:
            """
            Should only be called once, and only when this file is imported as a
            module.
            """
            cls.__ExecutingScriptModule = sys.modules['__main__']
            cls.__PossibleScriptDir = cls.__tryGettingDir()

        @classmethod
        def getPossibleDir(cls) -> str or None:
            return cls.__PossibleScriptDir

        @classmethod
        def allowRelativePaths(cls, topLevelPkgDir : str) -> None:

            def verifyExeScriptDirIsReachableFromTopLevelPackage() -> None:
                commonPathPrefix = \
                  os.path.commonprefix(
                    [absTopLevelPkgDir, cls.__PossibleScriptDir])
                if builtins.len(commonPathPrefix) > 0 \
                  and commonPathPrefix == absTopLevelPkgDir:
                        return None
                else:
                    raise ExecutingScript.InvalidTopLevelPackageError()

            def calculateQualifiedPkgNameForExeScript() -> str:
                if mainModule.__package__ is None:
                    exeScriptPkgPathRelativeToTopLevelPkg = \
                      (cls.__PossibleScriptDir.partition(
                        os.path.dirname(
                          absTopLevelPkgDir))[2]).split(os.path.sep)

                    return \
                      '.'.join(
                        filter(
                          lambda x: x != '',
                            exeScriptPkgPathRelativeToTopLevelPkg))
                else:
                    return mainModule.__package__

            absTopLevelPkgDir = \
              os.path.abspath(
                os.path.join(
                  cls.__PossibleScriptDir,
                  topLevelPkgDir))

            mainModule = sys.modules['__main__']

            verifyExeScriptDirIsReachableFromTopLevelPackage()

            mainModule.__package__ = calculateQualifiedPkgNameForExeScript()

            absTopLevelPkgParentDir = os.path.dirname(absTopLevelPkgDir)
            if absTopLevelPkgParentDir not in sys.path:
                sys.path.insert(1, absTopLevelPkgParentDir)

            __import__(mainModule.__package__)

        @classmethod
        def __tryGettingDir(cls) -> str or None:

            def ifFrozenThenGetScriptDir() ->  str or None:
                def isAppFrozen():
                    """Return ``True`` if we're running from a frozen program."""

                    import imp

                    # new py2exe | # tools/freeze
                    return (
                        (getattr(sys, "frozen", sys) is not sys) or 
                        (imp.PY_FROZEN == imp.find_module('__main__')) )

                # If App frozen then script dir is same as python executable dir.
                if isAppFrozen() and sys.executable is not None:
                    if( builtins.len(sys.executable) == 0 ):
                        return None
                    else:
                        return sys.executable

                return None

            def tryGettingScriptDirFromCallStack() -> str or None:
                scriptDir = None
                try:
                    import inspect

                    frameStack = inspect.stack()

                    if frameStack is not None:
                        for frame in frameStack:
                            try:
                                nameAttr = '__name__'
                                if nameAttr in frame[0].f_globals:
                                    if frame[0].f_globals[nameAttr] == '__main__':
                                        scriptDir = \
                                          os.path.abspath( \
                                            os.path.dirname( \
                                              frame[1]))
                                        break
                            finally:
                                del frame
                finally:
                    del frameStack
                    del inspect

                return scriptDir

            def tryGettingScriptDirFromSysArgv() -> str or None:
                scriptDirStr = sys.argv[0]
                if( scriptDirStr is not None and
                  builtins.len(scriptDirStr) !=0 ):
                    return os.path.abspath(os.path.dirname(scriptDirStr))
                else:
                    return None

            def tryGettingScriptDirFromExecutingScriptFileAttr() \
              -> str or None:

                if getattr(
                  cls.__ExecutingScriptModule,
                  '__file__',
                  cls.__ExecutingScriptModule) \
                    is cls.__ExecutingScriptModule:

                    return None
                else:
                    return os.path.abspath(os.path.dirname(
                      cls.__ExecutingScriptModule.__file__))

            toRet = ifFrozenThenGetScriptDir()
            if toRet is None:
                toRet = tryGettingScriptDirFromCallStack()
            if toRet is None:
                toRet = tryGettingScriptDirFromSysArgv()
            if toRet is None:
                toRet = tryGettingScriptDirFromExecutingScriptFileAttr()

            return toRet

    __InitRegistration = \
      _OnImport.addInitor(ft.partial(__Impl.init))

if __name__ != '__main__':
    _OnImport.initAll()