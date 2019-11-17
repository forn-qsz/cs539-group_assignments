from sys import stdin
from collections import defaultdict
import sys
import operator

START, END = ('<s>', '</s>')


class Helper:
    def __init__(self):
        self.unigram = defaultdict(float)
        self.bigram = defaultdict(lambda: defaultdict(float)) #28*28
        self.e_c = defaultdict(lambda: defaultdict(float))#27*27
        self.frac_counts = defaultdict(lambda: defaultdict(float))
        self.voc = []
        self.cipher_list = []
        self.e_c_result = defaultdict(str)
        #self.token = 0
    def read(self):
        for sentence in stdin:
            self.cipher_list.append([char for char in sentence][:-1])
        with open('train.txt') as f:
            lines = f.read().splitlines()
        f.close()
        for line in lines:
            chars = [START] + list(line.replace(' ', '_')) + [END]
            #self.token += (len(chars)-1)# - <s>
            self.unigram[START] += 1
            self.unigram[chars[1]] += 1
            self.bigram[START][chars[1]] += 1
            for i in range(2, len(chars)):
                self.unigram[chars[i]] += 1
                self.bigram[chars[i-1]][chars[i]] += 1
        self.voc = list(self.unigram.keys()) #<s> = start posibility

        for e1 in self.voc:
            for e2 in self.voc:
                if e1 != END and e2 != START:
                    self.bigram[e1][e2] /= self.unigram[e1]
                if(e1 != START and e1 != END):
                    if(e2 != START and e2 != END):
                        self.e_c[e1][e2] = 1/(len(self.voc)-2)
        self.voc.remove('<s>')
        self.voc.remove('</s>')
    def normalize(self):
        for e1 in self.voc:
            #if(e1 in self.frac_counts):
            probs = []
            for e2 in self.voc:
                probs.append(self.frac_counts[e1][e2])
            prob_factor = 1 / sum(probs)
            for e2 in self.voc:
                self.e_c[e1][e2] = self.frac_counts[e1][e2] * prob_factor
    def print_table(self):
        non_zeros = 0
        #sys.stderr.write("iteration " + str(iterative) + '    ----- corpus prob = ' + str(corpus_prob) + '\n')
        for e1 in self.voc:
            l = []
            l.append(e1 + '|->' + '\t')
            for e2 in self.voc:
                if (self.e_c[e1][e2] > 0.01):
                    l.append(e2 + ': ' + str(round(self.e_c[e1][e2], 2)) + '    ')
                    non_zeros += 1
            sys.stderr.write(''.join(l) + '\n')
        sys.stderr.write('nonzeros = ' + str(non_zeros) + '\n')
        sys.stderr.write('\n')
    def decode(self):
        for e2 in self.voc:
            max = -1
            d = 'none'
            #print(max(self.e_c[e2].items(), key=operator.itemgetter(1))[0], e2)

            for e1 in self.voc:
                if(self.e_c[e1][e2] > max):
                    max = self.e_c[e1][e2]
                    d = e1
            self.e_c_result[e2] = d
            #print(e2, d)



class EM:
    def __init__(self, cipher, transaction, table):
        self.cipher = cipher
        self.table = table
        self.transaction = transaction
        self.forward = defaultdict(lambda: defaultdict(float))
        self.backward = defaultdict(lambda: defaultdict(float))
        self.combine = defaultdict(lambda: defaultdict(float))
        self.fraction = defaultdict(lambda: defaultdict(float))
        self.o = cipher
        self.voc = list(self.table.keys())


    def forward_func(self):
        T = len(self.o)
        for t in range(T):
            for e1 in self.voc:
                if(t == 0):
                    self.forward[t][e1] = self.transaction['<s>'][e1] * self.table[e1][self.o[t]]#<s>
                else:
                    p = 0
                    for e2 in self.voc:
                        p += self.forward[t-1][e2] * self.transaction[e2][e1]
                    self.forward[t][e1] = p * self.table[e1][self.o[t]]
        p = 0
        for e in self.voc:
            self.forward[T-1][e] *= self.transaction[e]['</s>']#</s>
            p += self.forward[T-1][e]
        return p

    def backward_func(self):
        T = len(self.o)
        for t in range(T-1, -1, -1):
            for e1 in self.voc:
                if(t == T-1):
                    self.backward[t][e1] = self.transaction[e1]['</s>'] * self.table[e1][self.o[t]]
                else:
                    p = 0
                    for e2 in self.voc:
                        p += self.backward[t+1][e2] * self.transaction[e1][e2]
                    self.backward[t][e1] = p * self.table[e1][self.o[t]]
        p = 0
        for e in self.voc:
            self.backward[0][e] *= self.transaction['<s>'][e]
            p += self.backward[0][e]
        return p
    def dp(self, f_counts):
        T = len(self.o)

        self.forward_func()
        self.backward_func()

        for t in range(T):
            p_x = 0
            for e in self.voc:
                p_x += self.forward[t][e] * self.backward[t][e]
            for e in self.voc:
                self.combine[t][e] = self.forward[t][e] * self.backward[t][e]/p_x
        for e in self.voc:
            for t in range(T):
                f_counts[e][self.o[t]] += self.combine[t][e]
                #f_counts[self.o[t]][e] += self.combine[self.o[t]][e]
        return f_counts



def main():
    h = Helper()
    h.read()
    iteration = 0
    #print(h.bigram['_'])

    while(iteration < 50):

        #E_step
        for i in range(len(h.cipher_list)):
            em = EM(h.cipher_list[i], h.bigram, h.e_c)
            h.frac_counts = em.dp(h.frac_counts)
        #M_step
        h.normalize()
        iteration += 1
    #sys.stderr.write("epoch " + str(iteration) + '    ----- log(corpus prob) =  0' + '\n')
    #h.print_table()
    h.decode()
    for i in range(len(h.cipher_list)):
        sentence = []
        for j in range(len(h.cipher_list[i])):
            sentence.append(h.e_c_result[h.cipher_list[i][j]])
        print(''.join(sentence))
    


if __name__ == "__main__":
    main()
