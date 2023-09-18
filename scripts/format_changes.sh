#!/bin/sh
set -e

# select commmitted python and xml files (not deleted)
pythonFilesToFormat="$(git --no-pager diff --name-status --no-color --cached | awk '$1 ~ /^R[0-9]+$/ && $3 ~ /\.py/ {print $3; next}; $1 != "D" && $2 ~ /\.py/ {print $2}')"
xmlFilesToFormat="$(git --no-pager diff --name-status --no-color --cached | awk '$1 ~ /^R[0-9]+$/ && $3 ~ /\.xml/ {print $3; next}; $1 != "D" && $2 ~ /\.xml/ {print $2}')"

echo "Python files to format:"
echo "$pythonFilesToFormat"
for sourceFilePath in $pythonFilesToFormat
do
  poetry run black "$(pwd)/$sourceFilePath"
  git add $sourceFilePath
done

echo "XML files to format:"
echo "$xmlFilesToFormat"
for sourceFilePath in $xmlFilesToFormat
do
  poetry run xmlformat --indent 4 --eof-newline --overwrite --selfclose --infile "$(pwd)/$sourceFilePath"
  git add $sourceFilePath
done

printf "\n"
