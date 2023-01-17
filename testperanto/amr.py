from testperanto.trees import TreeNode, str_to_position_tree

def amr_str(tree, indent=""):
    """Takes the root node of a tree and prints it out in amr format.
    
    Parameters
    ----------
    tree : testperanto.trees.TreeNode
        the input tree
    indent : str
        the base number of spaces to indent each line

    Returns
    -------
    str
        a Penman-style formatting of the tree    
    """
    if len(tree.get_children()) == 0:
        return indent + tree.get_simple_label()
    child0 = tree.get_child(0)
    assert child0.get_simple_label() == "inst", f"tree: {tree}"
    inst0 = child0.get_child(0).get_simple_label()
    res = f"({inst0}"
    for child in tree.get_children()[1:]:
        if child.get_simple_label() == "mods":
            if child.get_child(0).get_simple_label() != "-null-":
                for grandchild in child.get_children():
                    recursive = amr_str(grandchild.get_child(0), indent + " " * 3)
                    my_indent = indent + " " * 3
                    res += f"\n{my_indent}:{grandchild.get_simple_label()} {recursive}"
        else:
            recursive = amr_str(child, indent + " " * 3)
            my_indent = indent + " " * 3
            res += f"\n{my_indent}:{child.get_simple_label()} {recursive}"
    res += ")"
    return res

def amr_parse1(filepath):
    file = open(filepath, mode='r')
    lines = file.readlines()
    file.close()
    amrs = []
    curr = ""
    for line in lines:
        if line[0] == '#':
            if curr != "":
                amrs.append(curr)
            curr = ""
        else:
            line = line.replace(":", " ").strip()
            curr += " " + line
    return amrs[1:]

def amr_parse(s):
    """ not done """
    tokens = cool_split(s)
    stack = [tok for tok in tokens][::-1]
    root = TreeNode()
    root.label = tuple(["ROOT"])
    node_stack = [root]
    while len(stack) > 0:
        next_tok = stack.pop()
        if next_tok == "(":
            inst_node = TreeNode()
            inst_node.label = tuple(['inst'])
            node_stack[-1].children.append(inst_node)
            node_stack.append(inst_node)
            node = TreeNode()
            label = stack.pop()
            if stack[-1] == "/":
                label = label + stack.pop() + stack.pop()
            node.label = tuple([label])
            node_stack[-1].children.append(node)

        elif next_tok == ")":
            node_stack.pop()

        elif next_tok[0] == ":":
            node_stack.pop()
            node = TreeNode()
            node.label = tuple([next_tok[1:]])
            node_stack[-1].children.append(node)
            node_stack.append(node)

    return root


def cool_split(s):
    lines = s.split('\n')
    uncommented_lines = '\n'.join([line for line in lines if line[0] != '#'])
    chunks = uncommented_lines.split()
    for chunk in chunks:
        next_token = ""
        for char in chunk:
            if char == "(" or char == ")":
                if len(next_token) > 0:
                    yield next_token 
                    next_token = ""
                yield char
            else:
                next_token += char
        if len(next_token) > 0:
            yield next_token