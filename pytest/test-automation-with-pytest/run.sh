#!/usr/bin/env bash

if [ $# -eq 0 ]
then
pytest
elif [ $# -eq 1 ] && [ -d ${1} ]
then
pytest ${1}
elif [ $# -eq 1 ] && [ -f ${1} ]
then
pytest ${1}
else
pytest -m ${@:1}
fi