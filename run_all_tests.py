#!python3
# Run all the doctests in this folder

import glob, importlib, os, sys

for file in glob.iglob("*.py"):
    if file==__file__: continue
    print("\nProcessing "+file)
    # print(sys.executable+" "+file)
    os.system('"'+sys.executable+'"'+" "+file)
    # importlib.import_module(file.replace(".py",""))

