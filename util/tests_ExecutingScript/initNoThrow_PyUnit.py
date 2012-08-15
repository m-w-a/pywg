#! /usr/bin/env python3.2

def scriptBroadcaster(scriptListner):
    scriptListner()

from ExecutingScript import *
ExecutingScript.init('initNoThrow_PyUnit')

import unittest

class Test_initNoThrow(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()