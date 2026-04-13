from __future__ import annotations

from typing import cast

from lark import Token, Tree


def to_dict(d_list: list) -> dict:
    output = {}
    for d in d_list:
        if isinstance(d, dict):
            output.update(d)
        else:
            raise Exception("Element is not a dictionary.")
    return output


def data_equals(children: list, path: list[int], data: str) -> bool:
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


def get_child(children: list, path: list[int]) -> Tree | Token | None:
    output = None
    for p in path:
        if not isinstance(children, list):
            raise Exception("Children not a list.")
        if len(children) > p:
            output = children[p]
            if isinstance(children[p], Tree):
                children = children[p].children
        else:
            raise Exception("Index greater than the list size.")
    return output


def get_tree_child(children: list, path: list[int]) -> Tree:
    return cast(Tree, get_child(children, path))


def get_only_value(children: list[dict]) -> dict:
    if len(children) == 1:
        return children[0][list(children[0])[0]]
    else:
        raise Exception("Not only one key dictionary.")


def all_tree_children_equal(children: list, child_type: str) -> bool:
    return all(isinstance(child, Tree) and child.data == child_type for child in children)
