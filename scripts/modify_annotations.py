#!/usr/bin/env python
from __future__ import print_function
import sys
import os

def main(input_directory, start_timestamp):
    inputfile = os.path.join(input_directory, 'annotations.txt')
    if os.path.exists(inputfile):
        f = open(inputfile, 'r')
        lines = f.readlines()
        f.close()

        header = False
        f = open(inputfile, 'w')
        for line in lines:
            if not header:
                print(line, file=f)
                header = True
                continue

            parts = line.split()
            for i in range(1, len(parts)):
                parts[i] = float(parts[i]) - start_timestamp

            print(" ".join(map(str, parts)), file=f)

        f.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: %s <peers-directory> <experiment start timestamp>" % (sys.argv[0]))
        print(sys.argv, file=sys.stderr)

        exit(1)

    main(sys.argv[1], int(sys.argv[2]))
