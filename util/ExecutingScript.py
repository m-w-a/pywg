#! /usr/bin/env python3.2

import sys
import os
import builtins
import types

class ExecutingScript:
    """
    Utility class to aid in retrieving info about the executing python script,
    aka, the "script".

    Use of this class requires that the executing script have the following
    function:

      def scriptBroadcaster(scriptListner):
          scriptListner()

    Use of this script requires the executing script:
      1) Have this module as its first import.
      2) Immediately after importing this module, to call this class's init 
         function.
    """

    __DidInit = False
    __ScriptModuleProper = None
    __ExecutingScriptModule = None
    __ScriptDir = None
    __RequiredScriptBroadCasterFuncName = 'scriptBroadcaster'

    class UninitializedError(Exception): pass
    class RequirementUnsatisfiedError(Exception): pass

    @classmethod
    def init(cls, scriptNameAsModule : str) -> None:
        """
        Class initializer.

        scriptNameAsModule:
          The executing script's module name. Note, this is the variable with 
          the same name as the scripts' filename minus the file extension, and
          is NOT the same thing as the variable __name__, since most likely 
          __name__ == '__main__'.

        Throws:
          RequirementUnsatisfiedError:
            If __main__ module is missing the function scriptBroadcaster, as
            described in this class's documentation.

        This should be the first function called in the executing script.
        """

        def verifyMainModuleHasRequiredAttributes() -> None:
            mainModule = sys.modules['__main__']
            requiredAttr = \
              getattr(
                mainModule, 
                cls.__RequiredScriptBroadCasterFuncName,
                mainModule)
            if requiredAttr is not mainModule:
                if builtins.type(requiredAttr) is not types.FunctionType:
                    errMsg = \
                      "__main__ module attribute: '{0}' must be of "\
                      "type function".format(__RequiredScriptBroadCasterFuncName)
                    raise cls.RequirementUnsatisfiedError(errMsg)
            else:
                errMsg = \
                  '__main__ module missing the following attributes: {0}'\
                  .format(cls.__RequiredScriptBroadCasterFuncName)
                raise cls.RequirementUnsatisfiedError(errMsg)

        verifyMainModuleHasRequiredAttributes()

        cls.__ScriptModuleProper = sys.modules.get(scriptNameAsModule)
        cls.__ExecutingScriptModule = sys.modules['__main__']
        cls.__ScriptDir = cls.__tryGettingDir()
        cls.__DidInit = False

    @classmethod
    def getPossibleDir(cls) -> os.path or None:
        """
        Try getting the script directory, taking into account all corner cases.

        scriptNameAttr:
          The executing scripts __name__ attribute.

        Returns:
          None if unable to get the executing scripts directory, else
          An absolute path that may or may NOT be the scripts directory (for the
          reasons why, consult "The Algorithm" section below).

        Throws:
          UninitializedError

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
        Else, try the module script's __file__.
          (Note, this presupposes that the script itself has been loaded as a
          module.)
          Note, this may return a false path in Windows if os.chdir() has been 
          previously executed.
        Else, try the executing script's __file__.
          Note, this may fail since in interactive mode the __file__ will not
          exist for the script run from the prompt.
          Note, this may return a false path in Windows if os.chdir() has been 
          previously executed.
        """

        cls.__VerifyInitialization()
        return cls.__ScriptDir

    @classmethod
    def __tryGettingDir(cls) -> os.path or None:

        def ifFrozenThenGetScriptDir() ->  os.path or None:
            def isAppFrozen():
                """Return ``True`` if we're running from a frozen program."""

                import imp

                # new py2exe | # tools/freeze
                return (
                    (getattr(sys, "frozen", sys) is not sys) or 
                    (imp.PY_FROZEN == imp.find_module('__main__')) )

            # If App frozen then script dir is same as python executable dir.
            if isAppFrozen() and sys.executable:
                return os.path.abspath(os.path.dirname(sys.executable))

            return None

        def tryGettingScriptDirFromCallStack() -> os.path or None:

            scriptDir = None

            def scriptListner() -> os.path or None:
                try:
                    import inspect

                    frame = inspect.stack()[1]

                    if frame is not None:
                        # The script module should be the only one calling this
                        # function, so the calling the frame should contain
                        # the correct filepath of the script.
                        nonlocal scriptDir
                        scriptDir = \
                          os.path.abspath(os.path.dirname(frame[1]))

                finally:
                    del inspect
                    # Always delete frames when done with them.
                    del frame

            cls.__ExecutingScriptModule.scriptBroadcaster(scriptListner)
            return scriptDir

        def tryGettingScriptDirFromSysArgv() -> os.path or None:
            scriptDirStr = sys.argv[0]
            if(scriptDirStr):
                return os.path.abspath(os.path.dirname(scriptDirStr))
            else:
                return None

        def tryGettingScriptDirFromScriptModuleProperFileAttr() \
          -> os.path or None:

            if cls.__ScriptModuleProper is not None:
                return os.path.abspath(
                  os.path.dirname(
                    cls.__ScriptModuleProper.__file__))

            return None

        def tryGettingScriptDirFromExecutingScriptFileAttr() -> os.path or None:
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
            toRet = tryGettingScriptDirFromScriptModuleProperFileAttr()
        if toRet is None:
            toRet = tryGettingScriptDirFromExecutingScriptFileAttr()

        return toRet

    @classmethod
    def __VerifyInitialization(cls):
        if not cls.__DidInit:
            raise UninitializedError()