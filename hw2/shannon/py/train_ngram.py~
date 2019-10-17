from collections import defaultdict, Counter
import sys

def train_char_lm(order=1, f=sys.stdin):
    data = f.read()
    lm = defaultdict(Counter)
    pad = "~" * order
    data = pad + data
    for i in xrange(len(data)-order):
        history, char = data[i:i+order], data[i+order]
        lm[history.upper()][char.upper()]+=1
    def normalize(counter):
        s = float(sum(counter.values()))
        return [(c,cnt/s) for c,cnt in counter.iteritems()]
    outlm = {hist: normalize(chars) for hist, chars in lm.iteritems()}
    return outlm

def print_lm(lm):
    kvs = [(k,v) for (k,v) in sorted(lm, reverse=True, key=lambda (_, v): v) if k == ' ' or k.isalpha()]
    norm = sum(v for (k,v) in kvs)
    #print "\t".join("%s: %.4lf" % (k,v/norm) for (k,v) in kvs)
    print '"%s",' % ("".join(k for (k,v) in kvs)),
    #print ", ".join("%5lf" % (v/norm) for (k,v) in kvs)

#lm = train_char_lm(order=0)
#print_lm(lm[''])

lm = train_char_lm(order=1)
for prev in sorted(lm):
    if prev == ' ' or prev.isalpha():
        #print prev
        print_lm(lm[prev])
        print "\t// " + prev
