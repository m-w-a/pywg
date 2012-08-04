#! /usr/bin/env python3.2

from _Enum import *
import unittest

class Test_EnumCanOnlyInheritFromClassObject(unittest.TestCase):
  
  def setUp(self): pass
  def tearDown(self): pass
  
  def test_OnlyInheritFromClassObjectSuccessfully(self):
    class Color(metaclass=Enum): pass
    class Color(object, metaclass=Enum): pass


if __name__ == '__main__':
  unittest.main()