Summary
-------
This library enables the use of C++ like enums in Python3. This was done some time before C++ like enums were officially added to Python3. It's uncanny how the official version matches my own version.

Requirements and Rationale
--------------------------
Can be found here: "./lang/EnumRequirementsAndRationale.txt".

Unit Tests
----------
Can be found in "./lang" and "./util".
All unit tests except for the ones in "./util/tests_ExecutingScript" can be run via "./runtest.py". For the former, one has to run "./util/tests_ExecutingScript/runtest.sh".

Sample Usage
------------
from pywg.lang import *

class Color(metaclass=Enum):
    R = 1
    G = ...
    B = G + 1