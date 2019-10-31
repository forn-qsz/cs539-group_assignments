import operator
from sys import stdin



states = ('pro', 'n', 'aux', 'det','v', 'prep','conj', 'f')
start_probs = { 'pro': 0.25, 'n': 0.25, 'aux': 0.25, 'det': 0.25}
tran_probs = {'pro': {'v': 0.25, 'conj': 0.25, 'aux': 0.25, 'f': 0.25},
              'det': {'n': 1.0},
              'n':   {'n': 0.1666666666, 'conj': 0.1666666666, 'prep': 0.1666666666, 'aux': 0.1666666666, 'verb':0.1666666666,'f': 0.1666666666},
              'v':   {'pro': 0.1428571428, 'n': 0.1428571428, 'conj': 0.1428571428, 'prep': 0.1428571428, 'aux': 0.1428571428,'det' : 0.1428571428, 'f': 0.1428571428},
              'conj':{'det': 0.25, 'n': 0.25, 'v': 0.25, 'pro':0.25},
              'prep':{'det': 0.3333333333, 'n': 0.3333333333, 'aux': 0.3333333333},
              'aux': { 'v': 0.3333333333, 'prep': 0.3333333333, 'f': 0.3333333333}}
emit_probs = { 'I' :{'pro':0.5, 'n':0.5},
    'hope':{'v':0.5, 'n':0.5},
    'that':{'conj':0.25, 'pro':0.25, 'adj':0.25, 'adv':0.25},
    'this':{'pro':0.3333333333, 'adj':0.3333333333, 'adv':0.3333333333},
    'works':{'n':0.3333333333, 'v':0.3333333333, 'adj':0.3333333333},
    'They':{'pro': 1.0},
    'can':{'aux': 0.3333333333, 'v':0.3333333333, 'n':0.3333333333},
    'fish':{'v':0.5, 'n':0.5},
    'A':{'prep':0.3333333333, 'det':0.3333333333, 'n':0.3333333333},
    'panda': { 'n': 1.0 },
	'eats': { 'n': 0.5, 'v': 0.5 },
	'shoots': { 'n': 0.5, 'v': 0.5 },
	'and': { 'conj': 1.0 },
	'leaves': { 'n': 0.5, 'v': 0.5 },
    'a':{'prep':0.3333333333, 'det':0.3333333333, 'n':0.3333333333},
    'Time':{'v': 0.3333333333, 'n':0.3333333333, 'adj':0.3333333333},
    'flies':{'v':0.5, 'n':0.5},
    'like':{'v':0.1666666666, 'prep':0.1666666666, 'adj':0.1666666666, 'n':0.1666666666, 'adv':0.1666666666, 'aux':0.1666666666},
    'an':{'an':0.5, 'det': 0.5},
    'arrow':{'v':0.5, 'n':0.5},
    '</s>' : {'f':1}}




def viterbi(observe, states, start_probs, tran_probs, emit_probs):
    v = [{}]
    for st in states:
        if st in start_probs and st in emit_probs[observe[0]]:
            v[0][st] = {"prob": start_probs[st] * emit_probs[observe[0]][st], "prev": None}
        else:
            v[0][st] = {"prob": 0.0, "prev":None}
    #print(v[0])


    for i in range(1, len(observe)):
        v.append({})
        for st in states:
            max_probs = -1
            prev = 'None'
            for prev_st in states:
                if prev_st in tran_probs and st in tran_probs[prev_st]:
                    tmp_probs =  v[i-1][prev_st]['prob'] * tran_probs[prev_st][st]
                    #print(tmp_probs)
                    if tmp_probs >= max_probs:
                        max_probs = tmp_probs
                        prev = prev_st
                #prev_state =
            if st in emit_probs[observe[i]]:
                v[i][st] = {"prob": max_probs * emit_probs[observe[i]][st], "prev": prev}
            else:
                v[i][st] = {"prob": 0.0, "prev":prev}
            #if(i == 3):
                #print(st, max_probs)
        #print("----------")
            #print(st, prev, max_probs)
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
#observe = ('I', 'hope', 'that', 'this', 'works')

for line in stdin:
    observe = ()
    word = line.split()
    observe = tuple (word)
    #print (observe)
    viterbi(observe, states, start_probs, tran_probs, emit_probs)
#viterbi(observe, states, start_probs, tran_probs, emit_probs)
