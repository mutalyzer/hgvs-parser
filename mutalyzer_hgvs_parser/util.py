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
    for i, p in enumerate(path):
        if isinstance(children, list) and len(children) > p:
            parent = children[p]
            if isinstance(children[p], Tree):
                children = children[p].children
        else:
            return False
    return parent.data == data


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
    """
    It happens quite often to
    """
    if len(children) == 1:
        return children[0][list(children[0])[0]]
    else:
        raise Exception("Not only one key dictionary.")
