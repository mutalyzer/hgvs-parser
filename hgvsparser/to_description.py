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
    version = ''
    if isinstance(r, dict):
        if r.get('type') == 'genbank':
            accession = r.get('accession')
            if r.get('version'):
                version = '.%s' % r['version']
        elif r.get('type') == 'lrg':
            accession = r.get('id')
    return '%s%s' % (accession, version)


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
            specific_locus = '(%s.%s)' % (s['accession'], s['version'])
        elif specific_locus_type == 'gene':
            if s.get('transcript variant'):
                selector = '_v%s' % s.get('transcript variant')
            elif s.get('protein isoform'):
                selector = '_i%s' % s.get('protein isoform')
            else:
                selector = ''
            specific_locus = '(%s%s)' % (s.get('id'), selector)

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
    location = insertions = ''
    if v.get('location'):
        location = location_to_description(v.get('location'))
    if v.get('insertions'):
        insertions = insertions_to_description(v['insertions'])
    variant = '%s%s%s' %(location, v.get('type'), insertions)
    return variant


def location_to_description(l):
    """
    Convert the location dictionary model to string.
    :param l: Location dictionary.
    :return: Equivalent location string representation.
    """
    if l['type'] == 'point':
        return position_to_description(l)
    elif l['type'] == 'range':
        if l.get('uncertain'):
            return '(%s_%s)' %(position_to_description(l.get('start')),
                               position_to_description(l.get('end')))
        else:
            start = location_to_description(l.get('start'))
            end = location_to_description(l.get('end'))
            return '%s_%s' %(start, end)


def position_to_description(p):
    """
    Convert the position dictionary model to string.
    :param p: Position dictionary.
    :return: Equivalent position string representation.
    """
    outside_cds = offset = ''
    if p.get('outside_cds'):
        if p['outside_cds'] == 'downstream':
            outside_cds = '*'
        elif p['outside_cds'] == 'upstream':
            outside_cds = '-'
    if p.get('uncertain'):
        position = '?'
    else:
        position = str(p.get('position'))
    if p.get('offset'):
        offset = str(p.get('offset'))
    return '%s%s%s' %(outside_cds, position, offset)


def insertions_to_description(insertions):
    """
    Convert the insertions dictionary model to string.
    :param insertions: Insertions dictionary.
    :return: Equivalent insertions string representation.
    """
    output = ''
    insertions_list = []
    for i in insertions:
        if i.get('sequence'):
            insertions_list.append(i.get('sequence'))
        elif i.get('location'):
            insertions_list.append(location_to_description(i['location']))
            if i.get('inverted'):
                insertions_list[-1] += 'inv'
        elif i.get('reference_location'):
            insertions_list.append(model_to_description(i))
    if len(insertions) > 1:
        return '[%s]' % ';'.join(insertions_list)
    else:
        return insertions_list[0]
