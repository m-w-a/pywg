#! /usr/bin/env python3.2

# This test should only be run as an executable.
if __name__ == '__main__':

    _Exception = None
    try:
        def scriptBroadcaster(scriptListner):
            scriptListner()

        from ExecutingScript import *
        ExecutingScript.init('initThrowDueToReinitialization')
        ExecutingScript.init('initThrowDueToReinitialization')

    # Catch all exceptions, and test for specific kind later.
    except Exception as ex:
        _Exception = ex

    import unittest

    class Test_initThrowDueToReinitialization(unittest.TestCase):
        def test(self):
            with self.assertRaises(ExecutingScript.AlreadyInitializedError):
                if(_Exception is not None):
                    raise _Exception

    import sys
    unittest.main(argv=[ sys.argv[0] ])