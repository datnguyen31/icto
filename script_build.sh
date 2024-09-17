#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Please choose a mission directory and target"
    exit 1
fi

MISSION=$1
TARGET=$2
echo "Building: $MISSION"
echo "Target: $TARGET"

make clean
make MISSION=$MISSION TOOLCHAIN=$TARGET -j2 install