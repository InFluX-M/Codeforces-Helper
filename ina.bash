#!/bin/bash

# Check if a name was provided as an argument
if [ -z "$1" ]; then
    echo "Usage: ./ina.sh {name}"
    exit 1
fi

NAME=$1
TPS_SAMPLE_DIR="tps-sample/tests"
LOGS_DIR="tps-sample/logs"
SANDBOX_DIR="tps-sample/sandbox"
CHECKER_FILE="tps-sample/checker/._checker.cpp.compile.out"

# Ensure the directories and files exist
if [[ ! -d "$TPS_SAMPLE_DIR" ]]; then
    echo "Directory $TPS_SAMPLE_DIR does not exist."
    exit 1
fi

if [[ ! -f "input.txt" ]] || [[ ! -f "output.txt" ]]; then
    echo "Both input.txt and output.txt must be present in the current directory."
    exit 1
fi

# Copy input.txt and output.txt to the tests directory with the new names
cp input.txt "$TPS_SAMPLE_DIR/0-$NAME.in"
cp output.txt "$TPS_SAMPLE_DIR/0-$NAME.out"

# Append the required strings to gen_summary and mapping
echo "0-$NAME" >> "$TPS_SAMPLE_DIR/gen_summary"
echo "samples 0-$NAME" >> "$TPS_SAMPLE_DIR/mapping"

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

echo "Files copied, entries appended, and specified files/directories removed successfully."
