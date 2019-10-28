import numpy as np
from collections import defaultdict, deque

START_SYMBOL = '<s>'
STOP_SYMBOL = '</s>'
LOG_PROB_OF_ZERO = -1000

def viterbi(words, taglist, known_words, q_values, e_values):
'''Return the most probable POS tag sequence for the input.

    Args:

'''
    tagged = []

    # pi[(k, u, v)]: max probability of a tag sequence ending in tags u, v at position k
    # bp[(k, u, v)]: backpointers to recover the argmax of pi[(k, u, v)]
    pi = defaultdict(float)
    bp = {}

    # Initialization
    pi[(0, START_SYMBOL, START_SYMBOL)] = 0.0

    # Define tagsets S(k)
    def S(k):
        if k in (-1, 0):
            return {START_SYMBOL}
        else:
            return taglist

    # Number of words
    n = len(words)

    # The Viterbi algorithm
    for k in range(1, n+1):
        for u in S(k-1):
            for v in S(k):
                max_score = float('-Inf')
                max_tag = None
                for w in S(k - 2):
                    if e_values.get((words[k-1], v), 0) != 0:
                        score = pi.get((k-1, w, u), LOG_PROB_OF_ZERO) + \
                                q_values.get((w, u, v), LOG_PROB_OF_ZERO) + \
                                e_values.get((words[k-1], v))
                        if score > max_score:
                            max_score = score
                            max_tag = w
                pi[(k, u, v)] = max_score
                bp[(k, u, v)] = max_tag

    max_score = float('-Inf')
    u_max, v_max = None, None
    for u in S(n-1):
        for v in S(n):
            score = pi.get((n, u, v), LOG_PROB_OF_ZERO) + \
                    q_values.get((u, v, STOP_SYMBOL), LOG_PROB_OF_ZERO)
            if score > max_score:
                max_score = score
                u_max = u
                v_max = v

    tag = deque()
    tags.append(v_max)
    tags.append(u_max)

    for i, k in enumerate(range(n-2, 0, -1)):
        tags.append(bp[(k+2, tags[i+1], tags[i])])
    tags.reverse()

    tagged_sentence = deque()
    for j in range(0, n):
        tagged_sentence.append(words[j] + '/' + tags[j])
    tagged_sentence.append('\n')
    tagged.append(' '.join(tagged_sentence))

    return tagged

def main():
    print()

if __name__=='__main__':
    main()