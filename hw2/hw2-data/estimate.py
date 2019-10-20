from sys import stdin

epron = {}
dic = {}
l = []

for line in stdin:
    l.append(line.split())
for i in range(0, len(l), 3):
    tmp = [''] * len(l[i])
    for j in range(len(l[i+1])):
        if(tmp[int(l[i+2][j])-1] != ''):
            tmp[int(l[i+2][j])-1] += ' '
        tmp[int(l[i+2][j])-1] += l[i+1][j]
    for j in range(len(tmp)):
        k = (l[i][j], tmp[j])
        if not k in dic:
            dic[k] = 1
        else:
            dic[k] += 1
        if not l[i][j] in epron:
            epron[l[i][j]] = 1
        else:
            epron[l[i][j]] += 1
for k in sorted(dic):
    p = dic[k] / epron[k[0]]
    if(p > 0.05):
        print(k[0] + " : " + k[1] + " # " + str(p))
