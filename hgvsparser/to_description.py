"""
Convert from the nested dictionary based variant model to a string description.
"""

def model_to_description(model):
    """
    Convert the variant description model to string.
    :param model: Dictionary holding the variant description model.
    :return: Equivalent reference string representation.
    """
    reference = reference_to_description(model.get('reference'))
    description = reference
    description += specific_locus_to_description(model.get('specific_locus'))
    description += ':'
    if model.get('coordinate_system'):
        description += model.get('coordinate_system') + '.'
    if model.get('variants'):
        if len(model.get('variants')) > 1:
            description += '['
        for variant in model.get('variants'):
            description += variant_to_description(variant)
        if len(model.get('variants')) > 1:
            description += ']'
    return description


def reference_to_description(r):
    """
    Convert the reference dictionary model to string.
    :param r: Dictionary holding the reference model.
    :return: Equivalent reference string representation.
    """
    reference = ''
    if isinstance(r, dict):
        reference_type = r.get('type')
        if reference_type == 'genbank':
            reference += r.get('accession')
            if r.get('version'):
                reference += '.' + r.get('version')
        if reference_type == 'lrg':
            reference += r.get('id')
    return reference


def specific_locus_to_description(s):
    """
    Convert the specific locus dictionary model to string.
    :param s: Dictionary holding the specific locus model.
    :return: Equivalent specific locus string representation.
    """
    if isinstance(s, dict):
        specific_locus = ''
        specific_locus_type = s.get('type')
        if specific_locus_type == 'accession':
            specific_locus = '(' + s.get('accession') + '.' + s.get('version') + ')'
        elif specific_locus_type == 'gene':
            specific_locus += '(' + s.get('id')
            if s.get('transcript variant'):
                specific_locus += '_v' + s.get('transcript variant') + ')'
            if s.get('protein isoform'):
                specific_locus += '_i' + s.get('protein isoform') + ')'
        elif specific_locus_type == 'lrg transcript':
            specific_locus = s.get('transcript variant')
        elif specific_locus_type == 'lrg protein':
            specific_locus = s.get('protein isoform')
        return specific_locus
    else:
        return ''


def variant_to_description(v):
    """
    Convert the variant dictionary model to string.
    :param p: Variant dictionary.
    :return: Equivalent variant string representation.
    """
    location = ''
    if v.get('location'):
        location = location_to_description(v.get('location'))
    variant = '%s%s' %(location, v.get('type'))
    return variant


def location_to_description(l):
    """
    Convert the location dictionary model to string.
    :param l: Location dictionary.
    :return: Equivalent location string representation.
    """
    if l.get('position'):
        return position_to_description(l)
    if l.get('start'):
        if l.get('start').get('uncertain'):
            start = '(%s_%s)' %(position_to_description(l.get('start').get('uncertain').get('start')),
                                position_to_description(l.get('start').get('uncertain').get('end')))
        else:
            start = position_to_description(l.get('start'))
        if l.get('end'):
            if l.get('end').get('uncertain'):
                end = '(%s_%s)' % (position_to_description(l.get('end').get('uncertain').get('start')),
                                   position_to_description(l.get('end').get('uncertain').get('end')))
            else:
                end = position_to_description(l.get('end'))
            return '%s_%s' %(start, end)
        else:
            return start
    if l.get('uncertain'):
        return '(%s_%s)' %(position_to_description(l.get('uncertain').get('start')),
                           position_to_description(l.get('uncertain').get('end')))


def position_to_description(p):
    """
    Convert the position dictionary model to string.
    :param p: Position dictionary.
    :return: Equivalent position string representation.
    """
    if p.get('outside_translation'):
        if p.get('outside_translation') == 'upstream':
            outside_translation = '*'
        if p.get('outside_translation') == 'downstream':
            outside_translation = '-'
    else:
        outside_translation = ''
    position = str(p.get('position'))
    if p.get('offset'):
        offset = str(p.get('offset'))
    else:
        offset = ''
    return '%s%s%s' %(outside_translation, position, offset)
