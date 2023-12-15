#!/bin/bash

# Source file path
source_file="/home/jeison/ic/repositorios/solucao_ic/teste/wallet.txt"

# Destination directory
destination_dir="/home/jeison/ic/repositorios/solucao_ic/aqui/file.txt"

# Loop to copy the file 10000 times
for ((i=0; i<10000; i++)); do
    file_content=$(<"$source_file")

    # Check if content equals "root"
    if [ "$file_content" = "root" ]; then
        echo "a"    
    fi
    
done