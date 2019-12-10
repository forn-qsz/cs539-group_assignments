from nlm import NLM
import math
import sys
import random

if __name__ == "__main__":
    NLM.load('base')

    h = NLM("t o m _ a n d _ j e r r y")
    t = 0.5
    
    for _ in range(10):
        h = NLM("t o m _ a n d _ j e r r y")
        s = list(h.next_prob().keys())

        while s != "</s>":
            prob_dict = h.next_prob()

            for c, p in prob_dict.items():
                prob_dict = {c: p**(1/t)}

            [choice] = random.choices(s, [prob_dict[c] for c in s])

            if choice != "</s>":
                print(choice, end=' ')
                h += choice

            else:
                print(choice)
                h += choice
                h = NLM()
                break