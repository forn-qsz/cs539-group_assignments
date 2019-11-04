from __future__ import print_function
from _collections import defaultdict
import sys

START, END = ("<s>", "</s>")

best = defaultdict(lambda:defaultdict(float))
best[0]["<s>"] = 1
back = defaultdict(dict)

def backtrack(i,tag):
	if i == 0:
		return []
	return backtrack(i - 1,back[i][tag]) + [(words[i],tag)]


tags = {"they":["PRO"], "can":["V","N","AUX"], "fish":["V","N"]
      ,"I":["PRO"],"i":["PRO"],"hope":["V","N"], "that":["PRO","CONJ","DET"], "this":["PRO","DET"],"works":["V","N"]
      ,"a":["DET"],"panda":["N"],"eats":["V"],"shoots":["V","N"],"and":["CONJ"],"leaves":["N"]
      ,"time":["N"],"flies":["V"], "like":["ADJ","PREP","V","N"],"an":["DET"],"arrow":["N"]
      ,"</s>":["</s>"],"<s>":["<s>"]}
ptag = {"<s>":{"PRO":0.3,"DET":0.3,"N": 0.3,"PREP":0.1}
      ,"PRO":{"CONJ":0.4,"V":0.4,"AUX":0.1,"</s>":0.1}
      ,"DET":{"N":0.1,"V":0.5}
      ,"N":{"AUX":0.05,"V":0.3,"CONJ":0.4,"N":0.05,"</s>":0.2}
      ,"AUX":{"AUX":1.0},"PREP":{"DET":0.1,"N":0.1,"DET":0.4,"PRO":0.4}
      ,"V":{"DET":0.2,"PRO":0.1,"</s>":0.1, "PREP":0.1,"CONJ":0.2,"N":0.2}
      ,"CONJ":{"PRO":0.1,"N":0.1,"DET":0.4,"V":0.4}}

pword = {'</s>': {'</s>': 1},
            'ADJ': {'like': 1.0},
            'AUX': {'can': 1.0},
            'CONJ': {'and': 0.5, 'that': 0.5},
            'DET': {'a': 0.3846153846153846,
            'an': 0.3846153846153846,
            'that': 0.11538461538461538,
            'this': 0.11538461538461538},
            'N': {'arrow': 0.16949152542372883,
            'can': 0.03389830508474577,
            'fish': 0.08474576271186442,
            'hope': 0.08474576271186442,
            'leaves': 0.16949152542372883,
            'like': 0.016949152542372885,
            'panda': 0.16949152542372883,
            'shoots': 0.08474576271186442,
            'time': 0.16949152542372883,
            'works': 0.016949152542372885},
            'PREP': {'like': 1.0},
            'PRO': {'I': 0.2777777777777778,
            'i': 0.2777777777777778,
            'that': 0.08333333333333334,
            'they': 0.2777777777777778,
            'this': 0.08333333333333334},
            'V': {'can': 0.020833333333333336,
            'eats': 0.20833333333333334,
            'fish': 0.10416666666666667,
            'flies': 0.20833333333333334,
            'hope': 0.10416666666666667,
            'like': 0.0625,
            'shoots': 0.10416666666666667,
            'works': 0.1875}}

line = "I hope that this works"
x=0
for x in range(0, 1):
    words = [START] + line.split() + [END]
    for i, word in enumerate(words[1:],1):
        for tag in tags[word]:
            for prev in best[i - 1]:
                if tag in ptag[prev]:
                    score = best[i - 1][prev] * ptag[prev][tag] * pword[tag][word]
                    if score > best[i][tag]:
                        best[i][tag] = score
                        back[i][tag] = prev
    print(backtrack(len(words) - 1, "</s>")[:-1])
