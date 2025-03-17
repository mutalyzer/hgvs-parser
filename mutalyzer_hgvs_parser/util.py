from lark import Tree


def to_dict(d_list):
    output = {}
    for d in d_list:
        if isinstance(d, dict):
            output.update(d)
        else:
            raise Exception("Element is not a dictionary.")
    return output


def data_equals(children, path, data):
    parent = None
    for p in path:
        if isinstance(children, list) and p < len(children):
            parent = children[p]
            if isinstance(parent, Tree):
                children = parent.children
            else:
                return False
        else:
            return False

    return isinstance(parent, Tree) and parent.data == data


def get_child(children, path):
    output = None
    for p in path:
        if not isinstance(children, list):
            raise Exception("Children not a list.")
        if len(children) > p:
            output = children[p]
            if isinstance(children[p], Tree):
                children = children[p].children
        else:
            raise Exception("Index greater then the list size.")
    return output


def get_only_value(children):
    if len(children) == 1:
        return children[0][list(children[0])[0]]
    else:
        raise Exception("Not only one key dictionary.")


def all_tree_children_equal(children, child_type):
    for child in children:
        if not isinstance(child, Tree):
            return False
        else:
            if child.data != child_type:
                return False
    return True
