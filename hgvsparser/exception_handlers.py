TERMINALS = {
    'ACCESSION': 'accession (e.g., NG_012337)',
    'VERSION': 'version (e.g., "1")',
    'GENE_NAME': 'gene name (e.g., SDHD)',
    'GENBANK_LOCUS_SELECTOR': 'genbank locus selector (e.g., v001, i001)',
    'LRG_LOCUS': 'lrg specific locus (e.g., p1, t1)',
    'COORDINATE_SYSTEM': 'coordinate system: (e.g., "g", "c")',
    'POSITION': 'position (e.g., 100)',
    'OFFSET': 'position offset ("-" or "+")',
    'OUTSIDE_CDS': 'outside CDS ("*" or "-")',
    'DOT': '"." between the coordinate system and the operation(s)',
    'COLON': '":" between the reference part and the coordinate system',
    'UNDERSCORE': '"_" between start and end in range or uncertain positions',
    'LPAR': '"(" for an uncertain position start',
    'RPAR': '")" for an uncertain position end',
    'SEMICOLON': '";" to separate variants',
    'LSQB': '"[" for multiple variants, insertions, or repeats',
    'RSQB': '"]" for multiple variants, insertions, or repeats',
    'DEL': 'deletion operation (e.g., 10del)',
    'DUP': 'duplication operation (e.g., 10dup)',
    'INS': 'insertion operation (e.g., 11_12insTA, ins10_20)',
    'CON': 'conversion operation (e.g., 10_12con20_22)',
    'EQUAL': '"=" to indicate no changes',
    'DELETED': 'deleted nucleotide in a substitution operation',
    'INSERTED': 'inserted nucleotide in a substitution operation',
    'DELETED_SEQUENCE': 'deleted sequence (e.g., ATG)',
    'DELETED_LENGTH': 'deleted length (e.g., 50)',
    'DUPLICATED_SEQUENCE': 'duplicated sequence (e.g., "A")',
    'DUPLICATED_LENGTH': 'duplicated length (e.g., 50)',
    'INVERTED': 'inv',
    'INSERTED_SEQUENCE': 'inserted sequence',
    'MORETHAN': '">" in a substitution operation',
    'SEQUENCE': 'sequence (e.g., ATG)',
    'REPEAT_LENGTH': 'repeat length (e.g., 50)',
    'NT': 'nucleotide, (e.g., "A")',
    'NAME': 'name',
    'LETTER': 'letter',
    'DIGIT': 'digit',
    'NUMBER': 'number',
    'LCASE_LETTER': 'lower case letter',
    'UCASE_LETTER': 'upper case letter',
}


def unexpected_characters(exception, parser, description):
    print(exception)
    print('Unexpected input: "{}"\n'.format(
        description[exception.pos_in_stream]))
    print(exception.get_context(description))
    print('Expecting:')
    for allowed in exception.allowed:
        if TERMINALS.get(allowed):
            print('  - {}'.format(TERMINALS[allowed]))
        else:
            print('  - {}'.format(allowed))


def parse_error_handler(exception, description):
    print(exception)
