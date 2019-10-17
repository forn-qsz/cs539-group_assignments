#!/usr/bin/env python
from __future__ import division
from collections import Counter
import numpy as np
import sys
import random
import math
from random import randint
from readchar import readchar, readkey

def take_guess():    
    while True:
        a = readkey()
        if a in ['\x03', '\x04']:
            exit(1)
        if a.upper() in letterspace:
            return a.upper()

def play(test):
    pos = 0 
    n = len(test)
    print "please guess!"
    while pos < n:
        guessed = set()
        key = take_guess()
        guesses = 1
        while key != test[pos]:
            print "\r", key, guesses, 
            if key not in guessed:
                guesses += 1
                guessed.add(key)
            print "guessed:", "".join(sorted(guessed)),
            key = take_guess()
        print "\r", key, guesses, "\033[K" # success
        pos += 1 # move on

letterspace = map(chr, range(ord('A'), ord('Z')+1)) + [' ']
def take_guess_lm(lm, prev, guesses):
    try:
        return lm[prev][guesses-1]
    except:
        return letterspace[randint(0,26)] # smoothing

def run(test, order, lm):
    pos = 0 
    n = len(test)
    guess_seq = []
    prev = "~" * (order-1)
    while pos < n:
        guessed = set()
        guesses = 1
        key = take_guess_lm(lm, prev, guesses)  
        while key != test[pos]:
            #print key, guesses
            if key not in guessed:
                guesses += 1
                guessed.add(key)
            key = take_guess_lm(lm, prev, guesses)
        print "%s%d" % (key if key != " " else "_", guesses),
        guess_seq.append(guesses)
        pos += 1 # move on
        prev = (prev[1:] + key) if order > 1 else ''
    print
    return guess_seq

def read_lm(filename):
    f = open(filename)
    return eval(f.read())

def entropy(guess_seq):
    s = np.array(Counter(guess_seq).values()) / len(guess_seq)
    return -sum( p * math.log(p, 2) for p in s)
    
if __name__ == "__main__":
    print "start"
    tests = []
    for line in open(sys.argv[1]):
        tests.append(line.strip())
    #order, lm = read_lm(sys.argv[2])
    es = 0
    all_guess_seqs = []
    for i in xrange(len(tests)):
        play(tests[random.randint(0, len(tests)-1)])
        #play(tests[i])
        print "end"
    exit(0)

    for i in xrange(len(tests)):
        #play(tests[random.randint(0, len(tests)-1)])
        guess_seq = run(tests[i], order, lm)
        e = entropy(guess_seq)
        print "entropy:", e
        es += e
        all_guess_seqs.extend(guess_seq)
    print "total entropy:", entropy(all_guess_seqs) #, es / len(tests) -- wrong
