#! /usr/bin/env python3.2

class Noop:
    def __enter__(self):
        pass
    def __exit__(self, *exc_info):
        pass

_Noop = Noop()

def noop() -> Noop:
    return _Noop