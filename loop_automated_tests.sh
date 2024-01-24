#!/bin/bash

# Source file path
source_file="./tests/wallet.txt"

# Destination directory
destination_dir="./tests/file.txt"

# Loop to copy the file 10000 times
for ((i=0; i<10; i++)); do
    sudo python3 automated_tests.py    
done