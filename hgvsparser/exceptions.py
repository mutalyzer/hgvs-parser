from lark.exceptions import UnexpectedCharacters
from lark.load_grammar import _TERMINAL_NAMES

TERMINALS = {
    'ACCESSION': 'accession: NM_00000',
    'VERSION': 'version: 1',
    'GENE_NAME': 'gene name:SDHD',
    'GENBANK_LOCUS_SELECTOR': 'genbank locus selector: _v001',
    'LRG_LOCUS': 'lrg specific locus: p1, t1',
    'COORDINATE_SYSTEM': 'coordinate system: g',
    'DELETED': 'deleted',
    'INSERTED': 'inserted',
    'DELETED_SEQUENCE': 'deleted sequence',
    'DELETED_LENGTH': 'deleted length',
    'DUPLICATED_SEQUENCE': 'duplicated sequence',
    'DUPLICATED_LENGTH': 'duplicated length',
    'INVERTED': 'inv',
    'INSERTED_SEQUENCE': 'inserted sequence',
    'SEQUENCE': 'sequence',
    'REPEAT_LENGTH': 'repeat length',
    'POSITION': 'position',
    'OFFSET': 'offset',
    'OUTSIDE_CDS': 'outside CDS: * or -',
    'LCASE_LETTER': 'lower case letter',
    'UCASE_LETTER': 'upper case letter',
    'NAME': 'name',
    'LETTER': 'letter',
    'DIGIT': 'digit',
    'NUMBER': 'number',
    'NT': 'nucleotide: A',
    'DOT': '.',
    'COLON': ':',
    'UNDERSCORE': '_',
    'LPAR': '(',
    'RPAR': ')',
    'SEMICOLON': ';',
    'LSQB': '[',
    'RSQB': ']',
    'MORETHAN': '',
    'DEL': 'deletion operation: 10del',
    'DUP': 'duplication operation: 10dup',
    'INS': 'insertion operation: 11_12insTA',
    'CON': 'conversion operation: 10_12con12_14',
    'EQUAL': '='
}


def exception_handler(exception, parser, description):
    print(exception.get_context(description))
    print('No terminal defined for: %s' % description[exception.pos_in_stream])
    print('\nExpecting:')
    for allowed in exception.allowed:
        if TERMINALS.get(allowed.name):
            print("  - %s" % TERMINALS[allowed.name])
        else:
            print("  - %s" % allowed.name)

