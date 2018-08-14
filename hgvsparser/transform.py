import json
from lark import Tree


def transform(parse_tree):
    """
    Builds the equivalent nested dictionary model from the lark parse tree.

    :param parse_tree: Lark based parse tree.
    :return: Nested dictionary equivalent for the parse tree.
    """
    tree_model = {
        'reference': get_reference(parse_tree),
        'coordinate_system': extract_value(parse_tree, 'coordinatesystem', 'COORD'),
    }
    return tree_model


def extract_value(parse_tree, rule_name, token_name):
    """
    Extracts the token value from a parse tree, given the rule name and the
    token name.
    :return: The token value or None, if not found.
    """
    rule_tree = parse_tree.find_data(rule_name)
    if rule_tree:
        rule_tree_list = list(rule_tree)
        if rule_tree_list:
            token_list = rule_tree_list[0].children
            for token in token_list:
                if token.type == token_name:
                    return token.value


def get_reference(parse_tree):
    """
    Convert the reference information from the parse tree.
    """
    reference = {}
    specific_locus = {}

    genbank_ref_tree = get_subtree(parse_tree, 'genbankref')
    print(genbank_ref_tree)
    if isinstance(genbank_ref_tree, Tree):
        # get the accession and the version
        reference['type'] = 'genbank'
        genbank_tokens = {
            'ACCESSION': 'id',
            'VERSION': 'version',
        }
        reference.update(extract_tokens(genbank_ref_tree, genbank_tokens))

        # get the spcific locus
        specific_locus_tree = get_subtree(genbank_ref_tree, 'specificlocus')
        specific_locus.update(extract_tokens(specific_locus_tree,
                                             genbank_tokens))
        if specific_locus:
            specific_locus['type'] = 'accession'
        else:
            genbank_specific_locus = {
                'GENENAME': 'id',
                'TRANSVAR': 'selector',
            }
            specific_locus.update(extract_tokens(specific_locus_tree,
                                                 genbank_specific_locus))
            if specific_locus.get('selector'):
                specific_locus['type'] = 'gene transcript'
            else:
                specific_locus.update(extract_tokens(specific_locus_tree,
                                                     {'PROTISO': 'selector'}))
                if specific_locus.get('selector'):
                    specific_locus['type'] = 'gene protein'

    lrg_ref_tree = get_subtree(parse_tree, 'lrgref')
    if isinstance(lrg_ref_tree, Tree):
        reference['type'] = 'lrg'
        lrg_token_types = {
            'LRGREF': 'id',
        }
        reference.update(extract_tokens(lrg_ref_tree, lrg_token_types))
        lrg_specific_locus = {
            'LRGSPECIFICLOCUS': 'id'
        }
        specific_locus.update(extract_tokens(lrg_ref_tree, lrg_specific_locus))
        if specific_locus:
            if 't' in specific_locus['id']:
                specific_locus['type'] = 'transcript'
            elif specific_locus and 'p' in specific_locus['id']:
                specific_locus['type'] = 'protein'

    if specific_locus:
        reference['specific_locus'] = specific_locus

    return reference


def extract_tokens(parse_tree, token_types):
    """
    Extract the token_types from a parse_tree.

    :param parse_tree: A lark parse tree.
    :param token_types: Dictionary with the keys representing the tokens to be
    extracted and the values representing the new keys.
    :return: A dictionary with the token_types values as keys and the token
    values as values.
    """
    tokens = {}
    if isinstance(parse_tree, Tree):
        for token in parse_tree.scan_values(lambda t: t.type in token_types):
            tokens[token_types[token.type]] = token.value
    return tokens


def get_subtree(parse_tree, rule_name):
    """
    Returns the subtree for the corresponding rule name.

    Note: It assumes that there is only one such subtree.
    :param parse_tree: Parent tree in which to search for the subtree.
    :param rule_name: The name of the rule to search subtree for.
    :return: found subtree or None
    """
    sub_tree_filter = parse_tree.find_data(rule_name)
    sub_tree_list = list(sub_tree_filter)
    if sub_tree_list and len(sub_tree_list) == 1:
        return sub_tree_list[0]
