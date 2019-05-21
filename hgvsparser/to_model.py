"""
Convert from the lark based parse tree to the dictionary variant model.
"""

from lark import Tree
from lark.lexer import Token
import copy


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
            sub_model = {'type': 'equal', 'source': 'reference'}
        elif parse_tree.data in ['variants', 'inserted']:
            sub_model = []
        for child_tree in parse_tree.children:
            convert(child_tree, sub_model)
        # Now we go up in the hierarchy, so its time to create the model.
        add_sub_module(parse_tree.data, model, sub_model)


def add_sub_module(node, model, sub_model):
    """
    Creates the model for a particular node by adding its submodel.

    :param node: Node name (from the parse tree data).
    :param model: Current model for the particular node.
    :param sub_model: Submodel to be added to the node model.
    """
    if isinstance(model, dict):
        if node == 'description':
            model['model'] = sub_model
        # Reference
        elif node in ['reference']:
            model['references'] = compose_reference_object(sub_model)
        elif node == 'reference_id':
            model['reference'] = sub_model
        elif node == 'specific_locus':
            if sub_model.get('genbank_locus'):
                model['specific_locus'] = sub_model['genbank_locus']
            else:
                model['specific_locus'] = sub_model
        elif node == 'reference':
            model.update(sub_model)
        elif node == 'variants':
            references = extract_references_from_variants(sub_model)
            if references:
                model['references'] = references
            model[node] = sub_model
        # Locations
        elif node in ['point', 'range']:
            sub_model['type'] = node
            model['location'] = sub_model
        elif node == 'uncertain':
            sub_model['uncertain'] = True
            sub_model['type'] = 'range'
            model['location'] = sub_model
        elif node in ['start', 'end', 'location']:
            model[node] = sub_model['location']
        elif node == 'uncertain_start':
            model['start'] = sub_model['location']
        elif node == 'uncertain_end':
            model['end'] = sub_model['location']
        elif node == 'inserted_location':
            model['inserted'] = [sub_model]
        elif node == 'reference_location':
            model[node] = reference_location(sub_model)
        # Variants
        elif node == 'equal_all':
            model['type'] = 'equal'
        elif node in ['substitution', 'deletion', 'duplication',
                      'insertion', 'inversion', 'conversion',
                      'deletion_insertion', 'equal']:
            model['type'] = node
            model['source'] = 'reference'
            model.update(sub_model)
        # Other
        elif node == 'deleted':
            sub_model.update({'source': 'description'})
            model[node] = [sub_model]
        # Length
        elif node == 'length':
            print(sub_model)
            if 'number' in sub_model:
                model[node] = int(sub_model['number'])
        else:
            model[node] = sub_model
    elif isinstance(model, list):
        model.append(sub_model)


def add_token(parent, token_type, token_value):
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


def compose_reference_object(sub_model):
    reference = copy.deepcopy(sub_model['reference'])
    if sub_model.get('specific_locus'):
        reference['specific_locus'] = \
            sub_model['specific_locus']
    if sub_model.get('coordinate_system'):
        reference['coordinate_system'] = \
            sub_model['coordinate_system']
    return {'reference': reference}


def extract_references_from_variants(sub_model):
    references = {}
    for variant in sub_model:
        if 'inserted' in variant:
            new_inserted = []
            for insertion in variant['inserted']:
                if 'reference_location' in insertion:
                    reference = insertion['reference_location']['reference']
                    id = insertion['reference_location']['id']
                    references[id] = reference

                    source = insertion['reference_location']['source']
                    new_insertion = {'source': source}
                    if insertion['reference_location'].get('location'):
                        new_insertion['location'] = insertion[
                            'reference_location']['location']
                    new_inserted.append(new_insertion)
                else:
                    new_insertion = insertion
                    if insertion.get('source') is None:
                        new_insertion.update({'source': 'reference'})
                    new_inserted.append(new_insertion)
            variant['inserted'] = new_inserted
    return references


def reference_location(sub_model):
    output = {'reference': sub_model['reference']}

    if sub_model.get('location'):
        output['location'] = sub_model['location']
    output['source'] = reference_model_to_description(
        compose_reference_object(sub_model)['reference'])

    output['id'] = get_reference_id(output['reference'])
    return output


def value_to_str(dictionary, value, left='', right=''):
    if dictionary.get(value):
        return '{}{}{}'.format(left, dictionary[value], right)
    else:
        return ''


def specific_locus_to_description(locus):
    if locus and locus.get('type'):
        if 'genbank' in locus['type']:
            return '({}{})'.format(value_to_str(locus, 'accession'),
                                   value_to_str(locus, 'version', '.'))
        if 'lrg' in locus['type']:
            if locus.get('transcript_variant'):
                return '{}'.format(value_to_str(locus, 'transcript_variant'))
            elif locus.get('transcript isoform'):
                return '{}'.format(value_to_str(locus, 'transcript_isoform'))
    return ''


def reference_model_to_description(reference):
    if reference.get('type'):
        if reference['type'] == 'genbank':
            return '{}{}{}{}'.format(value_to_str(reference, 'accession'),
                                     value_to_str(reference, 'version', '.'),
                                     specific_locus_to_description(
                                         reference.get('specific_locus')),
                                     value_to_str(
                                         reference,
                                         'coordinate_system', ':', '.'))
        if reference['type'] == 'lrg':
            return '{}{}{}'.format(value_to_str(reference, 'id'),
                                   specific_locus_to_description(
                                       reference.get('specific_locus')),
                                   value_to_str(
                                       reference,
                                       'coordinate_system', ':', '.'))


def get_reference_id(reference):
    if reference.get('type'):
        if reference['type'] == 'genbank':
            return '{}{}'.format(value_to_str(reference, 'accession'),
                                 value_to_str(reference, 'version', '.')
                                 )
        if reference['type'] == 'lrg':
            return '{}'.format(value_to_str(reference, 'id'))


def to_model_open_grammar(parse_tree):
    """
    Convert a parse tree, obtained by using the open grammar, to the
    description model.
    """
    model = {}
    if isinstance(parse_tree, Tree):
        for child in parse_tree.children:
            if isinstance(child, Token):
                if child.type == 'COORDINATE_SYSTEM':
                    model['coordinate_system'] = child.value
            elif isinstance(parse_tree, Tree):
                if child.data == 'reference':
                    model['reference'] = reference_to_model_open_grammar(
                        child)
                elif child.data == 'variants':
                    model['variants'] = variants_to_model_open_grammar(
                        child)

    return {'model': model}


def reference_to_model_open_grammar(reference_tree):
    if len(reference_tree.children) == 1:
        return {'id': reference_tree.children[0].value}
    elif len(reference_tree.children) == 2:
        return {'id': reference_tree.children[0].value,
                'selector': reference_to_model_open_grammar(
                    reference_tree.children[1])}


def variants_to_model_open_grammar(variants_tree):
    variants = []
    for variant in variants_tree.children:
        variants.append(variant_to_model_open_grammar(variant))
    return variants


def inserted_to_model_open_grammar(inserted_tree):
    inserted = []
    for inserted_subtree in inserted_tree.children:
        insert = {}
        for insert_part in inserted_subtree.children:
            if isinstance(insert_part, Token):
                if insert_part.type == 'SEQUENCE':
                    insert.update({'sequence': insert_part.value,
                                   'source': 'description'})
                elif insert_part.type == 'INVERTED':
                    insert['inverted'] = True
            elif isinstance(insert_part, Tree):
                if insert_part.data == 'location':
                    insert['location'] = location_to_model_open_grammar(
                        insert_part)
                    insert['source'] = 'reference'
                elif insert_part.data == 'description':
                    for description_part in insert_part.children:
                        print(description_part)
                        if isinstance(description_part, Token) and \
                                description_part.type == 'COORDINATE_SYSTEM':
                            insert['coordinate_system'] = description_part.value
                        elif description_part.data == 'variants':
                            if len(description_part.children) != 1:
                                raise Exception('Nested descriptions?')
                            else:
                                insert['location'] = \
                                    location_to_model_open_grammar(
                                        description_part.children[0])
                        elif description_part.data == 'reference':
                            insert['source'] = reference_to_model_open_grammar(
                                description_part)

        inserted.append(insert)

    return inserted


def variant_to_model_open_grammar(variant_tree):
    variant = {'location': location_to_model_open_grammar(
        variant_tree.children[0])}
    variant_tree = variant_tree.children[1]
    variant['type'] = variant_tree.data
    variant['source'] = 'reference'
    print(variant_tree)
    if variant_tree.data == 'substitution':
        if isinstance(variant_tree.children[0], Token):
            variant['deleted'] = [{'sequence': variant_tree.children[0].value,
                                   'source': 'description'}]
            variant['inserted'] = inserted_to_model_open_grammar(
                variant_tree.children[1])
        else:
            variant['inserted'] = inserted_to_model_open_grammar(
                variant_tree.children[0])
    if variant_tree.data == 'deletion':
        if isinstance(variant_tree.children[0], Token):
            variant['deleted'] = [{'sequence': variant_tree.children[0].value,
                                   'source': 'description'}]
            variant['inserted'] = inserted_to_model_open_grammar(
                variant_tree.children[1])
        else:
            variant['inserted'] = inserted_to_model_open_grammar(
                variant_tree.children[0])

    return variant


def point_to_model_open_grammar(point_tree):
    if point_tree.data == 'uncertain_point':
        return {**range_to_model_open_grammar(point_tree),
                **{'uncertain': True}}
    point = {'type': 'point'}
    for token in point_tree.children:
        if token.type == 'OUTSIDE_CDS':
            if token.value == '*':
                point['outside_cds'] = 'downstream'
            elif token.value == '-':
                point['outside_cds'] = 'upstream'
        elif token.type == 'NUMBER':
            point['position'] = int(token.value)
        elif token.type == 'UNKNOWN':
            point['uncertain'] = True
        elif token.type == 'OFFSET':
            if '?' in token.value:
                point['offset'] = {'uncertain': True}
                if '+' in token.value:
                    point['offset']['downstream'] = True
                elif '-' in token.value:
                    point['offset']['upstream'] = True
            else:
                point['offset'] = {'value': int(token.value)}
    return point


def range_to_model_open_grammar(range_tree):
    range_location = {'type': 'range',
                      'start': point_to_model_open_grammar(
                          range_tree.children[0]),
                      'end': point_to_model_open_grammar(
                          range_tree.children[1])}
    return range_location


def location_to_model_open_grammar(location_tree):
    location_tree = location_tree.children[0]
    if location_tree.data in ['point', 'uncertain_point']:
        return point_to_model_open_grammar(location_tree)
    elif location_tree.data == 'range':
        return range_to_model_open_grammar(location_tree)
