#! /usr/bin/env python3.2

import types
import builtins

class StaticProxy:
    """
    A proxy class for functions and methods to aid in defining local static
    variables.

    Usage:
      def foo():
          selfStatic = StaticProxy(foo)
          foo.StaticVar1 = ...
          foo.StaticVar2 = ...
          ...

    Throws:
      TypeError
        On any attempts to get attributes on this class.
        On any attempts to delete attributes on this class.

        Rationale:
          Since this is just a proxy class with a very specific purpose,
          all operations complemental to but tangential to said purpose shall
          be disallowed for the sake of clarity.
    """
    def __init__(self, func: (types.FunctionType, types.MethodType) ):
        self.__Func = func

    def __getattribute__(self, name):
        cls = self.__class__
        raise TypeError(cls.__IllegalOperationMsg)

    def __setattr__(
      self,
      name : str,
      valueProxy : (types.LambdaType, types.FunctionType) )
        -> None:

        if builtins.getattr(self.__Func, name, self.__Func) is self.__Func:
            builtins.setattr(self.__Func, name, valueProxy())

    def __setattr__(self, name):
        cls = self.__class__
        raise TypeError(cls.__IllegalOperationMsg)

    __IllegalOperationMsg = 'Illegal operation.'