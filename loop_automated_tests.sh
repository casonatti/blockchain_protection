#!/bin/bash

# Source file path
source_file="/home/jeison/ic/repositorios/solucao_ic/teste/wallet.txt"

# Destination directory
destination_dir="/home/jeison/ic/repositorios/solucao_ic/aqui/file.txt"

# Loop to copy the file 10000 times
for ((i=0; i<10; i++)); do
    sudo python3 automated_tests.py    
done