"""
Convert from the lark based parse tree to the dictionary variant model.
"""

from lark import Tree
from lark.lexer import Token


def parse_tree_to_model(parse_tree):
    """
    Wrapper around the actual parse tree to dictionary model converter.
    :param parse_tree: Lark based parse tree.
    :return: Nested dictionary equivalent for the parse tree.
    """
    model = {}
    convert(parse_tree, model)

    return model


def convert(parse_tree, model):
    """
    Parse tree to nested dictionary model converter.
    """
    if isinstance(parse_tree, Token):
        add_token(model, parse_tree.type, parse_tree.value)
    elif isinstance(parse_tree, Tree):
        sub_model = {}
        if parse_tree.data == 'equal_all':
            sub_model = {'type': 'equal'}
        elif parse_tree.data in ['variants', 'inserted']:
            sub_model = []
        for child_tree in parse_tree.children:
            convert(child_tree, sub_model)
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
                model['inserted'] = [sub_model]
            # Variant type
            elif parse_tree.data == 'equal_all':
                model['type'] = 'equal'
            elif parse_tree.data in ['substitution', 'deletion', 'duplication',
                                     'insertion', 'inversion', 'conversion',
                                     'deletion_insertion', 'equal']:
                model['type'] = parse_tree.data
                model.update(sub_model)
            else:
                model[parse_tree.data] = sub_model
        elif isinstance(model, list):
            model.append(sub_model)


def add_token(parent, token_type, token_value):
    """
    Adds tree tokens to the parent dictionary.
    """
    if isinstance(parent, dict):
        if token_type == 'POSITION':
            if token_value != '?':
                parent['position'] = int(token_value) - 1
            else:
                parent['uncertain'] = True
        elif token_type == 'OFFSET':
            if '?' in token_value:
                parent['offset'] = {'uncertain': True}
            else:
                parent['offset'] = {'value': int(token_value)}
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
