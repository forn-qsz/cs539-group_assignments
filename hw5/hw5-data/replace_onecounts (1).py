#!/usr/local/bin/python3
import sys
import tree
from collections import defaultdict

log = sys.stderr

word_count = defaultdict(int)
trees = []

def preorder(node, operation=lambda _: None):
    if node.subs is None:
        op_string = operation(node)
        if op_string is None:
            word_count[node.word] += 1
        node.word = op_string if op_string is not None else node.word
        return
    for sub in node.subs:
        preorder(sub, operation=operation)

def process_lines(line):
    line_tree = tree.Tree.parse(line)
    preorder(line_tree)
    trees.append(line_tree)
    
if __name__ == "__main__":
    for line in sys.stdin:
        process_lines(line)
    for tree_node in trees:
        replaceToUnk = lambda n : "<unk>" if word_count[n.word] == 1 else n.word
        preorder(tree_node, operation=replaceToUnk)
        print(tree_node)
    for word, count in word_count.items():
        if count > 1:
            print(word, file=log)
    

    