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
    string_dict = {}

    def __init__(self):
        ## Read while initializing
        self.read()

    def read(self):
        '''
        for line in sys.stdin:
            print(line)
            self.input_list.append(line.strip().split(' '))
        '''
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
            option = True
            with open(sys.argv[2]) as f:
                for line in f:
                    self.term.append(line.strip())

    def enum(self, key, string=[]):
        result = self.pcfg_dic[key]
        if isinstance(result, dict):
            if len(result.keys()) > 1:
                new_string = string.copy()
                for k in result.keys():
                    new_string = string
                    if len(k.split()) > 1:
                        for k_1 in k.split():
                            # Nonterminal
                            new_string2 = new_string.copy()
                            if k_1 in self.pcfg_dic.keys():
                                self.enum(k_1, new_string2)
                            else:
                                string.append(k_1)
                    else:
                        if k_1 in self.pcfg_dic.keys():
                                self.enum(k_1, new_string)
                        else:
                            string.append(k_1)
            else:
                for k in result.keys():
                    new_string = string
                    if len(k.split()) > 1:
                        for k_1 in k.split():
                            # Nonterminal
                            new_string2 = new_string.copy()
                            if k_1 in self.pcfg_dic.keys():
                                self.enum(k_1, new_string2)
                            else:
                                string.append(k_1)
                    else:
                        if k_1 in self.pcfg_dic.keys():
                                self.enum(k_1, new_string)
                        else:
                            string.append(k_1)

    def output(self):
        print(self.pcfg_dic)

if __name__ == "__main__":
    h = helper()
    h.output()