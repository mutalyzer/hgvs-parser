from mutalyzer_hgvs_parser.hgvs_parser import HgvsParser
from mutalyzer_hgvs_parser.convert import description_to_model
from mutalyzer_hgvs_parser.exceptions import UnexpectedCharacter, ParsingError
from lark import ParseError, GrammarError


def parse_description(description, grammar_file, start_rule):
    """
    Parse a description.

    :param description: Description to be parsed
    :param grammar_file: Path towards the grammar file.
    :param start_rule: Start rule for the grammar.
    """
    params = {}
    if grammar_file:
        params['grammar_path'] = grammar_file
    if start_rule:
        params['start_rule'] = start_rule

    parser = HgvsParser(**params)
    return parser.parse(description)


def parse_description_to_model(description, grammar_file, start_rule):
    """
    Parse a description and convert its parse tree to a dictionary model.

    :param description: Description to be parsed.
    :param grammar_file: Path towards grammar file.
    :param start_rule: Root rule for the grammar.
    """
    errors = []
    try:
        parse_tree = parse_description(description, grammar_file, start_rule)
    except GrammarError as e:
        errors.append({'Parser not generated due to a grammar error.': str(e)})
    except FileNotFoundError as e:
        errors.append({'Grammar file not found.': str(e)})
    except ParsingError as e:
        errors.append({'Parsing error.': str(e)})
        print(vars(e))
    except UnexpectedCharacter as e:
        errors.append({'Unexpected character.': str(e)})

    if not errors:
        try:
            model = description_to_model(parse_tree)
        except Exception as e:
            errors.append({'Some error.': str(e)})
    if errors:
        return {'errors': errors}
    else:
        return model
