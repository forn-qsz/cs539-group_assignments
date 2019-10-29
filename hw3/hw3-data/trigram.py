import operator
import sys



def viterbi(observe, states, start_probs, tran_probs, emit_probs):
    v = [{}]
    for st in states:
        if 
            v[0][st] = {"prob": max_probs, "prev": ('<s>','<s>')}
    '''
    #print(v[0])
    tmp = []
    for k in tran_probs[state]:
        tmp.append(k)
    states = tuple(tmp)
    #print(states)
    for i in range(1, 2):
        v.append({})
        max_probs = -1
        state = ('<s>','<s>')
        for st in states:
            if( st[1]!= '</s>' and observe[i] in emit_probs[st[1]]):

                tmp_probs = tran_probs[v[i-1]['state']][st] * emit_probs[st[1]][observe[i]]
                    #print(tmp_probs)
                tmp_state = st
                print(tmp_probs, tmp_state)
                #print(tmp_probs)
                if tmp_probs >= max_probs:
                    max_probs = tmp_probs
                    state = tmp_state
                #prev_state =
        v[i] = {"state" : state, "prob": max_probs, "prev": v[i-1]['state']}
    print(v[1])

    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in v[-1].values())
    previous = None
     # Get most probable state and its backtrack
    for st, data in v[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    for t in range(len(v) - 2, -1, -1):
        opt.insert(0, v[t + 1][previous]["prev"])
        previous = v[t + 1][previous]["prev"]
    print(' '.join(opt), max_prob)
'''
#observe = ('I', 'hope', 'that', 'this', 'works')

emit_probs = {}
tran_probs = {}
start_probs = {}
states = []
observe = ('P', 'I', 'A', 'N', 'O')
#tran_probs
for line in open(sys.argv[1]):
    l = line.split()
    if((l[0],l[1]) not in tran_probs):
        tran_probs[(l[0], l[1])] = {(l[1],l[3]) : float(l[5])}
        states.append((l[1],l[3]))
    else:
        tran_probs[(l[0], l[1])][(l[1],l[3])] = float(l[5])
    if ((l[0],l[1]) == ('<s>', '<s>')):
        start_probs[(l[1],l[3])] = float(l[5])

#print(tran_probs[('<s>', '<s>')][('<s>', 'AH')])
#emit_probs
for line in open(sys.argv[2]):
    l = line.split()
    if(l[0] not in emit_probs):
        if (l[3] == '#'):
            emit_probs[l[0]] = {l[2] : float(l[4])}
        elif (l[4] == '#'):
            emit_probs[l[0]] = {l[2] + " " + l[3] : float(l[5])}
        else:
            emit_probs[l[0]] = {l[2] + " " + l[3] + " " + l[4] : float(l[6])}
    else:
        if (l[3] == '#'):
            emit_probs[l[0]][l[2]] = float(l[4])
        elif (l[4] == '#'):
            emit_probs[l[0]][l[2] + " " + l[3]] = float(l[5])
        else:
            emit_probs[l[0]][l[2] + " " + l[3] + " " + l[4]] = float(l[6])
#print(start_probs)
#print(emit_probs)
#print(states)
#viterbi(observe, states, start_probs ,tran_probs, emit_probs)
