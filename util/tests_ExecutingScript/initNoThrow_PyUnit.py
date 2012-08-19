#! /usr/bin/env python3.2

_Exception = None
try:
    def scriptBroadcaster(scriptListner):
        scriptListner()

    from ExecutingScript import *
    ExecutingScript.init('initNoThrow_PyUnit')

except Exception as ex:
    _Exception = ex

import unittest

class Test_initNoThrow(unittest.TestCase):
    def test(self):
        if _Exception is not None:
            raise _Exception

if __name__ == '__main__':
    import sys
    unittest.main(argv=[sys.argv[0]])