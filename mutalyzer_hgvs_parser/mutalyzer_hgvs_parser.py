from .hgvs_parser import HgvsParser
from .convert import to_model
from .exceptions import UnexpectedCharacter, ParsingError, UnsupportedStartRule
from lark import GrammarError


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
        params['grammar_path'] = grammar_file
    if start_rule:
        params['start_rule'] = start_rule

    parser = HgvsParser(**params)
    return parser.parse(description)


def parse_description_to_model(description,
                               grammar_file=None, start_rule=None):
    """
    Parse a description and convert the resulted parse tree into a
    dictionary model.

    :param description: Description to be parsed.
    :param grammar_file: Path towards grammar file.
    :param start_rule: Root rule for the grammar.
    :return: Dictionary model.
    """
    errors = []
    try:
        parse_tree = parse_description(description, grammar_file, start_rule)
    except GrammarError as e:
        errors.append({'Parser not generated due to a grammar error.': str(e)})
    except FileNotFoundError as e:
        errors.append({'Grammar file not found.': str(e)})
    except UnexpectedCharacter as e:
        errors.append({'Unexpected character.': e.serialize()})
    except ParsingError as e:
        errors.append({'Parsing error.': e.serialize()})

    if not errors:
        try:
            model = to_model(parse_tree, start_rule)
        except UnsupportedStartRule as e:
            errors.append({'UnsupportedStartRule': str(e)})
        except Exception as e:
            errors.append({'Some error.': str(e)})
    if errors:
        return {'errors': errors}
    else:
        return model
