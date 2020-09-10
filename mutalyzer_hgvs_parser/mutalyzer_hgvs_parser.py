from lark import GrammarError, ParseError

from .convert import to_model
from .exceptions import UnexpectedCharacter, UnexpectedEnd, UnsupportedStartRule
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
    errors = []
    try:
        parse_tree = parse_description(description, grammar_file, start_rule)
    except GrammarError:
        errors.append(
            {
                "code": "EGRAMMAR",
                "details": "Parser not generated due to a grammar error.",
            }
        )
    except FileNotFoundError:
        errors.append({"code": "EGRAMMARFILE", "details": "Grammar file not found. {}"})
    except UnexpectedCharacter as e:
        errors.append(
            dict(
                {"code": "ESYNTAXUC", "details": "Unexpected character."},
                **e.serialize()
            )
        )
    except UnexpectedEnd as e:
        errors.append(
            dict(
                {"code": "ESYNTAXUEOF", "details": "Unexpected end of input."},
                **e.serialize()
            )
        )
    except ParseError as e:
        errors.append({"code": "ESYNTAXP", "details": "Parsing error."})

    if not errors:
        try:
            model = to_model(parse_tree, start_rule)
        except UnsupportedStartRule as e:
            errors.append({"UnsupportedStartRule": str(e)})
        except Exception as e:
            errors.append({"Some error.": str(e)})
    if errors:
        return {"errors": errors}
    else:
        return model
