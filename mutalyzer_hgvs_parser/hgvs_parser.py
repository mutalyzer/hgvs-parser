import os

from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF

from .exceptions import UnexpectedCharacter, UnexpectedEnd


class HgvsParser:
    def __init__(self, grammar_path=None, start_rule=None, ignore_white_spaces=True):
        if grammar_path:
            self._grammar_path = grammar_path
        else:
            self._grammar_path = os.path.join(
                os.path.dirname(__file__), "ebnf/hgvs_mutalyzer_3.g")
        if start_rule:
            self._start_rule = start_rule
        else:
            self._start_rule = "description"
        self._ignore_whitespaces = ignore_white_spaces
        self._create_parser()

    def _create_parser(self):
        with open(self._grammar_path) as grammar_file:
            grammar = grammar_file.read()

        if self._ignore_whitespaces:
            grammar += "\n%import common.WS\n%ignore WS"

        self._parser = Lark(
            grammar, parser="earley", start=self._start_rule, ambiguity="explicit"
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
    return parser.parse(description)
