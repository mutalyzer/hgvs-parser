"""
Module for parsing HGVS variant descriptions.
"""

import os

from lark.tree import pydot__tree_to_png

from lark import Lark, Token, Transformer, Tree
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF

from .exceptions import UnexpectedCharacter, UnexpectedEnd


def _all(conditions):
    for condition in conditions:
        print(condition)
        if not condition:
            return False
    return True


def _in(tree, data):
    for sub_tree in tree.children:
        if sub_tree.data == data:
            return True
    return False


def debug(f):
    def wrapper(*args):
        t = f(*args)
        if t:
            print(f.__name__)
        return t

    return wrapper


@debug
def _is_uncertain_location_variants(children):
    """
    """
    if (
        children[0].data == children[1].data == "variants"
        and _in(children[0], "variants_certain")
        and _in(children[1], "variants_predicted")
        and len(children[0].children) == 1
        and len(children[0].children[0].children) == 1
        and _in(children[0].children[0].children[0], "location")
    ):
        return True
    else:
        return False


@debug
def _is_uncertain_location_variants_2(children):
    """
    """
    CONDITIONS = [
        len(children) == 2,
        children[0].data == children[1].data == "variants",
        children[0].children[0].data == "variants_certain",
        children[1].children[0].data == "variants_predicted",
        children[0].children[0].children[0].data == "variant",
        children[1].children[0].children[0].data == "variant"
     ]
    return _all(CONDITIONS)


@debug
def _is_uncertain_location_variant(children):
    """
    """
    if (
        children[0].data == children[1].data == "variant"
        and _in(children[0], "variant_certain")
        and _in(children[1], "variant_predicted")
        and len(children[0].children) == 1
        and _in(children[0].children[0], "location")
    ):
        return True
    else:
        return False


@debug
def _is_insert_length(children):
    if (
        children[0].data == children[1].data == "insert"
        and _in(children[0], "length")
        and _in(children[1], "location")
    ):
        return True
    else:
        return False


@debug
def _is_insert_location(children):
    if (
        children[0].data == children[1].data == "insert"
        and _in(children[0], "location")
        and _in(children[1], "length")
    ):
        return True
    else:
        return False


@debug
def _variant_certain_del_delins_repeat(children):
    """
    variant start rule: "10_11delinsR2:g.10_15"
    deletion insertion
    """
    if (
        len(children) == 3
        and children[0].data == "variant_certain"
        and children[1].data == "variant_certain"
        and children[2].data == "variant_certain"
        and _in(children[0], "deletion")
        and _in(children[1], "deletion_insertion")
        and _in(children[2], "repeat")
    ):
        return True
    else:
        return False


@debug
def _variant_certain_insertion_repeat(children):
    """
    variant start rule: "10_11delinsR2:g.10_15"
    deletion insertion
    """
    if (
        len(children) == 2
        and children[0].data == "variant_certain"
        and children[1].data == "variant_certain"
        and _in(children[0], "insertion")
        and _in(children[1], "repeat")
    ):
        return True
    else:
        return False

@debug
def _variant_certain_repeat_substitution(children):
    """
    """
    return (
        len(children) == 2
        and children[0].data == children[1].data == "variant_certain"
        and _in(children[0], "repeat")
        and _in(children[1], "substitution")
        and children[1].children[1].data == "substitution"
        and children[1].children[1].children[0].data == "inserted"
        and children[1].children[1].children[0].children[0].data == "insert"
        and len(children[1].children[1].children[0].children[0].children) == 1
        and isinstance(children[1].children[1].children[0].children[0].children[0], Tree)
        and children[1].children[1].children[0].children[0].children[0].data == "length"
    )


@debug
def _variant_certain_repeat_substitution_2(children):
    """
    """
    return (
        len(children) == 2
        and children[0].data == "variant_certain"
        and children[1].data == "variant_certain"
        and _in(children[0], "repeat")
        and _in(children[1], "substitution")
        and children[1].children[1].data == "substitution"
        and children[1].children[1].children[0].data == "inserted"
        and children[1].children[1].children[0].children[0].data == "insert"
        and len(children[1].children[1].children[0].children[0].children) == 1
        and isinstance(children[1].children[1].children[0].children[0].children[0], Token)
    )


@debug
def _variants_certain_predicted_uncertain_location(children):
    """
    R1(R2(R3)):g.(10_15)
    """
    if (
        children[0].data == children[1].data == "variants"
        and _in(children[0], "variants_certain")
        and _in(children[1], "variants_predicted")
        and children[0].children[0].children[0].data == "variant"
        and len(children[0].children[0].children[0].children) == 1
        and children[0].children[0].children[0].children[0].data == "variant_certain"
    ):
        return True
    else:
        return False


@debug
def _variants_certain_predicted_variant(children):
    """
    R1(R2(R3)):g.(10_15)
    """
    if (
        children[0].data == children[1].data == "variants"
        and _in(children[0], "variants_certain")
        and _in(children[1], "variants_predicted")
        and len(children[0].children[0].children[0].children[0].children[0].children) > 1
    ):
        return True
    else:
        return False


@debug
def _description_dna_protein(children):
    """
    R1:100insA
    - we opt for "description_dna"
    TODO: Leave it undefined and do the check based on
          the reference type?
    """
    if (len(children) == 2 and children[0].data == children[1].data == "description"
            and _in(children[0], "description_dna") and _in(children[1], "description_protein")):
        return True
    else:
        return False


class AmbigTransformer(Transformer):
    def _ambig(self, children):
        if _is_uncertain_location_variants(children):
            # "R1:(1_2)": uncertain location instead of predicted variant
            return children[0]
        elif _is_uncertain_location_variant(children):
            return children[0]
        elif _is_insert_length(children):
            return children[0]
        elif _is_insert_location(children):
            return children[1]
        elif _variant_certain_del_delins_repeat(children):
            return children[1]
        elif _variants_certain_predicted_uncertain_location(children):
            return children[0]
        elif _variant_certain_insertion_repeat(children):
            return children[0]
        elif _variants_certain_predicted_variant(children):
            return children[1]
        elif _variant_certain_repeat_substitution(children):
            return children[1]
        elif _variant_certain_repeat_substitution_2(children):
            return children[0]
        elif _description_dna_protein(children):
            return children[0]
        elif _is_uncertain_location_variants_2(children):
            return children[1]
            # if _in(children[0], "repeat") and _in(children[1], "substitution"):
            #     if (
            #         children[1].children[1].data == "substitution"
            #         and children[1].children[1].children[0].data == "inserted"
            #         and children[1].children[1].children[0].children[0].data == "insert"
            #         and len(children[1].children[1].children[0].children[0].children)
            #         == 1
            #         and isinstance(
            #             children[1].children[1].children[0].children[0].children[0],
            #             Tree,
            #         )
            #         and children[1].children[1].children[0].children[0].children[0].data
            #         == "length"
            #     ):
            #         # "PREF:p.Ala2[10]"
            #         return children[0]
            #     else:
            #         # "PREF:p.Ser68Arg"
            #         return children[1]
            # elif (
            #     _in(children[0], "substitution")
            #     and len(children[1].children) == 1
            #     and _in(children[1], "location")
            # ):
            #     return children[1]
            # elif _in(children[0], "insertion") and _in(children[1], "repeat"):
            #     print("7")
            #     return children[0]
        # elif (
        #     children[0].data == children[1].data == "variants"
        #     and _in(children[0], "variants_certain")
        #     and _in(children[1], "variants_predicted")
        # ):
            # "NP_003997.1:p.(Trp24Cys)": on uncertain variant
            # return children[1]
        # elif children[0].data == "variant":
        #     if (
        #         len(children[1].children) > 1
        #         and children[1].children[1].data == "repeat"
        #     ):
                # variant start rule: "10_11insNM_000001.1:c.100_200"
                # return children[0]
            # elif (
            #     len(children[1].children) > 1
            #     and children[1].children[1].data == "deletion_insertion"
            #     and children[0].children[1].data == "deletion"
            # ):
                # variant start rule: 10_11delinsR2:g.10_15
                # return children[1]
        # elif children[0].data == children[1].data == "description":
        #     if _in(children[0], "description_dna") and _in(
        #         children[1], "description_protein"
        #     ):
                # "R1:100insA": we opt for "description_dna"
                # TODO: Leave it undefined and do the check based on
                #       the reference type?
                # return children[0]
        return Tree("_ambig", children)


class ProteinTransformer(Transformer):
    def p_variants(self, children):
        return Tree("variants", children)

    def p_variants_certain(self, children):
        return Tree("variants_certain", children)

    def p_variants_predicted(self, children):
        return Tree("variants_predicted", children)

    def p_variant(self, children):
        return Tree("variant", children)

    def p_variant_certain(self, children):
        return Tree("variant_certain", children)

    def p_variant_predicted(self, children):
        return Tree("variant_predicted", children)

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

    def extension(self, children):
        return Tree("extension", children)

    def extension_n(self, children):
        point = Tree(
            "point", [Token("NUMBER", children[0].value), Token("OUTSIDE_CDS", "-")]
        )
        location = [Tree("location", [point])]
        return Tree("inserted", [Tree("insert", location)])

    def extension_c(self, children):
        inserted = [Tree("insert", [Token("P_SEQUENCE", children[0]).value])]
        if isinstance(children[1], Token):
            inserted.append(Tree("insert", [Token("P_SEQUENCE", children[1].value)]))
        else:
            inserted.append(Tree("insert", [Tree("location", [children[1]])]))
        return Tree("inserted", inserted)

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

    def P_COORDINATE_SYSTEM(self, name):
        return Token("COORDINATE_SYSTEM", name.value)


class FinalTransformer(Transformer):
    def variants(self, children):
        if children[0].data == "variants_certain":
            return Tree("variants", children[0].children)
        if children[0].data == "variants_predicted":
            return Tree("variants_predicted", children[0].children)
        return Tree("variants", children)

    def variant(self, children):
        if children[0].data == "variant_certain":
            return Tree("variant", children[0].children)
        if children[0].data == "variant_predicted":
            return Tree("variants_predicted", children[0].children)
        return Tree("variants", children)


def read_files(file_name):
    grammar_path = os.path.join(os.path.dirname(__file__), f"ebnf/{file_name}")
    with open(grammar_path) as grammar_file:
        return grammar_file.read()


class HgvsParser:
    """
    HGVS parser object.
    """

    def __init__(self, grammar_path=None, start_rule=None, ignore_white_spaces=True):
        """
        :arg str grammar_path: Path to a different EBNF grammar file.
        :arg str start_rule: Alternative start rule for the grammar.
        :arg bool ignore_white_spaces: Ignore or not white spaces in the description.
        """
        self._grammar_path = grammar_path
        self._start_rule = start_rule
        self._ignore_whitespaces = ignore_white_spaces
        self._create_parser()

    def _create_parser(self):
        if self._grammar_path:
            with open(self._grammar_path) as grammar_file:
                grammar = grammar_file.read()
        else:
            grammar = read_files("top.g")
            grammar += read_files("dna.g")
            grammar += read_files("protein.g")
            grammar += read_files("reference.g")
            grammar += read_files("common.g")

        start_rule = self._start_rule if self._start_rule else "description"

        if self._ignore_whitespaces:
            grammar += "\n%import common.WS\n%ignore WS"

        self._parser = Lark(
            grammar, parser="earley", start=start_rule, ambiguity="explicit"
        )

    def parse(self, description):
        """
        Parse the provided description.

        :arg str description: An HGVS description.
        :returns: A parse tree.
        :rtype: lark.Tree
        """
        try:
            parse_tree = self._parser.parse(description)
        except UnexpectedCharacters as e:
            raise UnexpectedCharacter(e, description)
        except UnexpectedEOF as e:
            raise UnexpectedEnd(e, description)
        return parse_tree

    def status(self):
        """
        Print parser's status information.
        """
        print("Parser type: %s" % self._parser_type)
        if self._parser_type == "lark":
            print(" Employed grammar path: %s" % self._grammar_path)
            print(" Options:")
            print("  Parser class: %s" % self._parser.parser_class)
            print("  Parser: %s" % self._parser.options.parser)
            print("  Lexer: %s" % self._parser.options.lexer)
            print("  Ambiguity: %s" % self._parser.options.ambiguity)
            print("  Start: %s" % self._parser.options.start)
            print("  Tree class: %s" % self._parser.options.tree_class)
            print(
                "  Propagate positions: %s" % self._parser.options.propagate_positions
            )


def parse(description, grammar_path=None, start_rule=None):
    """
    Parse the provided HGVS `description`, or the description part,
    e.g., a location, a variants list, etc., if an appropriate alternative
    `start_rule` is provided.

    :arg str description: Description (or description part) to be parsed.
    :arg str grammar_path: Path towards a different grammar file.
    :arg str start_rule: Alternative start rule for the grammar.
    :returns: Parse tree.
    :rtype: lark.Tree
    """
    parser = HgvsParser(grammar_path, start_rule)

    # pydot__tree_to_png(parser.parse(description), "temp_original.png")
    #
    # pydot__tree_to_png(
    #     FinalTransformer().transform(
    #         AmbigTransformer().transform(
    #             ProteinTransformer().transform(parser.parse(description))
    #         )
    #     ),
    #     "temp.png",
    # )
    # pydot__tree_to_png(
    #                 AmbigTransformer().transform(
    #             ProteinTransformer().transform(parser.parse(description))
    #
    #     ),
    #     "temp_after_ambig.png",
    # )
    return FinalTransformer().transform(
        AmbigTransformer().transform(
            ProteinTransformer().transform(parser.parse(description))
        )
    )
