import operator
import sys
from sys import stdin

def viterbi(observe, states, start_probs, tran_probs, emit_probs):
    v = [{}, {}]
    for st1 in states:
        if(st1 == '<s>'):
            for st2 in states:
                if(st2 != '<s>' and observe[0] in emit_probs[st2]):
                    state = (st1, st2)
                    v[0][state] = {"prob": tran_probs[('<s>', '<s>')][state] * emit_probs[st2][observe[0]], "prev": ('<s>','<s>')}
    for st in states:
        if (st != '<s>' and observe[1] in emit_probs[st]):
            for prev_st in v[0]:
                state = (prev_st[1], st)
                prev = prev_st
                probs =  v[0][prev_st]['prob'] * tran_probs[prev_st][state]
                v[1][state] = {"prob": probs * emit_probs[st][observe[1]], "prev": prev}
    for i in range(2, len(observe)):
        v.append({})
        for st in states:
            if (st != '<s>' and observe[i] in emit_probs[st]):
                for prev_st in v[i-1]:
                    state = (prev_st[1] ,st)
                    max_probs = -1
                    prev = 'None'
                    for prev2_st in v[i-2]:
                        prev_state = (prev2_st[1], prev_st[1])
                        tmp_probs = v[i-1][prev_state]['prob'] * tran_probs[prev_state][state]
                        if tmp_probs >= max_probs:
                            max_probs = tmp_probs
                            prev = prev_state
                    if(max_probs != -1):
                        v[i][state] = {"prob": max_probs* emit_probs[st][observe[i]], "prev": prev}

    for prev_st in v[-1]:
        #print(prev_st)
        v[-1][prev_st]['prob'] *= tran_probs[prev_st][(prev_st[1], '</s>')]

    opt = []
    max_prob = max(value["prob"] for value in v[-1].values())
    previous = None

     # Get most probable state and its backtrack
    for st, data in v[-1].items():
        if data["prob"] == max_prob:
            opt.append(st[1])
            previous = st
            break

    for t in range(len(v) - 2, -1, -1):
        opt.insert(0, v[t + 1][previous]["prev"][1])
        previous = v[t + 1][previous]["prev"]
    print(' '.join(opt), max_prob)

def preprocess(observe):
    combine = []
    vowels = ['A', 'E', 'I', 'O', 'U']
    skip = False
    for i in range(len(observe)):
        if(skip):
            skip = False
            continue
        else:
            if(i+1 == len(observe)):
                combine.append(observe[i])
                break
            one = True
            for st in states:
                if(st != '<s>' and observe[i]+observe[i+1] in emit_probs[st]):
                    if(((observe[i] in vowels or (i-1 > -1 and observe[i-1] in vowels)) and observe[i+1] in vowels) or ((i+2) == len(observe))):
                        combine.append(observe[i]+observe[i+1])
                        one = False
                        skip = True
                        break
            if(one):
                combine.append(observe[i])
    return tuple(combine)

emit_probs = {}
tran_probs = {}
start_probs = {('<s>', '<s>') : 1.0}
states = []


#data
for line in open(sys.argv[1]):
    l = line.split()
    if((l[0],l[1]) not in tran_probs):
        tran_probs[(l[0], l[1])] = {(l[1],l[3]) : float(l[5])}
        states.append(l[0])
    else:
        tran_probs[(l[0], l[1])][(l[1],l[3])] = float(l[5])
states = tuple(set(states))
#emit_probs
for line in open(sys.argv[2]):
    l = line.split()
    if(l[0] not in emit_probs):
        if (l[3] == '#'):
            emit_probs[l[0]] = {l[2] : float(l[4])}
        elif (l[4] == '#'):
            emit_probs[l[0]] = {l[2] + l[3] : float(l[5])}
        else:
            emit_probs[l[0]] = {l[2] + l[3] + l[4] : float(l[6])}
    else:
        if (l[3] == '#'):
            emit_probs[l[0]][l[2]] = float(l[4])
        elif (l[4] == '#'):
            emit_probs[l[0]][l[2] + l[3]] = float(l[5])
        else:
            emit_probs[l[0]][l[2] + l[3] + l[4]] = float(l[6])
#main
for line in stdin:
    observe = tuple(line.split())
    observe = preprocess(observe)
    #print(observe)
    viterbi(observe, states, start_probs ,tran_probs, emit_probs)
