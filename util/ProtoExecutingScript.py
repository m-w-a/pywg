def allowRelativePathsInSubpackageScript(\
  scriptModuleNameAttr : str,  scriptModulePackageAttr : str) \
    -> str:

    # boilerplate to allow running as script directly
    if scriptModuleNameAttr == '__main__' and scriptModulePackageAttr is None:
        import sys, os, inspect
        # The following assumes the script is in the top level of 
        # the package directory.  We use dirname() to help get the parent
        # directory to add to sys.path, so that we can import the current
        # package.  This is necessary since when invoked directly, the 'current'
        # package is not automatically imported.

        try:
            # DO NOT USE __file__ 
            # __file__ fails if script is called in different ways on Windows
            # __file__ fails if someone has executed os.chdir()
            # sys.argv[0] also fails because it doesn't not always contains the
            # path
            frame = inspect.stack()[1]
            scriptFilepath = os.path.abspath(frame[1])
            if(scriptFilepath is None):
              scriptFilepath = sys.argv[0]

            packageDir = \
              os.path.dirname(os.path.dirname(os.path.dirname(scriptFilepath)))

            if packageDir not in sys.path:
                sys.path.insert(1, packageDir)

            scriptModulePackageAttr = 'tmp.tmp2'

            # Import the top level package directory.
            __import__('tmp', globals(), locals(), [], 0)

        finally:
            del sys, os, inspect
            # Always delete frames when done with them.
            del frame
        
        return scriptModulePackageAttr
        
        # Import the top level package directory.
        # Can this be automated?
    #    import tmp

__package__ = allowRelativePathsInSubpackageScript(__name__, __package__)
from ..t2 import *

print("{0}".format(hw()))
