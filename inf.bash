#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Usage: inf {id contest}"
    exit 1
fi

# Execute the Python script with the provided contest ID
python3 "/home/{$USER}/Codeforces Helper/main.py" "$1
