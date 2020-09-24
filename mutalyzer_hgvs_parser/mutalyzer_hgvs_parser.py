from .convert import to_model
from .hgvs_parser import HgvsParser


def parse_description(description, grammar_file=None, start_rule=None):
    """
    Parse a description and return the parse tree.

    :param description: Description to be parsed
    :param grammar_file: Path towards the grammar file.
    :param start_rule: Start rule for the grammar.
    :return: Lark parse tree.
    """
    params = {}
    if grammar_file:
        params["grammar_path"] = grammar_file
    if start_rule:
        params["start_rule"] = start_rule

    parser = HgvsParser(**params)
    return parser.parse(description)


def parse_description_to_model(description, grammar_file=None, start_rule=None):
    """
    Parse a description and convert the resulted parse tree into a
    dictionary model.

    :param description: Description to be parsed.
    :param grammar_file: Path towards grammar file.
    :param start_rule: Root rule for the grammar.
    :return: Dictionary model.
    """
    parse_tree = parse_description(description, grammar_file, start_rule)
    return to_model(parse_tree, start_rule)
