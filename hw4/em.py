from sys import stdin
from collections import defaultdict
from collections import Counter


epron = []
jpron = []

#epron = ['B', 'OW', 'T']
#jpron = ['B', 'O', 'O', 'T', 'O']

#epron = ['T', 'EH', 'S', 'T']
#jpron = ['T', 'E', 'S','U', 'T', 'O']
all_path = []

def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]

def enum(epron, jpron, path, ek_pair, count=0):
    if(len(epron) == 1):
        k = []
        for i in range(len(jpron)):
            k.append(jpron[i])
        path[(epron[0], count)] = ''.join(k)
        ek_pair[epron[0]][''.join(k)] = 0
        all_path.append(path.copy())
        #print (path)
        count = 0
    else:
        for i in range(len(jpron) - len(epron) + 1):
            k = []
            for j in range(i + 1):
                k.append(jpron[j])
            path[(epron[0], count)] = ''.join(k)
            ek_pair[epron[0]][''.join(k)] = 0
            enum(epron[1:], jpron[i+1:], path, ek_pair, count + 1)
def ini_ek(ek_pair):
    for e in ek_pair:
        for j in ek_pair[e]:
            ek_pair[e][j] = 0

def em(fractional_counts, ek_pair):
    iterative = 0
    corpus_prob = [0]
    #e_step
    while(1 - corpus_prob[iterative] > 0.01):
        ini_ek(ek_pair)
        for i in range(len(all_path)):
            for j in all_path[i]:
                ek_pair[j[0]][all_path[i][j]] += fractional_counts[i]['prob']
        #print(ek_pair)
        p_xz = []
        for i in range(len(fractional_counts)):
            prob = float(1)
            for j in range(len(epron)):
                jp = fractional_counts[i]['path'][j]
                #print(ek_pair[epron[j]][jp])
                prob *= ek_pair[epron[j]][jp]
            fractional_counts[i]['prob'] = prob  #regenerate
            p_xz.append(prob)
        #print(fractional_counts)
        #m_step
        corpus_prob.append(sum(p_xz))
        p_xz = normalize(p_xz)

        for i in range(len(fractional_counts)):
            fractional_counts[i]['prob'] = p_xz[i]
        #print table
        non_zeros = 0
        print("iteration " + str(iterative) + '    ----- corpus prob = ' + str(corpus_prob[iterative]))
        for e in ek_pair:
            l = []
            l.append(e + '|->   ')
            for j in ek_pair[e]:
                if (ek_pair[e][j] > 0.01):
                    l.append(j + ': ' + str(round(ek_pair[e][j], 2)) + '    ')
                    non_zeros += 1
            print(''.join(l))
        print('nonzeros = ' + str(non_zeros))
        iterative += 1



index = 0
for line in stdin:
    #print(line)
    if(index % 3 == 0):
        epron = line.split()
    elif(index % 3 == 1):
        jpron = line.split()
    index += 1
path = defaultdict(dict)
ek_pair = {}
for i in epron:
    ek_pair[i] = {}
enum(epron, jpron, path, ek_pair)

#initialize fractional_counts
fractional_counts = []
for i in range(len(all_path)):
    tmp = []
    for j in all_path[i]:
        tmp.append(all_path[i][j])
    fractional_counts.append({})
    fractional_counts[i] = {'path' : tuple(tmp), 'prob' : float(0)}
for i in range(len(fractional_counts)):
    fractional_counts[i]['prob'] = 1/len(fractional_counts)
em(fractional_counts, ek_pair)
#print(fractional_counts)
