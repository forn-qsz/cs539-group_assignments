import sys
import os

filename = 'test.txt.space_restored.nlm.base'

with open(filename, 'r') as fin:
    with open(filename + '.new', "w") as fout:
        for line in fin:
            fout.write(line.replace('<s>', '').replace('</s>', '').replace(' ', '').replace('_', ' '))