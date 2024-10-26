#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -le 1 ]; then
    echo "Please choose a mission directory and target"
    exit 1
fi

MISSION=$1
TARGET=$2
JOBS=${3:-2}  # Set JOBS to 2 if not provided
CLEAN=$4

echo "Building: $MISSION"
echo "Target: $TARGET"
echo "Jobs: $JOBS"

# Check if CLEAN is declared and not empty
if [ -n "$CLEAN" ]; then
    make clean
fi

make MISSION=$MISSION TOOLCHAIN=$TARGET -j$JOBS install