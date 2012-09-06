import unittest
import builtins
from .. import *

class Test_StaticVariables(unittest.TestCase):
    def test_creation(self) -> None:
        def foo() -> None:
            static = StaticProxy(foo)
            static.Var1 = lambda: 'StaticVar_1'
            pass

        foo()
        self.assertTrue(builtins.hasattr(foo, 'Var1'))

if __name__ == '__main__':
    unittest.main()
