import sys
import heapq
from collections import defaultdict

START, END = ("<s>", "</s>")
K = int(sys.argv[1])

def backtrack(back, i, e1, e, k):
    if i == 1:
        return [e]
    elif i <= 0:
        return []

    idx2, e2, j = back[i][e1][e][k]
    return backtrack(back, i-j, e2, e1, idx2) + [e]

p3epron = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
pjpron = defaultdict(lambda: defaultdict(float))
eprons = set([START, END])
with open(sys.argv[2]) as f1, open(sys.argv[3]) as f2:
    for line in f1:
        l = line.split()
        p3epron[l[0]][l[1]][l[3]] = float(l[5])
    for line in f2:
        l = line.split(':')
        epron = l[0].strip()
        l = l[1].split('#')
        jprons = l[0].strip()
        pjpron[jprons][epron] = float(l[1].strip())
        eprons.add(epron)

for line in sys.stdin:
    best = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    back = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    jprons_input = [START] + line.split() + [END] * 2
    best[0][START][START] = [-1.0]
    pjpron[END][END] = 1.0
    for e in eprons:
        p3epron[e][END][END] = 1.0
        if e in p3epron[START][START] and e in pjpron[jprons_input[1]]:
            best[1][e][START] = [-1.0 * p3epron[START][START][e] * pjpron[jprons_input[1]][e]]
    for i in range(2, len(jprons_input)):
        jprons = [jprons_input[i], jprons_input[i - 1] + ' ' + jprons_input[i],
                  jprons_input[i - 2] + ' ' + jprons_input[i - 1] + ' ' + jprons_input[i]]
        e0prons = []
        for jpron in jprons:
            e0prons += pjpron[jpron].keys()
        e0prons = set(e0prons)
        e2prons = []
        for j in range(1, 4):
            e2prons += best[i - j].keys()
        e2prons = set(e2prons)
        for e in e0prons:
            for e1 in e2prons:
                temp_score = []
                temp_trace = []
                idx = defaultdict(lambda : defaultdict(int))
                for j in range(1, 4):
                    if e1 in best[i - j]:
                        for e2 in best[i - j][e1]:
                            if e in p3epron[e2][e1] and e in pjpron[jprons[j - 1]]:
                                temp_score.append((best[i - j][e1][e2][idx[j][e2]] * p3epron[e2][e1][e] *
                                                   pjpron[jprons[j - 1]][e], len(temp_trace)))
                                temp_trace.append((idx[j][e2], e2, j))
                                idx[j][e2] += 1
                heapq.heapify(temp_score)
                for k in range(K):
                    if len(temp_score) == 0:
                        break
                    m_score = heapq.heappop(temp_score)
                    m_idx, e2, j = temp_trace[m_score[1]]
                    best[i][e][e1].append(m_score[0])
                    back[i][e1][e].append((m_idx, e2, j))
                    if idx[j][e2] < len(best[i-j][e1][e2]):
                        heapq.heappush(temp_score, (best[i-j][e1][e2][idx[j][e2]] * p3epron[e2][e1][e] *
                                               pjpron[jprons[j - 1]][e], len(temp_trace)))
                        temp_trace.append((idx[j][e2], e2, j))
                        idx[j][e2] += 1

    for k in range(K):
        result = backtrack(back, len(jprons_input) - 1, END, END, k)[:-2]
        print ' '.join(result), '#', "%.6e" % -best[len(jprons_input)-1][END][END][k]

