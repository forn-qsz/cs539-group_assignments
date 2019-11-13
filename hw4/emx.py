from sys import stdin
from collections import defaultdict
from collections import Counter

epron = []
jpron = []

all_path = []
fractional_counts = []
forward = defaultdict(lambda: defaultdict(float))
backward = defaultdict(lambda: defaultdict(float))

def multiplyList(myList) :
    result = 1
    for x in myList:
         result = result * x
    return result

def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]

def print_table(eprons, jprons, table):
    for jp in jprons:
        print('\t' + jp)
    for i in range(len(eprons)):
        print(eprons[i], end='\t')
        for ep in table[i]:
            print(ep, end='\t')

def em_forward(eprons, jprons, table):
    n, m = len(eprons), len(jprons)
    forward['0']['0'] = 1
    # consider each epron
    for i in range(0, n):
        epron = eprons[i]
        # consider each start index for distributing
        # j: the start index
        print(i, list(forward[str(i)].keys()))
        for j in list(forward[str(i)].keys()):
            #print(i, j)
            # m-j: the maximum number of jprons that the current epron can distribute
            for k in range(1, min(m-int(j), 3)+1):
                jseg = ''.join(jprons[int(j):int(j)+k])
                if jseg in table[epron].keys():
                    score = forward[str(i)][j] * table[epron][jseg]
                else:
                    score = 0
                forward[str(i+1)][str(int(j)+k)] += score

def em_backward(eprons, jprons, table):
    n, m = len(eprons), len(jprons)
    backward[str(n+1)][str(m+1)] = 1
    # consider each epron
    for i in range(n+1, 1, -1):
        epron = eprons[i-2]
        #print(epron)
        # consider each start index for distributing
        # j: the start index
        print(i, list(backward[str(i)].keys()))
        for j in list(backward[str(i)].keys()):

            # m-j: the maximum number of jprons that the current epron can distribute
            for k in range(1, min(int(j)-1, 3)+1):
                #print(i, j)
                print(int(j)-k-1,int(j)-1)
                jseg = ''.join(jprons[int(j)-k-1:int(j)-1])
                #print(jseg)
                if jseg in table[epron].keys():
                    score = backward[str(i)][j] * table[epron][jseg]
                else:
                    score = 0
                backward[str(i-1)][str(int(j)-k)] += score
    #print(backward)
def enum(epron, jpron, path, ek_pair, pair, count=0):
    if(len(epron) == 1):
        k = []
        for i in range(len(jpron)):
            k.append(jpron[i])
        path[(epron[0], count)] = ''.join(k)
        ek_pair[epron[0]][''.join(k)] = 0
        all_path[pair].append(path.copy())
        count = 0
    else:
        for i in range(len(jpron) - len(epron) + 1):
            k = []
            for j in range(i + 1):
                k.append(jpron[j])
            path[(epron[0], count)] = ''.join(k)
            ek_pair[epron[0]][''.join(k)] = 0
            enum(epron[1:], jpron[i+1:], path, ek_pair, pair, count + 1)
def ini_ek(ek_pair):
    for e in ek_pair:
        for j in ek_pair[e]:
            ek_pair[e][j] = 0
def uni_ek(ek_pair):
    for e in ek_pair:
        for j in ek_pair[e]:
            ek_pair[e][j] = 1/len(ek_pair[e])
    return ek_pair

def em(fractional_counts, ek_pair):
    iterative = 0
    corpus_prob = [0]
    #e_step
    while(1 - corpus_prob[iterative] > 0.01 and iterative < 20):
        ini_ek(ek_pair)
        for i in range(len(all_path)):
            for j in range(len(all_path[i])):
                for k in all_path[i][j]:
                    #print(k[0], all_path[i][j][k])
                    ek_pair[k[0]][all_path[i][j][k]] += fractional_counts[i][j]['prob']

        for e in ek_pair:
            p_ej = []
            for j in ek_pair[e]:
                p_ej.append(ek_pair[e][j])
            p_ej = normalize(p_ej)
            #print(p_ej)
            ind = 0
            for j in ek_pair[e]:
                ek_pair[e][j] = p_ej[ind]
                ind += 1
        #print(ek_pair)

        c_prob = []
        for i in range(len(fractional_counts)):
            p_xz = []
            for j in range(len(fractional_counts[i])):
                prob = float(1)
                for k in range(len(epron[i])):
                    jp = fractional_counts[i][j]['path'][k]
                    #print(epron[i][k] ,jp)
                    #print(ek_pair[epron[i][k]][jp])
                    prob *= ek_pair[epron[i][k]][jp]
                fractional_counts[i][j]['prob'] = prob  #regenerate
                #print(fractional_counts[i][j]['prob'])
                p_xz.append(prob)
            c_prob.append(sum(p_xz))
            p_xz = normalize(p_xz)
            #print(p_xz)
            for l in range(len(fractional_counts[i])):
                fractional_counts[i][l]['prob'] = p_xz[l]
        #print(fractional_counts)
        #m_step
        corpus_prob.append(multiplyList(c_prob))
        #print(corpus_prob)

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
    if(index % 2 == 0):
        epron.append(line.split())
    elif(index % 2 == 1):
        jpron.append(line.split())
    index += 1

ek_pair = {}
for i in epron:
    for j in i:
        ek_pair[j] = {}
for i in range(len(epron)):
    path = defaultdict(dict)
    all_path.append([])
    enum(epron[i], jpron[i], path, ek_pair, i)
#enum(epron, jpron, path, ek_pair)
#print(ek_pair)
#print(all_path[1])
#initialize fractional_counts

for i in range(len(all_path)):
    fractional_counts.append([])
    for j in range(len(all_path[i])):
        tmp = []
        for k in all_path[i][j]:
            tmp.append(all_path[i][j][k])
        fractional_counts[i].append({})
        fractional_counts[i][j] = {'path' : tuple(tmp), 'prob' : float(0)}
for i in range(len(fractional_counts)):
    for j in range(len(fractional_counts[i])):
        fractional_counts[i][j]['prob'] = 1/len(fractional_counts[i])
#ini_ek(ek_pair)
#print(ek_pair)
em_forward(epron[0], jpron[0], uni_ek(ek_pair))
em_backward(epron[0], jpron[0], uni_ek(ek_pair))
#print(backward)
#em(fractional_counts, ek_pair)
#print(fractional_counts)
