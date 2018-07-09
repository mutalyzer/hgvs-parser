import json
from lark import Tree


def transform(parse_tree):
    variant = {
        'accession': extract_value(parse_tree, 'accno', 'ACC'),
        'version': extract_value(parse_tree, 'accno', 'VERSION'),
        'coordinate_system': extract_value(parse_tree, 'reftype', 'COORD'),
        # 'specific_locus': get_specific_locus(parse_tree)
    }
    print(json.dumps(variant, indent=2))


def get_coordinate_system(parse_tree):
    coord = list(parse_tree.find_data('reftype'))[0].children
    print(coord)


def extract_value(parse_tree, rule_name, token_name):
    rule_tree = parse_tree.find_data(rule_name)
    if rule_tree:
        rule_tree_list = list(rule_tree)
        if rule_tree_list:
            token_list = rule_tree_list[0].children
            for token in token_list:
                if token.type == token_name:
                    return token.value


def get_accession_version(parse_tree):
    accno = list(parse_tree.find_data('accno'))[0].children
    accession = None
    version_no = None
    for t in accno:
        if t.type == 'ACC':
            accession = t.value
        if t.type == 'VERSION':
            version_no = int(t.value)
    return accession, version_no


def get_specific_locus(parse_tree):
    gene_symbol = parse_tree.find_data('genesymbol')
    if gene_symbol:
        gene_symbol = list(gene_symbol)
    if gene_symbol:
        gene_symbol = gene_symbol[0].children
    accession = None
    version_no = None
    print(gene_symbol)
    return accession, version_no


def extract_reference_information(parse_tree):
    reference = {}

    genbank_ref_tree = get_subtree(parse_tree, 'genbankref')
    if isinstance(genbank_ref_tree, Tree):
        ncbi_token_types = {
            'ACC': 'accession',
            'VERSION': 'version',
        }
        reference.update(extract_tokens(genbank_ref_tree, ncbi_token_types))

    lrg_ref_tree = get_subtree(parse_tree, 'lrg')
    if isinstance(lrg_ref_tree, Tree):
        lrg_token_types = {
            'NUMBER': 'accession',
        }
        print(lrg_ref_tree)
        reference.update(extract_tokens(lrg_ref_tree, lrg_token_types))

    print(extract_tokens(get_subtree(parse_tree, 'transvar'), {'NUMBER': 'transvar'}))

    return reference


def extract_tokens(parse_tree, token_types):
    tokens = {}
    if isinstance(parse_tree, Tree):
        for token in parse_tree.scan_values(lambda t: t.type in token_types):
            tokens[token_types[token.type]] = token.value
            print(vars(token))

    return tokens


def get_subtree(parse_tree, rule_name):
    """
    Returns the subtree for the corresponding rule name.

    Note: It assumes that there is only one such subtree:
    :param parse_tree: Parent tree in which to search for the subtree.
    :param rule_name: The name of the rule to search subtree for.
    :return: found subtree or None
    """
    sub_tree_filter = parse_tree.find_data(rule_name)
    sub_tree_list = list(sub_tree_filter)
    if sub_tree_list and len(sub_tree_list) == 1:
        return sub_tree_list[0]
