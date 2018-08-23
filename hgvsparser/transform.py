import json
from lark import Tree
from lark.lexer import Token


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

    coordinate = extract_value(parse_tree, 'coordinatesystem', 'COORDINATE')
    update_dict(tree_model, coordinate, 'coordinate_system')

    # variants = get_variants(parse_tree)
    # update_dict(tree_model, variants, 'variants')

    update_dict(tree_model, notes, 'notes')

    return tree_model


def get_specific_locus(parse_tree):
    """
    Convert the specific locus information from the parse tree.
    """
    specific_locus = {}
    notes = []

    # get the specific locus
    spec_loc_tree = extract_subtree(parse_tree, 'specificlocus')

    if isinstance(spec_loc_tree, Tree):
        accession = extract_value(spec_loc_tree, 'genbanklocus', 'ACCESSION')
        version = extract_value(spec_loc_tree, 'genbanklocus', 'VERSION')
        gene_name = extract_value(spec_loc_tree, 'genbanklocus', 'GENENAME')
        selector = extract_value(spec_loc_tree, 'genbanklocus', 'SELECTOR')
        lrglocus = extract_value(spec_loc_tree, 'specificlocus', 'LRGLOCUS')

        # Accession type, e.g., 'NG_012337.1(NM_012459.2)'
        if accession:
            specific_locus['type'] = 'accession'
            specific_locus['accession'] = accession
        if version:
            specific_locus['version'] = version

        # Gene type, e.g., 'NC_012920.1(MT-TL1_i001)'
        if gene_name:
            specific_locus['type'] = 'gene'
            specific_locus['id'] = gene_name
            if selector:
                if selector.startswith('_v'):
                    specific_locus['transcript variant'] = selector[2:]
                elif selector.startswith('_i'):
                    specific_locus['protein isoform'] = selector[2:]
                else:
                    # The grammar should not allow to reach this step.
                    notes.append('selector not proper specified')

        # LRG type, e.g., 'LRG_24t1'
        if lrglocus:
            if lrglocus.startswith('t'):
                specific_locus['type'] = 'lrg transcript'
                specific_locus['transcript variant'] = lrglocus
            elif lrglocus.startswith('p'):
                specific_locus['type'] = 'lrg protein'
                specific_locus['protein isoform'] = lrglocus
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
        accession = extract_value(refid_tree, 'refid', 'ACCESSION')
        version = extract_value(refid_tree, 'refid', 'VERSION')

        if accession and accession.startswith('LRG'):
            reference['type'] = 'lrg'
            reference['id'] = accession
            if version:
                notes.append('version supplied for LRG reference')
        else:
            reference['type'] = 'genbank'
            reference['accession'] = accession
        if version:
            reference['version'] = version

    return reference, notes


def get_variants(parse_tree):
    variants = []
    variants_tree = extract_subtree(parse_tree, 'variants')
    for variant_tree in variants_tree.children:
        variant = get_variant(variant_tree.children[0])
        variants.append(variant)
    return variants


def get_variant(variant_tree):
    if not isinstance(variant_tree, Tree):
        return None
    variant = {'type': variant_tree.data}

    if variant_tree.data == 'del':
        variant['location'] = get_location(extract_subtree(variant_tree,'loc'))
        seq = extract_value(variant_tree, 'del', 'SEQ')
        length = extract_value(variant_tree, 'del', 'NUMBER')
        if seq or length:
            deleted = {'source': 'description'}
            if seq:
                deleted['sequence'] = seq
            if length:
                deleted['length'] = length
            variant['deleted'] = deleted
    return variant


def get_location(location_tree):
    if location_tree.data == 'loc':
        location_tree = location_tree.children[0]
    if location_tree.data == 'ptloc':
        return get_ptloc(location_tree)
    elif location_tree.data == 'rangeloc':
        return get_rangeloc()
    else:
        raise Exception


def get_ptloc(location_tree):
    location = {}
    position = extract_value(location_tree, 'ptloc', 'POSITION')
    outsidetranslation = extract_value(location_tree, 'ptloc', 'OUTSIDETRANSLATION')
    offset = extract_value(location_tree, 'ptloc', 'OFFSET')
    position = int(position) if position and position != '?' else position
    if position:
        location = {'position': position}
    if offset:
        location['offset'] = int(offset)
    if outsidetranslation:
        if outsidetranslation == '-':
            location['downstream'] = True
        if outsidetranslation == '*':
            location['upstream'] = True
    return location


def get_rangeloc():
    return



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
