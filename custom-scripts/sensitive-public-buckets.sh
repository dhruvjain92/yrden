#!/bin/bash

# This script runs plugin to find all the public buckets and then traverse the objects in those buckets to find sensitve files.
# Extension filter can be checked in the script sensitive-files.py
# Currently runs for 1 region for one profile
# Based on the buckets size, this script may take a long time to run

ENV="stage" # Target AWS Profile
cd ..
file_name=$(date -u +"%Y-%m-%dT%H:%M:%SZ"-"public-s3.txt")
buckets_list=$(echo $ENV | python3 yrden.py --mode plugin --name public-s3 --format file --output-file $file_name)
sensitive_file_name=$(date -u +"%Y-%m-%dT%H:%M:%SZ"-"sensitive-files.txt")
while IFS= read -r line
do
  f_name=$(echo $line | tr -d "[:space:]")
  echo $f_name
  echo -e "stage\n$f_name" | python3 yrden.py --mode plugin --name get-sensitive-files --format file --output-file $sensitive_file_name
done < "./output/$file_name"
echo "Output is stored in: $sensitive_file_name"
