from sys import stdin

l = []
dic = {}
output = []
for line in stdin:
    word = line.split()
    l.append(list(word[0]))
print("gen")
for i in range(len(l)):
    if not '0' in dic:
        dic['0'] = 1
    else:
        dic['0'] += 1
    output.append(("0", l[i][0], l[i][0], "*e*"))
    state = [l[i][0]]
    for j in range(1, len(l[i])+1):
        s = ''
        s = s.join(state)
        if not s in dic:
            dic[s] = 1
        else:
            dic[s] += 1
        if(j != len(l[i])):
            output.append((s, s + l[i][j], l[i][j], "*e*"))
            state.append(l[i][j])
        else:
            output.append((s, "gen", "*e*", s))
            if not (s+"*e*") in dic:
                dic[s+"*e*"] = 1
            else:
                dic[s+"*e*"] += 1
output = sorted(set(output))
for w in output:
    if(w[1]!= 'gen'):
        p = dic[w[1]]/dic[w[0]]
    else:
        p = dic[w[0]+"*e*"]/dic[w[0]]
    print("(" + w[0] +" (" + w[1] + " " + w[2] + " " + w[3] + " " + str(p) + "))")
