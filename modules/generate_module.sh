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

# Function to replace text in files
replace_text() {
    local file=$1
    sed -i "s/sample/${INPUT_NAME,,}/g" "$file"
    sed -i "s/Sample/${INPUT_NAME^}/g" "$file"
    sed -i "s/SAMPLE/${INPUT_NAME^^}/g" "$file"
}

# Function to rename files and directories
rename_files() {
    local path=$1
    local new_path=$(echo "$path" | sed "s/sample/${INPUT_NAME,,}/g" | sed "s/Sample/${INPUT_NAME^}/g" | sed "s/SAMPLE/${INPUT_NAME^^}/g")
    if [ "$path" != "$new_path" ]; then
        mv "$path" "$new_path"
    fi
}

# Export the functions and variable for use with find
export -f replace_text
export -f rename_files
export INPUT_NAME

# Find all files in the new directory and replace text
find "$NEW_DIR" -type f -exec bash -c 'replace_text "$0"' {} \;

# Find all files and directories in the new directory and rename them
find "$NEW_DIR" -depth -exec bash -c 'rename_files "$0"' {} \;

echo "Template directory copied, indicators replaced, and files renamed successfully."