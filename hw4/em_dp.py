from sys import stdin
from collections import defaultdict
from collections import Counter
import copy

class Helper:
    def __init__(self):
        self.eprons_list = []
        self.jprons_list = []
        self.ek_pair = {}
        self.all_path = []
        self.frac_counts = {}

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
        self.frac_counts = copy.deepcopy(self.ek_pair)

    def uni_ek(self):
        for e in self.ek_pair:
            for j in self.ek_pair[e]:
                self.ek_pair[e][j] = 1/len(self.ek_pair[e])

    def ini_frac_counts(self):
        for e in self.frac_counts:
            for j in self.frac_counts[e]:
                self.frac_counts[e][j] = 0
        return self.frac_counts

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

    def normalize(self):
        for e in self.ek_pair:
            probs = []
            for j in self.ek_pair[e]:
                probs.append(self.ek_pair[e][j])
            prob_factor = 1 / sum(probs)
            for j in self.ek_pair[e]:
                self.ek_pair[e][j] *= prob_factor

class EM:
    def __init__(self, eprons, jprons, table):
        self.eprons = eprons
        self.jprons = jprons
        self.table = table
        self.forward_dic = defaultdict(lambda: defaultdict(float))
        self.backward_dic = defaultdict(lambda: defaultdict(float))
        self.p_x = 0
        #print(self.table)

    def forward(self):
        n, m = len(self.eprons), len(self.jprons)
        self.forward_dic['0']['0'] = 1
        #print(self.table)
        # consider each epron
        for i in range(0, n):
            epron = self.eprons[i]
            # consider each start index for distributing
            for j in list(self.forward_dic[str(i)].keys()):
                # m-j: the maximum number of jprons that the current epron can distribute
                for k in range(1, min(m-int(j), 3)+1):
                    jseg = ''.join(self.jprons[int(j):int(j)+k])
                    if jseg in self.table[epron].keys():
                        score = self.forward_dic[str(i)][j] * self.table[epron][jseg]
                    else:
                        score = 0
                    self.forward_dic[str(i+1)][str(int(j)+k)] += score
        return self.forward_dic[str(n)][str(m)]

    def backward(self):
        n, m = len(self.eprons), len(self.jprons)
        self.backward_dic[str(n+1)][str(m+1)] = 1
        # consider each epron
        for i in range(n+1, 1, -1):
            epron = self.eprons[i-2]
            # consider each start index for distributing
            for j in list(self.backward_dic[str(i)].keys()):
                # j-1: the number of jprons that we left
                for k in range(1, min(int(j)-1, 3)+1):
                    jseg = ''.join(self.jprons[int(j)-k-1:int(j)-1])
                    if jseg in self.table[epron].keys():
                        score = self.backward_dic[str(i)][j] * self.table[epron][jseg]
                    else:
                        score = 0
                    self.backward_dic[str(i-1)][str(int(j)-k)] += score


    def dp(self, f_counts):
        self.p_x = self.forward()
        self.backward()

        n = len(self.eprons)
        m = len(self.jprons)

        #print(self.forward_dic)
        for i in range(0, n):
            #print(eprons[i])
            for j in list(self.forward_dic[str(i)].keys()):
                #print(j)
                for k in range(1, min(m-int(j), 3)+1):
                    jseg = ''.join(self.jprons[int(j):int(j)+k])
                    #print(eprons[i], jseg)
                    if jseg in self.table[self.eprons[i]].keys():
                        forward_u = self.forward_dic[str(i)][j]
                        backward_v = self.backward_dic[str(i+2)][str(int(j)+k+1)]
                        p_u_v = self.table[self.eprons[i]][jseg]
                        #print(self.eprons[i], jseg, forward_u, backward_v)
                        f_counts[self.eprons[i]][jseg] += forward_u * backward_v * p_u_v / self.p_x
        return f_counts


def main():
    h = Helper()
    h.read()
    #data1
    h.uni_ek()
    iterative = 0
    corpus_prob = 0
    #em
    while(1 - corpus_prob > 0.01 and iterative < 15):
        corpus_prob = 1
        #E-step
        h.ini_frac_counts()
        for i in range(len(h.eprons_list)):
            em = EM(h.eprons_list[i], h.jprons_list[i], h.ek_pair)
            h.frac_counts = em.dp(h.frac_counts)
            corpus_prob *= em.p_x
        #M_step
        h.ek_pair = copy.deepcopy(h.frac_counts)
        h.normalize()
        #print table
        non_zeros = 0
        print("iteration " + str(iterative) + '    ----- corpus prob = ' + str(corpus_prob))
        for e in h.ek_pair:
            l = []
            l.append(e + '|->   ')
            for j in h.ek_pair[e]:
                if (h.ek_pair[e][j] > 0.01):
                    l.append(j + ': ' + str(round(h.ek_pair[e][j], 2)) + '    ')
                    non_zeros += 1
            print(''.join(l))
        print('nonzeros = ' + str(non_zeros))
        iterative += 1
if __name__ == "__main__":
    main()
