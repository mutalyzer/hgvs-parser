import os

from lark import Lark


def create_protein_parser(start_rule="description", ignore_whitespaces=True):
    grammar_path = os.path.join(os.path.dirname(__file__), "ebnf/protein.g")
    with open(grammar_path) as grammar_file:
        grammar = grammar_file.read()

    if ignore_whitespaces:
        grammar += "\n%import common.WS\n%ignore WS"

    return Lark(grammar, parser="earley", start=start_rule, ambiguity="explicit")


def parse_protein(description):
    protein_parser = create_protein_parser()
    return protein_parser.parse(description)
