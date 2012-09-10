import unittest
import builtins
from .. import *

class Test_StaticVariableCreationAndAssignment(unittest.TestCase):
    def test_functionStaticVariables(self) -> None:
        def foo() -> None:
            static = StaticInitor(foo)
            static.Var1 = lambda: var1Value

        var1Value = 'StaticVar_1'

        foo()
        self.assertTrue(builtins.hasattr(foo, 'Var1'))
        self.assertEqual(foo.Var1, var1Value)

    def test_methodStaticVariables(self) -> None:
        class Bar:
            def foo(self):
                static = StaticInitor(Bar.foo)
                static.Var1 = lambda: var1Value
                static.Var2 = lambda: var2Value

        var1Value = 'StaticVar_1'
        var2Value = 10

        Bar().foo()

        self.assertTrue(builtins.hasattr(Bar.foo, 'Var1'))
        self.assertTrue(builtins.hasattr(Bar.foo, 'Var2'))

        self.assertEqual(Bar.foo.Var1, var1Value)
        self.assertEqual(Bar.foo.Var2, var2Value)

class Test_GettingAttributesRaisesError(unittest.TestCase):

    __ErrMsgSubStr = 'Illegal operation.'

    def test_functionStaticVariables(self) -> None:
        def foo() -> None:
            static = StaticInitor(foo)
            static.Var1 = lambda: '1'

            ref = static.Var1

        cls = self.__class__
        with self.assertRaisesRegex(TypeError, cls.__ErrMsgSubStr):
            foo()

    def test_methodStaticVariables(self) -> None:
        class Bar:
            def foo(self):
                static = StaticInitor(Bar.foo)
                static.Var1 = lambda: 1

                ref = static.Var1

        cls = self.__class__
        with self.assertRaisesRegex(TypeError, cls.__ErrMsgSubStr):
            Bar().foo()

class Test_DeletingAttributesRaisesError(unittest.TestCase):
    __ErrMsgSubStr = 'Illegal operation.'

    def test_functionStaticVariables(self) -> None:
        def foo() -> None:
            static = StaticInitor(foo)
            static.Var1 = lambda: '1'

            del static.Var1

        cls = self.__class__
        with self.assertRaisesRegex(TypeError, cls.__ErrMsgSubStr):
            foo()

    def test_methodStaticVariables(self) -> None:
        class Bar:
            def foo(self):
                static = StaticInitor(Bar.foo)
                static.Var1 = lambda: 1

                del static.Var1

        cls = self.__class__
        with self.assertRaisesRegex(TypeError, cls.__ErrMsgSubStr):
            Bar().foo()

class Test_StaticVariablesBehaveStatically(unittest.TestCase):
    def test_functionStaticVariables(self) -> None:
        def foo() -> int:
            static = StaticInitor(foo)
            static.Var1 = lambda: 0

            foo.Var1 += 1
            return foo.Var1

        self.assertEqual(foo(), 1)
        self.assertEqual(foo(), 2)

    def test_methodStaticVariables(self) -> None:
        class Bar:
            def foo(self) -> int:
                static = StaticInitor(Bar.foo)
                static.Var1 = lambda: 0

                Bar.foo.Var1 += 1
                return Bar.foo.Var1

        self.assertEqual(Bar().foo(), 1)
        self.assertEqual(Bar().foo(), 2)

class Test_StaticVariableReinitializationSilentlyFails(unittest.TestCase):
    def test_functionStaticVariables(self) -> None:
        def foo():
            static = StaticInitor(foo)
            static.Var1 = lambda: 0
            static.Var1 = lambda: '0'

            return foo.Var1

        self.assertEqual(foo(), 0)
        self.assertEqual(foo(), 0)

    def test_methodStaticVariables(self) -> None:
        class Bar:
            def foo(self):
                static = StaticInitor(Bar.foo)
                static.Var1 = lambda: 0
                static.Var1 = lambda: '0'

                return Bar.foo.Var1

        self.assertEqual(Bar().foo(), 0)
        self.assertEqual(Bar().foo(), 0)

if __name__ == '__main__':
    unittest.main()
