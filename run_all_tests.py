#!python3
# Run all the doctests in this folder

import glob, importlib, os

for file in glob.iglob("*.py"):
    if file==__file__: continue
    print("\nProcessing "+file)
    os.system("python "+file)
    # importlib.import_module(file.replace(".py",""))

