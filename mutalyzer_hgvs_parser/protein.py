import os

from lark import Lark, Token, Transformer, Tree
from lark.tree import pydot__tree_to_png

from .convert import parse_tree_to_model


def _in(tree, data):
    for sub_tree in tree.children:
        if sub_tree.data == data:
            return True
    return False


class AmbigTransformer(Transformer):
    def _ambig(self, children):
        # pydot__tree_to_png(Tree("_ambig", children), "ambig.png")
        if children[0].data == children[1].data == "p_variant":
            if _in(children[0], "p_repeat") and _in(children[1], "p_substitution"):
                if (
                    children[1].children[1].data == "p_substitution"
                    and children[1].children[1].children[0].data == "p_inserted"
                    and children[1].children[1].children[0].children[0].data
                    == "p_insert"
                    and len(children[1].children[1].children[0].children[0].children)
                    == 1
                    and isinstance(
                        children[1].children[1].children[0].children[0].children[0],
                        Tree,
                    )
                    and children[1].children[1].children[0].children[0].children[0].data
                    == "p_length"
                ):
                    return children[0]
                return children[1]
            elif (
                _in(children[0], "p_substitution")
                and len(children[1].children) == 1
                and _in(children[1], "p_location")
            ):
                return children[1]
        elif children[0].data == children[1].data == "description":
            if _in(children[0], "description_dna") and _in(
                children[1], "description_protein"
            ):
                return children[0]
        elif children[0].data == children[1].data == "p_insert":
            if _in(children[0], "p_length") and _in(children[1], "p_location"):
                return children[0]
            elif _in(children[0], "p_location") and _in(children[1], "p_length"):
                return children[1]
        return Tree("_ambig", children)


class ProteinTransformer(Transformer):
    def p_variants(self, children):
        if len(children) == 1 and children[0].data == "p_variants_certain":
            return Tree("variants", children[0].children)
        return Tree("variants", children)

    def p_variant(self, children):
        return Tree("variant", children)

    def p_location(self, children):
        return Tree("location", children)

    def p_range(self, children):
        return Tree("range", children)

    def p_length(self, children):
        return Tree("length", children)

    def p_point(self, children):
        return Tree("point", children)

    def p_deletion(self, children):
        return Tree("deletion", children)

    def p_deletion_insertion(self, children):
        return Tree("deletion_insertion", children)

    def p_duplication(self, children):
        return Tree("duplication", children)

    def p_equal(self, children):
        return Tree("equal", children)

    def frame_shift(self, children):
        new_children = []
        for child in children:
            if isinstance(child, Token):
                new_children.append(Tree("insert", [Token("P_SEQUENCE", child.value)]))
            else:
                new_children.append(Tree("insert", [child]))
        if new_children:
            return Tree("frame_shift", [Tree("inserted", new_children)])
        else:
            return Tree("frame_shift", [])

    def p_insertion(self, children):
        return Tree("insertion", children)

    def p_repeat(self, children):
        return Tree("repeat", children)

    def p_substitution(self, children):
        return Tree("substitution", children)

    def p_inserted(self, children):
        return Tree("inserted", children)

    def p_insert(self, children):
        return Tree("insert", children)

    def p_repeat_number(self, children):
        return Tree("repeat_number", children)

    def p_repeat_mixed(self, children):
        return Tree("repeat_mixed", children)

    def p_repeat_number(self, children):
        return Tree("length", children)


def read_files(file_name):
    grammar_path = os.path.join(os.path.dirname(__file__), f"ebnf/{file_name}")
    with open(grammar_path) as grammar_file:
        return grammar_file.read()


def create_protein_parser(start_rule="description", ignore_whitespaces=True):
    grammar = read_files("top.g")
    grammar += read_files("dna.g")
    grammar += read_files("protein.g")
    grammar += read_files("reference.g")
    grammar += read_files("common.g")

    if ignore_whitespaces:
        grammar += "\n%import common.WS\n%ignore WS"

    return Lark(grammar, parser="earley", start=start_rule, ambiguity="explicit")


def parse_protein(description, start_rule="description"):
    protein_parser = create_protein_parser(start_rule)
    parse_tree = protein_parser.parse(description)
    new_parse_tree = ProteinTransformer().transform(
        AmbigTransformer().transform(parse_tree)
    )
    return new_parse_tree


def parse_protein_to_model(description, start_rule="description"):
    return parse_tree_to_model(parse_protein(description, start_rule))
