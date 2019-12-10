from nlm import NLM
import math
import sys

if __name__ == "__main__":

    NLM.load('base')
    p = 0
    l = 0
    
    for line in sys.stdin:
        line = line.strip().replace(" ", "_")
        h = NLM()

        for char in line:
            p += -math.log(h.next_prob(char), 2)
            h += char
        p += -math.log(h.next_prob("</s>"), 2)
        l += len(line) + 1

    entropy = p / l
    print('Entropy:', entropy)