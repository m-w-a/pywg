import types

def addStaticMarkerIfNotPresent(
  func : (types.FunctionType, types.MethodType),
  marker : str) \
    -> bool:
    """Adds the marker 'marker' to 'func' as an attribute, if not already
    present. 'marker' maybe any string, including an invalid identifier. Returns
    whether addition was successful.

    Use this to add static variables to functions, like so:

        def foo(...):
            if addStaticMarkerIfNotPresent(foo, '$sm'):
                foo.StaticVar = ...
    """

    if getattr(func, marker, func) is func:
        setattr(func, marker, True)
        return True
    else:
        return False
