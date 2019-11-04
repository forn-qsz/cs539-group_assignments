#!/usr/bin/python

from collections import defaultdict
estimates = {}

lines = open("epron-jpron.data", "r").readlines()
for i in xrange(len(lines)/3):
    line1 = lines[3 * i].strip()
    line2 = lines[3 * i + 1].strip()
    line3 = lines[3 * i + 2].strip()

    en_pronounce = line1.split()
    jp_pronounce = line2.split()
    mapping = [int(x)-1 for x in line3.split()]



    jp_mappings = [[] for _ in en_pronounce]
    for jp,mapped in zip(jp_pronounce, mapping):
        en = en_pronounce[mapped]
        jp_mappings[mapped].append(jp)

        
        
        #estimates[en] = estimates.get(en, defaultdict(float))
        #estimates[en][jp] += 1
    for jp_list, en in zip(jp_mappings, en_pronounce):
        key = tuple(jp_list)
        estimates[en] = estimates.get(en, defaultdict(float))
        estimates[en][key] += 1

    """
    print line1
    print line2
    print line3
    """



outfile = open("epron-jpron.probs", "w")
wfst = open("epron-jpron.wfst", "w")
BOS = "0BOS"
wfst.write(BOS + "\n")

filtered_estimates = {}
index = 1
for en in sorted(estimates.keys()):
    filtered = sorted([(en, jp, estimates[en][jp]) for jp in estimates[en].keys()], reverse=True)
    filtered_estimates[en] = filtered_estimates.get(en, defaultdict(float))
    
    Z = sum([count for en, jp, count in filtered])
    for en, jp, count in filtered:
        estimates[en][jp] /= Z
        prob = estimates[en][jp]
        #if len(jp) > 3:
        #    continue
        if prob < 0.01:
            print en, jp, prob, prob * Z
            
            continue


        filtered_estimates[en][jp] = prob

        jp = " ".join(jp)
        string = en + " : " + jp + " # " + str(prob)
        outfile.write(string + "\n")



    for jp in filtered_estimates[en]:
        Z = sum(filtered_estimates[en].values())
        #print filtered_estimates
        filtered_estimates[en][jp] /= Z
        #print filtered_estimates
        
        prob = filtered_estimates[en][jp]
        if len(jp) == 1:
            wfst.write("(" + BOS + " (" + BOS + " " + en + " " + jp[0] + " " + str(prob) + "))" + "\n")
        else:
            prev_state = BOS
            next_state = str(index)
            wfst.write("(" + prev_state + " (" + next_state + " " + en + " " + "*e*" + " " + str(prob) + "))" + "\n")
            prev_state = next_state
            index += 1
            for j in jp[:-1]:
                next_state = str(index)
                wfst.write("(" + prev_state + " (" + next_state + " " + "*e*" + " " + j + " " + "1" + "))" + "\n")
                index += 1
                prev_state = next_state
            wfst.write("(" + prev_state + " (" + BOS + " " + "*e*" + " " + jp[-1] + " " + "1" + "))" + "\n")
        #print en, jp, prob

