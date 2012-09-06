#! /usr/bin/env python3.2

import types
import builtins

class StaticProxy:
    """
    A proxy class for functions and methods to aid in defining local static
    variables. Any attributes added to instances of this class will become
    static variables of the proxified function or method.

    Usage:
      def foo():
          static = StaticProxy(foo)
          static.StaticVar1 = lambda ...
          static.StaticVar2 = function identifier ...
          ...

    Note:
      The instance attributes of this class should only be assigned lambda or
      function expressions, that when evaluated with no parameters shall return
      the desired initialization value for said attributes.

    Throws:
      TypeError
        On any attempts to get attributes on this class.
        On any attempts to delete attributes on this class.

        Rationale:
          Since this is just a proxy class with a very specific purpose,
          all operations complemental to but tangential to said purpose shall
          be disallowed for the sake of clarity.

      ReinitializationError
        If any attribute is set more than once on an instance of this class.
    """

    class ReinitializationError(Exception): pass

    def __init__(self, func: (types.FunctionType, types.MethodType) ):
        attrNameFunc = "_{0}__Func".format(__class__.__name__)
        super().__setattr__(attrNameFunc, func)

    def __getattr__(self, name):
        cls = self.__class__
        raise TypeError(cls.__IllegalOperationMsg)

    def __setattr__(
      self,
      name : str,
      valueProxy : (types.LambdaType, types.FunctionType) ) \
        -> None:

        if builtins.getattr(self.__Func, name, self.__Func) is self.__Func:
            builtins.setattr(self.__Func, name, valueProxy())
        else:
            raise ReinitializationError()

    def __delattr__(self, name):
        cls = self.__class__
        raise TypeError(cls.__IllegalOperationMsg)

    __IllegalOperationMsg = 'Illegal operation.'