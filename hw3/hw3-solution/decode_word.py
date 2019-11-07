import sys
from collections import defaultdict

START, END = ("<s>", "</s>")

# eword-epron.data
wepron = defaultdict(float)
# eword.wfsa
ewords = defaultdict(float)
# epron-jpron.probs
pjpron = defaultdict(lambda: defaultdict(float))
# tags
eprons = set([START, END])

def backtrack(back, i, e1, e):
    if i == 1:
        return [e]
    elif i <= 0:
        return []
    e2, j = back[i][e1][e]
    return backtrack(back, i-j, e2, e1) + [e]

def multi_dict(dic, list, value):
    if not dic[list[0]]:
        dic[list[0]] = defaultdict(float)

    if len(list) == 1:
        dic[list[0]]['result'] = value
        dic[list[0]]['prob'] = ewords[value]
        return dic
    
    if len(list) == 2:
        if not dic[list[0]][list[1]]:
            dic[list[0]][list[1]] = defaultdict(float)
        dic[list[0]][list[1]]['result'] = value
        dic[list[0]][list[1]]['prob'] = ewords[value]
        return dic

    dic = multi_dict(dic[list[0]], list[1:], value)

def dig_dict(dic, list):
    if len(list) > 1:
        return dig_dict(dic[list[0]], list[1:])
    else:
        return dic[list[0]]

with open(sys.argv[1]) as f1, open(sys.argv[2]) as f2, open(sys.argv[3]) as f3:
    # eword.wfsa
    for line in f1:
        if len(line) > 2:
            l = line.split(' ', 3)
            eword, prob = l[2], l[3][:len(l[3])-3]
            #_, _, eword, prob = line.split(' ', 3)
            ewords[eword] = float(prob)
    # eword-epron.data
    for line in f2:
        l = line.split(' ', 1)
        eword, epron_list = l[0], l[1].rstrip('\n').split(' ')
        multi_dict(wepron, epron_list, eword)
    # epron-jpron.probs
    for line in f3:
        l = line.split(':')
        epron = l[0].strip()
        l = l[1].split('#')
        jprons = l[0].strip()
        pjpron[jprons][epron] = float(l[1].strip())
        eprons.add(epron)

for line in sys.stdin:
    best = defaultdict(float)
    back = defaultdict(float)
    trace = []

    jprons_input = line.split()

    for i in range(0, len(jprons_input)):
        best_e = None
        for j in range(i+1, min(i+4, len(jprons_input))):
            jprons = ' '.join(jprons_input[i:j])
            # each epron
            # <s> <s> *P*
            for e in pjpron[jprons]:
                current = trace + [e]
                print(current)
                tmp_dict = dig_dict(wepron, current)
                if tmp_dict:
                    score = pjpron[jprons][e]
                    if score > best[i]:
                        best[i] = score
                        back[i] = (tmp_dict['result'], j)
                        best_e = e
        if len(trace) > i:
            trace.pop()
        trace.append(best_e)