#! /usr/bin/env python3.2

from .. import Enum
import builtins
import unittest
import codeop

# R1
class Test_EnumCanOnlyInheritFromClassObject(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_okIfOnlyInheritFromObject(self) -> None:

        def testEmptyBaseClass() -> None:
            class Color(metaclass=Enum):
                pass

            class Color(metaclass=Enum):
                R = 1

            class Color(metaclass=Enum):
                R = 1
                G = 2

        def testObjectAsSoleDeclaredBaseClass() -> None:
            class Color(object, metaclass=Enum):
                pass

            class Color(object, metaclass=Enum):
                R = 1

            class Color(object, metaclass=Enum):
                R = 1
                G = 2

        testEmptyBaseClass()
        testObjectAsSoleDeclaredBaseClass()

    def test_notOkIfSoleBaseClassNotObject(self) -> None:

        expectedErrMsgSubStr = 'has base classes other than object'

        with self.assertRaisesRegex(TypeError, expectedErrMsgSubStr):
            class Color(int, metaclass=Enum):
                pass

        with self.assertRaisesRegex(TypeError, expectedErrMsgSubStr):
            class Color(float, metaclass=Enum):
                R = 1

        with self.assertRaisesRegex(TypeError, expectedErrMsgSubStr):
            class Color(Exception, metaclass=Enum):
                R = 1
                G = 2

    def test_notOkIfMultipleInherit(self) -> None:

        expectedErrMsgSubStr = 'has base classes other than object'

        with self.assertRaisesRegex(TypeError, expectedErrMsgSubStr):
            class Color(int, float, metaclass=Enum):
                pass

        with self.assertRaisesRegex(TypeError, expectedErrMsgSubStr):
            class Color(int, float, str, metaclass=Enum):
                pass

        with self.assertRaisesRegex(TypeError, expectedErrMsgSubStr):
            class Color(int, float, metaclass=Enum):
                R = 1

        with self.assertRaisesRegex(TypeError, expectedErrMsgSubStr):
            class Color(int, float, Exception, metaclass=Enum):
                R = 1
                G = 2

# R2
class Test_EnumConstantsMustBeValidPythonIdentifiers(unittest.TestCase):

    def test_okIfValidIds(self) -> None:
        class SingleLetterIds(metaclass=Enum):
            R = 1
            G = 2
            B = 3

        class IdsWithDigits(metaclass=Enum):
            Camry99 = 30
            Corolla03 = 31
            Lexus12 = 32

        class IdsWithDigitsAndUnderscores(metaclass=Enum):
            class_of_1 = 1
            ClassOf_2 = 2
            Class_Of_3 = 3

    def test_notOkIfInvalidIds(self) -> None:
        with self.assertRaises(SyntaxError):
            codeop.compile_command(
              'class Color(metaclass=Enum):'\
              '  R$ = 1')

        with self.assertRaises(SyntaxError):
            codeop.compile_command(
              'class Class(metaclass=Enum):'\
              '  1998 = 1998')

# R3
class Test_EnumConstantsMustBeOfTypeIntOrEllipsis(unittest.TestCase):

    def test_okIfOfTypeIntOrEllipsis(self) -> None:

        def testOkIfOfTypeInt() -> None:

            def testPlainNumbers() -> None:
                class MonoChrome(metaclass=Enum):
                    R = 1

                class HDTV(metaclass=Enum):
                    R = 1
                    G = 2
                    B = 3

            def testExpressions() -> None:
                class PlasmaTv(metaclass=Enum):
                    R = 1
                    G = R + 1
                    B = G + 1
                    Magenta = R * 10
                    Cyan = G + R + 5
                    Velvet = Cyan + Magenta - 1

            testPlainNumbers()
            testExpressions()

        def testOkIfOfTypeEllipsis() -> None:
            class MonoChrome(metaclass=Enum):
                R = ...

            class HDTV(metaclass=Enum):
                R = ...
                G = ...
                B = ...

        def testOkIfBothOfTypeIntOrEllipsis() -> None:
            class HDTV(metaclass=Enum):
                R = ...
                G = 1
                B = ...

            class PlasmaTv(metaclass=Enum):
                R = ...
                G = 1
                B = 11
                Magenta = ...
                Cyan = G + B
                Velvet = ...

        testOkIfOfTypeInt()
        testOkIfOfTypeEllipsis()
        testOkIfBothOfTypeIntOrEllipsis()

    def test_notOkIfNotOfTypeIntNorEllipsis(self):

        expectedErrMsgSubStr = \
          'these user declared attributes are not of type int or ellipsis:'

        def testUnmixedSingleInvalidType() -> None:

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    R = 0.0

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    R = 'Red'

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    R = []

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    R = ()

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    R = {}

        def testMixedSingleInvalidType() -> None:

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    R = 0.0
                    G = ...

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    R = 'Red'
                    G = 1

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    G = ...
                    R = []

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    G = 1
                    R = ()

            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'R'])):

                class Color(metaclass=Enum):
                    G = ...
                    R = {}
                    B = 1

        def testUnmixedMultipleInvalidTypes() -> None:
            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'AK, AR, CA, DL'])):

                class State(metaclass=Enum):
                    AK = 1.1
                    AR = []
                    CA = ()
                    DL = {}

        def testMixedMultipleInvalidTypes() -> None:
            with self.assertRaisesRegex(
              TypeError,
              ' '.join([expectedErrMsgSubStr, 'AK, CA, PA, MS'])):

                class State(metaclass=Enum):
                    AK = 1.1
                    AR = 0
                    CA = ()
                    DL = ...
                    PA = []
                    LI = AR + 10
                    MI = LI + AR
                    MS = {}

        testUnmixedSingleInvalidType()
        testMixedSingleInvalidType()
        testUnmixedMultipleInvalidTypes()
        testMixedMultipleInvalidTypes()

# R4
class Test_EnumConstantsAreOfTypeEnum(unittest.TestCase):

    def test(self) -> None:
        class Color(metaclass=Enum):
            R = ...
            G = 1
            B = G + 1
            Magenta = B + G
            Cyan = builtins.len(['Crayola'])

        self.assertIsInstance((Color.R), Color)
        self.assertIsInstance((Color.G), Color)
        self.assertIsInstance((Color.B), Color)
        self.assertIsInstance((Color.Magenta), Color)
        self.assertIsInstance((Color.Cyan), Color)

# R5
class Test_EnumConstantAttributeRelatedTests(unittest.TestCase):

    # R5.1.*
    def test_NameRelatedAttributes(self) -> None:
        class MyEnum(metaclass=Enum):
            R = ...
            Green = 10
            Camry = Green + 11
            To_Yoooota = ...

        self.assertEqual(MyEnum.R.Name, 'MyEnum.R')
        self.assertEqual(str(MyEnum.R), MyEnum.R.Name)

        self.assertEqual(MyEnum.Green.Name, 'MyEnum.Green')
        self.assertEqual(str(MyEnum.Green), MyEnum.Green.Name)

        self.assertEqual(MyEnum.Camry.Name, 'MyEnum.Camry')
        self.assertEqual(str(MyEnum.Camry), MyEnum.Camry.Name)

        self.assertEqual(MyEnum.To_Yoooota.Name, 'MyEnum.To_Yoooota')
        self.assertEqual(str(MyEnum.To_Yoooota), MyEnum.To_Yoooota.Name)

    # R5.2*
    def test_ValueRelatedAttributes(self) -> None:

        def testInitialEnumConstAssignedEllipsis() -> None:
            class PlasmaTv(metaclass=Enum):
                R = ...

            self.assertEqual(PlasmaTv.R.Value, 0)
            self.assertEqual(int(PlasmaTv.R), PlasmaTv.R.Value)

        def testInitialEnumConstNotAssignedEllipses() -> None:

            def testInitialEnumConstAssignedZero() -> None:
                class PlasmaTv(metaclass=Enum):
                    R = 0

                self.assertEqual(PlasmaTv.R.Value, 0)
                self.assertEqual(int(PlasmaTv.R), PlasmaTv.R.Value)

            def testInitialEnumConstAssignedNonZero() -> None:
                class PlasmaTv(metaclass=Enum):
                    R = 10

                self.assertEqual(PlasmaTv.R.Value, 10)
                self.assertEqual(int(PlasmaTv.R), PlasmaTv.R.Value)

            testInitialEnumConstAssignedZero()
            testInitialEnumConstAssignedNonZero()

        def testConsecutiveAssignmentsOfSameType() -> None:

            def testConsecutiveEllipseAssignments() -> None:
                class PlasmaTv(metaclass=Enum):
                    R = ...
                    G = ...

                self.assertEqual(PlasmaTv.R.Value, 0)
                self.assertEqual(int(PlasmaTv.R), PlasmaTv.R.Value)

                self.assertEqual(PlasmaTv.G.Value, 1)
                self.assertEqual(int(PlasmaTv.G), PlasmaTv.G.Value)

            def testConsecutiveIntAssignments() -> None:
                class PlasmaTv(metaclass=Enum):
                    R = 52
                    G = 9

                self.assertEqual(PlasmaTv.R.Value, 52)
                self.assertEqual(int(PlasmaTv.R), PlasmaTv.R.Value)

                self.assertEqual(PlasmaTv.G.Value, 9)
                self.assertEqual(int(PlasmaTv.G), PlasmaTv.G.Value)

            testConsecutiveEllipseAssignments()
            testConsecutiveIntAssignments()

        def testIntExpression() -> None:
            class PlasmaTv(metaclass=Enum):
                R = 1
                B = 10
                G = R + B

            self.assertEqual(PlasmaTv.G.Value, 11)
            self.assertEqual(int(PlasmaTv.G), PlasmaTv.G.Value)

        def testAssignmentOfEnumConst() -> None:
            class PlasmaTv(metaclass=Enum):
                R = 1
                G = R

            self.assertEqual(PlasmaTv.G.Value, PlasmaTv.R.Value)
            self.assertEqual(int(PlasmaTv.G), PlasmaTv.G.Value)

        def testComboOfAllPreviousCases() -> None:
            class PlasmaTv(metaclass=Enum):
                R = ...
                G = 1
                B = 11
                Magenta = ...
                Cyan = G + B
                Velvet = ...
                SkyBlue = ...
                Grass = G

            self.assertEqual(PlasmaTv.R.Value, 0)
            self.assertEqual(int(PlasmaTv.R), PlasmaTv.R.Value)

            self.assertEqual(PlasmaTv.G.Value, 1)
            self.assertEqual(int(PlasmaTv.G), PlasmaTv.G.Value)

            self.assertEqual(PlasmaTv.B.Value, 11)
            self.assertEqual(int(PlasmaTv.B), PlasmaTv.B.Value)

            self.assertEqual(PlasmaTv.Magenta.Value, 12)
            self.assertEqual(int(PlasmaTv.Magenta), PlasmaTv.Magenta.Value)

            self.assertEqual(PlasmaTv.Cyan.Value, 12)
            self.assertEqual(int(PlasmaTv.Cyan), PlasmaTv.Cyan.Value)

            self.assertEqual(PlasmaTv.Velvet.Value, 13)
            self.assertEqual(int(PlasmaTv.Velvet), PlasmaTv.Velvet.Value)

            self.assertEqual(PlasmaTv.SkyBlue.Value, 14)
            self.assertEqual(int(PlasmaTv.SkyBlue), PlasmaTv.SkyBlue.Value)

            self.assertEqual(PlasmaTv.Grass.Value, 1)
            self.assertEqual(
              int(PlasmaTv.Grass),
              PlasmaTv.Grass.Value)

        testInitialEnumConstAssignedEllipsis()
        testInitialEnumConstNotAssignedEllipses()
        testConsecutiveAssignmentsOfSameType()
        testIntExpression()
        testAssignmentOfEnumConst()
        testComboOfAllPreviousCases()

# R6
class Test_EnumConstantsHashedOnValuesAttribute(unittest.TestCase):
    def test(self) -> None:
        class Color(metaclass=Enum):
            R = 1
            G = ...

        self.assertEqual(builtins.hash(Color.R), hash(1))
        self.assertEqual(builtins.hash(Color.G), hash(2))

# R7
class Test_EnumConstantsTotallyOrderedOnValuesAttribute(unittest.TestCase):
    def test(self) -> None:
        class PlasmaTv(metaclass=Enum):
            R = ...
            G = 1
            B = 11
            Magenta = ...
            Cyan = G + B
            Velvet = ...
            SkyBlue = ...
            Grass = G

        enumConsts = \
          [
            PlasmaTv.R, PlasmaTv.G, PlasmaTv.B, PlasmaTv.Magenta, PlasmaTv.Cyan,
            PlasmaTv.Velvet, PlasmaTv.SkyBlue, PlasmaTv.Grass
          ]

        for enumConst_j in enumConsts:
            for enumConst_k in enumConsts:
                if enumConst_j.Value < enumConst_k.Value:
                    self.assertLess(enumConst_j, enumConst_k)
                if enumConst_j.Value <= enumConst_k.Value:
                    self.assertLessEqual(enumConst_j, enumConst_k)
                if enumConst_j.Value == enumConst_k.Value:
                    self.assertEqual(enumConst_j, enumConst_k)
                if enumConst_j.Value >= enumConst_k.Value:
                    self.assertGreaterEqual(enumConst_j, enumConst_k)
                if enumConst_j.Value > enumConst_k.Value:
                    self.assertGreater(enumConst_j, enumConst_k)

# R8
class Test_EnumConstantsAttributesAreImmutable(unittest.TestCase):

    class __Color(metaclass=Enum):
        R = 1
        G = ...

    __ExpectedErrMsgSubStr = 'Illegal operation.'

    def test_attributesNotAssignable(self) -> None:
        cls = self.__class__

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.R.Name = "Rouge"

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.R.Value = 11

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.G.Name = 'Grass'

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.G.Value = 12

    def test_attributesNotCreatable(self) -> None:
        cls = self.__class__

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.R.SomeNewAttribute = "Newness"

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.G.Value2 = 2

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.G.Value2 = ...

    def test_attributesNotDeletable(self) -> None:
        cls = self.__class__

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            del cls.__Color.R.Name

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            del cls.__Color.R.Value

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            del cls.__Color.G.Name

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            del cls.__Color.G.Value

# R9
class _ColorForEnumConstPickleTest(metaclass=Enum):
    R = 1
    G = ...

class Test_EnumConstantsArePickable(unittest.TestCase):
    def test(self) -> None:
        from pickle import loads, dumps

        r = loads(dumps(_ColorForEnumConstPickleTest.R))
        g = loads(dumps(_ColorForEnumConstPickleTest.G))

        self.assertEqual(_ColorForEnumConstPickleTest.R, r)
        self.assertEqual(_ColorForEnumConstPickleTest.G, g)

# R10
class Test_EnumsNotClientInstantiable(unittest.TestCase):
    __ExpectedErrMsgSubStr = 'Illegal operation.'

    def test(self) -> None:
        cls = self.__class__

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            class Color(metaclass=Enum):
                pass

            Color()

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            class Color(metaclass=Enum):
                R = 1

            Color()

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            class Color(metaclass=Enum):
                R = ...
                G = 1

            Color()

# R11
class Test_EnumAttributesAreImmutable(unittest.TestCase):

    class __Color(metaclass=Enum):
        R = 1
        G = ...

    __ExpectedErrMsgSubStr = 'Illegal operation.'

    def test_attributesNotAssignable(self) -> None:
        cls = self.__class__

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.R = 'Foo'

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.G = cls.__Color.R

    def test_attributesNotCreatable(self) -> None:
        cls = self.__class__

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.SomeNewAttribute = ...

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            cls.__Color.SomeOtherNewAttribute = 1

    def test_attributesNotDeletable(self) -> None:
        cls = self.__class__

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            del cls.__Color.R

        with self.assertRaisesRegex(TypeError, cls.__ExpectedErrMsgSubStr):
            del cls.__Color.G

# R12
class Test_EnumIteration(unittest.TestCase):
    def test_emptyEnum(self) -> None:
        class Color(metaclass=Enum):
            pass

        for enumConsts in Color:
            self.fail('Expected empty iteration.')

    def test_nonEmptyEnum(self) -> None:
        class PlasmaTv(metaclass=Enum):
            R = ...
            G = 1
            B = 11
            Magenta = ...
            Cyan = G + B
            Velvet = ...
            SkyBlue = ...
            Grass = G

        enumConstsFromIterator = builtins.list(builtins.iter(PlasmaTv))
        enumConstsFromManualEntry = \
          [
            PlasmaTv.R,
            PlasmaTv.G,
            PlasmaTv.B,
            PlasmaTv.Magenta,
            PlasmaTv.Cyan,
            PlasmaTv.Velvet,
            PlasmaTv.SkyBlue,
            PlasmaTv.Grass
          ]

        self.assertEqual(enumConstsFromIterator, enumConstsFromManualEntry)

# R13
class Test_EnumStrSpecialFunction(unittest.TestCase):
    def test_emptyEnum(self) -> None:
        class Color(metaclass=Enum):
            pass

        expectedEnumStr = "<class '{0}.Color': {{}}>".format(Color.__module__)
        self.assertEqual(builtins.str(Color), expectedEnumStr)

    def test_enumWithOneConst(self) -> None:
        class Color(metaclass=Enum):
            R = 1

        expectedEnumStr = \
          "<class '{0}.Color': {{'Color.R': 1}}>".format(Color.__module__)
        self.assertEqual(builtins.str(Color), expectedEnumStr)

    def test_enumWithThreeConts(self) -> None:
        class Color(metaclass=Enum):
            R = 1
            G = ...
            B = 13

        expectedEnumStr = \
          "<class '{0}.Color': {{'Color.R': 1, 'Color.G': 2, 'Color.B': 13}}>"\
          .format(Color.__module__)
        self.assertEqual(builtins.str(Color), expectedEnumStr)

# R14
class _PlasmaTvForEnumPickleTest(metaclass=Enum):
    R = ...
    G = 1
    B = 11
    Magenta = ...
    Cyan = G + B
    Velvet = ...
    SkyBlue = ...
    Grass = G

class Test_EnumsArePickable(unittest.TestCase):
    def test(self) -> None:
        from pickle import loads, dumps

        pickledEnum = loads(dumps(_PlasmaTvForEnumPickleTest))
        self.assertEqual(_PlasmaTvForEnumPickleTest, pickledEnum)

if __name__ == '__main__':
    unittest.main()