#! /usr/bin/env python3.2

import builtins
import collections
import functools

class Enum(type):
  @classmethod
  def __prepare__(mcls, clsName, bases, **kwds):
    return collections.OrderedDict()
  
  # mcls:
  #   The metaclass (ie, this class).
  # clsName:
  #   The name of the class to be created.
  # bases:
  #   a list of the clsName's declared base classes
  # dxn:
  #   clsName's attributes.
  def __new__(mcls, clsName, bases, dxnry):
    
    def checkClassToBeCreatedHasNoBaseClasses() -> None:
      if builtins.len(bases) > 0:
        if builtins.len(bases) == 1 and object in bases:
          pass
        else:
          raise \
            TypeError( \
              '{clsName}: has base classes other than object'\
              .format(clsName=clsName))
    
    def checkUserDefinedAttributeTypesOfClassToBeCreated() -> None:
      permissibleTypes = frozenset([int, type(...)])
      misTypedAttrNames = []
      for attr in dxnry.items():
        attrName = attr[0]
        attrObj = attr[1]
        if not mcls.__isPythonSpecialName(attrName):
          if builtins.type(attrObj) not in permissibleTypes:
            misTypedAttrNames.append(attrName)
      
      if builtins.len(misTypedAttrNames) > 0:
        errMsg = \
          '{clsName}: these user declared attributes are not of type int or '\
          'ellipsis: {attributes}'\
          .format(clsName=clsName, attributes=', '.join(misTypedAttrNames))
         
        raise TypeError(errMsg)
    
    checkClassToBeCreatedHasNoBaseClasses()
    checkUserDefinedAttributeTypesOfClassToBeCreated()
    
    return super().__new__(mcls, clsName, bases, dxnry)
  
  # cls:
  #   The class that was just created (and not its instance!).
  # clsName:
  #   The name of cls as a string.
  # bases:
  #   a list of the cls’s base classes (excluding object, and therefore 
  #   possibly empty)
  # dict:
  #   cls's class attributes.
  def __init__(cls, clsName, bases, dxnry):
    super().__init__(clsName, bases, dxnry)
    
    def addClassData(cls, clsName, dxnry) -> None:
      lastEnumConstValue = -1
      for attr in dxnry.items():
        attrName = attr[0]
        attrObj = attr[1]
        if not cls.__class__.__isPythonSpecialName(attrName):
          enumConst = cls()
          enumConst.Name = '{clsName}.{attrName}'.format(**locals())
          
          if type(attrObj) == int:
            enumConst.Value = attrObj
          else:
            enumConst.Value = lastEnumConstValue + 1
          
          lastEnumConstValue = enumConst.Value
          
          builtins.setattr(cls, attrName, enumConst)
    
    def addClassFunctions(cls, clsName, dxnry) -> None:
      def __str__(self): return self.Name
      def __int__(self): return self.Value
      def __eq__(self, other):
        if not builtins.isinstance(other, self.__class__):
          return NotImplemented
        return self.Value == other.Value
      def __hash__(self): return builtins.hash(self.Value)
      def __lt__(self, other):
        if not builtins.isinstance(other, self.__class__):
          return NotImplemented
        return self.Value < other.Value
      def __setattr__(self, name, value):
        raise TypeError('Illegal operation.')
      def __delattr__(self, name):
        raise TypeError('Illegal operation.')
      
      cls.__str__ = __str__
      cls.__int__ = __int__
      cls.__eq__ = __eq__
      cls.__hash__ = __hash__
      cls.__lt__ = __lt__
      cls.__setattr__ = __setattr__
      cls.__delattr__ = __delattr__
      
      cls = functools.total_ordering(cls)
    
    addClassData(cls, clsName, dxnry)
    addClassFunctions(cls, clsName, dxnry)

  @staticmethod
  def __isPythonSpecialName(name : str) -> bool:
    return name.startswith('__') and name.endswith('__')

if __name__ == '__main__':
  class Color(metaclass=Enum):
    R = 1
    G = ...
    B = 101
  #  def foo(): pass

  #class FancyColor(Color, metaclass=Enum): pass

  print(Color.R.Name)
  print(Color.R.Value)
  print(Color.G.Value)
  print(Color.B.Value)
  print(Color.R)
  print(Color.G)
  print(Color.B)
  print(repr(Color.R))
  print(Color.R != Color.R)