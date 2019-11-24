import sys
from collections import defaultdict

class helper:
    open_brackets = '('
    close_brackets = ')'
    brackets_map = {')':'('}
    result_dic = None
    result_dic_list = []
    word_count_dic = defaultdict(int)

    def __init__(self):
        
        ## Read while initializing
        self.read()

    def assign_result_dic(self, stack, s=None):
        tmp_stack = stack.copy()
        tmp_dic = self.result_dic
        ## Assign new/old word
        if s:
            ## Count word appear times
            self.word_count_dic[s] += 1
            while(tmp_stack):
                tmp_dic = tmp_dic[tmp_stack.pop(0)]
            if tmp_dic[s]:
                tmp_dic[s] += 1
            else:
                tmp_dic[s] = 1
        ## Assign new tag
        else:
            while(len(tmp_stack)>1):
                tmp_dic = tmp_dic[tmp_stack.pop(0)]
            tmp_dic[tmp_stack.pop(0)] = defaultdict(dict)

    def list_to_dic(self, list, stack=[], start=True):
        while stack and list or start:
            start = False
            s = list.pop(0)
            ## (TOP
            if s[0] in self.open_brackets:
                stack.append(s[1:])
                ## Assign tags in stack into result_dic
                self.assign_result_dic(stack)
                ## Iterate until found a word
                self.list_to_dic(list, stack, start)
            # Does)
            else:
                if len(stack) < 1:
                    sys.exit("Parentheses not balanced!")
                else:
                    ## Assign word to the current tag
                    self.assign_result_dic(stack, s.replace(')', '').replace('\n', ''))
                    ## Pop used tags
                    while s[-1] == ')':
                        s = s.replace(')', '', 1)
                        stack.pop()
                    break

    def enum_result_dic(self, result_dic, begin=True):
        for k, v in result_dic.items():
            if isinstance(v, dict):
                if begin:
                    print("(" + k, end='')
                else:
                    print(" (" + k, end='')
                self.enum_result_dic(v, False)
                print(')', end='')
            else:
                if self.word_count_dic[k] == 1:
                    print(" <unk>", end='')
                else:
                    print(' ' + k, end='')

    def binarized_dic(self, k, v):
        bi_dic = defaultdict(dict)
        k_p = k + '\''
        v_p = v.copy()
        ## The first kv pair
        bi_dic[list(v.keys())[0]] = v_p.pop(list(v.keys())[0])
        ## The second kv pair
        bi_dic[k_p] = v_p
        return bi_dic

    def binarize(self, result_dic):
        for k, v in result_dic.items():
            if isinstance(v, dict):
                if len(v.keys()) > 2:
                    result_dic[k] = self.binarized_dic(k, v)
                self.binarize(result_dic[k])

    def read(self):
        for line in sys.stdin:
            self.result_dic = defaultdict(dict)
            self.list_to_dic(line.split(' '), [], True)
            self.binarize(self.result_dic)
            self.result_dic_list.append(self.result_dic.copy())

    def output(self):
        for result_dic in self.result_dic_list:
            self.enum_result_dic(result_dic)
            print()

def main():
    h = helper()
    h.output()

if __name__ == "__main__":
    main()