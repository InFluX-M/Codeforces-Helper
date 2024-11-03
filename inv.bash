#!/bin/bash

# Save the current directory
CURRENT_DIR=$(pwd)
LOGS_DIR="tps-sample/logs"
SANDBOX_DIR="tps-sample/sandbox"
CHECKER_FILE="tps-sample/checker/._checker.cpp.compile.out"

# Navigate to the tps-sample directory
cd tps-sample || exit

# Remove the specified directories and file
if [[ -d "$LOGS_DIR" ]]; then
    rm -r "$LOGS_DIR"
    echo "Removed directory: $LOGS_DIR"
fi

if [[ -d "$SANDBOX_DIR" ]]; then
    rm -r "$SANDBOX_DIR"
    echo "Removed directory: $SANDBOX_DIR"
fi

if [[ -f "$CHECKER_FILE" ]]; then
    rm "$CHECKER_FILE"
    echo "Removed file: $CHECKER_FILE"
fi

# Execute the command
tps invoke ../main.cpp -r -s

# Navigate back to the original directory
cd "$CURRENT_DIR"
