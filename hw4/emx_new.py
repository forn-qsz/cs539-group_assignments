from sys import stdin
from collections import defaultdict
from collections import Counter

class Helper:
    def __init__(self):
        self.eprons_list = []
        self.jprons_list = []
        self.ek_pair = {}
        self.all_path = []
        self.fractional_counts = []

    def read(self):
        index = 0
        for line in stdin:
            if(index % 2 == 0):
                self.eprons_list.append(line.split())
            elif(index % 2 == 1):
                self.jprons_list.append(line.split())
            index += 1
        for i in self.eprons_list:
            for j in i:
                self.ek_pair[j] = {}
        for i in range(len(self.eprons_list)):
            path = defaultdict(dict)
            self.all_path.append([])
            self.enum(self.eprons_list[i], self.jprons_list[i], path, self.ek_pair, i)
        for i in range(len(self.all_path)):
            self.fractional_counts.append([])
            for j in range(len(self.all_path[i])):
                tmp = []
                for k in self.all_path[i][j]:
                    tmp.append(self.all_path[i][j][k])
                self.fractional_counts[i].append({})
                self.fractional_counts[i][j] = {'path' : tuple(tmp), 'prob' : float(0)}
        for i in range(len(self.fractional_counts)):
            for j in range(len(self.fractional_counts[i])):
                self.fractional_counts[i][j]['prob'] = 1/len(self.fractional_counts[i])

    def ini_ek(self):
        for e in self.ek_pair:
            for j in self.ek_pair[e]:
                self.ek_pair[e][j] = 0

    def uni_ek(self):
        for e in self.ek_pair:
            for j in self.ek_pair[e]:
                self.ek_pair[e][j] = 1/len(self.ek_pair[e])
        return self.ek_pair

    def enum(self, epron, jpron, path, ek_pair, pair, count=0):
        if(len(epron) == 1):
            k = []
            for i in range(len(jpron)):
                k.append(jpron[i])
            path[(epron[0], count)] = ''.join(k)
            ek_pair[epron[0]][''.join(k)] = 0
            self.all_path[pair].append(path.copy())
            count = 0
        else:
            for i in range(len(jpron) - len(epron) + 1):
                k = []
                for j in range(i + 1):
                    k.append(jpron[j])
                path[(epron[0], count)] = ''.join(k)
                ek_pair[epron[0]][''.join(k)] = 0
                self.enum(epron[1:], jpron[i+1:], path, ek_pair, pair, count + 1)

    def multiplyList(self, myList):
        result = 1
        for x in myList:
            result = result * x
        return result

    def normalize(self, probs):
        prob_factor = 1 / sum(probs)
        return [prob_factor * p for p in probs]

class EM:
    def __init__(self, eprons_list, jprons_list, table):
        self.eprons_list = eprons_list
        self.jprons_list = jprons_list
        self.table = table
        self.forward_dic = defaultdict(lambda: defaultdict(float))
        self.backward_dic = defaultdict(lambda: defaultdict(float))

    def forward(self, num):
        eprons = self.eprons_list[num]
        jprons = self.jprons_list[num]
        n, m = len(eprons), len(jprons)
        self.forward_dic['0']['0'] = 1
        # consider each epron
        for i in range(0, n):
            epron = eprons[i]
            # consider each start index for distributing
            for j in list(self.forward_dic[str(i)].keys()):
                # m-j: the maximum number of jprons that the current epron can distribute
                for k in range(1, min(m-int(j), 3)+1):
                    jseg = ''.join(jprons[int(j):int(j)+k])
                    if jseg in self.table[epron].keys():
                        score = self.forward_dic[str(i)][j] * self.table[epron][jseg]
                    else:
                        score = 0
                    self.forward_dic[str(i+1)][str(int(j)+k)] += score

    def backward(self, num):
        eprons = self.eprons_list[num]
        jprons = self.jprons_list[num]
        n, m = len(eprons), len(jprons)
        self.backward_dic[str(n+1)][str(m+1)] = 1
        # consider each epron
        for i in range(n+1, 1, -1):
            epron = eprons[i-2]
            # consider each start index for distributing
            for j in list(self.backward_dic[str(i)].keys()):
                # j-1: the number of jprons that we left
                for k in range(1, min(int(j)-1, 3)+1):
                    jseg = ''.join(jprons[int(j)-k-1:int(j)-1])
                    if jseg in self.table[epron].keys():
                        score = self.backward_dic[str(i)][j] * self.table[epron][jseg]
                    else:
                        score = 0
                    self.backward_dic[str(i-1)][str(int(j)-k)] += score

    '''
    def dp(self, fractional_counts, ek_pair, num):
        self.forward(num)
        self.backward(num)
        eprons = self.eprons_list[num]
        jprons = self.jprons_list[num]
        n = len(eprons)
        m = len(jprons)
        f_count = 0
        print(self.forward_dic, self.backward_dic)
        for i in self.forward_dic.copy().keys():
            j_fix = 0
            for init, j in enumerate(self.forward_dic[i]):
                if init == 0:
                    j_fix = int(j)
                    forw = self.forward_dic[str(int(i)-1)][str(int(j)-1)]
                    print(j_fix)
                if i != '0':
                    print(i,j,''.join(jprons[int(i):int(j)+1]))
                    f_count += forw * self.backward_dic[str(int(i)+1)][str(int(j)+1)] * ek_pair[eprons[int(i)-1]][''.join(jprons[j_fix-1:int(j)])]
                    print(f_count)
    '''

def main():
    h = Helper()
    h.read()

    em = EM(h.eprons_list, h.jprons_list, h.uni_ek())
    em.dp(h.fractional_counts, h.ek_pair, 0)

if __name__ == "__main__":
    main()