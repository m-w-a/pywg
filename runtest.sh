#!/bin/bash

usageMsg="\
Usage:
  runtest.sh \
    <python-executable> \
    <testfile1 [testfile2 ...]> \
    [unittest options]"

if [ \( $# -eq 0 \) -o \
     \( $# -eq 1 -a "$1" = "--help" \) ]
then
    echo "${usageMsg}"
    exit 0
fi

my_abs_filepath="${BASH_SOURCE[0]}"
my_abs_parentpath="$( cd "$( dirname "$my_abs_filepath" )" && pwd )"

pythonExe="$1"
packageDir="${my_abs_parentpath}"

cmd=("${pythonExe}" -m unittest discover -t "${packageDir}" -p "$@")

echo "${cmd[@]}"
eval "${cmd[@]}"