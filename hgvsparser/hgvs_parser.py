"""
Module to parse HGVS variant descriptions.
"""

import os
from lark import Lark
from lark.exceptions import ParseError, UnexpectedCharacters
from hgvsparser.pyparsing_based_parser import PyparsingParser
from hgvsparser.exception_handlers import parse_error_handler
from hgvsparser.exception_handlers import unexpected_characters


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

    def _create_lark_parser(self):
        """
        Lark based parser instantiation.
        """
        with open(self._grammar_path) as grammar_file:
            grammar = grammar_file.read()

        if self._ignore_whitespaces:
            grammar += '\n%import common.WS\n%ignore WS'

        parser = None
        try:
            parser = Lark(grammar, parser='earley',
                          start=self._start_rule, ambiguity='resolve')
        except Exception as exc:
            print('Lark parser not generated from the \'%s\' grammar file.'
                  % self._grammar_path)
            print(exc)
        self._parser = parser

    def _create_pyparsing_parser(self):
        """
        Pyparsing based parser instantiation.
        """
        parser = None
        try:
            parser = PyparsingParser()
        except Exception as exc:
            print('Pyparsing based parser not generated.')
            print(exc)
        self._parser = parser

    def parse(self, description):
        """
        Parse the actual description. It requires the parser to be already set.
        :param description: HGVS description (str).
        :return: The parse tree directly (should it be changed to return
                 another format?).
        """
        parse_tree = None
        if self._parser is None:
            print('No parsing defined')
        try:
            parse_tree = self._parser.parse(description)
        except UnexpectedCharacters as exception:
            unexpected_characters(exception, self._parser, description)
        except ParseError as exception:
            parse_error_handler(exception, description)
        except Exception as exception:
            print(exception)
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
