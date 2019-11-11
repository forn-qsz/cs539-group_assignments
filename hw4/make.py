from sys import stdin
from collections import defaultdict

epron = ['W', 'AY', 'N']
jpron = ['W', 'A', 'I', 'N']

#epron = ['AY', 'N']
#jpron = ['I', 'N']

#epron = ['T','O']
#jpron = ['O', 'T', 'O']

#epron = ['B', 'OW', 'T']
#jpron = ['B', 'O', 'O', 'T', 'O']

#epron = ['T', 'EH', 'S', 'T']
#jpron = ['T', 'E', 'S','U', 'T', 'O']
l = []
def enum(epron, jpron, path, count=0):
    if(len(epron) == 1):
        k = []
        for i in range(len(jpron)):
            k.append(jpron[i])
        path[(epron[0], count)] = k
        l.append(path.copy())
        #print (path)
        count = 0
    else:
        for i in range(len(jpron) - len(epron) + 1):
            k = []
            for j in range(i + 1):
                k.append(jpron[j])
            path[(epron[0], count)] = k
            enum(epron[1:], jpron[i+1:], path, count + 1)

path = defaultdict(dict)
enum(epron, jpron, path)

#initialize
all_path = {}
for p in l:
    tmp = []
    for j in p:
        #print(j)
        for jp in p[j]:
            #print(jp, j[1]+1)
            tmp.append(j[1]+1)
    all_path[tuple(tmp)] = float(0)
for k in all_path:
    all_path[k] = 1/len(all_path)
print(all_path)

ek_pair = {}
count_dic = {}

#dic = {'W': {'W' : 0.0, 'WA' : 0.0}, 'AY': {'A' : 0.0, 'AI', 'I':0.0}, 'N':
