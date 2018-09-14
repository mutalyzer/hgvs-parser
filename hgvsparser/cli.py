"""
CLI entry point.
"""

import argparse
import json

from . import usage, version
from hgvsparser.hgvs_parser import HgvsParser
from lark import ParseError
from hgvsparser.to_model import parse_tree_to_model
from hgvsparser.to_description import model_to_description
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


def hgvs_parser(description, convert_to_model, save_png,
                grammar_file, start_rule):
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
    # parser.status()
    try:
        parse_tree = parser.parse(description)
    except ParseError as e:
        print(e)
    else:
        if parse_tree is not None:
            print('\nSuccessfully parsed HGVS description:\n %s' % description)
            if convert_to_model:
                model = parse_tree_to_model(parse_tree)
                print('\nEquivalent model:')
                print(json.dumps(model['model'], indent=2))
                print("\nEquivalent model description:\n %s" %
                      model_to_description(model['model']))
            if save_png:
                pydot__tree_to_png(parse_tree, 'test.png')
                print("image saved to test.png")
        else:
            print("Parse error.")


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

    parser.add_argument('-p',
                        required=False, action='store_true',
                        help='use the pyparsing parser')

    parser.add_argument('-g',
                        required=False,
                        help='path to grammar file')

    parser.add_argument('-t',
                        required=False, action='store_true',
                        help='transform to model')

    parser.add_argument('-s',
                        required=False, action='store_true',
                        help='save graph as "temp.png"')

    parser.add_argument('-r',
                        required=False,
                        help='rule to start for the grammar')

    args = parser.parse_args()

    if args.p:
        pyparsing_parser(args.description)
    else:
        hgvs_parser(args.description, args.t, args.s, args.g, args.r)


if __name__ == '__main__':
    main()
