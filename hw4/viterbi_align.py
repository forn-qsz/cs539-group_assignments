from sys import stdin
from collections import defaultdict
import sys

epron = []
jpron = []
all_path = []
ek_pair = defaultdict(lambda: defaultdict(float))

def enum(epron, jpron, path, pair, count=0):
    if(len(epron) == 1):
        k = []
        for i in range(len(jpron)):
            k.append(jpron[i])
        path[(epron[0], count)] = ' '.join(k)
        all_path[pair].append(path.copy())
        count = 0
    else:
        for i in range(len(jpron) - len(epron) + 1):
            k = []
            for j in range(i + 1):
                k.append(jpron[j])
            path[(epron[0], count)] = ' '.join(k)
            enum(epron[1:], jpron[i+1:], path, pair, count + 1)
#read
with open(sys.argv[1]) as f1:
    for line in f1:
        l = line.split(':')
        e = l[0].strip()
        l = l[1].split('#')
        j = l[0].strip()
        p = float(l[1].strip())
        ek_pair[e][j] = p
index = 0
for line in stdin:
    if(index % 3 == 0):
        epron.append(line.split())
    elif(index % 3 == 1):
        jpron.append(line.split())
    index += 1
#finding all path
for i in range(len(epron)):
    path = defaultdict(dict)
    all_path.append([])
    enum(epron[i], jpron[i], path, i)
#viterbi
for i in range(len(all_path)):
    max = -1
    max_index = -1
    print(' '.join(epron[i]))
    print(' '.join(jpron[i]))
    for j, path in enumerate(all_path[i]):
        prob = 1
        for jp in path:
            if(ek_pair[jp[0]][path[jp]]):
                prob *= ek_pair[jp[0]][path[jp]]
            else:
                prob *= 0.001
        if(prob > max):
            max = prob
            max_index = j
    for key, value in all_path[i][max_index].items():
        for jj in value.split(' '):
            print(key[1]+1, end=' ')
    print('')
