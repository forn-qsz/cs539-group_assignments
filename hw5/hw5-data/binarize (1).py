#!/usr/local/bin/python3
import sys
import tree
from collections import defaultdict

root=None

def process_node(tree_node):
    all_subs = tree_node.subs
    if all_subs and len(all_subs) > 2:
        tree_node.subs = [all_subs.pop()]
        c_node = tree_node
        while len(all_subs) > 2:
            op_tree = tree.Tree(c_node.label, c_node.span, wrd=c_node.word, subs=[all_subs.pop()])
            c_node.subs.append(op_tree)
            c_node = op_tree
        op_tree = tree.Tree(c_node.label, c_node.span, wrd=c_node.word, subs=all_subs)
        c_node.subs.append(op_tree)
        

def preorder(node, operation=lambda _: None):
    operation(node)
    if node.subs is None:
        return
    for sub in node.subs:
        preorder(sub, operation=operation)

def process_lines(line):
    line_tree = tree.Tree.parse(line)
    root = line_tree
    preorder(line_tree, operation=process_node)
    print(line_tree)
    
if __name__ == "__main__":
    for line in sys.stdin:
        process_lines(line)

