import json
from lark import Tree


class MultipleEntries(Exception):
    pass


def update_dict(dictionary, value, key):
    """
    Update a dictionary only if value is not None.
    """
    if value:
        dictionary[key] = value
    if value is False:
        dictionary[key] = value


def transform(parse_tree):
    """
    Builds the equivalent nested dictionary model from the lark parse tree.

    :param parse_tree: Lark based parse tree.
    :return: Nested dictionary equivalent for the parse tree.
    """
    tree_model = {}
    notes = []

    reference, nts = get_reference(parse_tree)
    notes.extend(nts)

    specloc, nts = get_specific_locus(parse_tree)
    notes.extend(nts)

    update_dict(tree_model, reference, 'reference')
    update_dict(tree_model, specloc, 'specific_locus')

    if reference.get('type') == 'genbank':
        if specloc.get('type') and specloc.get('type').startswith('lrg'):
            notes.append('lrg locus provided for genbank reference')

    if reference.get('type') == 'lrg':
        if specloc.get('type') and not specloc.get('type').startswith('lrg'):
            notes.append('genbank locus provided for lrg reference')

    coord_sys = extract_value(parse_tree, 'coordinatesystem', 'COORD')
    update_dict(tree_model, coord_sys, 'coordinate_system')

    update_dict(tree_model, notes, 'notes')

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


def get_specific_locus(parse_tree):
    specific_locus = {}
    notes = []

    # get the specific locus
    spec_loc_tree = extract_subtree(parse_tree, 'specificlocus')
    tokens = {
        'ACCESSION': 'id',
        'VERSION': 'selector'}
    specific_locus.update(extract_tokens(spec_loc_tree, tokens))
    if specific_locus:
        specific_locus['type'] = 'accession'
    else:
        tokens = {
            'GENENAME': 'id',
            'SELECTOR': 'selector',
        }
        specific_locus.update(extract_tokens(spec_loc_tree, tokens))
        if specific_locus:
            selector = specific_locus.get('selector')
            if selector:
                if selector.startswith('_v'):
                    specific_locus['type'] = 'gene transcript'
                    specific_locus['selector'] = selector[2:]
                elif specific_locus.get('selector').startswith('_i'):
                    specific_locus['type'] = 'gene protein'
                    specific_locus['selector'] = selector[2:]
                else:
                    # The grammar should not allow to reach this step.
                    notes.append('selector not proper specified')
            else:
                specific_locus['type'] = 'gene'
        else:
            tokens = {
                'LRGSPECIFICLOCUS': 'id'
            }
            specific_locus.update(extract_tokens(spec_loc_tree, tokens))
            if specific_locus:
                if specific_locus.get('id').startswith('t'):
                    specific_locus['type'] = 'lrg transcript'
                elif specific_locus.get('id').startswith('p'):
                    specific_locus['type'] = 'lrg protein'
                else:
                    # The grammar should not allow to reach this step.
                    specific_locus['type'] = 'lrg'
                    notes.append('selector not proper specified')

    return specific_locus, notes


def get_reference(parse_tree):
    """
    Convert the reference information from the parse tree.
    """
    reference = {}
    notes = []

    refid_tree = extract_subtree_child(parse_tree, parent='reference', child='refid')
    if isinstance(refid_tree, Tree):
        tokens = {
            'ACCESSION': 'id',
            'VERSION': 'version',
        }
        reference.update(extract_tokens(refid_tree, tokens))

        if reference.get('id') and reference.get('id').startswith('LRG'):
            if reference.get('version'):
                notes.append('version supplied for LRG reference')
            else:
                reference['type'] = 'lrg'
        else:
            reference['type'] = 'genbank'

    return reference, notes


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


def extract_subtree_child(parse_tree, parent, child):
    """
    Returns the subtree child for the corresponding rule name.
    Note: It assumes that there is only one such subtree.

    :param parse_tree:
    :param parent: Rule name for which we search the children.
    :param child: The child to be extracted.
    :return: Found child subtree or None.
    """
    sub_tree_filter = parse_tree.find_data(parent)
    sub_tree_list = list(sub_tree_filter)
    if sub_tree_list and len(sub_tree_list) == 1:
        for sub_tree in sub_tree_list[0].children:
            if sub_tree.data == child:
                return sub_tree
    else:
        raise MultipleEntries('Multiple trees for rule "%".' % parent)


def extract_subtree(parse_tree, rule_name):
    """
    Returns the subtree for the corresponding rule name.
    Note: It assumes that there is only one such subtree.

    :param parse_tree: Parent tree in which to search for the subtree.
    :param rule_name: The name of the rule to search subtree for.
    :return: Found subtree or None.
    """
    sub_tree_filter = parse_tree.find_data(rule_name)
    sub_tree_list = list(sub_tree_filter)
    if sub_tree_list:
        if len(sub_tree_list) == 1:
            return sub_tree_list[0]
        else:
            raise MultipleEntries('Multiple trees for rule "%s".' % rule_name)
