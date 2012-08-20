#!/bin/bash

# Usage: runtest.sh python-executable testfile(s)

if [ \( $# -eq 0 \) -o \
    \( $# -eq 1 \) -o \
    \( $# -eq 1 -a "$1" = "--help" \) ]
then
    echo "Usage: runtest.sh python-executable testfile(s)"
    exit 0
fi

pythonExe="$1"
for ((argIndx=2; argIndx <= $#; ++argIndx))
do
    pyScript="${!argIndx}"
    pyScriptAbsParentPath="$( cd "$( dirname "${pyScript}" )" && pwd )"
    cmd=("${pythonExe}" "${pyScript}" "${pyScriptAbsParentPath}")

     echo "${cmd[@]}"
     eval "${cmd[@]}"
done