#!/bin/bash

for i in {1..6}; do
  for j in {1..5}; do
    file="./output/${i}-base${j}.gjf"
    
    if [[ -f $file ]]; then
      echo "Running G09 for $file..."
      G09 "$file"
    else
      echo "File $file not found, skipping..."
    fi
  done
done

