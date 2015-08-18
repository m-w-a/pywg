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

testEnumeratedFiles()
{
    local cmd=(
        "${pythonExe}" -m unittest discover -t "${packageDir}" -p "${@:2}")
    echo "${cmd[@]}"
    eval "${cmd[@]}"
}

testDiscoveredFiles()
{
    local dirToStartSearch="$3"

    local subRunners=( \
        $(find "${dirToStartSearch}" \
            -mindepth 2 \
            -name runtest.sh \
            -type f \
            -print0 \
          | \
            xargs -0 echo) )

    local subRunnerDirs=()
    local findCmdPruneSubStmt=''
    # Compute subRunnerDirs and findCmdPruneSubStmt
    for subRunner in "${subRunners[@]}"
    do
        local subDir="$(dirname "${subRunner}")"
        local subDirsToPrune="${subDir}/*"

        subRunnerDirs+=("${subDir}")
        findCmdPruneSubStmt=""${findCmdPruneSubStmt}" -not -path \""${subDirsToPrune}"\""
    done

    run()
    {
        local pythonExe="$1"
        local packageDir="$2"
        local test="$3"

        local cmd=(
            "${pythonExe}"
                -m unittest discover
                -t "${packageDir}"
                -p "\"*_PyUnit.py\"")

        local currentDir="$(cd "$(dirname "${test}")" && pwd)"
        echo "cd ${currentDir}"
        echo "${cmd[@]}"
        eval "${cmd[@]}"
    }

    export -f run

    local cmd=(find "${dirToStartSearch}" 
        "${findCmdPruneSubStmt}" 
        -name "\"*_PyUnit.py\""
        -type f 
        -execdir bash -c
            "\"run "${pythonExe}" "\"${packageDir}\"" \"{}\" \""
            "\";\"")

    echo "${cmd[@]}"
    eval "${cmd[@]}"

    for subRunnerDir in "${subRunnerDirs[@]}"
    do
        local cmd=(
          cd "${subRunnerDir};" bash "./runtest.sh" "${pythonExe}" "--all")
        echo "${cmd[@]}"
        eval "${cmd[@]}"
    done
}

if [ $# -eq 3 -a "$2" = '--all' ]
then
    if [ ! -d "$3" ]
    then
        echo "Argument 3 must specify a directory."
        exit 1
    fi
    
    testDiscoveredFiles "$@"
else
    testEnumeratedFiles "$@"
fi