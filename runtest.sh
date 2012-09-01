#!/bin/bash

#------------------------------------------------------------------------------#
# Bash script to aid in running tests via unittest's import mechanism.
#------------------------------------------------------------------------------#

usageMsg="\
Usage:
  runtest.sh <python-executable> <testfile1 [testfile2 ...]> [unittest options]
  runtest.sh <python-executable> --all <directory>"

if [ \( $# -eq 0 \) -o \
     \( $# -eq 1 -a "$1" = "--help" \) ]
then
    echo "${usageMsg}"
    exit 0
fi

my_abs_filepath="${BASH_SOURCE[0]}"
my_abs_parentpath="$( cd "$( dirname "${my_abs_filepath}" )" && pwd )"

pythonExe="$1"
packageDir="${my_abs_parentpath}"

if [ $# -eq 3 -a "$2" = '--all' ]
then
    if [ ! -d "$3" ]
    then
        echo "Argument 3 must specify a directory."
        exit 1
    fi

    dirToStartSearch="$3"

    subRunnersList=( \
        $(find "${dirToStartSearch}" \
            -name runtest.sh \
            -type f \
            -mindepth 2 \
            -print0 \
          | \
            xargs -0 echo) )

    subRunnersDirList=()
    pruneSubStmt=''
    for subRunner in "${subRunnersList[@]}"
    do
        subDir="$(dirname "${subRunner}")"
        subDirsToPrune="${subDir}/*"

        subRunnersDirList+=("${subDir}")
        pruneSubStmt=""${pruneSubStmt}" -not -path \""${subDirsToPrune}"\""
    done

    run()
    {
        pythonExe="$1"
        packageDir="$2"
        test="$3"

        cmd=("${pythonExe}"
            -m unittest discover
              -t "${packageDir}"
              -p "${test}")

        currentDir="$(cd "$(dirname "${test}")" && pwd)"
        echo "cd ${currentDir}"
        echo "${cmd[@]}"
        eval "${cmd[@]}"
    }

    export -f run

    cmd=(find "${dirToStartSearch}" 
        "${pruneSubStmt}" 
        -name "\"*_PyUnit.py\""
        -type f 
        -execdir bash -c
            "\"run "${pythonExe}" "\"${packageDir}\"" \"{}\" \""
            "\";\"")

    echo "${cmd[@]}"
    eval "${cmd[@]}"

    for subRunnerDir in "${subRunnersDirList[@]}"
    do
        cmd=(cd "${subRunnerDir};" bash "./runtest.sh" "${pythonExe}" "--all")
        echo "${cmd[@]}"
        eval "${cmd[@]}"
    done
else
    cmd=("${pythonExe}" -m unittest discover -t "${packageDir}" -p "${@:2}")
    echo "${cmd[@]}"
    eval "${cmd[@]}"
fi