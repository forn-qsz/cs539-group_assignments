import sys
sys.path.insert(1, '../')
from nlm import NLM
from math import log

path = './test.txt.nospaces'

if __name__ == "__main__":
    
    NLM.load("huge")

    f = open(path,'r')

    h = NLM()

    for line in f.readlines():
        beam = [(0, h)]
        b = 20
        for c in list(line[:-1]) + ["</s>"]:
            newbeam = []
            for score, state in beam:
                newscore = score + log(state.next_prob(c))
                newstate = state + c
                newbeam.append((newscore, newstate))

                newscore = score + log(state.next_prob("_")) + log((state+"_").next_prob(c))
                newstate = state + '_' + c
                newbeam.append((newscore, newstate))

            beam = sorted(newbeam, reverse = True)[:b]

        score, state = beam[0]
        print(" ".join(state.history).replace('<s>', '').replace('</s>', '').replace(' ', '').replace('_', ' '))
