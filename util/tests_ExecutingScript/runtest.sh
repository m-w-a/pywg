#!/bin/bash

#------------------------------------------------------------------------------#
# Bash shell script needed to verifiably pass in the executing python scripts
# home directory as a command line argument to the python unit test.
#------------------------------------------------------------------------------#

usageMsg="\
Usage: runtest.sh --help
Usage: runtest.sh python-executable --all
Usage: runtest.sh python-executable testfile(s)

Second form executes all tests of the form '*PyUnit.py' in the directory which
this script is found.

Third form executes each command-line specified test file in its own directory."

if [ \( $# -eq 0 \) -o \
    \( $# -eq 1 \) -o \
    \( $# -eq 1 -a "$1" = "--help" \) ]
then
    echo "${usageMsg}"
    exit 0
fi

my_abs_filepath="${BASH_SOURCE[0]}"
my_abs_parentpath="$( cd "$( dirname "$my_abs_filepath" )" && pwd )"

testfiles=
if [ $# -eq 2 -a "$2" = '--all' ]
then
    testfiles=(\
        $(find "${my_abs_parentpath}" -name "*PyUnit.py" -type f -maxdepth 1) )
else
    testfiles=("${@:2}")
fi

pythonExe="$1"
for ((argIndx=0; argIndx < ${#testfiles[@]}; ++argIndx))
do
    pyScript="${testfiles[${argIndex}]}"
    pyScriptAbsParentPath="$( cd "$( dirname "${pyScript}" )" && pwd )"
    pyScriptName="$(basename "${pyScript}")"
    cmd=("${pythonExe}" "${pyScriptName}" "${pyScriptAbsParentPath}")

    echo "cd "${pyScriptAbsParentPath}"" 
    echo "${cmd[@]}"
    eval "cd "${pyScriptAbsParentPath}"; ${cmd[@]}"
done