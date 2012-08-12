import unittest
from .._addStaticMarkerIfNotPresent import *

class Test_addStaticMarkerIfNotPresent(unittest.TestCase):
  
  def setUp(self):
    self.__markers = []
    self.__funcs = []
    
    validIdentifiers = ['validId', '_St', '__my_id', 'camelCase_w']
    invalidIdentifiers = ['$id', 'id with spaces  ', '$9808 $#!(*%&']
    
    self.__markers.extend(validIdentifiers)
    self.__markers.extend(invalidIdentifiers)
    
    def emptyFunc(): pass
    def noParamFunc(): return x;
    def oneParamFunc(name : str) -> None: pass
    def twoParamFunc(arg1 : int, arg2 : dict) -> float: pass
    
    self.__funcs.extend(\
      [emptyFunc, noParamFunc, oneParamFunc, twoParamFunc])
    
    class Methods:
      def emptyFunc(): pass
      def noParamFunc(): return x;
      def oneParamFunc(name : str) -> None: pass
      def twoParamFunc(arg1 : int, arg2 : dict) -> float: pass

    self.__funcs.extend([\
        Methods.emptyFunc, \
        Methods.noParamFunc, \
        Methods.oneParamFunc, \
        Methods.twoParamFunc\
      ])
  
  def test_markerAdded(self) -> None:
    
    def test(\
      func : (types.FunctionType, types.MethodType), \
      marker : str) \
        -> bool:
      
      didAdd = addStaticMarkerIfNotPresent(func, marker)
      self.assertEqual(True, didAdd)
      self.assertTrue(hasattr(func, marker))

    for marker in self.__markers:
      for func in self.__funcs:
        test(func, marker)
  
  def test_markerNotAdded(self) -> None:

    def addMarker(\
      func : (types.FunctionType, types.MethodType), \
      marker : str) \
        -> bool:
      
      didAdd = addStaticMarkerIfNotPresent(func, marker)
      self.assertEqual(True, didAdd)
      self.assertTrue(hasattr(func, marker))
    
    def test(\
      func : (types.FunctionType, types.MethodType), \
      marker : str) \
        -> bool:
      
      didAdd = addStaticMarkerIfNotPresent(func, marker)
      self.assertEqual(False, didAdd)
      self.assertTrue(hasattr(func, marker))
    
    for marker in self.__markers:
      for func in self.__funcs:
        addMarker(func, marker)
    
    for marker in self.__markers:
      for func in self.__funcs:
        test(func, marker)

if __name__ == '__main__':
  unittest.main()
