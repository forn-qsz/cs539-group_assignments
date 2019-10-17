#!/usr/bin/env python

from collections import defaultdict, Counter
import sys

def train_char_lm(corpus, max_order=2):
    def normalize(counter):
        s = float(sum(counter.values()))
        return {c: cnt/s for c,cnt in counter.iteritems()}
    lms = defaultdict(lambda: defaultdict(Counter))    
    pad = "~" * (max_order-1)
    for line in corpus:
        line = pad + line.strip()
        for order in xrange(1, max_order+1):
            for i in xrange(len(line)-order+1):
                history, char = line[i:i+order-1], line[i+order-1]
                lms[order][history.upper()][char.upper()]+=1
    outlm = {o: {hist: normalize(chars) for hist, chars in lm.iteritems()} for o, lm in lms.iteritems()}
    return outlm

def print_lm(lms, prev, order):
    #kvs = [(k,v) for (k,v) in sorted(lm, reverse=True, key=lambda (_, v): v) if k == ' ' or k.isalpha()]
    weight = {}
    prevs = {}
    for o in xrange(1, order+1):
        weight[o] = 5**o # higher order is more important
        prevs[o] = prev[-o+1:] if o > 1 else ''
    base = lms[1]['']
    # interpolation-backoff
    kvs = [(k, sum(weight[o]*lms[o][prevs[o]].get(k,0) for o in xrange(1, order+1))) for k in base if k in letterspace] 
    #print kvs
    kvs = sorted(kvs, reverse=True, key=lambda(_, v): v)
    norm = sum(v for (k,v) in kvs)
    #print "\t".join("%s: %.4lf" % (k,v/norm) for (k,v) in kvs)
    #print '"%s",' % ("".join(k for (k,v) in kvs)),
    return "".join(k for (k,v) in kvs)
    #print ", ".join("%5lf" % (v/norm) for (k,v) in kvs)

#lm = train_char_lm(order=0)
#print_lm(lm[''])

if __name__ == "__main__":
    letterspace = set(map(chr, range(ord('A'), ord('Z')+1)) + [' ', '~', ''])
    try:
        order = int(sys.argv[1])
    except:
        order = 2

    corpus = sys.stdin.readlines()

    lms = train_char_lm(corpus, order)
    # for o in xrange(1, order+1):
    #     lms[o] = train_char_lm(corpus, order=o) # lower-order backoff
    final_lm = {}
    for prev in sorted(lms[order]): # potential bug: smoothing
        if set(prev) < letterspace:
            final_lm[prev] = print_lm(lms, prev, order)
            #print "\t// " + prev
    print (order, final_lm)
