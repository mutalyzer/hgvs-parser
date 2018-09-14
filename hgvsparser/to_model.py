"""
Convert from the lark based parse tree to the dictionary variant model.
"""

from lark import Tree
from lark.lexer import Token


class MultipleEntries(Exception):
    pass


def parse_tree_to_model(parse_tree):
    """
    Builds the equivalent nested dictionary model from the lark parse tree.

    :param parse_tree: Lark based parse tree.
    :return: Nested dictionary equivalent for the parse tree.
    """
    tree_model = get_variants(parse_tree)

    return tree_model['model']


def add_tokens(parent, token_type, token_value):
    """
    Adds tree tokens to the parent dictionary.
    """
    if isinstance(parent, dict):
        if token_type == 'POSITION':
            if token_value != '?':
                parent['position'] = int(token_value)
            else:
                parent['uncertain'] = True
        elif token_type == 'OFFSET':
            if token_value == '?':
                parent['uncertain_offset'] = True
            else:
                parent['offset'] = int(token_value)
        elif token_type == 'OUTSIDE_CDS':
            if token_value == '*':
                parent['outside_cds'] = 'downstream'
            if token_value == '-':
                parent['outside_cds'] = 'upstream'
        elif token_type in ['INSERTED']:
            parent['inserted'] = [
                {
                    'source': 'description',
                    'sequence': token_value,
                }
            ]
        elif token_type in ['INSERTED_SEQUENCE']:
            parent['source'] = 'description'
            parent['sequence'] = token_value
        elif token_type in ['DELETED', 'DELETED_SEQUENCE']:
            parent['deleted'] = [
                {
                    'source': 'description',
                    'sequence': token_value,
                }
            ]
        elif token_type == 'DELETED_LENGTH':
            parent['deleted'] = [
                {
                    'source': 'description',
                    'length': int(token_value),
                }
            ]
        elif token_type == 'INVERTED':
            parent['inverted'] = True
        elif token_type == 'ACCESSION':
            if token_value.startswith('LRG'):
                parent['id'] = token_value
                parent['type'] = 'lrg'
            else:
                parent[token_type.lower()] = token_value
                parent['type'] = 'genbank'
        elif token_type == 'GENE_NAME':
            parent['id'] = token_value
            parent['type'] = 'gene'
        elif token_type == 'GENBANK_LOCUS_SELECTOR':
            if token_value.startswith('v'):
                parent['transcript_variant'] = token_value[1:]
            elif token_value.startswith('i'):
                parent['protein_isoform'] = token_value[1:]
        elif token_type == 'LRG_LOCUS':
            if token_value.startswith('t'):
                parent['type'] = 'lrg transcript'
                parent['transcript_variant'] = token_value
            elif token_value.startswith('p'):
                parent['type'] = 'lrg protein'
                parent['protein_isoform'] = token_value
        else:
            parent[token_type.lower()] = token_value
    # TODO: raise exception.


def to_variant_model(parse_tree, model):
    """

    :param parse_tree:
    :param model:
    """
    if isinstance(parse_tree, Token):
        add_tokens(model, parse_tree.type, parse_tree.value)
    elif isinstance(parse_tree, Tree):
        sub_model = {}
        if parse_tree.data in ['variants', 'insertions']:
            sub_model = []
        for child_tree in parse_tree.children:
            to_variant_model(child_tree, sub_model)
        if isinstance(model, dict):
            if parse_tree.data == 'description':
                model['model'] = sub_model
            # Reference
            elif parse_tree.data == 'reference_id':
                model['reference'] = sub_model
            elif parse_tree.data == 'specific_locus':
                if sub_model.get('genbank_locus'):
                    model['specific_locus'] = sub_model['genbank_locus']
                else:
                    model['specific_locus'] = sub_model
            elif parse_tree.data == 'reference':
                model.update(sub_model)
            # Locations
            elif parse_tree.data in ['point', 'range']:
                sub_model['type'] = parse_tree.data
                model['location'] = sub_model
            elif parse_tree.data == 'uncertain':
                sub_model['uncertain'] = True
                sub_model['type'] = 'range'
                model['location'] = sub_model
            elif parse_tree.data in ['start', 'end', 'location']:
                model[parse_tree.data] = sub_model['location']
            elif parse_tree.data == 'uncertain_start':
                model['start'] = sub_model['location']
            elif parse_tree.data == 'uncertain_end':
                model['end'] = sub_model['location']
            elif parse_tree.data == 'inserted_location':
                model['insertions'] = [sub_model]
            # Variant type
            elif parse_tree.data in ['substitution', 'del', 'dup', 'ins',
                                     'inv', 'con', 'delins', 'equal']:
                model['type'] = parse_tree.data
                model.update(sub_model)
            else:
                model[parse_tree.data] = sub_model
        elif isinstance(model, list):
            model.append(sub_model)
        # TODO: raise exception.


def get_variants(parse_tree):

    variants = {}

    to_variant_model(parse_tree, variants)

    return variants


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
                if isinstance(token, Token) and token.type == token_name:
                    return token.value


def extract_tokens_to_dict(parse_tree, token_types):
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
