#! /usr/bin/env python3.2

from _Enum import *
import unittest
import codeop

class Test_EnumCanOnlyInheritFromClassObject(unittest.TestCase):
  
  def setUp(self): pass
  def tearDown(self): pass
  
  def test_pInherit(self) -> None:
    
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
    
  def test_nInherit(self) -> None:
    
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
  
  def test_pValidIds(self) -> None:
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
  
  def test_nValidIds(self):
    with self.assertRaises(SyntaxError):
      codeop.compile_command(\
        'class Color(metaclass=Enum):'\
        '  R$ = 1')
    
    with self.assertRaises(SyntaxError):
      codeop.compile_command(\
        'class Class(metaclass=Enum):'\
        '  1998 = 1998')
    
#  def test_EnumConstantsAreValidPythonIdentifiers(self):
#    class Color(metaclass=Enum):
#      $R = 1

if __name__ == '__main__':
  unittest.main()