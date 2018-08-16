"""
CLI entry point.
"""

import argparse
import json

from . import usage, version
from hgvsparser.hgvs_parser import HgvsParser
from lark import ParseError
from hgvsparser.transform import transform, extract_tokens, get_reference
from lark.tree import pydot__tree_to_png


def pyparsing_parser(description):
    print(description)
    parser = HgvsParser(parser_type='pyparsing')
    parser.status()
    parse_tree = parser.parse(description)
    if parse_tree is not None:
        print("Successful parsing.")
        print(parse_tree.dump())

    else:
        print("Parse error.")


def hgvs_parser(description, transform_to_model, save_png, grammar_file, start_rule):
    """
    Parse the HGVS description.

    :param save_png:
    :param transform_to_model:
    :param description: HGVS description
    """
    print(description)
    if grammar_file:
        parser = HgvsParser(grammar_path=grammar_file)
    else:
        parser = HgvsParser()
    parser.status()
    try:
        parse_tree = parser.parse(description)
    except ParseError as e:
        print(e)
    else:
        if parse_tree is not None:
            print("Successful parsing.")
            print("parse_tree")
            print(parse_tree.pretty())
            print(parse_tree)
            if transform_to_model:
                try:
                    model = transform(parse_tree)
                    print(json.dumps(model, indent=2))
                except Exception as e:
                    print("Transform error: \n %s\n" % str(e))

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

    parser.add_argument('description', help="HGVS variant description to be parsed")

    parser.add_argument('-p',
                        required=False, action='store_true',
                        help='use the pyparsing parser instead of the Lark one')

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
