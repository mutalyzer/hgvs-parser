

class UnexpectedCharacter(Exception):
    def __init__(self, exception, description):
        self.line = exception.line
        self.column = exception.column
        self.allowed = exception.allowed
        self.considered_tokens = exception.considered_tokens
        self.pos_in_stream = exception.pos_in_stream
        self.state = exception.state
        self.unexpected_character = description[self.pos_in_stream]
        self.description = description
        self.expecting = get_expecting(exception.allowed)

        message = 'Unexpected character \'{}\' at position {}:\n'.format(
            self.unexpected_character, self.column)
        message += self.get_context()
        message += '\nExpecting:'
        for expecting in self.expecting:
            message += '\n - {}'.format(expecting)
        super(UnexpectedCharacter, self).__init__(message)

    def get_context(self):
        return '\n {}\n {}{}'.format(
            self.description, ' ' * self.pos_in_stream, '^')

    def serialize(self):
        return {'line': self.line,
                'column': self.column,
                'pos_in_stream': self.pos_in_stream,
                'unexpected_character': self.unexpected_character,
                'description': self.description,
                'expecting': self.expecting}


class ParsingError(Exception):
    def __init__(self, exception):
        """
        Todo: This should be revisited (lark does not offer the same
              info as for the UnexpectedCharacters above).
        """
        if 'Unexpected end of input!' in str(exception):
            lark_terminals = list(set(
                [val for i, val in enumerate(str(exception).
                                             split(':')[1].split('\''))
                 if i % 2 == 1]))
            self.expecting = get_expecting(lark_terminals)
            self.message = 'Lark ParseError: Unexpected end of input!' \
                           '\nExpecting:'
            for expecting in self.expecting:
                self.message += '\n - {}'.format(expecting)

    def serialize(self):
        return {'details': 'Unexpected end of input',
                'expecting': self.expecting}


def get_expecting(lark_terminal_list):
    expecting = []
    for lark_terminal in lark_terminal_list:
        if TERMINALS.get(lark_terminal):
            expecting.append(TERMINALS[lark_terminal])
        else:
            expecting.append(lark_terminal)
    return expecting


TERMINALS = {
    'ACCESSION': 'accession (e.g., NG_012337)',
    'VERSION': 'version (e.g., \'1\')',
    'GENE_NAME': 'gene name (e.g., SDHD)',
    'GENBANK_LOCUS_SELECTOR': 'genbank locus selector (e.g., v001, i001)',
    'LRG_LOCUS': 'lrg specific locus (e.g., p1, t1)',
    'COORDINATE_SYSTEM': 'a coordinate system: '
                         '\'g\', \'o\', \'m\', \'c\', \'n\', \'r\', or \'p\'',
    'POSITION': 'position (e.g., 100)',
    'OFFSET': 'position offset (\'-\' or \'+\')',
    'OUTSIDE_CDS': '\'*\' or \'-\' for an outside CDS location',
    'DOT': '\'.\' between the coordinate system and the operation(s)',
    'COLON': '\':\' between the reference part and the coordinate system',
    'UNDERSCORE': '\'_\' between start and end in range or uncertain positions',
    'LPAR': '\'(\' for an uncertainty start',
    'RPAR': '\')\' for an uncertainty end',
    'SEMICOLON': '\';\' to separate variants',
    'LSQB': '\'[\' for multiple variants, insertions, or repeats',
    'RSQB': '\']\' for multiple variants, insertions, or repeats',
    'DEL': 'deletion operation (e.g., 10del)',
    'DUP': 'duplication operation (e.g., 10dup)',
    'INS': 'insertion operation (e.g., 11_12insTA, ins10_20)',
    'CON': 'conversion operation (e.g., 10_12con20_22)',
    'EQUAL': '\'=\' to indicate no changes',
    'DELETED': 'deleted nucleotide in a substitution operation',
    'INSERTED': 'inserted nucleotide in a substitution operation',
    'DELETED_SEQUENCE': 'deleted sequence (e.g., ATG)',
    'DELETED_LENGTH': 'deleted length (e.g., 50)',
    'DUPLICATED_SEQUENCE': 'duplicated sequence (e.g., \'A\')',
    'DUPLICATED_LENGTH': 'duplicated length (e.g., 50)',
    'INVERTED': 'inv',
    'INSERTED_SEQUENCE': 'inserted sequence',
    'MORETHAN': '\'>\' in a substitution operation',
    'SEQUENCE': 'sequence (e.g., ATG)',
    'REPEAT_LENGTH': 'repeat length (e.g., 50)',
    'NT': 'nucleotide, (e.g., \'A\')',
    'NAME': 'name',
    'LETTER': 'a letter',
    'DIGIT': 'a digit',
    'NUMBER': 'a number (to indicate a location or a length)',
    'LCASE_LETTER': 'lower case letter',
    'UCASE_LETTER': 'upper case letter',
    'UNKNOWN': '?'
}


class NoParserDefined(Exception):
    pass


class UnsupportedParserType(Exception):
    pass


class UnsupportedStartRule(Exception):
    def __init__(self, start_rule):
        self.message = 'Start rule \'{}\' not supported.'.format(start_rule)
        super().__init__(self.message)
