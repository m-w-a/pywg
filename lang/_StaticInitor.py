#! /usr/bin/env python3.2

import types
import builtins

class StaticInitor:
    """
    A proxy class for functions and methods to aid in defining local static
    variables. Any attributes added to instances of this class will become
    static variables of the proxified function or method.

    Usage:
      def foo():
          static = StaticInitor(foo)
          static.StaticVar1 = lambda ...
          static.StaticVar2 = function identifier ...
          ...

    Note:
      The instance attributes of this class should only be assigned lambda,
      function, or method expressions, that when evaluated with no parameters 
      shall return the desired initialization value for said attributes.

      Rationale:
        Initialization values for static variables might need to be computed,
        and this may be costly. Since static variables must be checked to see
        if they are already set at *runtime*, and then set them if necessary,
        we avoid the unnecessary computation to calculate initial values for
        all those other times that a function or method is called but its static
        variables are set by using callables instead.

    Note:
      Reinitialization of static variables for the same function or method via
      any instances of this will silently fail.

      Rationale:
        No efficient solution has been found to distinguish between the
        following two scenarios:

        Case1:
          def foo() -> int:
              static = StaticInitor(foo)
              static.Var1 = lambda: 0

              return foo.Var1

        foo()
        foo()

        Case2:
          def bar() -> int:
              static = StaticInitor(bar)
              static.Var1 = lambda: 1
              static.Var1 = lambda: '1'

              return bar.Var1

        bar()

        According to Python language rules foo.Var1 is reinitialized in Case1
        via the second call to foo(), but this should be legal and silently
        fail. In Case2 bar.Var1 is also reinitialized via a single call to bar(),
        but this reinitialization should clearly be illegal. Unfortunately,
        no clean way has been found to differentiate between the two cases
        without polluting foo/bar with a bunch of attributes, hence the
        decision has been made to silently allow but fail on reinitialization
        of static variables.

    Throws:
      TypeError
        On any attempts to get attributes on this class.
        On any attempts to delete attributes on this class.

        Rationale:
          Since this is a proxy class with a very specific purpose,
          all operations complemental with but tangential to said purpose shall
          be disallowed for the sake of clarity.

    """

    def __init__(self, func: (types.FunctionType, types.MethodType) ):
        attrNameFunc = "_{0}__Func".format(__class__.__name__)
        super().__setattr__(attrNameFunc, func)

    def __getattr__(self, name):
        cls = self.__class__
        raise TypeError(cls.__IllegalOperationMsg)

    def __setattr__(
      self,
      name : str,
      valueProxy : (types.LambdaType, types.FunctionType, types.MethodType) ) \
        -> None:

        cls = self.__class__

        if builtins.getattr(self.__Func, name, self.__Func) is self.__Func:
            builtins.setattr(self.__Func, name, valueProxy())

    def __delattr__(self, name):
        cls = self.__class__
        raise TypeError(cls.__IllegalOperationMsg)

    __IllegalOperationMsg = 'Illegal operation.'