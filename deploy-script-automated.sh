#!/usr/bin/env bash

# Save the current IFS
OLD_IFS="$IFS"

# Set IFS to comma for splitting the output of the command
IFS=','

# Execute the command and split the output, then store it in an array
read -ra PROJECTS <<< "$(poetry poly diff -s)"

# Restore the original IFS
IFS="$OLD_IFS"

# Example usage: iterate over the array and print each project
for project in "${PROJECTS[@]}"; do
    ./deploy-script.sh "$project"

    cd "./projects/$project/terraform"
    echo "Deploying $project"
    echo $(pwd)
    cd -
done
