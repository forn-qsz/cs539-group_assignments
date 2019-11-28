import sys
from collections import defaultdict

class helper:
    input_list = [] #.txt
    pcfg_dic = defaultdict(lambda: defaultdict(float)) #.bin
    nonterm = [] #nonterminal
    term = [] #terminal
    tree = []
    replace = [] #replace for unknown
    option = False #train_dict
    none_count = 0

    def __init__(self):
        ## Read while initializing
        self.read()

    def read(self):
        for line in sys.stdin:
            self.input_list.append(line.strip().split(' '))
        with open(sys.argv[1]) as f:
            for line in f:
                l = line.split('->')
                X = l[0].strip()
                l = l[1].split('#')
                YZ = l[0].strip()
                self.pcfg_dic[X][YZ] = float(l[1].strip())
        #nonterminal list
        for k in self.pcfg_dic:
            self.nonterm.append(k)
        self.nonterm = list(set(self.nonterm))

        #optional train_dict
        if len(sys.argv) == 3:
            self.option = True
            with open(sys.argv[2]) as f:
                for line in f:
                    self.term.append(line.strip())
        #if('night' not in self.term):
            #print("fdss")
    def backtrack(self, back, x, y, v):
        l = back[x][y][v]
        bi = False
        for i in range(len(l)):
            new_x = l[i][0]
            new_y = l[i][1]
            new_v = l[i][2]
            #nonterminal
            if new_v in self.nonterm:
                if new_v[-1] == '\'':
                    bi = True
                if bi == False:
                    self.tree.append(' (')
                    self.tree.append(new_v)
                self.backtrack(back, new_x, new_y, new_v)
            #terminal
            else:
                #replace unknown word
                if(new_v == '<unk>'):
                    new_v = self.replace.pop(0)
                self.tree.append(' '+ new_v)
        if bi == False:
            self.tree.append(')')

    def cyk_alg(self, text):
        score = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        back = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        var = defaultdict(lambda: defaultdict(list))
        text = text
        self.tree = []
        #node
        n = len(text)
        for i in range(n):
            for A in self.nonterm:
                if(self.option == True and text[i] not in self.term):
                    self.replace.append(text[i])
                    #print('fuck')
                    text[i] = '<unk>'
                if(text[i] in self.pcfg_dic[A]):
                    score[i][i+1][A] = self.pcfg_dic[A][text[i]]
                    back[i][i+1][A] = [[i, i+1, text[i]]]
                    var[i][i+1].append(A)

            added = True
            while(added):
                added = False
                for B in var[i][i+1]:
                    for A in self.nonterm:
                        if(score[i][i+1][B] > 0 and B in self.pcfg_dic[A]):
                            prob = self.pcfg_dic[A][B] * score[i][i+1][B]
                            if(prob > score[i][i+1][A]):
                                score[i][i+1][A] = prob
                                back[i][i+1][A] = [[i, i+1, B]]
                                var[i][i+1].append(A)
                                added = True
        #from 1 ~ n
        for diff in range(2, n+1):
            for i in range(n):
                begin = i
                end = i + diff
                for split in range(begin+1, end):
                    for B in var[begin][split]:
                        for C in var[split][end]:
                            for A in self.nonterm:
                                combine = B + ' ' + C
                                prob = score[begin][split][B] * score[split][end][C] * self.pcfg_dic[A][combine]
                                if (prob > score[begin][end][A]):
                                    score[begin][end][A] = prob
                                    back[begin][end][A] = [[begin, split, B], [split, end, C]]
                                    var[begin][end].append(A)
                added = True
                while(added):
                    added = False
                    for B in var[begin][end]:
                        for A in self.nonterm:
                            if(score[begin][end][B] > 0 and B in self.pcfg_dic[A]):
                                prob = self.pcfg_dic[A][B] * score[begin][end][B]
                                if(prob > score[begin][end][A]):
                                    score[begin][end][A] = prob
                                    back[begin][end][A] = [[begin, end, B]]
                                    var[begin][end].append(A)
                                    added = True

        #print(score[0][n])

        #print tree
        if(score[0][n]['TOP'] == 0):#deal with failure
            print("NONE")
            self.none_count += 1
        else:
            self.tree.append('(TOP')
            self.backtrack(back, 0, n, 'TOP')
            print(''.join(self.tree))



def main():
    h = helper()
    for senten in h.input_list:
        h.cyk_alg(senten)
    print("NONE COUNT : " + str(h.none_count))
    #h.cyk_alg(h.input_list[25])

if __name__ == "__main__":
    main()
