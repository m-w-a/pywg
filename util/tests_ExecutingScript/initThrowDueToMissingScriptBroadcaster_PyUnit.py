#! /usr/bin/env python3.2

_Exception = None
try:
    from ExecutingScript import *
    ExecutingScript.init('initNoThrowDueToMissingScriptBroadcaster')

except Exception as ex:
    _Exception = ex

import unittest

class Test_initThrowDueToMissingScriptBroadcaster(unittest.TestCase):
    def test(self):
        expectedErrMsgSubStr = \
          '__main__ module missing the following attributes: scriptBroadcaster'
        with self.assertRaisesRegex(
          ExecutingScript.RequirementUnsatisfiedError,
          expectedErrMsgSubStr):
            if(_Exception is not None):
                raise _Exception

if __name__ == '__main__':
    import sys

    unittest.main(argv=[ sys.argv[0] ])