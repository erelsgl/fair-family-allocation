#!bash
# Run all the doctests in this folder

for file in *.py
do
    echo
    echo "Processing $file"
    python3 $file
done
