#! /usr/bin/env python3.2

class Noop:
    """
    Context manager class which does nothing on __enter__ and __exit__.
    """
    def __enter__(self):
        pass
    def __exit__(self, *exc_info):
        pass

_Noop = Noop()

def noop() -> Noop:
    """
    Returns a singleton instance of Noop context manager.
    """
    return _Noop