import operator
import sys



def viterbi(observe, states, start_probs, tran_probs, emit_probs):
    v = [{}]
    #print(start_probs)
    #print(states)
    for st1 in states:
        if(st1 == '<s>'):
            for st2 in states:
                if(st2 != '<s>' and observe[0] in emit_probs[st2]):
                    state = (st1, st2)
                    v[0][state] = {"prob": tran_probs[('<s>', '<s>')][state] * emit_probs[st2][observe[0]], "prev": ('<s>','<s>')}
    #print(v[0])

    for i in range(1, 5):
        v.append({})
        for st in states:
            if (st != '<s>' and observe[i] in emit_probs[st]):
                max_probs = -1
                prev = 'None'
                next = ()
                for prev_st in v[i-1]:
                    state = (prev_st[1], st)
                    tmp_probs =  v[i-1][prev_st]['prob'] * tran_probs[prev_st][state]
                    if tmp_probs >= max_probs:
                        max_probs = tmp_probs
                        prev = prev_st
                        next = state
                #prev_state =
                if(max_probs != -1):
                    v[i][next] = {"prob": max_probs * emit_probs[st][observe[i]], "prev": prev}
'''
    for st in states:
        if(st == '<s>' and ob)
            max_probs = -1
            prev = 'None'
            next = ()
            for prev_st in v[i-1]:
                state = (prev_st[1], st)
                tmp_probs =  v[i-1][prev_st]['prob'] * tran_probs[prev_st][state]
                if tmp_probs >= max_probs:
                    max_probs = tmp_probs
                    prev = prev_st
                    next = state
            #prev_state =
            if(max_probs != -1):
                v[i][next] = {"prob": max_probs * emit_probs[st][observe[i]], "prev": prev}
'''
    for i in range(len(v)):
        print(v[i])
        print("-----------")

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
    print(opt, max_prob)
    #print(' '.join(opt), max_prob)


emit_probs = {}
tran_probs = {}
start_probs = {('<s>', '<s>') : 1.0}
states = []
observe = ('P', 'I', 'A', 'N', 'O', '</s>')
#tran_probs
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
viterbi(observe, states, start_probs ,tran_probs, emit_probs)
