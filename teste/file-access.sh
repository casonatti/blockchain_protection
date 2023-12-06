#!/bin/bash

file_path="/home/jeison/ic/repositorios/solucao_ic/teste/wallet.txt"
num_accesses=10000  # Change this to the desired number of accesses
interval_seconds=2  # Change this to the desired interval between accesses

for ((i=1; i<=num_accesses; i++)); do
    echo "Accessing file $file_path, attempt $i"
    
    # Perform file access operation here (e.g., read the file)
    echo "$i"
    date +%s.%N
    cat "$file_path"
    # You can add more file access operations if needed
    
    # Simulate a delay between accesses
#    sleep $interval_seconds
done
