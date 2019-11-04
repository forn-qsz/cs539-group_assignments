#!/usr/bin/python

from sortedcontainers import SortedSet

BOS = "0BOS"
EOS = "EOS"

vocabulary = SortedSet()
letters = [chr(i) for i in xrange(ord("A"), ord("Z")+1)]
word_list = open("eword-epron.data","r").readlines()
prefixes = {}

for line in word_list:
    line = line.strip().split()
    word = line[0]
    pronounciation = line[1:]
    vocabulary.add(word)

    for i in xrange(1,len(word)+1):
        key = word[:i]
        prefixes[key] = prefixes.get(key, SortedSet())
        prefixes[key].add(word)

        

outfile = open("espell-eword.wfst", "w")
outfile.write(EOS + "\n")

transitions = []
return_statements = []
prefix_keys = SortedSet(prefixes.keys())

for letter in letters:
    if letter in prefix_keys:
        prev_state = BOS
        next_state = letter

        transitions.append("(" + prev_state + " (" + next_state + " " + letter + " " + "*e*" + "))")
        if letter in vocabulary:
            return_statement = "(" + next_state + " (" + BOS + " " + "_" + " " + letter + "))"
            return_statements.append(return_statement)

            return_statement = "(" + prev_state + " (" + EOS + " " + letter + " " + letter + "))"
            return_statements.append(return_statement)

for prefix in prefixes:
    if not prefix:
        continue
    prev_state = prefix
    for letter in letters:
        next_state = prefix + letter
        if next_state in prefix_keys:
            transition = "(" + prev_state + " (" + next_state + " " + letter + " " + "*e*" + "))"
            transitions.append(transition)
            
            if next_state in vocabulary:
                return_statement = "(" + next_state + " (" + BOS + " " + "_" + " " + next_state + "))"
                return_statements.append(return_statement)

                return_statement = "(" + prev_state + " (" + EOS + " " + letter + " " + next_state + "))"
                return_statements.append(return_statement)
            
for transition in sorted(transitions):
    outfile.write(transition + "\n")
for return_statement in sorted(return_statements):
    outfile.write(return_statement + "\n")



