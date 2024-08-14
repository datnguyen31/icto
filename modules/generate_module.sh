#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_name> <template_directory>"
    exit 1
fi

INPUT_NAME=$1
TEMPLATE_DIR=$2
NEW_DIR=${INPUT_NAME}

# Copy the template directory to the new directory
cp -r "$TEMPLATE_DIR" "$NEW_DIR"

# Find all files in the new directory and replace text
find "$NEW_DIR" -type f -exec bash -c '
    file="$1"
    INPUT_NAME="$2"
    sed -i "s/sample/${INPUT_NAME,,}/g" "$file"
    sed -i "s/Sample/${INPUT_NAME^}/g" "$file"
    sed -i "s/SAMPLE/${INPUT_NAME^^}/g" "$file"
' _ {} "$INPUT_NAME" \;

# Find all files and directories in the new directory and rename them
find "$NEW_DIR" -depth -exec bash -c '
    path="$1"
    INPUT_NAME="$2"
    new_path=$(echo "$path" | sed "s/sample/${INPUT_NAME,,}/g" | sed "s/Sample/${INPUT_NAME^}/g" | sed "s/SAMPLE/${INPUT_NAME^^}/g")
    if [ "$path" != "$new_path" ]; then
        mv "$path" "$new_path"
    fi
' _ {} "$INPUT_NAME" \;

# Remove any empty directories that may have been created
find "$NEW_DIR" -type d -empty -delete

echo "Template directory copied, indicators replaced, and files renamed successfully."