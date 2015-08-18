#!/bin/bash

#------------------------------------------------------------------------------#
# The python unit test scripts in this directory and it subdirectories are 
# intended to be run as stand alone executables, not imported and run via
# the "python -m unittest" mechanism or programmatically via another python 
# script. This is because they are intended to test features of the executing 
# script itself.
#------------------------------------------------------------------------------#

usageMsg="\
Usage: runtest.sh --help
Usage: runtest.sh <python-executable> --all
Usage: runtest.sh <python-executable> <testfile1 [testfile2 ...]>

Second form executes all tests of the form '*PyUnit.py' in the directory which
this script is found.

Third form executes each command-line specified test file in its own directory.
"

if [ \( $# -eq 0 \) -o \
    \( $# -eq 1 \) -o \
    \( $# -eq 1 -a "$1" = "--help" \) ]
then
    echo "${usageMsg}"
    exit 0
fi

my_abs_filepath="${BASH_SOURCE[0]}"
my_abs_parentpath="$( cd "$( dirname "$my_abs_filepath" )" && pwd )"

unittestPattern="*_ExPyUnit.py"

testfiles=
if [ $# -eq 2 -a "$2" = '--all' ]
then
    testfiles=(\
        $(find "${my_abs_parentpath}" \
            -name "${unittestPattern}" \
            -type f \
            -print0 \
          | \
            xargs -0 echo) )
else
    testfiles=("${@:2}")
fi

pythonExe="$1"
for ((argIndx=0; argIndx < ${#testfiles[@]}; ++argIndx))
do
    pyScript="${testfiles[${argIndx}]}"
    pyScriptAbsParentPath="$( cd "$( dirname "${pyScript}" )" && pwd )"
    pyScriptName="$(basename "${pyScript}")"
    # The executing scripts path needs to be passed in because there is no 
    # universally reliable way to access it in python.
    cmd=("${pythonExe}" "${pyScriptName}" "${pyScriptAbsParentPath}")

    echo "cd "${pyScriptAbsParentPath}"" 
    echo "${cmd[@]}"
    eval "cd "${pyScriptAbsParentPath}"; ${cmd[@]}"
done