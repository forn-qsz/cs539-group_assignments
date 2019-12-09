import sys
sys.path.insert(1, '../')
from nlm import NLM
from math import log

path = './test.txt.novowels'

if __name__ == "__main__":
    NLM.load("base")

    f = open(path,'r')

    VOWELS = ['a', 'e', 'i', 'o', 'u']
    MAX_REPEAT = 2
    h = NLM()

    for line in f.readlines():
        line = line.replace(' ', '_')
        beam = [(0, h)]
        b = 40
        for c in list(line[:-1]) + ["</s>"]:
            newbeam = []
            prev = [beam]
            for i in range(MAX_REPEAT+1):
                tmp = []
                for score, state in prev[-1]:
                    newscore = score + log(state.next_prob(c))
                    newstate = state + c
                    newbeam.append((newscore, newstate))
                    if i <= MAX_REPEAT:
                        for vowel in VOWELS:
                            newscore = score + log(state.next_prob(vowel))
                            newstate = state + vowel
                            tmp.append((newscore, newstate))
                prev.append(tmp)

            beam = sorted(newbeam, reverse = True, key = lambda x : x[0])[:b]

        score, state = beam[0]
        print(" ".join(state.history).replace('<s>', '').replace('</s>', '').replace(' ', '').replace('_', ' '))
