#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Define the relative path from the script's directory
RELATIVE_PATH="src/main.py"

# Combine the script's directory with the relative path
TARGET_PATH="$SCRIPT_DIR/$RELATIVE_PATH"

#echo "The target path is: $TARGET_PATH"

fastapi run $TARGET_PATH --port 3000
