"""
Module for converting lark parse trees to their equivalent dictionary models.
"""

from lark import Tree
from lark.lexer import Token
from .exceptions import UnsupportedStartRule


def to_model(parse_tree, start_rule=None):
    """
    Entry point for conversions.
    """
    if start_rule is None:
        return description_to_model(parse_tree)
    if start_rule == 'reference':
        return _reference_to_model(parse_tree)
    elif start_rule == 'variants':
        return _variants_to_model(parse_tree)
    elif start_rule == 'variant':
        return _variant_to_model(parse_tree)
    elif start_rule == 'location':
        return _location_to_model(parse_tree)
    raise UnsupportedStartRule(start_rule)


def description_to_model(parse_tree):
    """
    Converts the lark tree obtained by parsing an HGVS description to
    a nested dictionary model.

    :param parse_tree: Lark based parse tree.
    :return: Nested dictionary equivalent for the parse tree.
    """
    model = {}
    if isinstance(parse_tree, Tree):
        for child in parse_tree.children:
            if isinstance(child, Token):
                if child.type == 'COORDINATE_SYSTEM':
                    model['coordinate_system'] = child.value
            elif isinstance(parse_tree, Tree):
                if child.data == 'reference':
                    model['reference'] = _reference_to_model(child)
                elif child.data == 'variants':
                    model['variants'] = _variants_to_model(child)
    return model


def _reference_to_model(reference_tree):
    """
    Converts a lark tree corresponding to the reference rule to its
    dictionary model.

    :param reference_tree: Lark reference parse tree.
    :return: Dictionary model.
    """
    if len(reference_tree.children) == 1:
        return {'id': reference_tree.children[0].value}
    elif len(reference_tree.children) == 2:
        return {'id': reference_tree.children[0].value,
                'selector': _reference_to_model(reference_tree.children[1])}


def _variants_to_model(variants_tree):
    """
    Converts a lark tree corresponding to the variants rule to its
    dictionary model.

    :param variants_tree: Lark parse tree.
    :return: Dictionary model.
    """
    variants = []
    for variant in variants_tree.children:
        variants.append(_variant_to_model(variant))
    return variants


def _variant_to_model(variant_tree):
    """
    Converts a lark tree corresponding to the variant rule to its
    dictionary model.

    :param variant_tree: Lark parse tree.
    :return: Dictionary model.
    """
    if variant_tree.data == '_ambig':
        variant_tree = _solve_del_variant_ambiguity(variant_tree)

    variant = {'location': _location_to_model(
        variant_tree.children[0])}
    if len(variant_tree.children) == 2:
        variant_tree = variant_tree.children[1]
        variant['type'] = variant_tree.data
        variant['source'] = 'reference'
        if variant_tree.data == 'repeat':
            variant['inserted'] = _repeat_to_model(variant_tree.children)
        elif len(variant_tree.children) == 1:
            if variant_tree.data == 'deletion':
                variant['deleted'] = _deleted_to_model(
                    variant_tree.children[0])
            else:
                variant['inserted'] = _inserted_to_model(
                    variant_tree.children[0])
        elif len(variant_tree.children) == 2:
            variant['deleted'] = _deleted_to_model(variant_tree.children[0])
            variant['inserted'] = _inserted_to_model(variant_tree.children[1])

    return variant


def _solve_del_variant_ambiguity(variant):
    """
    Deals with the following type of ambiguity:
        REF1:100delinsREF2:100_200
    where this variant can be seen as a deletion in which insREF2 is
    wrongly interpreted as a reference, or as a deletion insertion, case
    in which REF2 is the reference (correct).
    """
    if variant.children[0].children[1].data == 'deletion_insertion' \
            and variant.children[1].children[1].data == 'deletion':
        return variant.children[0]
    elif variant.children[1].children[1].data == 'deletion_insertion' \
            and variant.children[0].children[1].data == 'deletion':
        return variant.children[1]


def _location_to_model(location_tree):
    """
    Converts a lark tree corresponding to the location rule to its
    dictionary model.

    :param location_tree: Lark parse tree.
    :return: Dictionary model.
    """
    location_tree = location_tree.children[0]
    if location_tree.data == 'range':
        return _range_to_model(location_tree)
    elif location_tree.data in ['point', 'uncertain_point']:
        return _point_to_model(location_tree)


def _range_to_model(range_tree):
    """
    Converts a lark tree corresponding to a range rule to a
    dictionary model.

    :param range_tree:
    :return:
    """
    range_location = {'type': 'range',
                      'start': _point_to_model(
                          range_tree.children[0]),
                      'end': _point_to_model(
                          range_tree.children[1])}
    return range_location


def _point_to_model(point_tree):
    """
    Converts a lark tree corresponding to a point/uncertain point rule
    to a dictionary model.

    :param point_tree: Lark parse tree.
    :return: Dictionary model.
    """
    if point_tree.data == 'uncertain_point':
        return {**_range_to_model(point_tree),
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


def _repeat_to_model(repeats):
    """
    Converts a lark tree corresponding to a repeat rule to a
    dictionary model.

    :param repeats: Lark parse tree.
    :return: Dictionary model.
    """
    model_repeats = []
    make_new_inserted = True
    for repeat in repeats:
        if make_new_inserted:
            inserted = {}
            make_new_inserted = False
        if isinstance(repeat, Token):
            inserted['sequence'] = repeat.value
        elif isinstance(repeat, Tree):
            inserted['length'] = _length_to_model(repeat)
            model_repeats.append(inserted)
            make_new_inserted = True
    return model_repeats


def _length_to_model(length_tree):
    """
    Converts a lark tree corresponding to a length rule to a
    dictionary model.

    :param length_tree: Lark parse tree.
    :return: Dictionary model.
    """
    length_tree = length_tree.children[0]
    if isinstance(length_tree, Token):
        return _length_point_to_model(length_tree)
    elif length_tree.data == 'exact_range':
        return {'type': 'range',
                'start': _length_point_to_model(length_tree.children[0]),
                'end': _length_point_to_model(length_tree.children[1]),
                'uncertain': True}


def _length_point_to_model(length_point_token):
    """
    Generates a point dictionary model from a lark token that
    corresponds to a length instance.

    :param length_point_token: Lark token.
    :return: Dictionary model.
    """
    if length_point_token.type == 'UNKNOWN':
        return {'type': 'point',
                'uncertain': True}
    if length_point_token.type == 'NUMBER':
        return {'type': 'point',
                'value': int(length_point_token.value)}


def _deleted_to_model(deleted):
    """
    Generates a deleted dictionary model from a lark token or parse
    tree that corresponds to a deleted instance.

    :param deleted:
    :return:
    """
    if isinstance(deleted, Token):
        return [{'sequence': deleted.value,
                'source': 'description'}]
    return _inserted_to_model(deleted)


def _inserted_to_model(inserted_tree):
    """
    Converts a lark tree corresponding to the inserted rule to its
    equivalent dictionary model.

    :param inserted_tree: Lark parse tree.
    :return: Dictionary model.
    """
    inserted = []
    for inserted_subtree in inserted_tree.children:
        insert = {}
        if inserted_subtree.data == '_ambig':
            inserted_subtree = _solve_insert_ambiguity(inserted_subtree)
        for insert_part in inserted_subtree.children:
            if isinstance(insert_part, Token):
                if insert_part.type == 'SEQUENCE':
                    insert.update({'sequence': insert_part.value,
                                   'source': 'description'})
                elif insert_part.type == 'INVERTED':
                    insert['inverted'] = True
            elif isinstance(insert_part, Tree):
                if insert_part.data == 'location':
                    insert['location'] = _location_to_model(insert_part)
                    insert['source'] = 'reference'
                elif insert_part.data == 'length':
                    insert['length'] = _length_to_model(insert_part)
                elif insert_part.data == 'description':
                    for description_part in insert_part.children:
                        if isinstance(description_part, Token) and \
                                description_part.type == 'COORDINATE_SYSTEM':
                            insert['coordinate_system'] = \
                                description_part.value
                        elif description_part.data == 'variants':
                            if len(description_part.children) != 1:
                                raise Exception('Nested descriptions?')
                            variant = description_part.children[0]
                            if len(variant.children) != 1:
                                raise Exception('Nested descriptions?')
                            else:
                                insert['location'] = \
                                    _location_to_model(
                                        variant.children[0])
                        elif description_part.data == 'reference':
                            insert['source'] = _reference_to_model(
                                description_part)
        inserted.append(insert)
    return inserted


def _solve_insert_ambiguity(insert):
    """
    Deals with ambiguities in the insert part. They arise between locations
    and lengths.

    Example:
    - REF:100>200 - 200 can be interpreted as a location or a length.

    We interpret insert as length (size) for the following:
    - NUMBER
    - (NUMBER)
    - (NUMBER_NUMBER)
    Examples:
    - 10, (10) something of length 10 is inserted;
    - (10_20): something of a length between 10 and 20 is inserted.
    - (?_20)
    - (20_?)
    - ?

    We interpret insert as location for the following:
    - point_point
    - (point_point)_point
    - point_(point_point)
    Examples:
    - 10_20
    - 10_(20_30)
    - (10_20)_30
    - (10_20)_(30_40)
    """
    if len(insert.children) == 2:
        if insert.children[0].children[0].data == 'length' and \
                insert.children[1].children[0].data == 'location':
            return insert.children[0]
        elif insert.children[0].children[0].data == 'location' and \
                insert.children[1].children[0].data == 'length':
            return insert.children[1]
