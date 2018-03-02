"""
CLI entry point.
"""

import argparse
import json

from . import usage, version
from .hgvs_parser import HgvsParser


def pyparsing_parser(description):
    print(description)
    parser = HgvsParser(parser_type='pyparsing')
    parser.status()
    parse_tree = parser.parse(description)
    if parse_tree is not None:
        print("Success")
        print(json.dumps(parse_tree.asDict(), indent=2))
        print(parse_tree.dump())


def hgvs_parser(description):
    """
    Parse the HGVS description.

    :param description: HGVS description
    """
    print(description)
    parser = HgvsParser()
    parser.status()
    parse_tree = parser.parse(description)
    if parse_tree is not None:
        print("Success")
        print(parse_tree.pretty())
        from lark.tree import pydot__tree_to_png  # Just a neat utility function
        # pydot__tree_to_png(parse_tree, description + '.png')
        pydot__tree_to_png(parse_tree, 'test.png')


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

    args = parser.parse_args()

    if args.p:
        pyparsing_parser(args.description)
    else:
        hgvs_parser(args.description)


if __name__ == '__main__':
    main()
