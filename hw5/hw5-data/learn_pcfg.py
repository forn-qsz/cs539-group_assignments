import sys
from collections import defaultdict

class helper:
    open_brackets = '('
    close_brackets = ')'
    brackets_map = {')':'('}
    result_dic = None
    result_dic_list = []
    word_count_dic = defaultdict(int)
    tag_count_dic = defaultdict(int)

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

    def count_result_dic(self, result_dic):
        for k, v in result_dic.items():
            if isinstance(v, dict):
                for k_2 in v.keys():
                    key = k + ' -> ' + k_2
                    self.tag_count_dic[key] += 1
                self.count_result_dic(v)

    def read(self):
        for line in sys.stdin:
            self.result_dic = defaultdict(dict)
            self.list_to_dic(line.split(' '), [], True)
            self.result_dic_list.append(self.result_dic.copy())

    def output(self):
        for result_dic in self.result_dic_list[:2]:
            self.count_result_dic(result_dic)
            print(self.tag_count_dic)

def main():
    h = helper()
    h.output()

if __name__ == "__main__":
    main()