import json


def transform(tree):
    variant = {
        'accession': extract_value(tree, 'accno', 'ACC'),
        'version': extract_value(tree, 'accno', 'VERSION'),
        'coordinate_system': extract_value(tree, 'reftype', 'COORD'),
        # 'specific_locus': get_specific_locus(tree)
    }
    print(json.dumps(variant, indent=2))


def get_coordinate_system(tree):
    coord = list(tree.find_data('reftype'))[0].children
    print(coord)


def extract_value(tree, rule_name, token_name):
    rule_tree = tree.find_data(rule_name)
    if rule_tree:
        rule_tree_list = list(rule_tree)
        if rule_tree_list:
            token_list = rule_tree_list[0].children
            for token in token_list:
                if token.type == token_name:
                    return token.value


def get_accession_version(tree):
    accno = list(tree.find_data('accno'))[0].children
    accession = None
    version_no = None
    for t in accno:
        if t.type == 'ACC':
            accession = t.value
        if t.type == 'VERSION':
            version_no = int(t.value)
    return accession, version_no


def get_specific_locus(tree):
    gene_symbol = tree.find_data('genesymbol')
    if gene_symbol:
        gene_symbol = list(gene_symbol)
    if gene_symbol:
        gene_symbol = gene_symbol[0].children
    accession = None
    version_no = None
    print(gene_symbol)
    return accession, version_no
