import sys
sys.path.insert(1, '../')
from nlm import NLM
from math import log

path = './test.txt.novowels'

if __name__ == "__main__":

    NLM.load("base")

    f = open(path,'r')

    vowels = ['a', 'e', 'i', 'o', 'u']
    repeat_times = 2

    h = NLM()

    for line in f.readlines():
        line = line.replace(' ', '_')
        beam = [(0, h)]
        b = 40
        for c in list(line[:-1]) + ["</s>"]:
            new_beam = []
            prev = [beam]
            for i in range(repeat_times+1):
                tmp = []
                for score, state in prev[-1]:
                    new_score = score + log(state.next_prob(c))
                    new_state = state + c
                    new_beam.append((new_score, new_state))
                    if i <= repeat_times:
                        for vowel in vowels:
                            new_score = score + log(state.next_prob(vowel))
                            new_state = state + vowel
                            tmp.append((new_score, new_state))
                prev.append(tmp)

            beam = sorted(new_beam, reverse = True, key = lambda x : x[0])[:b]

        score, state = beam[0]

        print(" ".join(state.history).replace('<s>', '').replace('</s>', '').replace(' ', '').replace('_', ' '))
