#! /usr/bin/env python3.2

from _Enum import *
import unittest

class Test_EnumCanOnlyInheritFromClassObject(unittest.TestCase):
  
  def setUp(self): pass
  def tearDown(self): pass
  
  def test_OnlyInheritFromClassObjectSuccessfully(self):
    
    def testEmptyBaseClass():
      class Color(metaclass=Enum):
        pass
      
      class Color(metaclass=Enum):
        R = 1
      
      class Color(metaclass=Enum):
        R = 1
        G = 2
      
    def testObjectAsSoleDeclaredBaseClass():
      class Color(object, metaclass=Enum):
        pass
       
      class Color(object, metaclass=Enum):
        R = 1
        
      class Color(object, metaclass=Enum):
        R = 1
        G = 2
    
    testEmptyBaseClass()
    testObjectAsSoleDeclaredBaseClass()


if __name__ == '__main__':
  unittest.main()