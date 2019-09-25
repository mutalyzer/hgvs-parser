"""
CLI entry point.
"""

import argparse
import json
from . import usage, version
from .hgvs_parser import HgvsParser
from .mutalyzer_hgvs_parser import parse_description, \
    parse_description_to_model
from lark.tree import pydot__tree_to_png


def _pyparsing_parser(description):
    """
    Pyparsing based parser previously used in Mutalyzer.
    """
    parser = HgvsParser(parser_type='pyparsing')
    parser.status()
    parse_tree = parser.parse(description)
    if parse_tree is not None:
        print("Successful parsing.")
        print(parse_tree.dump())


def _parse_description(description, grammar_file, start_rule, save_png):
    """
    HGVS parsing with no conversion to model.
    """
    parse_tree = parse_description(description, grammar_file, start_rule)
    print('Successfully parsed description:\n {}'.format(description))
    if save_png:
        pydot__tree_to_png(parse_tree, save_png)
        print('Parse tree image saved to:\n %s ' % save_png)


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        description=usage[0], epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', action='version', version=version(parser.prog))

    parser.add_argument('description',
                        help="HGVS variant description to be parsed")

    parser.add_argument('-c',
                        required=False, action='store_true',
                        help='convert parse tree to model')

    parser.add_argument('-g',
                        required=False,
                        help='path to input grammar file')

    parser.add_argument('-r',
                        required=False,
                        help='start (top) rule for the grammar')

    parser.add_argument('-s',
                        required=False,
                        help='save parse tree as image')

    parser.add_argument('-p',
                        required=False, action='store_true',
                        help='use the pyparsing parser')

    args = parser.parse_args()

    if args.p:
        _pyparsing_parser(args.description)
    elif args.c:
        print(json.dumps(
            parse_description_to_model(description=args.description,
                                       grammar_file=args.g,
                                       start_rule=args.r),
            indent=2))
    else:
        _parse_description(description=args.description,
                           save_png=args.s,
                           grammar_file=args.g,
                           start_rule=args.r)


if __name__ == '__main__':
    main()
