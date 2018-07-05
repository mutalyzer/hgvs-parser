"""
CLI entry point.
"""

import argparse

from . import usage, version
from hgvsparser.hgvs_parser import HgvsParser
from lark import ParseError


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


def hgvs_parser(description):
    """
    Parse the HGVS description.

    :param description: HGVS description
    """
    print(description)
    parser = HgvsParser()
    parser.status()
    try:
        parse_tree = parser.parse(description)
    except ParseError as e:
        print(e)
    else:
        if parse_tree is not None:
            print("Successful parsing.")
            print(parse_tree.pretty())
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

    args = parser.parse_args()

    if args.p:
        pyparsing_parser(args.description)
    else:
        hgvs_parser(args.description)


if __name__ == '__main__':
    main()
