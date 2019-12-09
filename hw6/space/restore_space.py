import sys
sys.path.insert(1, '../')
from nlm import NLM
from math import log

if __name__ == "__main__":
    NLM.load("base")

    for line in open(sys.argv[1]):
        h = NLM()
        beam = [(0, h)]
        b = 20
        for c in list(x) + ["</s>"]:
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
        #print("".join(state.history[1:-1]).replace("_", " "))
        print(" ".join(state.history))
