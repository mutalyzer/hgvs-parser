"""
Module to parse HGVS variant descriptions.
"""

import os
from lark import Lark
from lark.exceptions import UnexpectedCharacters, ParseError
from .pyparsing_based_parser import PyparsingParser
from .exceptions import UnexpectedCharacter, NoParserDefined,\
    UnsupportedParserType, ParsingError


class HgvsParser:
    """
    Either the pyparsing method or the lark one.
    """

    def __init__(self, parser_type='lark', grammar_path='local',
                 start_rule='description', ignore_white_spaces=True):
        if grammar_path == 'local':
            self._grammar_path = os.path.join(os.path.dirname(__file__),
                                              'ebnf/hgvs_mutalyzer_3.g')
        else:
            self._grammar_path = grammar_path
        self._parser_type = parser_type
        self._start_rule = start_rule
        self._ignore_whitespaces = ignore_white_spaces
        if parser_type == 'lark':
            self._create_lark_parser()
        elif parser_type == 'pyparsing':
            self._create_pyparsing_parser()
        else:
            raise UnsupportedParserType(
                'Not supported parser type: {}'.format(self._parser_type))

    def _create_lark_parser(self):
        """
        Lark based parser instantiation.
        """
        with open(self._grammar_path) as grammar_file:
            grammar = grammar_file.read()

        if self._ignore_whitespaces:
            grammar += '\n%import common.WS\n%ignore WS'

        self._parser = Lark(grammar, parser='earley',
                            start=self._start_rule,
                            ambiguity='explicit')

    def _create_pyparsing_parser(self):
        """
        Pyparsing based parser instantiation.
        """
        self._parser = PyparsingParser()

    def parse(self, description):
        """
        Parse the actual description. It requires the parser to be already set.
        :param description: HGVS description (str).
        :return: The parse tree directly (should it be changed to return
                 another format?).
        """
        if self._parser is None:
            raise NoParserDefined('No parser defined.')
        try:
            parse_tree = self._parser.parse(description)
        except UnexpectedCharacters as e:
            raise UnexpectedCharacter(e, description)
        except ParseError as e:
            raise ParsingError(e)
        return parse_tree

    def status(self):
        """
        Prints status information.
        """
        print("Parser type: %s" % self._parser_type)
        if self._parser_type == 'lark':
            print(" Employed grammar path: %s" % self._grammar_path)
            print(" Options:")
            print("  Parser class: %s" % self._parser.parser_class)
            print("  Parser: %s" % self._parser.options.parser)
            print("  Lexer: %s" % self._parser.options.lexer)
            print("  Ambiguity: %s" % self._parser.options.ambiguity)
            print("  Start: %s" % self._parser.options.start)
            print("  Tree class: %s" % self._parser.options.tree_class)
            print("  Propagate positions: %s" %
                  self._parser.options.propagate_positions)
