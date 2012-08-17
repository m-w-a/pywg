#! /usr/bin/env python3.2

from _Enum import *
import builtins
import unittest
import codeop

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

  def test_notOkIfMultiplyInherit(self) -> None:

    expectedErrMsgSubStr = 'has base classes other than object'

    def testBaseClassNotObject() -> None:
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

    def testMultipleBaseClasses() -> None:
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

    testBaseClassNotObject()
    testMultipleBaseClasses()

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
      class_of_98 = 1998
      ClassOf_98 = 1998
      Class_Of_98 = 1998

  def test_notOkIfInvalidIds(self) -> None:
    with self.assertRaises(SyntaxError):
      codeop.compile_command(\
        'class Color(metaclass=Enum):'\
        '  R$ = 1')

    with self.assertRaises(SyntaxError):
      codeop.compile_command(\
        'class Class(metaclass=Enum):'\
        '  1998 = 1998')

class Test_EnumConstantsMustBeOfTypeIntOrEllipsis(unittest.TestCase):  
  def test_okIfOfTypeIntOrEllipsis(self) -> None:
    def test_okIfOfTypeInt() -> None:
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

    def test_okIfOfTypeEllipsis() -> None:
      class MonoChrome(metaclass=Enum):
        R = ...

      class HDTV(metaclass=Enum):
        R = ...
        G = ...
        B = ...

    def test_okIfBothOfTypeIntOrEllipsis() -> None:
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

    test_okIfOfTypeInt()
    test_okIfOfTypeEllipsis()
    test_okIfBothOfTypeIntOrEllipsis()

  def test_notOkIfNotOfTypeIntNorEllipsis(self):

    expectedErrMsgSubStr = \
      'these user declared attributes are not of type int or ellipsis:'

    def testUnmixedSingleInvalidType() -> None:    

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          R = 0.0

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          R = 'Red'

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          R = []

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          R = ()

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          R = {}

    def testMixedSingleInvalidType() -> None:

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          R = 0.0
          G = ...

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          R = 'Red'
          G = 1

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          G = ...
          R = []

      with self.assertRaisesRegex(\
        TypeError, 
        ' '.join([expectedErrMsgSubStr, 'R'])):

        class Color(metaclass=Enum):
          G = 1
          R = ()

      with self.assertRaisesRegex(\
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

class Test_EnumConstantsAreOfTypeEnum(unittest.TestCase):
  def test_typeEnumConstTypes(self) -> None:
    class Color(metaclass=Enum):
      R = ...
      G = 1
      B = G + 1
      Magenta = B + G
      Cyan = builtins.len(['Crayola'])

    self.assertIs(type(Color.R), Color)
    self.assertIs(type(Color.G), Color)
    self.assertIs(type(Color.B), Color)
    self.assertIs(type(Color.Magenta), Color)
    self.assertIs(type(Color.Cyan), Color)

#class Test_EnumConstantAttributeRelatedTests(unittest.TestCase):
  #def test_ValueRelatedAttributes(self) -> None:


if __name__ == '__main__':
  unittest.main()