"""
CLI entry point.
"""

import argparse
import json

from . import usage, version
from hgvsparser.hgvs_parser import HgvsParser
from hgvsparser.to_model import parse_tree_to_model
from lark import ParseError
from lark.tree import pydot__tree_to_png


def pyparsing_parser(description):
    """
    Pyparsing based parser previously used in Mutalyzer.
    """
    parser = HgvsParser(parser_type='pyparsing')
    parser.status()
    parse_tree = parser.parse(description)
    if parse_tree is not None:
        print("Successful parsing.")
        print(parse_tree.dump())
    else:
        print("Parse error.")


def hgvs_parser(description, convert_to_model,
                grammar_file, start_rule, save_png):
    """
    Parse the HGVS description.

    :param description: HGVS description.
    :param grammar_file: Path towards grammar file.
    :param start_rule: Root rule for the grammar.
    :param save_png: Save parse tree as png.
    :param convert_to_model:
    """
    if grammar_file:
        parser = HgvsParser(grammar_path=grammar_file, start_rule=start_rule)
    else:
        parser = HgvsParser()
    try:
        parse_tree = parser.parse(description)
    except ParseError as e:
        print(e)
    else:
        if parse_tree is not None:
            if convert_to_model:
                model = parse_tree_to_model(parse_tree)
                print(json.dumps(model['model'], indent=2))
                if save_png:
                    pydot__tree_to_png(parse_tree, save_png)
            else:
                print('Successfully parsed HGVS description:\n %s' %
                      description)
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
        pyparsing_parser(args.description)
    else:
        hgvs_parser(description=args.description,
                    convert_to_model=args.c,
                    save_png=args.s,
                    grammar_file=args.g,
                    start_rule=args.r)


if __name__ == '__main__':
    main()
