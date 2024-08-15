#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Please choose a mission directory"
    exit 1
fi

MISSION=$1
echo "Building: $MISSION"

make clean
make MISSION=$MISSION -j2 install