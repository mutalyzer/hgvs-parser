"""
CLI entry point.
"""

import argparse
import json

from lark.tree import pydot__tree_to_png

from . import usage, version
from .convert import _parse_tree_to_model
from .hgvs_parser import parse


def _parse(description, grammar_path, start_rule):
    """
    CLI wrapper for parsing with no conversion to model.
    """
    parse_tree = parse(description, grammar_path, start_rule)
    print("Successfully parsed:\n {}".format(description))
    return parse_tree


def _to_model(description, start_rule):
    """
    CLI wrapper for parsing, converting, and printing the model.
    """
    parse_tree = parse(description, start_rule=start_rule)
    model = _parse_tree_to_model(parse_tree, start_rule)
    print(json.dumps(model, indent=2))
    return parse_tree


def main():
    cli = argparse.ArgumentParser(
        description=usage[0],
        epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    cli.add_argument("-v", action="version", version=version(cli.prog))

    cli.add_argument(
        "description", help="the HGVS variant description to be parsed")

    cli.add_argument(
        "-r", help="alternative start (top) rule for the grammar")

    alt = cli.add_mutually_exclusive_group()

    alt.add_argument(
        "-c", action="store_true", help="convert the parse tree to the model")

    alt.add_argument(
        "-g", help="alternative input grammar file path (do not use with -c)")

    cli.add_argument(
        "-i", help="save the parse tree as a PNG image (pydot required!)")

    args = cli.parse_args()

    if args.c:
        parse_tree = _to_model(args.description, args.r)
    else:
        parse_tree = _parse(args.description, args.g, args.r)

    if args.i and parse_tree:
        pydot__tree_to_png(parse_tree, args.i)
        print("Parse tree image saved to:\n {}".format(args.i))


if __name__ == "__main__":
    main()
