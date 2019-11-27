import sys
from collections import defaultdict

class helper:
    input_list = []
    pcfg_dic = defaultdict(lambda: defaultdict(float))
    nonterm = []
    tree = []
    def __init__(self):
        ## Read while initializing
        self.read()
    def read(self):
        for line in sys.stdin:
            self.input_list.append(line.strip().split(' '))
        #print(self.input_list)
        with open(sys.argv[1]) as f:
            for line in f:
                l = line.split('->')
                #print(l)
                X = l[0].strip()
                #print(epron)
                l = l[1].split('#')
                YZ = l[0].strip()
                self.pcfg_dic[X][YZ] = float(l[1].strip())
        for k in self.pcfg_dic:
            self.nonterm.append(k)
        self.nonterm = list(set(self.nonterm))
        #print(self.nonterm)
    def backtrack(self, back, x, y, v):
        l = back[x][y][v]
        #print(l)
        for i in range(len(l)):
            new_x = l[i][0]
            new_y = l[i][1]
            new_v = l[i][2]
            self.tree.append(new_v)
            if new_v in self.nonterm:
                self.backtrack(back, new_x, new_y, new_v)
    def cyk_alg(self):
        score = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        back = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        text = self.input_list[0]
        n = len(text)
        for i in range(n):
            for A in self.nonterm:
                if(text[i] in self.pcfg_dic[A]):
                    score[i][i+1][A] = self.pcfg_dic[A][text[i]]
                    back[i][i+1][A] = [[i, i+1, text[i]]]
            added = True
            while(added):
                added = False
                for B in self.nonterm:
                    for A in self.nonterm:
                        if(score[i][i+1][B] > 0 and B in self.pcfg_dic[A]):
                            prob = self.pcfg_dic[A][B] * score[i][i+1][B]
                            if(prob > score[i][i+1][A]):
                                score[i][i+1][A] = prob
                                back[i][i+1][A] = [[i, i+1, B]]
                                added = True

        #1 ~ n
        for diff in range(2, n+1):
            for i in range(n):
                begin = i
                end = i + diff
                for split in range(begin+1, end):
                    for B in self.nonterm:
                        for C in self.nonterm:
                            for A in self.nonterm:
                                combine = B + ' ' + C
                                prob = score[begin][split][B] * score[split][end][C] * self.pcfg_dic[A][combine]
                                if (prob > score[begin][end][A]):
                                    score[begin][end][A] = prob
                                    back[begin][end][A] = [[begin, split, B], [split, end, C]]
                added = True
                while(added):
                    added = False
                    for B in self.nonterm:
                        for A in self.nonterm:
                            if(score[begin][end][B] > 0 and B in self.pcfg_dic[A]):
                                prob = self.pcfg_dic[A][B] * score[begin][end][B]
                                if(prob > score[begin][end][A]):
                                    score[begin][end][A] = prob
                                    back[begin][end][A] = [[begin, end, B]]
                                    added = True

        #print(back[2][5], score[2][5])
        #print tree
        self.tree.append('(TOP')
        self.backtrack(back, 0, n, 'TOP')
        print(' '.join(self.tree))


def main():
    h = helper()
    h.cyk_alg()
if __name__ == "__main__":
    main()
